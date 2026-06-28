const { spawn } = require('node:child_process');
const crypto = require('node:crypto');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');

const repoRoot = path.resolve(__dirname, '..');
const sessions = new Map();
const sessionIndex = new Map();
const MAX_ROLE_FILE_CHARS = 6000;
const MAX_ROLE_CONTEXT_CHARS = 45000;
const MAX_TRANSCRIPT_ITEMS = 6;
const MAX_TRANSCRIPT_ITEM_CHARS = 1600;
const MAX_TRANSCRIPT_CHARS = 10000;
const DEFAULT_CONTEXT_WINDOWS = {
  codex: 1000000,
  claude: 200000,
  deepseek: 128000
};
const REVIEWABLE_CODE_EXTENSIONS = new Set([
  '.cjs',
  '.css',
  '.html',
  '.js',
  '.jsx',
  '.mjs',
  '.ps1',
  '.py',
  '.sh',
  '.ts',
  '.tsx'
]);
const REVIEW_SKIP_DIRS = new Set([
  '.git',
  '.next',
  '.turbo',
  'dist',
  'node_modules',
  'out',
  'target',
  'vendor'
]);
const officeWorkspaceInstruction = `This office is an active local workspace session.

You may inspect and modify files in the local workspace when the user's request and the active role's authority allow it. Do not treat filesystem access as permission by itself. Respect role boundaries, approval gates, production/release limits, external communication limits, spending limits, and secrets boundaries. If a requested edit is outside role authority or needs approval, explain the blocker and request the needed approval.`;

function uniquePaths(paths) {
  return [...new Set(paths.filter(Boolean).map((candidate) => path.resolve(candidate)))];
}

function providerSessionKey(provider, roleSlug) {
  const normalizedProvider = String(provider || '').trim().toLowerCase();
  const normalizedRole = String(roleSlug || '').trim().toLowerCase();
  return normalizedRole ? `${normalizedProvider}:${normalizedRole}` : '';
}

function publicSessionSnapshot(sessionId, session) {
  return {
    sessionId,
    provider: session.provider || 'unknown',
    roleSlug: session.roleSlug || '',
    roleContext: session.roleContext || null,
    messages: Array.isArray(session.messages)
      ? session.messages.map((item) => ({
        role: item.role,
        text: item.text || item.content || ''
      }))
      : [],
    createdAt: session.createdAt || null,
    updatedAt: session.updatedAt || null
  };
}

function truncateText(value, maxChars) {
  const text = String(value || '');
  if (text.length <= maxChars) return text;
  return `${text.slice(0, Math.max(0, maxChars - 140))}\n\n[MindShare truncated ${text.length - maxChars} excess characters from this section before sending to the CLI.]`;
}

async function readFileHash(filePath) {
  const buffer = await fs.readFile(filePath);
  return crypto.createHash('sha256').update(buffer).digest('hex');
}

function isReviewableCodeFile(filePath) {
  return REVIEWABLE_CODE_EXTENSIONS.has(path.extname(filePath).toLowerCase());
}

async function walkReviewableCodeFiles(root, files = []) {
  const entries = await safeReadDir(root, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name.startsWith('.') && entry.name !== '.codex') continue;
    const entryPath = path.join(root, entry.name);
    if (entry.isDirectory()) {
      if (REVIEW_SKIP_DIRS.has(entry.name)) continue;
      await walkReviewableCodeFiles(entryPath, files);
    } else if (entry.isFile() && isReviewableCodeFile(entryPath)) {
      files.push(entryPath);
    }
  }
  return files;
}

async function snapshotReviewableCodeFiles(root = repoRoot) {
  const files = await walkReviewableCodeFiles(root);
  const snapshot = new Map();
  await Promise.all(files.map(async (filePath) => {
    try {
      const stats = await fs.stat(filePath);
      snapshot.set(path.resolve(filePath), {
        size: stats.size,
        mtimeMs: stats.mtimeMs,
        hash: await readFileHash(filePath)
      });
    } catch {
      // Ignore transient files that disappear during a build turn.
    }
  }));
  return snapshot;
}

async function changedReviewableCodeFiles(before, root = repoRoot) {
  const after = await snapshotReviewableCodeFiles(root);
  const changed = [];
  for (const [filePath, current] of after.entries()) {
    const previous = before.get(filePath);
    if (!previous || previous.hash !== current.hash) {
      changed.push({
        path: filePath,
        relativePath: path.relative(root, filePath),
        status: previous ? 'modified' : 'added',
        size: current.size
      });
    }
  }
  return changed.sort((a, b) => a.relativePath.localeCompare(b.relativePath));
}

function pushWithinBudget(parts, next, maxChars) {
  const currentLength = parts.reduce((total, part) => total + part.length, 0);
  const separatorLength = parts.length ? 6 : 0;
  if (currentLength + separatorLength + next.length <= maxChars) {
    parts.push(next);
    return true;
  }
  const remaining = maxChars - currentLength - separatorLength;
  if (remaining > 240) {
    parts.push(truncateText(next, remaining));
  }
  return false;
}

function listSessions() {
  return {
    ok: true,
    sessions: [...sessions.entries()].map(([sessionId, session]) => publicSessionSnapshot(sessionId, session))
  };
}

function resetProviderSession(payload = {}) {
  const provider = String(payload.provider || '').trim().toLowerCase();
  const roleSlug = String(payload.roleSlug || '').trim().toLowerCase();
  const sessionId = String(payload.sessionId || '').trim();
  const ids = new Set();

  if (sessionId && sessions.has(sessionId)) {
    ids.add(sessionId);
  }

  if (provider && roleSlug) {
    const indexedKey = providerSessionKey(provider, roleSlug);
    const indexedId = sessionIndex.get(indexedKey);
    if (indexedId) ids.add(indexedId);
    sessionIndex.delete(indexedKey);
  } else if (roleSlug) {
    ['codex', 'claude', 'deepseek'].forEach((candidateProvider) => {
      const indexedKey = providerSessionKey(candidateProvider, roleSlug);
      const indexedId = sessionIndex.get(indexedKey);
      if (indexedId) ids.add(indexedId);
      sessionIndex.delete(indexedKey);
    });
  }

  ids.forEach((candidateId) => {
    const session = sessions.get(candidateId);
    if (session) {
      sessionIndex.delete(providerSessionKey(session.provider, session.roleSlug));
    }
    sessions.delete(candidateId);
  });

  return {
    ok: true,
    reset: ids.size,
    roleSlug,
    provider: provider || 'all'
  };
}

async function createOrReuseProviderSession(provider, payload = {}) {
  const requestedRoleSlug = String(payload?.roleSlug || '').trim().toLowerCase();
  const indexedKey = providerSessionKey(provider, requestedRoleSlug);
  if (indexedKey) {
    const existingId = sessionIndex.get(indexedKey);
    const existingSession = existingId ? sessions.get(existingId) : null;
    if (existingSession) {
      return {
        ...publicSessionSnapshot(existingId, existingSession),
        ok: true,
        reused: true,
        initialMessage: null
      };
    }
  }

  const roleContext = requestedRoleSlug
    ? await loadRoleContext({ roleSlug: requestedRoleSlug }).catch(() => null)
    : null;
  const initialMessage = roleContext?.ok ? `This is ${roleContext.roleContext.name}'s office.` : null;
  const sessionId = crypto.randomUUID();
  const now = new Date().toISOString();
  sessions.set(sessionId, {
    provider,
    roleSlug: requestedRoleSlug,
    messages: initialMessage ? [{ role: 'user', content: initialMessage }] : [],
    roleContext: roleContext?.ok ? roleContext.roleContext : null,
    createdAt: now,
    updatedAt: now
  });
  if (indexedKey) {
    sessionIndex.set(indexedKey, sessionId);
  }
  return {
    ...publicSessionSnapshot(sessionId, sessions.get(sessionId)),
    ok: true,
    reused: false,
    initialMessage
  };
}

async function pathExists(candidatePath) {
  try {
    await fs.access(candidatePath);
    return true;
  } catch {
    return false;
  }
}

async function safeReadDir(candidatePath, options = {}) {
  try {
    return await fs.readdir(candidatePath, options);
  } catch {
    return [];
  }
}

async function withTimeout(promise, timeoutMs, fallback) {
  let timeout;
  try {
    return await Promise.race([
      promise,
      new Promise((resolve) => {
        timeout = setTimeout(() => resolve(fallback), timeoutMs);
      })
    ]);
  } finally {
    clearTimeout(timeout);
  }
}

async function pathExistsForConfiguration(candidatePath) {
  return withTimeout(pathExists(candidatePath), 750, false);
}

async function readDirForConfiguration(candidatePath, options = {}) {
  return withTimeout(safeReadDir(candidatePath, options), 1500, []);
}

function sourceRoots() {
  const codeRoot = path.dirname(repoRoot);
  return {
    home: os.homedir(),
    mindshare: repoRoot,
    mojo: path.join(codeRoot, 'mojo'),
    watch: path.join(codeRoot, 'watch'),
    mindshareDrive: 'G:\\My Drive\\Mindshare'
  };
}

