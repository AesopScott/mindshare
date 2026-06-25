const { spawn } = require('node:child_process');
const crypto = require('node:crypto');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');

const repoRoot = path.resolve(__dirname, '..');
const sessions = new Map();

const ROLE_CATALOG = {
  bea: {
    name: 'Bea',
    title: 'Mojo MAPS Engineer',
    level: 'Level 3 Staff',
    office: "Bea's office",
    roleRoot: path.join(repoRoot, '..', 'mojo', 'roles', 'mojo-maps-engineer'),
    files: [
      'WhoAmI.md',
      'name.md',
      'personality.md',
      'role-agent.md',
      'workflow.md',
      'loop.md',
      'Autonomy.md',
      'memory.md'
    ]
  },
  tess: {
    name: 'Tess',
    title: 'Autonomy Engineer',
    level: 'Level 4 Scoped Autonomy',
    office: "Tess's office",
    roleRoot: path.join(repoRoot, 'roles', 'autonomy-engineer'),
    files: [
      'WhoAmI.md',
      'name.md',
      'personality.md',
      'role-agent.md',
      'workflow.md',
      'loop.md',
      'Autonomy.md',
      'memory.md'
    ]
  }
};

function run(command, args, options = {}) {
  return new Promise((resolve) => {
    const child = spawn(command, args, {
      cwd: repoRoot,
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

  const sessionId = crypto.randomUUID();
  const requestedRoleSlug = String(payload?.roleSlug || '').trim();
  const roleContext = requestedRoleSlug
    ? await loadRoleContext({ roleSlug: requestedRoleSlug }).catch(() => null)
    : null;
  const initialMessage = roleContext?.ok ? `This is ${roleContext.roleContext.name}'s office.` : null;
  sessions.set(sessionId, {
    messages: initialMessage ? [{ role: 'user', content: initialMessage }] : [],
    roleContext: roleContext?.ok ? roleContext.roleContext : null
  });
  return {
    ok: true,
    sessionId,
    initialMessage,
    message: 'Connected to local Codex CLI using local ChatGPT authentication.',
    codexStatus: status.status
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

  const sessionId = crypto.randomUUID();
  const requestedRoleSlug = String(payload?.roleSlug || '').trim();
  const roleContext = requestedRoleSlug
    ? await loadRoleContext({ roleSlug: requestedRoleSlug }).catch(() => null)
    : null;
  const initialMessage = roleContext?.ok ? `This is ${roleContext.roleContext.name}'s office.` : null;
  sessions.set(sessionId, {
    messages: initialMessage ? [{ role: 'user', content: initialMessage }] : [],
    roleContext: roleContext?.ok ? roleContext.roleContext : null
  });
  return {
    ok: true,
    sessionId,
    initialMessage,
    message: 'Connected to local Claude CLI using local Claude authentication.',
    claudeStatus: status.status
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

  const fileSections = roleContext.files
    .filter((file) => file.exists)
    .map((file) => `## ${file.fileName}\nPath: ${file.path}\n\n${file.content}`)
    .join('\n\n---\n\n');

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

${fileSections || '(No canonical role files loaded.)'}

## Missing Expected Files

${missing || '(None)'}`;
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

async function loadRoleContext(payload = {}) {
  const roleSlug = String(payload?.roleSlug || payload?.name || '').trim().toLowerCase();
  const role = ROLE_CATALOG[roleSlug];
  if (!role) {
    return {
      ok: false,
      error: `No MindShare Local role context is registered for "${roleSlug}".`
    };
  }

  const files = await Promise.all(role.files.map((fileName) => readRoleFile(role.roleRoot, fileName)));
  const whoAmI = synthesizeWhoAmI(role, files);
  const roleContext = {
    slug: roleSlug,
    name: role.name,
    title: role.title,
    level: role.level,
    office: role.office,
    roleRoot: role.roleRoot,
    whoAmI,
    files
  };

  return {
    ok: true,
    roleContext,
    summary: `${role.name} context loaded from ${role.roleRoot}. ${files.filter((file) => file.exists).length} files loaded, ${files.filter((file) => !file.exists).length} expected files missing.`
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
  const transcriptItems = Array.isArray(payload?.transcript) ? payload.transcript : session.messages.slice(-12);
  const transcript = transcriptItems
    .map((item) => `${String(item.role || 'message').toUpperCase()}: ${item.content || item.text || ''}`)
    .join('\n');
  const attachmentText = formatAttachments(payload?.attachments);
  const prompt = `You are connected to the MindShare local office chat.

Respond from inside the active role context when one is selected. Use first person as that role. Do not modify files from this chat surface.

${buildRolePromptContext(session.roleContext)}

Conversation so far:
${transcript || '(new session)'}

Attached files for this turn:
${attachmentText}

If an attached file has a local path, you may inspect it if your CLI/runtime supports reading that file type. For image files, treat the local path as the image attachment reference.

USER: ${message}
`;

  const outputPath = path.join(os.tmpdir(), `mindshare-codex-${sessionId}.txt`);
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
    '--sandbox',
    'read-only',
    '-C',
    repoRoot,
    '--output-last-message',
    outputPath,
    '-'
  ], { timeout: 300000, input: prompt });

  if (!result.ok) {
    return {
      ok: false,
      error: (result.stderr || result.stdout || 'Codex exec failed.').trim()
    };
  }

  const reply = (await fs.readFile(outputPath, 'utf8')).trim();
  await fs.rm(outputPath, { force: true });
  session.messages.push({ role: 'user', content: message });
  session.messages.push({ role: 'assistant', content: reply });
  return { ok: true, reply };
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
  const transcriptItems = Array.isArray(payload?.transcript) ? payload.transcript : session.messages.slice(-12);
  const transcript = transcriptItems
    .map((item) => `${String(item.role || 'message').toUpperCase()}: ${item.content || item.text || ''}`)
    .join('\n');
  const attachmentText = formatAttachments(payload?.attachments);
  const prompt = `You are connected to the MindShare local office chat.

Respond from inside the active role context when one is selected. Use first person as that role. Do not modify files from this chat surface.

${buildRolePromptContext(session.roleContext)}

Conversation so far:
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
    '--permission-mode',
    'plan',
    '--model',
    'sonnet'
  ], { timeout: 300000, input: prompt });

  if (!result.ok) {
    return {
      ok: false,
      error: (result.stderr || result.stdout || 'Claude print failed.').trim()
    };
  }

  const reply = result.stdout.trim();
  session.messages.push({ role: 'user', content: message });
  session.messages.push({ role: 'assistant', content: reply });
  return { ok: true, reply };
}

module.exports = {
  connectCodex,
  connectClaude,
  loadRoleContext,
  sendCodexMessage,
  sendClaudeMessage
};