async function resolveAppContentRoot() {
  const candidates = uniquePaths([
    process.env.MINDSHARE_APP_CONTENT,
    path.join(__dirname, 'app-content'),
    path.join(repoRoot, 'local-client', 'app-content'),
    path.join(process.cwd(), 'app-content'),
    process.resourcesPath && path.join(process.resourcesPath, 'app-content'),
    process.resourcesPath && path.join(process.resourcesPath, 'app', 'app-content'),
    process.resourcesPath && path.join(process.resourcesPath, 'app.asar.unpacked', 'app-content')
  ]);

  for (const candidate of candidates) {
    if (await pathExists(path.join(candidate, 'manifest.json')) || await pathExists(path.join(candidate, 'mindshare', 'public', 'index.html'))) {
      return candidate;
    }
  }

  return candidates[0] || path.join(__dirname, 'app-content');
}

const ROLE_CATALOG = {
  "bea": {
    "name": "Bea",
    "title": "Mojo MAPS Engineer",
    "level": "Level 3 Staff",
    "office": "Bea's office",
    "rolePath": [
      "mindshare",
      "roles",
      "mojo-maps-engineer"
    ],
    "files": [
      "WhoAmI.md",
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "loop.md",
      "Autonomy.md",
      "memory.md"
    ]
  },
  "cal": {
    "name": "Cal",
    "title": "MAPS ASPM",
    "level": "Level 3 Staff",
    "office": "Cal's office",
    "rolePath": [
      "mindshare",
      "roles",
      "maps-agentic-systems-program-manager"
    ],
    "files": [
      "WhoAmI.md",
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "Autonomy.md",
      "memory.md"
    ]
  },
  "cole": {
    "name": "Cole",
    "title": "HR Director",
    "level": "Level 4 Scoped Autonomy",
    "office": "Cole's office",
    "rolePath": [
      "mindshare",
      "roles",
      "hr-director"
    ],
    "files": [
      "WhoAmI.md",
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "loop.md",
      "Autonomy.md",
      "memory.md"
    ]
  },
  "imani": {
    "name": "Imani",
    "title": "Data Engineering Director",
    "level": "Level 3 Staff",
    "office": "Imani's office",
    "rolePath": [
      "mindshare",
      "roles",
      "data-engineering-director"
    ],
    "files": [
      "WhoAmI.md",
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "loop.md",
      "Autonomy.md",
      "memory.md"
    ]
  },
  "lane": {
    "name": "Lane",
    "title": "Mojo Lab Operator",
    "level": "Level 3 Staff",
    "office": "Lane's office",
    "rolePath": [
      "mindshare",
      "roles",
      "lab-operator"
    ],
    "files": [
      "WhoAmI.md",
      "name.md",
      "role-agent.md",
      "workflow.md",
      "loop.md",
      "Autonomy.md",
      "memory.md"
    ]
  },
  "reid": {
    "name": "Reid",
    "title": "Release Manager",
    "level": "Level 3 Staff",
    "office": "Reid's office",
    "rolePath": [
      "mindshare",
      "roles",
      "release-manager"
    ],
    "files": [
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "loop.md",
      "Autonomy.md",
      "automation.md",
      "memory.md"
    ]
  },
  "tess": {
    "name": "Tess",
    "title": "Autonomy Engineer",
    "level": "Level 4 Scoped Autonomy",
    "office": "Tess's office",
    "rolePath": [
      "mindshare",
      "roles",
      "autonomy-engineer"
    ],
    "files": [
      "WhoAmI.md",
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "loop.md",
      "Autonomy.md",
      "memory.md"
    ]
  },
  "vik": {
    "name": "Vik",
    "title": "ASPA",
    "level": "Level 5 Policy Autonomy",
    "office": "Vik's office",
    "rolePath": [
      "mindshare",
      "roles",
      "maps-agentic-systems-program-architect"
    ],
    "files": [
      "WhoAmI.md",
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "loop.md",
      "Autonomy.md",
      "memory.md"
    ]
  },
  "scott": {
    "name": "Scott",
    "title": "Human Owner / Final Authority",
    "level": "Human Authority",
    "office": "Scott's office",
    "rolePath": [
      "mindshare"
    ],
    "files": [
      "AGENTS.md",
      "project-foundation.md"
    ]
  },
  "rae": {
    "name": "Rae",
    "title": "Chief Executive Officer",
    "level": "Level 3 Staff",
    "office": "Rae's office",
    "rolePath": [
      "mindshare",
      "roles",
      "chief-executive-officer"
    ],
    "files": [
      "WhoAmI.md",
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "Autonomy.md",
      "memory.md"
    ]
  },
  "paige": {
    "name": "Paige",
    "title": "Executive Assistant",
    "level": "Level 3 Staff",
    "office": "Paige's office",
    "rolePath": [
      "mindshare",
      "roles",
      "personal-assistant"
    ],
    "files": [
      "WhoAmI.md",
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "loop.md",
      "Autonomy.md",
      "memory.md"
    ]
  },
  "mara": {
    "name": "Mara",
    "title": "Front Desk Administrator",
    "level": "Level 3 Staff",
    "office": "Mara's office",
    "rolePath": [
      "mindshare",
      "roles",
      "front-desk-administrator"
    ],
    "files": [
      "WhoAmI.md",
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "loop.md",
      "Autonomy.md",
      "memory.md"
    ]
  },
  "finn": {
    "name": "Finn",
    "title": "Finance Director",
    "level": "Level 3 Staff",
    "office": "Finn's office",
    "rolePath": [
      "mindshare",
      "roles",
      "finance-director"
    ],
    "files": [
      "WhoAmI.md",
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "loop.md",
      "memory.md"
    ]
  },
  "ana": {
    "name": "Ana",
    "title": "Recruiter",
    "level": "Level 4 Scoped Autonomy",
    "office": "Ana's office",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter"
    ],
    "files": [
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "loop.md",
      "Autonomy.md",
      "memory.md",
      "recruiting.pipeline.json"
    ]
  },
  "matt": {
    "name": "Matt",
    "title": "Released MAPS ASPM",
    "level": "Released",
    "office": "Matt's historical office",
    "rolePath": [
      "mindshare",
      "roles",
      "released-maps-agentic-systems-program-manager"
    ],
    "files": [
      "WhoAmI.md",
      "name.md",
      "role-agent.md",
      "workflow.md",
      "Autonomy.md",
      "memory.md"
    ]
  },
  "liz": {
    "name": "Liz",
    "title": "Mojo Website Manager",
    "level": "Level 3 Staff",
    "office": "Liz's office",
    "rolePath": [
      "mindshare",
      "roles",
      "mojo-website-manager"
    ],
    "files": [
      "WhoAmI.md",
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "Autonomy.md",
      "memory.md"
    ]
  },
  "mae": {
    "name": "Mae",
    "title": "Communications Director",
    "level": "Level 4 Scoped Autonomy",
    "office": "Mae's office",
    "rolePath": [
      "mindshare",
      "roles",
      "communications-director"
    ],
    "files": [
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "loop.md",
      "Autonomy.md",
      "memory.md",
      "level4-proof.md"
    ]
  },
  "june": {
    "name": "June",
    "title": "Staff Writer",
    "level": "Level 3 Staff",
    "office": "June's office",
    "rolePath": [
      "mindshare",
      "roles",
      "staff-writer"
    ],
    "files": [
      "WhoAmI.md",
      "name.md",
      "personality.md",
      "role-agent.md",
      "Autonomy.md",
      "memory.md"
    ]
  },
  "jay": {
    "name": "Jay",
    "title": "Meetup Coordinator / Operator",
    "level": "Level 3 Staff",
    "office": "Jay's office",
    "rolePath": [
      "mindshare",
      "roles",
      "meetup-coordinator"
    ],
    "files": [
      "name.md",
      "personality.md",
      "role-agent.md",
      "workflow.md",
      "Autonomy.md",
      "memory.md"
    ]
  },
  "morgan-vale": {
    "name": "Morgan Vale",
    "title": "Operations Director",
    "level": "Level 2 Trainee",
    "office": "Morgan Vale's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-001-level2.md"
    ]
  },
  "priya-sen": {
    "name": "Priya Sen",
    "title": "Product Director",
    "level": "Level 2 Trainee",
    "office": "Priya Sen's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-002-level2.md"
    ]
  },
  "owen-kline": {
    "name": "Owen Kline",
    "title": "Technology Director",
    "level": "Level 2 Trainee",
    "office": "Owen Kline's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-003-level2.md"
    ]
  },
  "nia-calder": {
    "name": "Nia Calder",
    "title": "Engineering Director",
    "level": "Level 2 Trainee",
    "office": "Nia Calder's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-004-level2.md"
    ]
  },
  "mateo-ruiz": {
    "name": "Mateo Ruiz",
    "title": "Platform Engineering Director",
    "level": "Level 2 Trainee",
    "office": "Mateo Ruiz's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-005-level2.md"
    ]
  },
  "theo-nakamura": {
    "name": "Theo Nakamura",
    "title": "AI Systems Engineering Director",
    "level": "Level 2 Trainee",
    "office": "Theo Nakamura's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-007-level2.md"
    ]
  },
  "harper-quinn": {
    "name": "Harper Quinn",
    "title": "Security Engineering Director",
    "level": "Level 2 Trainee",
    "office": "Harper Quinn's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-008-level2.md"
    ]
  },
  "sloane-mercer": {
    "name": "Sloane Mercer",
    "title": "Revenue Director",
    "level": "Level 2 Trainee",
    "office": "Sloane Mercer's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-009-level2.md"
    ]
  },
  "june-park": {
    "name": "June Park",
    "title": "Staff Operations Director",
    "level": "Level 2 Trainee",
    "office": "June Park's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-011-level2.md"
    ]
  },
  "leon-archer": {
    "name": "Leon Archer",
    "title": "Executive Operations Director",
    "level": "Level 2 Trainee",
    "office": "Leon Archer's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-012-level2.md"
    ]
  },
  "mira-patel": {
    "name": "Mira Patel",
    "title": "PMO Director",
    "level": "Level 2 Trainee",
    "office": "Mira Patel's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-013-level2.md"
    ]
  },
  "gabe-rowan": {
    "name": "Gabe Rowan",
    "title": "Product Management Director",
    "level": "Level 2 Trainee",
    "office": "Gabe Rowan's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-014-level2.md"
    ]
  },
  "elise-hart": {
    "name": "Elise Hart",
    "title": "Product Operations Director",
    "level": "Level 2 Trainee",
    "office": "Elise Hart's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-015-level2.md"
    ]
  },
  "nora-voss": {
    "name": "Nora Voss",
    "title": "Service Design Director",
    "level": "Level 2 Trainee",
    "office": "Nora Voss's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-016-level2.md"
    ]
  },
  "kai-bennett": {
    "name": "Kai Bennett",
    "title": "Experience Design Director",
    "level": "Level 2 Trainee",
    "office": "Kai Bennett's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-017-level2.md"
    ]
  },
  "amara-hayes": {
    "name": "Amara Hayes",
    "title": "User Research Director",
    "level": "Level 2 Trainee",
    "office": "Amara Hayes's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-018-level2.md"
    ]
  },
  "drew-collins": {
    "name": "Drew Collins",
    "title": "Sales Director",
    "level": "Level 2 Trainee",
    "office": "Drew Collins's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-019-level2.md"
    ]
  },
  "celia-grant": {
    "name": "Celia Grant",
    "title": "Partnerships Director",
    "level": "Level 2 Trainee",
    "office": "Celia Grant's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-020-level2.md"
    ]
  },
  "jordan-hale": {
    "name": "Jordan Hale",
    "title": "Customer Success Director",
    "level": "Level 2 Trainee",
    "office": "Jordan Hale's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-021-level2.md"
    ]
  },
  "samira-knox": {
    "name": "Samira Knox",
    "title": "Support Director",
    "level": "Level 2 Trainee",
    "office": "Samira Knox's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-022-level2.md"
    ]
  },
  "mila-chen": {
    "name": "Mila Chen",
    "title": "People Operations Director",
    "level": "Level 2 Trainee",
    "office": "Mila Chen's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-023-level2.md"
    ]
  },
  "adrian-moss": {
    "name": "Adrian Moss",
    "title": "Legal Director",
    "level": "Level 2 Trainee",
    "office": "Adrian Moss's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-024-level2.md"
    ]
  },
  "isla-monroe": {
    "name": "Isla Monroe",
    "title": "Compliance Director",
    "level": "Level 2 Trainee",
    "office": "Isla Monroe's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-025-level2.md"
    ]
  },
  "victor-lane": {
    "name": "Victor Lane",
    "title": "Vendor Management Director",
    "level": "Level 2 Trainee",
    "office": "Victor Lane's candidate packet",
    "rolePath": [
      "mindshare",
      "roles",
      "recruiter",
      "level-4-work"
    ],
    "files": [
      "REC-026-level2.md"
    ]
  }
};

function run(command, args, options = {}) {
  return new Promise((resolve) => {
    const child = spawn(command, args, {
      cwd: repoRoot,
      env: { ...process.env, ...(options.env || {}) },
      shell: false,
      windowsHide: true
    });

    let stdout = '';
    let stderr = '';
    const timer = setTimeout(() => {
      child.kill();
      resolve({ ok: false, code: 'TIMEOUT', stdout, stderr: stderr || 'Command timed out.' });
    }, options.timeout || 30000);

    child.stdout.on('data', (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr.on('data', (chunk) => {
      stderr += chunk.toString();
    });
    child.on('error', (error) => {
      clearTimeout(timer);
      resolve({
        ok: false,
        code: error.code || 1,
        stdout,
        stderr: stderr || error.message
      });
    });
    child.on('close', (code) => {
      clearTimeout(timer);
      resolve({
        ok: code === 0,
        code,
        stdout,
        stderr
      });
    });

    if (options.input) {
      child.stdin.end(options.input);
    } else {
      child.stdin.end();
    }
  });
}

async function codexInstalled() {
  if (process.platform === 'win32') {
    return Boolean(await codexLaunch());
  }
  const result = await run('which', ['codex'], { timeout: 10000 });
  return result.ok && result.stdout.trim().length > 0;
}

async function firstCommand(name) {
  const result = await run(process.platform === 'win32' ? 'where.exe' : 'which', [name], { timeout: 10000 });
  if (!result.ok) {
    return null;
  }
  return result.stdout
    .split(/\r?\n/)
    .map((line) => line.trim())
    .find((line) => line.length > 0) || null;
}

async function codexLaunch() {
  if (process.platform === 'win32') {
    const codexJs = path.join(process.env.APPDATA || '', 'npm', 'node_modules', '@openai', 'codex', 'bin', 'codex.js');
    const nodeCommand = await firstCommand('node');
    try {
      await fs.access(codexJs);
      if (nodeCommand) {
        return { command: nodeCommand, argsPrefix: [codexJs] };
      }
    } catch {
      return null;
    }
  }
  const codex = await firstCommand('codex');
  return codex ? { command: codex, argsPrefix: [] } : null;
}

async function claudeLaunch() {
  if (process.platform === 'win32') {
    const claudeExe = path.join(
      process.env.APPDATA || '',
      'npm',
      'node_modules',
      '@anthropic-ai',
      'claude-code',
      'bin',
      'claude.exe'
    );
    try {
      await fs.access(claudeExe);
      return { command: claudeExe, argsPrefix: [] };
    } catch {
      // Fall through to PATH lookup.
    }
  }
  const claude = await firstCommand('claude');
  return claude ? { command: claude, argsPrefix: [] } : null;
}

async function codexLoginStatus() {
  const installed = await codexInstalled();
  if (!installed) {
    return {
      installed: false,
      loggedIn: false,
      status: 'Codex CLI is not installed or is not on PATH.'
    };
  }

  const launch = await codexLaunch();
  if (!launch) {
    return {
      installed: false,
      loggedIn: false,
      status: 'Codex CLI is not installed or could not be launched.'
    };
  }
  const result = await run(launch.command, [...launch.argsPrefix, 'login', 'status'], { timeout: 20000 });
  const status = (result.stdout || result.stderr).trim();
  return {
    installed: true,
    loggedIn: result.ok && status.includes('Logged in'),
    status: status || 'Codex CLI is installed but login status could not be confirmed.'
  };
}

async function claudeLoginStatus() {
  const launch = await claudeLaunch();
  if (!launch) {
    return {
      installed: false,
      loggedIn: false,
      status: 'Claude CLI is not installed or is not on PATH.'
    };
  }

  const result = await run(launch.command, [...launch.argsPrefix, 'auth', 'status'], { timeout: 20000 });
  const status = (result.stdout || result.stderr).trim();
  return {
    installed: true,
    loggedIn: result.ok && !/not authenticated|not logged in|login required/i.test(status),
    status: status || 'Claude CLI is installed but login status could not be confirmed.'
  };
}

async function connectCodex(payload = {}) {
  const status = await codexLoginStatus();
  if (!status.installed) {
    return {
      ok: false,
      action: 'install',
      message: 'Codex CLI is not installed. Install it locally, then restart MindShare Local Client.',
      codexStatus: status.status
    };
  }

  if (!status.loggedIn) {
    return {
      ok: false,
      action: 'login',
      message: 'Codex CLI is installed but not logged in. Run `codex login` locally, then reconnect.',
      codexStatus: status.status
    };
  }

  if (payload?.checkOnly) {
    return {
      ok: true,
      message: 'Codex CLI is ready.',
      codexStatus: status.status
    };
  }

  const sessionPayload = await createOrReuseProviderSession('codex', payload);
  return {
    ok: true,
    sessionId: sessionPayload.sessionId,
    initialMessage: sessionPayload.initialMessage,
    reused: sessionPayload.reused,
    message: 'Connected to local Codex CLI using local ChatGPT authentication.',
    codexStatus: status.status,
    roleContext: sessionPayload.roleContext,
    messages: sessionPayload.messages
  };
}

async function connectClaude(payload = {}) {
  const status = await claudeLoginStatus();
  if (!status.installed) {
    return {
      ok: false,
      action: 'install',
      message: 'Claude CLI is not installed. Install it locally, then restart MindShare Local Client.',
      claudeStatus: status.status
    };
  }

  if (!status.loggedIn) {
    return {
      ok: false,
      action: 'login',
      message: 'Claude CLI is installed but not logged in. Run `claude auth login` locally, then reconnect.',
      claudeStatus: status.status
    };
  }

  if (payload?.checkOnly) {
    return {
      ok: true,
      message: 'Claude CLI is ready.',
      claudeStatus: status.status
    };
  }

  const sessionPayload = await createOrReuseProviderSession('claude', payload);
  return {
    ok: true,
    sessionId: sessionPayload.sessionId,
    initialMessage: sessionPayload.initialMessage,
    reused: sessionPayload.reused,
    message: 'Connected to local Claude CLI using local Claude authentication.',
    claudeStatus: status.status,
    roleContext: sessionPayload.roleContext,
    messages: sessionPayload.messages
  };
}

async function readRoleFile(roleRoot, fileName) {
  const filePath = path.join(roleRoot, fileName);
  try {
    return {
      fileName,
      path: filePath,
      exists: true,
      content: await fs.readFile(filePath, 'utf8')
    };
  } catch (error) {
    if (error.code === 'ENOENT') {
      return {
        fileName,
        path: filePath,
        exists: false,
        content: ''
      };
    }
    throw error;
  }
}

async function readOptionalText(filePath) {
  try {
    return {
      path: filePath,
      exists: true,
      content: await fs.readFile(filePath, 'utf8')
    };
  } catch (error) {
    if (error.code === 'ENOENT') {
      return { path: filePath, exists: false, content: '' };
    }
    return { path: filePath, exists: false, content: `Unable to read file: ${error.message || String(error)}` };
  }
}

function parseConferenceRoomOccupants(rosterText) {
  const occupants = [];
  const seen = new Set();
  for (const rawLine of String(rosterText || '').split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#') || line.startsWith('|') || /^[-*]\s*$/.test(line)) continue;
    const match = line.match(/^(?:[-*]\s*)?([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)?)\s+[—-]\s+(.+)$/);
    if (!match) continue;
    const name = match[1].trim();
    const title = match[2].replace(/\s{2,}.*/, '').trim();
    const key = name.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    occupants.push({ name, title });
  }
  return occupants;
}

function listConferenceRoomInviteCandidates() {
  return Object.entries(ROLE_CATALOG)
    .map(([slug, role]) => ({
      slug,
      name: role.name,
      title: role.title,
      level: role.level,
      office: role.office
    }))
    .sort((left, right) => left.name.localeCompare(right.name));
}

async function loadConferenceRoomContext() {
  const roomRoot = path.join(repoRoot, 'rooms');
  const roomFile = await readOptionalText(path.join(roomRoot, 'conference-room.md'));
  const protocolFile = await readOptionalText(path.join(roomRoot, 'conference-room-prompt-protocol.md'));
  const cultureFile = await readOptionalText(path.join(repoRoot, 'MINDSHARE_CULTURE.md'));
  const rosterFile = await readOptionalText('G:\\My Drive\\Mindshare\\roles.md');
  const occupants = parseConferenceRoomOccupants(rosterFile.content);
  const fallbackOccupants = [
    { name: 'Scott', title: 'Human Owner / Final Authority' },
    { name: 'Rae', title: 'Chief Executive Officer' },
    { name: 'Vik', title: 'ASPA' },
    { name: 'Tess', title: 'Autonomy Engineer' },
    { name: 'Reid', title: 'Release Manager' },
    { name: 'Cole', title: 'HR Director' },
    { name: 'Ana', title: 'Recruiter' },
    { name: 'Mae', title: 'Communications Director' }
  ];
  const files = [
    { fileName: 'conference-room.md', path: roomFile.path, exists: roomFile.exists, content: roomFile.content },
    { fileName: 'conference-room-prompt-protocol.md', path: protocolFile.path, exists: protocolFile.exists, content: protocolFile.content },
    { fileName: 'roles.md', path: rosterFile.path, exists: rosterFile.exists, content: rosterFile.content },
    { fileName: 'MINDSHARE_CULTURE.md', path: cultureFile.path, exists: cultureFile.exists, content: cultureFile.content }
  ];
  const whoAmI = `# Who Am I

I am the MindShare Conference Room, the shared conversation surface for Scott and invited Mindshare roles.

I am not a manager, authority grant, autonomous runtime, or production system. I facilitate bounded room conversations by loading the conference-room contract, resolving invited participants, and helping each invited role speak when useful.

Current status: workflow-backed room.

Authority boundary: I do not activate roles, approve actions, expand authority, contact outsiders, spend money, change production, or write memory unless Scott explicitly asks or the project memory contract requires it.

Participation logic: when Scott invites everyone, a subset, a team, or asks for objections/round robin/decision pass, I use the room contract and prompt protocol to assemble role context, ask every invited role whether they should speak, and synthesize a concise room response.`;

  const candidates = listConferenceRoomInviteCandidates();
  return {
    ok: true,
    occupants: occupants.length ? occupants : fallbackOccupants,
    inviteCandidates: candidates,
    roomContext: {
      name: 'MindShare Conference Room',
      title: 'Shared Conversation Surface',
      level: 'Workflow-backed room',
      office: 'MindShare Conference Room',
      roleRoot: roomRoot,
      whoAmI,
      files
    }
  };
}

function synthesizeWhoAmI(role, files) {
  const existing = files.find((file) => file.fileName === 'WhoAmI.md' && file.exists);
  if (existing) {
    return existing.content;
  }

  const available = files
    .filter((file) => file.exists)
    .map((file) => `- ${file.fileName}`)
    .join('\n');

  return `# Who Am I

I am ${role.name}, the ${role.title}.

Office: ${role.office}
Autonomy level: ${role.level}

My dedicated WhoAmI.md file is not present yet, so MindShare Local synthesized this card from the available canonical role files:

${available || '- No role files were available.'}

I should answer in first person as ${role.name} and stay inside the authority boundaries in my role contract and autonomy file.`;
}

function buildRolePromptContext(roleContext) {
  if (!roleContext) {
    return 'No role context is currently selected.';
  }

  const fileSections = [];
  for (const file of roleContext.files.filter((candidate) => candidate.exists)) {
    const section = `## ${file.fileName}\nPath: ${file.path}\n\n${truncateText(file.content, MAX_ROLE_FILE_CHARS)}`;
    if (!pushWithinBudget(fileSections, section, MAX_ROLE_CONTEXT_CHARS)) break;
  }
  const renderedFileSections = fileSections
    .join('\n\n---\n\n');

  const omittedCount = roleContext.files
    .filter((file) => file.exists)
    .length - fileSections.length;

  const missing = roleContext.files
    .filter((file) => !file.exists)
    .map((file) => file.path)
    .join('\n');

  return `# Active MindShare Role

Name: ${roleContext.name}
Title: ${roleContext.title}
Level: ${roleContext.level}
Office: ${roleContext.office}
Role root: ${roleContext.roleRoot}

## Who Am I Card

${roleContext.whoAmI}

## Loaded Canonical Files

${renderedFileSections || '(No canonical role files loaded.)'}

${omittedCount > 0 ? `MindShare note: ${omittedCount} loaded file section(s) were omitted from this turn because the CLI context budget was reached. Ask for a specific file if needed.` : ''}

## Missing Expected Files

${missing || '(None)'}`;
}

function compactTranscript(transcriptItems) {
  const items = (Array.isArray(transcriptItems) ? transcriptItems : [])
    .slice(-MAX_TRANSCRIPT_ITEMS)
    .map((item) => {
      const role = String(item.role || 'message').toUpperCase();
      const text = truncateText(item.content || item.text || '', MAX_TRANSCRIPT_ITEM_CHARS);
      return `${role}: ${text}`;
    })
    .filter((text) => text.trim().length > 0);
  const parts = [];
  for (const item of items) {
    if (!pushWithinBudget(parts, item, MAX_TRANSCRIPT_CHARS)) break;
  }
  return parts.join('\n');
}

function formatAttachments(attachments) {
  if (!Array.isArray(attachments) || attachments.length === 0) {
    return '(None)';
  }
  return attachments.map((file, index) => {
    const name = String(file?.name || 'attachment');
    const filePath = String(file?.path || '');
    const type = String(file?.type || '');
    const size = Number(file?.size || 0);
    return [
      `${index + 1}. ${name}`,
      filePath ? `   Path: ${filePath}` : '   Path: unavailable from browser paste; ask the user to attach with the paperclip if you need local file access.',
      type ? `   Type: ${type}` : '',
      size ? `   Size: ${size} bytes` : ''
    ].filter(Boolean).join('\n');
  }).join('\n');
}

function parseJsonLines(text) {
  return String(text || '')
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.startsWith('{') && line.endsWith('}'))
    .map((line) => {
      try {
        return JSON.parse(line);
      } catch {
        return null;
      }
    })
    .filter(Boolean);
}

function extractCodexReply(stdout) {
  const events = parseJsonLines(stdout);
  const textFromItem = (item = {}) => {
    if (typeof item.text === 'string') return item.text.trim();
    if (typeof item.content === 'string') return item.content.trim();
    if (Array.isArray(item.content)) {
      return item.content
        .map((part) => typeof part === 'string' ? part : (part?.text || part?.content || ''))
        .join('')
        .trim();
    }
    return '';
  };

  const completed = [...events].reverse().find((event) =>
    event.type === 'item.completed' && event.item?.type === 'agent_message' && textFromItem(event.item)
  );
  if (completed) {
    return { events, reply: textFromItem(completed.item), complete: true };
  }

  const partial = [...events].reverse().map((event) => {
    if (event.item?.type === 'agent_message') return textFromItem(event.item);
    if (typeof event.delta === 'string') return event.delta.trim();
    if (typeof event.text === 'string') return event.text.trim();
    return '';
  }).find(Boolean) || '';

  return { events, reply: partial, complete: false };
}

function normalizeUsage(provider, usage = {}, extra = {}) {
  const inputTokens = Number(usage.input_tokens ?? usage.inputTokens ?? 0) || 0;
  const outputTokens = Number(usage.output_tokens ?? usage.outputTokens ?? 0) || 0;
  const cachedInputTokens = Number(
    usage.cached_input_tokens ??
    usage.cache_read_input_tokens ??
    usage.cacheReadInputTokens ??
    0
  ) || 0;
  const cacheCreationInputTokens = Number(
    usage.cache_creation_input_tokens ??
    usage.cacheCreationInputTokens ??
    0
  ) || 0;
  const reasoningOutputTokens = Number(usage.reasoning_output_tokens ?? 0) || 0;
  return {
    provider,
    inputTokens,
    outputTokens,
    cachedInputTokens,
    cacheCreationInputTokens,
    reasoningOutputTokens,
    totalContextInputTokens: inputTokens + cachedInputTokens + cacheCreationInputTokens,
    contextWindowTokens: Number(extra.contextWindowTokens || DEFAULT_CONTEXT_WINDOWS[provider] || 0) || null,
    costUsd: typeof extra.costUsd === 'number' ? extra.costUsd : null,
    model: extra.model || null,
    source: extra.source || `${provider}-cli`,
    measuredAt: new Date().toISOString()
  };
}

function providerRuntimeContext(provider, model) {
  const providerLabel = provider === 'claude'
    ? 'Claude CLI'
    : provider === 'deepseek'
      ? 'DeepSeek API'
      : 'Codex CLI';
  const modelLabel = model || (
    provider === 'claude'
      ? 'sonnet'
      : provider === 'deepseek'
        ? 'deepseek-v4-flash'
        : 'Codex CLI selected model'
  );
  return `Current runtime provider: ${providerLabel}.
Current runtime model: ${modelLabel}.
If the user asks which model or provider is being used, answer from these two current runtime lines. Do not infer the current provider or model from prior transcript messages.`;
}

async function pythonLaunch() {
  const configured = process.env.PYTHON || process.env.PYTHON_EXE;
  if (configured && await pathExists(configured)) {
    return configured;
  }
  const python = await firstCommand(process.platform === 'win32' ? 'python.exe' : 'python');
  if (python) {
    return python;
  }
  return firstCommand(process.platform === 'win32' ? 'py.exe' : 'python3');
}

async function runTessLevel4Automation(payload = {}) {
  const appContentRoot = await resolveAppContentRoot();
  const mindshareRoot = path.join(appContentRoot, 'mindshare');
  const scriptPath = path.join(mindshareRoot, 'roles', 'autonomy-engineer', 'scripts', 'level4automation.py');
  const python = await pythonLaunch();
  if (!python) {
    return { ok: false, error: 'Python is not installed or not on PATH.' };
  }
  if (!await pathExists(scriptPath)) {
    return { ok: false, error: `Tess Level 4 automation script was not found at ${scriptPath}.` };
  }

  const mode = payload.mode === 'scheduled' ? 'scheduled' : 'manual';
  const args = python.toLowerCase().endsWith('py.exe')
    ? ['-3', scriptPath, '--write', '--mode', mode]
    : [scriptPath, '--write', '--mode', mode];
  const result = await run(python, args, {
    timeout: 120000,
    env: {
      MINDSHARE_REPO_ROOT: mindshareRoot,
      MINDSHARE_AUTOMATIONS_ROOT: path.join(mindshareRoot, 'automations'),
      MINDSHARE_RELEASE_QUEUE: path.join(mindshareRoot, 'roles', 'autonomy-engineer', 'level4-release-management-queue.md')
    }
  });
  const output = (result.stdout || result.stderr || '').trim();
  let state = null;
  try {
    state = output ? JSON.parse(output) : null;
  } catch {
    state = null;
  }
  return {
    ok: result.ok,
    code: result.code,
    state,
    output,
    error: result.ok ? null : (result.stderr || result.stdout || 'Tess Level 4 automation failed.').trim()
  };
}

async function runPythonAutomation(scriptPath, mode, env) {
  const python = await pythonLaunch();
  if (!python) {
    return { ok: false, error: 'Python is not installed or not on PATH.' };
  }
  if (!await pathExists(scriptPath)) {
    return { ok: false, error: `Automation script was not found at ${scriptPath}.` };
  }

  const args = python.toLowerCase().endsWith('py.exe')
    ? ['-3', scriptPath, '--write', '--mode', mode]
    : [scriptPath, '--write', '--mode', mode];
  const result = await run(python, args, { timeout: 120000, env });
  const output = (result.stdout || result.stderr || '').trim();
  let state = null;
  try {
    state = output ? JSON.parse(output) : null;
  } catch {
    state = null;
  }
  return {
    ok: Boolean(state) && result.code !== 'TIMEOUT',
    code: result.code,
    state,
    output,
    error: result.code === 'TIMEOUT' ? (result.stderr || 'Automation timed out.').trim() : null
  };
}

async function runVikAutomation(payload = {}) {
  const appContentRoot = await resolveAppContentRoot();
  const mindshareRoot = path.join(appContentRoot, 'mindshare');
  const mojoRoot = path.join(appContentRoot, 'mojo');
  const roleRoot = path.join(mindshareRoot, 'roles', 'maps-agentic-systems-program-architect');
  const automationRoot = path.join(mojoRoot, 'automations', 'vik-handoff-check');
  const env = {
    VIK_ROLE_ROOT: roleRoot,
    VIK_ARCHITECTURE_BACKLOG: path.join(mojoRoot, 'agents', 'vik-aspa', 'architecture-backlog.md'),
    VIK_AUTOMATION_ROOT: automationRoot
  };
  const mode = payload.mode === 'scheduled' ? 'scheduled' : 'manual';
  const level4 = await runPythonAutomation(path.join(roleRoot, 'scripts', 'level4automation.py'), mode, env);
  const level5 = await runPythonAutomation(path.join(roleRoot, 'scripts', 'level5automation.py'), mode, env);
  return {
    ok: level4.ok && level5.ok,
    level4,
    level5,
    result: {
      level4: level4.state?.result || 'unavailable',
      level5: level5.state?.result || 'unavailable'
    }
  };
}

const configurationFileDescriptions = {
  'AGENTS.md': 'Repository instructions, role routing, and operating rules loaded by coding agents.',
  'project-foundation.md': 'MAPS control artifact for project foundation, source roots, and durable memory rules.',
  'gate.md': 'Tool-gate policy that defines approval and execution boundaries.',
  'gate-exceptions.md': 'Approved gate exceptions for narrowly scoped files, roles, or functions.',
  'roles.md': 'Organization roster, role structure, reporting lines, and current standing notes.',
  'role-artifacts.md': 'Inventory of role artifacts, source locations, file gaps, and ownership status.',
  'team-member-file-structure.md': 'Canonical checklist for required team-member files and role completeness.',
  'name.md': 'Identity card with name, title, organization, autonomy level, and role path.',
  'role-agent.md': 'Role contract defining job, scope, boundaries, handoffs, and operating authority.',
  'personality.md': 'Role voice, temperament, collaboration style, and interaction preferences.',
  'workflow.md': 'Role work process, expected inputs, outputs, checks, and handoff flow.',
  'memory.md': 'Durable role memory, history, current context, and important operating notes.',
  'WhoAmI.md': 'Session identity card injected into prompts so the role knows who it is.',
  'Autonomy.md': 'Autonomy contract defining current level and level 4, 5, and 6 capabilities.',
  'state.json': 'Structured current-state record for identity, standing, paths, and runtime metadata.',
  'gate-blocks.md': 'Known gate limitations, blocked actions, and approval routes for the role.',
  'session.md': 'Session routing, thread, or office context for the role.',
  'automation-old.md': 'Legacy automation definition retained for reference after the automation reset.',
  'loop-old.md': 'Legacy schedule or loop definition retained for reference after the automation reset.',
  'hook-spec-old.md': 'Legacy hook proposal retained for reference after the automation reset.',
  'script-spec-old.md': 'Legacy script proposal retained for reference after the automation reset.',
  'level4automation-old.py': 'Legacy level 4 automation script retained for reference after the automation reset.',
  'level5automation-old.py': 'Legacy level 5 automation script retained for reference after the automation reset.'
};

function configurationFileTitle(fileName) {
  const parsed = path.parse(fileName);
  if (fileName === 'AGENTS.md') return 'AGENTS';
  const base = parsed.name || fileName;
  return base
    .replace(/([a-z])([A-Z])/g, '$1 $2')
    .replace(/[-_]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase();
}

function configurationFileDescription(fileName) {
  if (configurationFileDescriptions[fileName]) return configurationFileDescriptions[fileName];
  const ext = path.extname(fileName).toLowerCase();
  if (ext === '.md') return 'Markdown source file for this role, agent, or global operating record.';
  if (ext === '.json') return 'Structured data file used by MindShare Central or role runtime checks.';
  if (ext === '.py') return 'Python script used by a role, automation, or support workflow.';
  return 'Source file available for local review and editing.';
}

function configurationFileRecord(filePath, missing = false) {
  const name = path.basename(filePath);
  return {
    name,
    title: configurationFileTitle(name),
    description: configurationFileDescription(name),
    path: filePath,
    missing
  };
}

async function collectFiles(rootPath) {
  const ignoredNames = new Set(['.git', '.claude', '.codex', '.obsidian', 'node_modules', '__pycache__', '.pytest_cache']);
  const files = [];
  const entries = await readDirForConfiguration(rootPath, { withFileTypes: true });
  for (const entry of entries) {
    if (ignoredNames.has(entry.name)) continue;
    const entryPath = path.join(rootPath, entry.name);
    if (entry.isFile()) {
      files.push(configurationFileRecord(entryPath, false));
    }
  }
  return files.sort((a, b) => a.path.localeCompare(b.path));
}

async function discoverDirectoryGroups(rootPath, label, category) {
  const entries = await readDirForConfiguration(rootPath, { withFileTypes: true });
  const groups = [];
  for (const entry of entries.filter((item) => item.isDirectory()).sort((a, b) => a.name.localeCompare(b.name))) {
    const root = path.join(rootPath, entry.name);
    const files = await collectFiles(root);
    groups.push({
      category,
      label: `${label}: ${entry.name}`,
      root,
      files
    });
  }
  return groups;
}

async function listConfigurationFiles() {
  const roots = sourceRoots();
  const standardPath = path.join(roots.mindshare, 'roles', 'hr-director', 'team-member-file-structure.md');
  const globalCandidates = [
    path.join(roots.mindshare, 'AGENTS.md'),
    path.join(roots.mindshare, 'project-foundation.md'),
    path.join(roots.home, '.codex', 'tool-gate', 'gate.md'),
    path.join(roots.home, '.codex', 'tool-gate', 'gate-exceptions.md'),
    path.join(roots.mindshare, 'roles', 'hr-director', 'team-member-file-structure.md'),
    path.join(roots.mindshareDrive, 'roles.md'),
    path.join(roots.mindshareDrive, 'role-artifacts.md')
  ];
  const globalFiles = [];
  for (const candidate of globalCandidates) {
    globalFiles.push(configurationFileRecord(candidate, !await pathExistsForConfiguration(candidate)));
  }

  const groups = [{
    category: 'global',
    label: 'Global Files',
    root: roots.mindshare,
    files: globalFiles
  }];

  groups.push(
    ...await discoverDirectoryGroups(path.join(roots.mindshare, 'roles'), 'Mindshare Role', 'role'),
    ...await discoverDirectoryGroups(path.join(roots.mindshare, 'agents'), 'Mindshare Agent', 'agent'),
    ...await discoverDirectoryGroups(path.join(roots.mojo, 'agents'), 'Mojo Agent', 'agent'),
    ...await discoverDirectoryGroups(path.join(roots.watch, 'agents'), 'Watch Agent', 'agent')
  );

  const totalFiles = groups.reduce((total, group) => total + group.files.length, 0);
  return {
    ok: true,
    standardPath,
    groups,
    totals: {
      groups: groups.length,
      files: totalFiles
    }
  };
}

async function openConfigurationFile(payload = {}) {
  const filePath = String(payload.path || '');
  const appName = String(payload.app || '').toLowerCase();
  if (!filePath || !await pathExists(filePath)) {
    return { ok: false, error: 'File does not exist.' };
  }
  if (appName === 'notepad') {
    spawn('notepad.exe', [filePath], { detached: true, stdio: 'ignore', windowsHide: false }).unref();
    return { ok: true };
  }
  if (appName === 'vscode') {
    const code = await firstCommand('code.cmd') || await firstCommand('code');
    if (!code) {
      return { ok: false, error: 'VS Code command `code` was not found on PATH.' };
    }
    spawn(code, [filePath], { detached: true, stdio: 'ignore', windowsHide: false }).unref();
    return { ok: true };
  }
  return { ok: false, error: `Unknown editor: ${appName || 'none'}.` };
}

async function loadRoleContext(payload = {}) {
  const roleSlug = String(payload?.roleSlug || payload?.name || '').trim().toLowerCase();
  const role = ROLE_CATALOG[roleSlug];
  if (!role) {
    return {
      ok: false,
      error: `No MindShare Local role context is registered for "${roleSlug}".`
    };
  }

  const appContentRoot = await resolveAppContentRoot();
  const roleRoot = path.join(appContentRoot, ...role.rolePath);
  const files = await Promise.all(role.files.map((fileName) => readRoleFile(roleRoot, fileName)));
  const whoAmI = synthesizeWhoAmI(role, files);
  const roleContext = {
    slug: roleSlug,
    name: role.name,
    title: role.title,
    level: role.level,
    office: role.office,
    roleRoot,
    contentRoot: appContentRoot,
    whoAmI,
    files
  };

  return {
    ok: true,
    roleContext,
    summary: `${role.name} context loaded from ${roleRoot}. ${files.filter((file) => file.exists).length} files loaded, ${files.filter((file) => !file.exists).length} expected files missing.`
  };
}

async function sendCodexMessage(payload) {
  const sessionId = String(payload?.sessionId || '');
  const message = String(payload?.message || '').trim();
  if (!sessions.has(sessionId)) {
    return { ok: false, error: 'No active Codex session.' };
  }
  if (!message) {
    if (!Array.isArray(payload?.attachments) || payload.attachments.length === 0) {
      return { ok: false, error: 'Message is empty.' };
    }
  }

  const status = await codexLoginStatus();
  if (!status.loggedIn) {
    return {
      ok: false,
      action: 'login',
      error: 'Codex CLI is not logged in. Run `codex login` locally, then reconnect.',
      codexStatus: status.status
    };
  }

  const session = sessions.get(sessionId);
  if (payload?.roleContext) {
    session.roleContext = payload.roleContext;
  }
  session.provider = session.provider || 'codex';
  const transcriptItems = Array.isArray(payload?.transcript) ? payload.transcript : session.messages.slice(-MAX_TRANSCRIPT_ITEMS);
  const transcript = compactTranscript(transcriptItems);
  const attachmentText = formatAttachments(payload?.attachments);
  const prompt = `You are connected to the MindShare local office chat.

Respond from inside the active role context when one is selected. Use first person as that role.

${providerRuntimeContext('codex')}

${officeWorkspaceInstruction}

${buildRolePromptContext(session.roleContext)}

Recent conversation only. Older turns stay visible in MindShare but are not resent to keep CLI token use bounded:
${transcript || '(new session)'}

Attached files for this turn:
${attachmentText}

If an attached file has a local path, you may inspect it if your CLI/runtime supports reading that file type. For image files, treat the local path as the image attachment reference.

USER: ${message}
`;

  const launch = await codexLaunch();
  if (!launch) {
    return {
      ok: false,
      action: 'install',
      error: 'Codex CLI is not installed or could not be launched.'
    };
  }
  const result = await run(launch.command, [...launch.argsPrefix,
    'exec',
    '--json',
    '--dangerously-bypass-approvals-and-sandbox',
    '-C',
    repoRoot,
    '-'
  ], { timeout: 900000, input: prompt });

  if (!result.ok) {
    const recovered = extractCodexReply(result.stdout);
    if (recovered.reply) {
      const reply = `${recovered.reply}\n\n[MindShare note: Codex stopped before a clean completion event (${result.code || 'error'}). This is the partial response recovered from the session output.]`;
      session.messages.push({ role: 'user', content: message });
      session.messages.push({ role: 'assistant', content: reply });
      session.updatedAt = new Date().toISOString();
      return { ok: true, reply, tokenUsage: null, partial: true };
    }
    return {
      ok: false,
      error: (result.stderr || result.stdout || 'Codex exec failed.').trim()
    };
  }

  const { events, reply } = extractCodexReply(result.stdout);
  const usageEvent = [...events].reverse().find((event) => event.type === 'turn.completed' && event.usage);
  const tokenUsage = usageEvent?.usage ? normalizeUsage('codex', usageEvent.usage) : null;
  session.messages.push({ role: 'user', content: message });
  session.messages.push({ role: 'assistant', content: reply });
  session.updatedAt = new Date().toISOString();
  return { ok: true, reply, tokenUsage };
}

function resolveDeepSeekApiKey() {
  const fromEnv = process.env.DEEPSEEK_API_KEY || process.env.DEEP_SEEK_API_KEY || process.env.DEEPSEEK_KEY;
  if (fromEnv) return fromEnv;

  try {
    const fs = require('fs');
    const path = require('path');
    const envPath = path.resolve(__dirname, '..', '..', 'mojo', '.env');
    const raw = fs.readFileSync(envPath, 'utf8');
    const lines = raw.split(/\r?\n/);
    const labelPatterns = [
      /polaris\s+routines\s*[-\/]?\s*deepseek/i,
      /deep\s*seek\s+routines\s*[-\/]?\s*mod\s+gen/i,
    ];
    for (let i = 0; i < lines.length; i++) {
      const trimmed = lines[i].trim();
      if (labelPatterns[0].test(trimmed)) {
        for (let j = i + 1; j < lines.length; j++) {
          const next = lines[j].trim();
          if (next && !next.startsWith('#')) return next.replace(/^['"]|['"]$/g, '');
        }
      }
    }
    for (let i = 0; i < lines.length; i++) {
      const trimmed = lines[i].trim();
      if (labelPatterns[1].test(trimmed)) {
        for (let j = i + 1; j < lines.length; j++) {
          const next = lines[j].trim();
          if (next && !next.startsWith('#')) return next.replace(/^['"]|['"]$/g, '');
        }
      }
    }
  } catch (_) {
    // file absent or unreadable — fall through
  }

  return '';
}

async function connectDeepSeek(payload = {}) {
  const apiKey = resolveDeepSeekApiKey();
  if (!apiKey) {
    return {
      ok: false,
      action: 'config',
      message: 'No DeepSeek API key found. Add DEEPSEEK_API_KEY to your .env or Mojo .env file.'
    };
  }
  if (payload?.checkOnly) {
    return {
      ok: true,
      message: 'DeepSeek API key is present and ready.'
    };
  }
  const sessionPayload = await createOrReuseProviderSession('deepseek', payload);
  return {
    ok: true,
    sessionId: sessionPayload.sessionId,
    initialMessage: sessionPayload.initialMessage,
    reused: sessionPayload.reused,
    message: 'Connected to DeepSeek API.',
    roleContext: sessionPayload.roleContext,
    messages: sessionPayload.messages
  };
}

async function getDeepSeekBalance() {
  const apiKey = resolveDeepSeekApiKey();
  if (!apiKey) {
    return {
      ok: false,
      action: 'config',
      error: 'No DeepSeek API key found. Add DEEPSEEK_API_KEY to your .env or Mojo .env file.'
    };
  }

  const baseUrl = (process.env.DEEPSEEK_API_BASE_URL || 'https://api.deepseek.com').replace(/\/+$/, '');
  let response;
  try {
    response = await fetch(`${baseUrl}/user/balance`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        Accept: 'application/json'
      }
    });
  } catch (error) {
    return {
      ok: false,
      error: `DeepSeek balance request failed: ${error.message || String(error)}`
    };
  }

  let payload;
  try {
    payload = await response.json();
  } catch {
    return {
      ok: false,
      error: `DeepSeek balance returned an unreadable response (HTTP ${response.status}).`
    };
  }

  if (!response.ok) {
    return {
      ok: false,
      action: response.status === 401 || response.status === 403 ? 'config' : 'error',
      error: payload?.error?.message || payload?.message || response.statusText || 'DeepSeek balance request failed.'
    };
  }

  const balanceInfos = Array.isArray(payload.balance_infos) ? payload.balance_infos : [];
  const usdBalance = balanceInfos.find((entry) => String(entry.currency || '').toUpperCase() === 'USD');
  const selected = usdBalance || balanceInfos[0] || null;
  if (!selected) {
    return {
      ok: false,
      error: 'DeepSeek balance response did not include a balance entry.',
      raw: payload
    };
  }

  const totalBalance = Number(selected.total_balance || 0);
  const grantedBalance = Number(selected.granted_balance || 0);
  const toppedUpBalance = Number(selected.topped_up_balance || 0);
  const currency = String(selected.currency || 'USD').toUpperCase();
  return {
    ok: true,
    currency,
    totalBalance,
    grantedBalance,
    toppedUpBalance,
    formatted: new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency,
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(totalBalance),
    balanceInfos
  };
}

async function sendDeepSeekMessage(payload) {
  const sessionId = String(payload?.sessionId || '');
  const message = String(payload?.message || '').trim();
  if (!sessions.has(sessionId)) {
    return { ok: false, error: 'No active DeepSeek session.' };
  }
  if (!message) {
    if (!Array.isArray(payload?.attachments) || payload.attachments.length === 0) {
      return { ok: false, error: 'Message is empty.' };
    }
  }

  const apiKey = resolveDeepSeekApiKey();
  if (!apiKey) {
    return {
      ok: false,
      action: 'config',
      error: 'No DeepSeek API key found. Add DEEPSEEK_API_KEY to your .env or Mojo .env file.'
    };
  }

  const session = sessions.get(sessionId);
  if (payload?.roleContext) {
    session.roleContext = payload.roleContext;
  }
  session.provider = session.provider || 'deepseek';
  const transcriptItems = Array.isArray(payload?.transcript) ? payload.transcript : session.messages.slice(-MAX_TRANSCRIPT_ITEMS);
  const transcript = compactTranscript(transcriptItems);
  const attachmentText = formatAttachments(payload?.attachments);
  const model = process.env.DEEPSEEK_MODEL || 'deepseek-v4-flash';
  const systemPrompt = `You are connected to the MindShare local office chat.

Respond from inside the active role context when one is selected. Use first person as that role.

${providerRuntimeContext('deepseek', model)}

${officeWorkspaceInstruction}

${buildRolePromptContext(session.roleContext)}`;

  const userContent = `Recent conversation only. Older turns stay visible in MindShare but are not resent to keep API token use bounded:
${transcript || '(new session)'}

Attached files for this turn:
${attachmentText}

If an attached file has a local path, you may inspect it if your runtime supports reading that file type. For image files, treat the local path as the image attachment reference.

USER: ${message}`;

  const baseUrl = (process.env.DEEPSEEK_API_BASE_URL || 'https://api.deepseek.com').replace(/\/+$/, '');

  let response;
  try {
    response = await fetch(`${baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: userContent }
        ]
      })
    });
  } catch (error) {
    return {
      ok: false,
      error: `DeepSeek API request failed: ${error.message || String(error)}`
    };
  }

  let parsed;
  try {
    parsed = await response.json();
  } catch {
    return {
      ok: false,
      error: `DeepSeek API returned an unreadable response (HTTP ${response.status}).`
    };
  }

  if (!response.ok) {
    const errorText = parsed?.error?.message || parsed?.message || response.statusText || 'DeepSeek API request failed.';
    const isAuthError = response.status === 401 || response.status === 403;
    return {
      ok: false,
      action: isAuthError ? 'config' : 'error',
      error: isAuthError
        ? 'DeepSeek API authentication failed. Check your DEEPSEEK_API_KEY in .env or Mojo .env.'
        : errorText
    };
  }

  const reply = parsed?.choices?.[0]?.message?.content || '';
  if (!reply) {
    return { ok: false, error: 'DeepSeek API returned an empty response.' };
  }

  const rawUsage = parsed?.usage;
  const tokenUsage = rawUsage
    ? normalizeUsage('deepseek', {
      input_tokens: rawUsage.prompt_tokens,
      output_tokens: rawUsage.completion_tokens
    }, {
      model,
      source: 'deepseek-api'
    })
    : null;

  session.messages.push({ role: 'user', content: message });
  session.messages.push({ role: 'assistant', content: reply });
  session.updatedAt = new Date().toISOString();
  return { ok: true, reply, tokenUsage };
}

function parseDeepSeekReview(reply) {
  const text = String(reply || '').trim();
  const jsonMatch = text.match(/```json\s*([\s\S]*?)```/i) || text.match(/(\{[\s\S]*\})/);
  if (jsonMatch) {
    try {
      const parsed = JSON.parse(jsonMatch[1] || jsonMatch[0]);
      return {
        passed: Boolean(parsed.passed),
        summary: String(parsed.summary || ''),
        findings: Array.isArray(parsed.findings) ? parsed.findings.map((finding) => String(finding)) : [],
        notFixed: String(parsed.not_fixed || parsed.notFixed || '')
      };
    } catch {
      // Fall through to text heuristics.
    }
  }
  const passed = /\bpass(ed|es)?\b/i.test(text) && !/\bfail(ed|ure)?\b|bug|risk|issue|regression/i.test(text);
  return {
    passed,
    summary: text.slice(0, 800),
    findings: passed ? [] : [text.slice(0, 1600)],
    notFixed: passed ? '' : 'DeepSeek is review-only in Combo mode and did not modify this file.'
  };
}

async function reviewFileWithDeepSeek(file) {
  const apiKey = resolveDeepSeekApiKey();
  if (!apiKey) {
    return {
      path: file.relativePath,
      absolutePath: file.path,
      status: 'error',
      passed: false,
      summary: 'DeepSeek API key is missing.',
      findings: ['Add DEEPSEEK_API_KEY to .env or Mojo .env, then restart MindShare Central.'],
      notFixed: 'DeepSeek did not review or fix this file because authentication is not configured.'
    };
  }

  let source = '';
  try {
    source = await fs.readFile(file.path, 'utf8');
  } catch (error) {
    return {
      path: file.relativePath,
      absolutePath: file.path,
      status: 'error',
      passed: false,
      summary: `Could not read file for review: ${error.message || error}`,
      findings: [],
      notFixed: 'DeepSeek did not review or fix this file because MindShare could not read it.'
    };
  }

  const model = process.env.DEEPSEEK_REVIEW_MODEL || process.env.DEEPSEEK_MODEL || 'deepseek-v4-flash';
  const prompt = `You are DeepSeek reviewing one file changed by a Claude build turn in MindShare Central Combo mode.

Review only. Do not rewrite the file. Do not propose broad refactors. Focus on concrete bugs, syntax errors, unsafe behavior, broken UI logic, incorrect async flow, API misuse, and regressions likely caused by this change.

Return strict JSON only:
{
  "passed": true or false,
  "summary": "one sentence",
  "findings": ["specific issues, empty when passed"],
  "not_fixed": "why DeepSeek did not fix it; always say review-only if issues remain"
}

File: ${file.relativePath}

Code:
\`\`\`
${truncateText(source, 45000)}
\`\`\``;

  const baseUrl = (process.env.DEEPSEEK_API_BASE_URL || 'https://api.deepseek.com').replace(/\/+$/, '');
  let response;
  try {
    response = await fetch(`${baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: 'system', content: 'You are a precise code reviewer. Return strict JSON only.' },
          { role: 'user', content: prompt }
        ],
        temperature: 0
      })
    });
  } catch (error) {
    return {
      path: file.relativePath,
      absolutePath: file.path,
      status: 'error',
      passed: false,
      summary: `DeepSeek review request failed: ${error.message || String(error)}`,
      findings: [],
      notFixed: 'DeepSeek did not fix this file because the review request failed.'
    };
  }

  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    return {
      path: file.relativePath,
      absolutePath: file.path,
      status: 'error',
      passed: false,
      summary: payload?.error?.message || payload?.message || response.statusText || 'DeepSeek review failed.',
      findings: [],
      notFixed: 'DeepSeek did not fix this file because the API review failed.'
    };
  }

  const reply = payload?.choices?.[0]?.message?.content || '';
  const parsed = parseDeepSeekReview(reply);
  return {
    path: file.relativePath,
    absolutePath: file.path,
    status: parsed.passed ? 'passed' : 'failed',
    passed: parsed.passed,
    summary: parsed.summary || (parsed.passed ? 'Passed DeepSeek review.' : 'DeepSeek reported review findings.'),
    findings: parsed.findings,
    notFixed: parsed.notFixed || (parsed.passed ? '' : 'DeepSeek is review-only in Combo mode and did not modify this file.'),
    raw: reply
  };
}

async function sendComboMessage(payload) {
  const codexSessionId = String(payload?.codexSessionId || '');
  const claudeSessionId = String(payload?.claudeSessionId || '');
  if (!sessions.has(codexSessionId)) return { ok: false, error: 'No active Codex session for Combo communication.' };
  const buildRequested = Boolean(payload?.buildRequested);
  if (!buildRequested) {
    const codexPayload = await sendCodexMessage({
      ...payload,
      sessionId: codexSessionId
    });
    return {
      ...codexPayload,
      combo: {
        mode: 'chat',
        reviews: [],
        changedFiles: [],
        passedCount: 0,
        failedCount: 0
      }
    };
  }
  if (!sessions.has(claudeSessionId)) return { ok: false, error: 'No active Claude session for Combo builds.' };

  const before = await snapshotReviewableCodeFiles(repoRoot);
  const claudePayload = await sendClaudeMessage({
    ...payload,
    sessionId: claudeSessionId
  });
  if (!claudePayload.ok) return claudePayload;

  const changedFiles = await changedReviewableCodeFiles(before, repoRoot);
  const reviews = [];
  for (const file of changedFiles.slice(0, 30)) {
    reviews.push(await reviewFileWithDeepSeek(file));
  }
  const skipped = changedFiles.slice(30).map((file) => ({
    path: file.relativePath,
    absolutePath: file.path,
    status: 'skipped',
    passed: false,
    summary: 'Skipped because Combo limits one turn to 30 reviewed files.',
    findings: [],
    notFixed: 'DeepSeek did not review or fix this file because the review limit was reached.'
  }));
  const allReviews = [...reviews, ...skipped];
  const passedCount = allReviews.filter((review) => review.status === 'passed').length;
  const failedCount = allReviews.filter((review) => review.status === 'failed' || review.status === 'error').length;

  const codexPrompt = `Combo mode completed a Claude build turn and DeepSeek code review.

Write the in-app response to Scott. Be concise and human. Mention:
- Claude performed the build.
- DeepSeek reviewed ${allReviews.length} changed code/script file(s).
- ${passedCount} passed and ${failedCount} need attention.
- Tell Scott the Code Review drawer has file-level results.

Do not claim DeepSeek fixed anything. It is review-only.

Original user request:
${String(payload?.message || '').trim()}

Claude build response:
${truncateText(claudePayload.reply || '', 6000)}

DeepSeek review results:
${truncateText(JSON.stringify(allReviews.map((review) => ({
  path: review.path,
  status: review.status,
  summary: review.summary,
  findings: review.findings,
  notFixed: review.notFixed
})), null, 2), 8000)}
`;

  const codexPayload = await sendCodexMessage({
    ...payload,
    sessionId: codexSessionId,
    message: codexPrompt,
    attachments: []
  });

  return {
    ok: true,
    reply: codexPayload.ok
      ? codexPayload.reply
      : `${claudePayload.reply || 'Claude build completed.'}\n\nDeepSeek reviewed ${allReviews.length} changed code/script file(s): ${passedCount} passed, ${failedCount} need attention. Open the Code Review drawer for details.`,
    tokenUsage: codexPayload.tokenUsage || claudePayload.tokenUsage || null,
    combo: {
      claude: claudePayload,
      codex: codexPayload,
      reviews: allReviews,
      changedFiles,
      passedCount,
      failedCount
    }
  };
}

async function sendClaudeMessage(payload) {
  const sessionId = String(payload?.sessionId || '');
  const message = String(payload?.message || '').trim();
  if (!sessions.has(sessionId)) {
    return { ok: false, error: 'No active Claude session.' };
  }
  if (!message) {
    if (!Array.isArray(payload?.attachments) || payload.attachments.length === 0) {
      return { ok: false, error: 'Message is empty.' };
    }
  }

  const status = await claudeLoginStatus();
  if (!status.loggedIn) {
    return {
      ok: false,
      action: 'login',
      error: 'Claude CLI is not logged in. Run `claude auth login` locally, then reconnect.',
      claudeStatus: status.status
    };
  }

  const session = sessions.get(sessionId);
  if (payload?.roleContext) {
    session.roleContext = payload.roleContext;
  }
  session.provider = session.provider || 'claude';
  const transcriptItems = Array.isArray(payload?.transcript) ? payload.transcript : session.messages.slice(-MAX_TRANSCRIPT_ITEMS);
  const transcript = compactTranscript(transcriptItems);
  const attachmentText = formatAttachments(payload?.attachments);
  const claudeModel = 'sonnet';
  const prompt = `You are connected to the MindShare local office chat.

Respond from inside the active role context when one is selected. Use first person as that role.

${providerRuntimeContext('claude', claudeModel)}

${officeWorkspaceInstruction}

${buildRolePromptContext(session.roleContext)}

Recent conversation only. Older turns stay visible in MindShare but are not resent to keep CLI token use bounded:
${transcript || '(new session)'}

Attached files for this turn:
${attachmentText}

If an attached file has a local path, you may inspect it if your CLI/runtime supports reading that file type. For image files, treat the local path as the image attachment reference.

USER: ${message}
`;

  const launch = await claudeLaunch();
  if (!launch) {
    return {
      ok: false,
      action: 'install',
      error: 'Claude CLI is not installed or could not be launched.'
    };
  }
  const result = await run(launch.command, [...launch.argsPrefix,
    '--print',
    '--output-format',
    'json',
    '--permission-mode',
    'bypassPermissions',
    '--dangerously-skip-permissions',
    '--model',
    claudeModel
  ], { timeout: 900000, input: prompt });

  if (!result.ok) {
    return {
      ok: false,
      error: (result.stderr || result.stdout || 'Claude print failed.').trim()
    };
  }

  let parsed = null;
  try {
    parsed = JSON.parse(result.stdout.trim());
  } catch {
    parsed = null;
  }

  if (parsed?.is_error || parsed?.api_error_status || parsed?.subtype === 'error') {
    const errorText = String(parsed?.result || parsed?.error || result.stderr || result.stdout || 'Claude CLI returned an error.').trim();
    const isAuthError = Number(parsed?.api_error_status || 0) === 401 || /authenticate|authentication|credentials|auth/i.test(errorText);
    return {
      ok: false,
      action: isAuthError ? 'login' : 'error',
      error: isAuthError
        ? 'Claude CLI authentication failed. Run `claude auth login` locally, then reconnect Claude in MindShare Central.'
        : errorText,
      claudeStatus: errorText,
      raw: parsed
    };
  }

  const reply = parsed?.result ?? result.stdout.trim();
  const modelName = parsed?.modelUsage ? Object.keys(parsed.modelUsage)[0] : null;
  const tokenUsage = parsed?.usage
    ? normalizeUsage('claude', parsed.usage, {
      costUsd: typeof parsed.total_cost_usd === 'number' ? parsed.total_cost_usd : null,
      model: modelName,
      source: 'claude-cli-json'
    })
    : null;
  session.messages.push({ role: 'user', content: message });
  session.messages.push({ role: 'assistant', content: reply });
  session.updatedAt = new Date().toISOString();
  return { ok: true, reply, tokenUsage };
}

module.exports = {
  connectCodex,
  connectClaude,
  connectDeepSeek,
  listSessions,
  resetProviderSession,
  loadRoleContext,
  loadConferenceRoomContext,
  listConferenceRoomInviteCandidates,
  listConfigurationFiles,
  openConfigurationFile,
  runTessLevel4Automation,
  runVikAutomation,
  getDeepSeekBalance,
  sendCodexMessage,
  sendClaudeMessage,
  sendComboMessage,
  sendDeepSeekMessage
};
