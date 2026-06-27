const { app, BrowserWindow, dialog, ipcMain, Menu, clipboard, shell } = require('electron');
const { spawn } = require('node:child_process');
const path = require('node:path');
const fs = require('node:fs');
const os = require('node:os');
const crypto = require('node:crypto');
const {
  connectCodex,
  connectClaude,
  connectDeepSeek,
  listSessions,
  resetProviderSession,
  loadRoleContext,
  loadConferenceRoomContext,
  listConferenceRoomInviteCandidates,
  runTessLevel4Automation,
  runVikAutomation,
  getDeepSeekBalance,
  sendCodexMessage,
  sendClaudeMessage,
  sendDeepSeekMessage,
  listConfigurationFiles,
  openConfigurationFile
} = require('./mindshare-local-client');

const bundledPublicRoot = path.join(__dirname, 'app-content', 'mindshare', 'public');
const devPublicRoot = path.join(__dirname, '..', 'public');
const skillsSourceRoot = path.join(__dirname, 'app-content', 'mojo', 'assets', 'maps', 'skills');
const sharedTemplatesRoot = path.join(__dirname, 'app-content', 'mojo', 'assets', 'maps', 'templates');
const codexHome = process.env.CODEX_HOME || path.join(os.homedir(), '.codex');
// Skills install into both the Claude Code and Codex skills directories.
const skillsInstallRoots = [
  path.join(os.homedir(), '.claude', 'skills'),
  path.join(codexHome, 'skills')
];
const SKILL_NAME_PATTERN = /^[a-z0-9][a-z0-9-]*$/;
const TEMPLATE_REF_PATTERN = /templates\/([A-Za-z0-9._-]+\.md)/g;

// A skill's SKILL.md references `templates/<name>.md` relative to its own folder.
// The multi-agent-* skills keep those templates centralized in the shared maps
// templates dir, so copy any referenced-but-missing template into the installed
// skill's own templates/ dir to keep it self-contained.
function installRelatedTemplates(skillDir) {
  const skillMd = path.join(skillDir, 'SKILL.md');
  if (!fs.existsSync(skillMd)) return [];
  const text = fs.readFileSync(skillMd, 'utf8');
  const referenced = new Set();
  for (const match of text.matchAll(TEMPLATE_REF_PATTERN)) referenced.add(match[1]);
  const copied = [];
  const skillTemplatesDir = path.join(skillDir, 'templates');
  for (const file of referenced) {
    const localCopy = path.join(skillTemplatesDir, file);
    if (fs.existsSync(localCopy)) continue; // skill already ships this template
    const shared = path.join(sharedTemplatesRoot, file);
    if (!shared.startsWith(sharedTemplatesRoot + path.sep) || !fs.existsSync(shared)) continue;
    fs.mkdirSync(skillTemplatesDir, { recursive: true });
    fs.copyFileSync(shared, localCopy);
    copied.push(file);
  }
  return copied;
}
const appIconPath = path.join(
  __dirname,
  'assets',
  process.platform === 'win32' ? 'mindshare-central-icon.ico' : 'mindshare-central-icon.png'
);
const TESS_LEVEL4_INTERVAL_MS = 30 * 60 * 1000;
const VIK_AUTOMATION_INTERVAL_MS = 30 * 60 * 1000;
let tessLevel4Timer = null;
let vikAutomationTimer = null;
let configurationFileCache = null;
let configurationFileCachePromise = null;
const envLoadedFiles = [];

function loadEnvFile(filePath) {
  if (!fs.existsSync(filePath)) return;
  const text = fs.readFileSync(filePath, 'utf8');
  for (const line of text.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#') || !trimmed.includes('=')) continue;
    const index = trimmed.indexOf('=');
    const name = trimmed.slice(0, index).trim();
    let value = trimmed.slice(index + 1).trim();
    if (!name || process.env[name]) continue;
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    process.env[name] = value;
  }
  envLoadedFiles.push(filePath);
}

function loadLocalEnvFiles() {
  const repoRoot = path.join(__dirname, '..');
  loadEnvFile(path.join(repoRoot, '.env.local'));
  loadEnvFile(path.join(repoRoot, '.env'));
  loadEnvFile(path.join(repoRoot, '..', 'mojo', '.env'));
}

function runPowerShell(script, timeoutMs = 5000) {
  return new Promise((resolve) => {
    const child = spawn('powershell.exe', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-WindowStyle', 'Hidden', '-Command', script], {
      windowsHide: true
    });
    let stdout = '';
    let stderr = '';
    const timeout = setTimeout(() => {
      child.kill();
      resolve({ ok: false, stdout, stderr: stderr || 'PowerShell shortcut process timed out.' });
    }, timeoutMs);
    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    child.on('error', (error) => {
      clearTimeout(timeout);
      resolve({ ok: false, stdout, stderr: error.message || String(error) });
    });
    child.on('close', (code) => {
      clearTimeout(timeout);
      resolve({ ok: code === 0, code, stdout, stderr });
    });
  });
}

async function refreshConfigurationFileCache() {
  configurationFileCachePromise = listConfigurationFiles()
    .then((payload) => {
      configurationFileCache = {
        ...payload,
        cachedAt: new Date().toISOString()
      };
      return configurationFileCache;
    })
    .catch((error) => {
      configurationFileCache = {
        ok: false,
        error: error.message || String(error),
        groups: [],
        totals: { groups: 0, files: 0 },
        cachedAt: new Date().toISOString()
      };
      return configurationFileCache;
    })
    .finally(() => {
      configurationFileCachePromise = null;
    });
  return configurationFileCachePromise;
}

async function getConfigurationFiles() {
  if (configurationFileCache) {
    refreshConfigurationFileCache();
    return configurationFileCache;
  }
  if (configurationFileCachePromise) {
    return configurationFileCachePromise;
  }
  return refreshConfigurationFileCache();
}

function clearAutomationTimer(role) {
  if (role === 'tess' && tessLevel4Timer) {
    clearInterval(tessLevel4Timer);
    tessLevel4Timer = null;
  }
  if (role === 'vik' && vikAutomationTimer) {
    clearInterval(vikAutomationTimer);
    vikAutomationTimer = null;
  }
}

function startAutomationTimer(role) {
  if (role === 'tess' && !tessLevel4Timer) {
    tessLevel4Timer = setInterval(() => {
      runTessLevel4Automation({ mode: 'scheduled' }).catch((error) => {
        console.warn('Tess Level 4 automation scheduled run failed.', error);
      });
    }, TESS_LEVEL4_INTERVAL_MS);
  }
  if (role === 'vik' && !vikAutomationTimer) {
    vikAutomationTimer = setInterval(() => {
      runVikAutomation({ mode: 'scheduled' }).catch((error) => {
        console.warn('Vik automation scheduled run failed.', error);
      });
    }, VIK_AUTOMATION_INTERVAL_MS);
  }
}

async function runAutomationNow(role) {
  if (role === 'tess') return runTessLevel4Automation({ mode: 'manual' });
  if (role === 'vik') return runVikAutomation({ mode: 'manual' });
  return { ok: false, error: `No automation runner is registered for ${role}.` };
}

async function triggerWindowsVoiceShortcut() {
  if (process.platform !== 'win32') {
    return { ok: false, error: 'The microphone shortcut is currently wired for Windows only.' };
  }
  const script = `
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class KeyboardInput {
  [StructLayout(LayoutKind.Sequential)]
  public struct INPUT {
    public UInt32 type;
    public KEYBDINPUT ki;
  }
  [StructLayout(LayoutKind.Sequential)]
  public struct KEYBDINPUT {
    public UInt16 wVk;
    public UInt16 wScan;
    public UInt32 dwFlags;
    public UInt32 time;
    public UIntPtr dwExtraInfo;
  }
  [DllImport("user32.dll")]
  public static extern UInt32 SendInput(UInt32 nInputs, INPUT[] pInputs, Int32 cbSize);
}
"@
$INPUT_KEYBOARD = 1
$KEYUP = 0x0002
$keys = @(0x11, 0x5B, 0x20, 0x20, 0x5B, 0x11)
$flags = @(0, 0, 0, $KEYUP, $KEYUP, $KEYUP)
$inputs = New-Object 'KeyboardInput+INPUT[]' $keys.Length
for ($i = 0; $i -lt $keys.Length; $i++) {
  $inputs[$i].type = $INPUT_KEYBOARD
  $inputs[$i].ki.wVk = [UInt16]$keys[$i]
  $inputs[$i].ki.wScan = 0
  $inputs[$i].ki.dwFlags = [UInt32]$flags[$i]
  $inputs[$i].ki.time = 0
  $inputs[$i].ki.dwExtraInfo = [UIntPtr]::Zero
}
$sent = [KeyboardInput]::SendInput([UInt32]$inputs.Length, $inputs, [Runtime.InteropServices.Marshal]::SizeOf([KeyboardInput+INPUT]))
if ($sent -ne $inputs.Length) {
  throw "SendInput sent $sent of $($inputs.Length) keyboard events."
}
Write-Output "sent=$sent"
`;
  const result = await runPowerShell(script);
  if (!result.ok) {
    return { ok: false, error: (result.stderr || result.stdout || 'Windows SendInput failed.').trim() };
  }
  return { ok: true, message: (result.stdout || '').trim() || 'Shortcut sent.' };
}

function getCloudflareApiToken() {
  return process.env.CLOUDFLARE_API_TOKEN || process.env.CF_API_TOKEN || '';
}

function titleCaseSlug(slug) {
  return String(slug || '')
    .split('-')
    .filter(Boolean)
    .map((part) => part.length <= 2 ? part.toUpperCase() : part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

function discoverMeetupGroups() {
  const watchRoot = path.resolve(__dirname, '..', '..', 'mojo', 'watch');
  if (!fs.existsSync(watchRoot)) return [];
  const groups = new Map();
  const dirs = fs.readdirSync(watchRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort((left, right) => left.localeCompare(right));
  for (const dir of dirs) {
    const indexPath = path.join(watchRoot, dir, 'index.html');
    if (!fs.existsSync(indexPath)) continue;
    const html = fs.readFileSync(indexPath, 'utf8');
    const matches = html.matchAll(/https:\/\/www\.meetup\.com\/(advanced-ai-concepts[^/"?#]*)\/?/gi);
    for (const match of matches) {
      const urlname = String(match[1] || '').trim();
      if (!urlname || groups.has(urlname)) continue;
      const titleMatch = html.match(/<title>([^<|]+)(?:\|[^<]*)?<\/title>/i);
      let city = titleMatch ? titleMatch[1].replace(/^Advanced AI Concepts\s*/i, '').trim() : '';
      if (!city) city = titleCaseSlug(dir);
      groups.set(urlname, {
        urlname,
        city,
        sourcePath: indexPath,
        link: `https://www.meetup.com/${urlname}/`
      });
    }
  }
  return [...groups.values()];
}

function meetupTokenStorePath() {
  const configured = String(process.env.MEETUP_TOKEN_STORE || '').trim();
  if (configured) return configured;
  return path.resolve(__dirname, '..', '..', 'mojo', 'meetup-oauth-token.json');
}

function readMeetupTokenStore() {
  const tokenPath = meetupTokenStorePath();
  if (!fs.existsSync(tokenPath)) {
    throw new Error(`Meetup token store was not found at ${tokenPath}.`);
  }
  const tokens = JSON.parse(fs.readFileSync(tokenPath, 'utf8'));
  if (!tokens?.access_token) {
    throw new Error('Meetup token store does not contain an access token.');
  }
  return { tokenPath, tokens };
}

function writeMeetupTokenStore(tokenPath, tokens) {
  const payload = {
    ...tokens,
    stored_at: new Date().toISOString()
  };
  fs.writeFileSync(tokenPath, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  return payload;
}

async function refreshMeetupToken(tokenPath, tokens) {
  if (!tokens?.refresh_token) {
    throw new Error('Meetup token store does not contain a refresh token.');
  }
  const body = new URLSearchParams({
    client_id: process.env.MEETUP_CLIENT_ID || '',
    client_secret: process.env.MEETUP_CLIENT_SECRET || '',
    grant_type: 'refresh_token',
    refresh_token: tokens.refresh_token
  });
  const response = await fetch('https://secure.meetup.com/oauth2/access', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body
  });
  const refreshed = await response.json().catch(() => ({}));
  if (!response.ok || !refreshed?.access_token) {
    throw new Error(refreshed?.error_description || refreshed?.error || 'Meetup refresh token request failed.');
  }
  return writeMeetupTokenStore(tokenPath, refreshed);
}

async function meetupGraphQL(query, variables = {}) {
  const { tokenPath, tokens } = readMeetupTokenStore();
  const runQuery = async (accessToken) => {
    const response = await fetch('https://api.meetup.com/gql-ext', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query, variables })
    });
    const payload = await response.json().catch(() => ({}));
    return { response, payload };
  };
  let result = await runQuery(tokens.access_token);
  const errorText = JSON.stringify(result.payload?.errors || '');
  if (errorText.includes('access_token_invalid') || result.response.status === 401) {
    const refreshed = await refreshMeetupToken(tokenPath, tokens);
    result = await runQuery(refreshed.access_token);
  }
  if (!result.response.ok || result.payload?.errors?.length) {
    const message = result.payload?.errors?.map((entry) => entry.message).join('; ') || `Meetup GraphQL failed with HTTP ${result.response.status}.`;
    throw new Error(message);
  }
  return result.payload;
}

async function fetchMeetupGroupMembersFromGraphQL(group) {
  const query = `query ($urlname: String!) {
    groupByUrlname(urlname: $urlname) {
      id
      name
      urlname
      city
      state
      country
      link
      stats {
        memberCounts {
          all
        }
      }
    }
  }`;
  const payload = await meetupGraphQL(query, { urlname: group.urlname });
  const node = payload?.data?.groupByUrlname;
  if (!node) {
    throw new Error(`Meetup group ${group.urlname} was not returned by GraphQL.`);
  }
  return {
    ...group,
    id: String(node.id || ''),
    name: String(node.name || group.name || `Advanced AI Concepts ${group.city}`),
    city: String(node.city || group.city),
    state: String(node.state || ''),
    country: String(node.country || ''),
    link: String(node.link || group.link),
    members: Number(node.stats?.memberCounts?.all || 0),
    memberStatus: 'oauth-graphql'
  };
}

function extractMeetupMembers(html) {
  const patterns = [
    /"memberCount"\s*:\s*(\d+)/i,
    /"membersCount"\s*:\s*(\d+)/i,
    /"numberOfMembers"\s*:\s*(\d+)/i,
    /([\d,]+)\s+members/i
  ];
  for (const pattern of patterns) {
    const match = pattern.exec(html);
    if (!match) continue;
    const value = Number(String(match[1] || '').replace(/,/g, ''));
    if (Number.isFinite(value) && value >= 0) return value;
  }
  return null;
}

async function fetchMeetupGroupMembers(group) {
  try {
    return await fetchMeetupGroupMembersFromGraphQL(group);
  } catch (oauthError) {
    const fallback = await fetchMeetupGroupMembersFromPublicPage(group);
    return {
      ...fallback,
      oauthError: oauthError.message || String(oauthError),
      memberStatus: fallback.memberStatus === 'live' ? 'public-fallback' : fallback.memberStatus
    };
  }
}

async function fetchMeetupGroupMembersFromPublicPage(group) {
  try {
    const response = await fetch(group.link, {
      headers: {
        'User-Agent': 'Mozilla/5.0 MindShare Central Meetup Dashboard',
        Accept: 'text/html,application/xhtml+xml'
      }
    });
    const html = await response.text();
    const members = extractMeetupMembers(html);
    const title = /<title>([^<]+)<\/title>/i.exec(html)?.[1] || '';
    const cleanTitle = title.replace(/\s*\|\s*Meetup\s*$/i, '').trim();
    return {
      ...group,
      city: cleanTitle.replace(/^Advanced AI Concepts\s*/i, '').trim() || group.city,
      name: cleanTitle || `Advanced AI Concepts ${group.city}`,
      members: members ?? 0,
      memberStatus: members === null ? 'unknown' : 'live',
      httpStatus: response.status
    };
  } catch (error) {
    return {
      ...group,
      members: 0,
      memberStatus: 'error',
      error: error.message || String(error)
    };
  }
}

async function getMeetupDashboard(payload = {}) {
  const sort = String(payload.sort || 'members-desc');
  const discovered = discoverMeetupGroups();
  const queue = [...discovered];
  const groups = [];
  const workers = Array.from({ length: Math.min(6, queue.length || 1) }, async () => {
    while (queue.length) {
      const group = queue.shift();
      groups.push(await fetchMeetupGroupMembers(group));
    }
  });
  await Promise.all(workers);
  groups.sort((left, right) => {
    if (sort === 'members-asc') return left.members - right.members || left.city.localeCompare(right.city);
    if (sort === 'city') return left.city.localeCompare(right.city);
    return right.members - left.members || left.city.localeCompare(right.city);
  });
  const totalMembers = groups.reduce((sum, group) => sum + Number(group.members || 0), 0);
  return {
    ok: true,
    groups,
    totalMembers,
    groupCount: groups.length,
    sort,
    source: {
      groupSource: 'C:\\Users\\scott\\Code\\mojo\\watch',
      countSource: groups.some((group) => group.memberStatus === 'oauth-graphql')
        ? 'Meetup OAuth GraphQL via Mojo .env token store'
        : 'Meetup public group pages fallback'
    },
    updatedAt: new Date().toISOString()
  };
}

const KLING_MODEL_PRESETS = {
  'kling-video-3': {
    modelName: process.env.KLING_VIDEO_3_MODEL || 'kling-v3-omni',
    label: 'Kling Video 3.0'
  },
  'kling-video-2-6': {
    modelName: process.env.KLING_VIDEO_2_6_MODEL || 'kling-v2-6',
    label: 'Kling Video 2.6'
  }
};

function base64UrlEncode(input) {
  const source = Buffer.isBuffer(input) ? input : Buffer.from(String(input));
  return source.toString('base64').replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
}

function createKlingJwt(accessKeyId, accessKeySecret) {
  const now = Math.floor(Date.now() / 1000);
  const header = { alg: 'HS256', typ: 'JWT' };
  const payload = {
    iss: accessKeyId,
    exp: now + 1800,
    nbf: now - 5
  };
  const encodedHeader = base64UrlEncode(JSON.stringify(header));
  const encodedPayload = base64UrlEncode(JSON.stringify(payload));
  const signature = crypto
    .createHmac('sha256', accessKeySecret)
    .update(`${encodedHeader}.${encodedPayload}`)
    .digest();
  return `${encodedHeader}.${encodedPayload}.${base64UrlEncode(signature)}`;
}

function getKlingCredentials() {
  const cleanCredential = (value) => {
    let cleaned = String(value || '').trim();
    if ((cleaned.startsWith('"') && cleaned.endsWith('"')) || (cleaned.startsWith("'") && cleaned.endsWith("'"))) {
      cleaned = cleaned.slice(1, -1).trim();
    }
    // Kling's console copy affordance can include labels such as "Access Key ID: ...".
    if (/^(access\s*key\s*id|access\s*key\s*secret|secret\s*key|api\s*key)\s*:/i.test(cleaned)) {
      cleaned = cleaned.split(':').slice(1).join(':').trim();
    }
    return cleaned;
  };
  const apiKey = cleanCredential(
    process.env.KLING_API_KEY ||
    process.env.Kling_API_KEY ||
    process.env.KLINGAI_API_KEY ||
    ''
  );
  const accessKeyId = cleanCredential(
    process.env.KLING_ACCESS_KEY_ID ||
    process.env.KLINGAI_ACCESS_KEY_ID ||
    process.env.KLING_API_ACCESS_KEY_ID ||
    process.env.KLING_ACCESS_KEY ||
    ''
  );
  const accessKeySecret = cleanCredential(
    process.env.KLING_ACCESS_KEY_SECRET ||
    process.env.KLINGAI_ACCESS_KEY_SECRET ||
    process.env.KLING_API_ACCESS_KEY_SECRET ||
    process.env.KLING_SECRET_KEY ||
    process.env.KLING_SECRET ||
    ''
  );
  return { apiKey, accessKeyId, accessKeySecret };
}

function getKlingBaseUrl() {
  const raw = process.env.KLING_API_DOMAIN || process.env.KLING_API_BASE_URL || 'https://api-singapore.klingai.com';
  return raw.replace(/\/+$/, '').endsWith('/v1') ? raw.replace(/\/+$/, '') : `${raw.replace(/\/+$/, '')}/v1`;
}

function safeKlingEndpoint(url) {
  return String(url || '').replace(/\/[A-Za-z0-9_-]{12,}(?=$|[/?#])/, '/:task_id');
}

function buildKlingAuthAttempts() {
  const { apiKey, accessKeyId, accessKeySecret } = getKlingCredentials();
  const attempts = [];
  if (apiKey) {
    attempts.push({ mode: 'api_key_bearer', token: apiKey });
    return attempts;
  }
  if (accessKeyId && accessKeySecret) {
    attempts.push({ mode: 'legacy_jwt', token: createKlingJwt(accessKeyId, accessKeySecret) });
  }
  return attempts;
}

function applyMindShareVideoBranding(prompt) {
  const cleanPrompt = String(prompt || '').trim();
  const brandName = process.env.MINDSHARE_VIDEO_BRAND_NAME || 'MindShare Central';
  const logoDirection = process.env.MINDSHARE_VIDEO_LOGO_DIRECTION ||
    `Begin with a clean one-second opening title card showing the ${brandName} wordmark/logo centered on a dark blue-black executive technology background. End with a matching one-second closing card showing the same ${brandName} wordmark/logo centered. Keep the logo sharp, legible, and unobstructed.`;
  if (!cleanPrompt) return logoDirection;
  if (/MindShare Central wordmark\/logo|opening title card showing the MindShare Central/i.test(cleanPrompt)) {
    return cleanPrompt;
  }
  return `${logoDirection}\n\nMain video content:\n${cleanPrompt}`;
}

async function fetchKlingJson(url, options = {}) {
  const authAttempts = buildKlingAuthAttempts();
  if (!authAttempts.length) {
    return {
      ok: false,
      code: 'missing_credentials',
      error: 'Set KLING_API_KEY or KLING_ACCESS_KEY_ID/KLING_ACCESS_KEY_SECRET in a local gitignored env file before starting MindShare Central.',
      source: { envFilesLoaded: envLoadedFiles.length }
    };
  }
  const failures = [];
  for (const authAttempt of authAttempts) {
    let response;
    try {
      response = await fetch(url, {
        ...options,
        headers: {
          Authorization: `Bearer ${authAttempt.token}`,
          'Content-Type': 'application/json',
          ...(options.headers || {})
        }
      });
    } catch (error) {
      failures.push({
        mode: authAttempt.mode,
        code: 'kling_network_error',
        error: error.message || String(error),
        endpoint: safeKlingEndpoint(url)
      });
      continue;
    }
    const payload = await response.json().catch(() => ({}));
    if (!response.ok || payload.code && String(payload.code) !== '0') {
      failures.push({
        mode: authAttempt.mode,
        code: 'kling_request_failed',
        status: response.status,
        error: payload.message || payload.msg || response.statusText || 'Kling request failed.',
        endpoint: safeKlingEndpoint(url),
        payload
      });
      continue;
    }
    return { ok: true, payload, authMode: authAttempt.mode };
  }
  const lastFailure = failures[failures.length - 1] || {};
  return {
    ok: false,
    code: lastFailure.code || 'kling_request_failed',
    status: lastFailure.status,
    error: lastFailure.error || 'Kling request failed.',
    endpoint: lastFailure.endpoint || safeKlingEndpoint(url),
    authMode: lastFailure.mode || 'unknown',
    authFailures: failures.map((failure) => ({
      mode: failure.mode,
      code: failure.code,
      status: failure.status,
      error: failure.error,
      endpoint: failure.endpoint,
      payload: failure.payload
    })),
    payload: lastFailure.payload
  };
}

async function generateOneKlingVideo({ imagePath, prompt, modelPreset, duration, mode, cfgScale, generateAudio, resolution, aspectRatio, voiceId, voiceName }) {
  const preset = KLING_MODEL_PRESETS[modelPreset] || KLING_MODEL_PRESETS['kling-video-3'];
  const hasImage = Boolean(imagePath);
  if (hasImage && !fs.existsSync(imagePath)) {
    return { ok: false, error: `Source image not found: ${imagePath}` };
  }
  const requestPayload = {
    model_name: preset.modelName,
    mode: mode || 'pro',
    duration: String(duration || '10'),
    prompt: applyMindShareVideoBranding(prompt),
    cfg_scale: Number.isFinite(Number(cfgScale)) ? Number(cfgScale) : 0.5
  };
  if (hasImage) {
    requestPayload.image = fs.readFileSync(imagePath).toString('base64');
  }
  if (resolution) {
    requestPayload.resolution = String(resolution);
  }
  if (aspectRatio) {
    requestPayload.aspect_ratio = String(aspectRatio);
  }
  requestPayload.sound = generateAudio ? 'on' : 'off';
  const selectedVoiceId = String(voiceId || '').trim();
  if (generateAudio && selectedVoiceId && selectedVoiceId !== 'auto' && !selectedVoiceId.startsWith('api:')) {
    const voiceDirection = voiceName ? String(voiceName).trim() : selectedVoiceId;
    if (voiceDirection) {
      requestPayload.prompt = `${requestPayload.prompt}\n\nVoice direction: ${voiceDirection}.`;
    }
  }
  if (generateAudio && selectedVoiceId.startsWith('api:')) {
    requestPayload.voice_list = [{
      voice_id: selectedVoiceId.slice(4),
      voice_language: 'en'
    }];
    if (voiceName) {
      requestPayload.voice_list[0].voice_name = String(voiceName);
    }
  }

  const baseUrl = getKlingBaseUrl();
  const generationType = hasImage ? 'image2video' : 'text2video';
  const startedAt = Date.now();
  const submit = await fetchKlingJson(`${baseUrl}/videos/${generationType}`, {
    method: 'POST',
    body: JSON.stringify(requestPayload)
  });
  if (!submit.ok) return { ...submit, stage: 'submit', model: preset.label, modelName: preset.modelName, generationType };
  const taskId = submit.payload?.data?.task_id;
  if (!taskId) {
    return { ok: false, code: 'missing_task_id', error: 'Kling did not return a task_id.', payload: submit.payload };
  }

  const maxPolls = Number(process.env.KLING_MAX_POLLS || 180) || 180;
  const pollMs = Number(process.env.KLING_POLL_MS || 5000) || 5000;
  for (let attempt = 0; attempt < maxPolls; attempt += 1) {
    await new Promise((resolve) => setTimeout(resolve, pollMs));
    const status = await fetchKlingJson(`${baseUrl}/videos/${generationType}/${taskId}`, { method: 'GET' });
    if (!status.ok) return { ...status, stage: 'poll', taskId, attempt: attempt + 1 };
    const data = status.payload?.data || {};
    const taskStatus = data.task_status;
    if (taskStatus === 'succeed') {
      const url = data.task_result?.videos?.[0]?.url;
      if (!url) return { ok: false, code: 'missing_video_url', error: 'Kling task succeeded but did not return a video URL.', payload: status.payload };
      return {
        ok: true,
        taskId,
        url,
        model: preset.label,
        modelName: preset.modelName,
        generationType,
        authMode: status.authMode || submit.authMode,
        sourceImage: imagePath || '',
        prompt: requestPayload.prompt,
        elapsedMs: Date.now() - startedAt
      };
    }
    if (taskStatus === 'failed') {
      return {
        ok: false,
        code: 'task_failed',
        taskId,
        error: data.task_status_msg || 'Kling task failed.',
        stage: 'poll',
        payload: status.payload
      };
    }
  }
  return { ok: false, code: 'task_timeout', taskId, stage: 'poll', error: 'Kling video generation timed out.' };
}

async function generateKlingVideo(payload = {}) {
  const images = Array.isArray(payload.images) ? payload.images : [];
  const prompt = String(payload.prompt || '').trim();
  const outputCount = Math.max(1, Math.min(4, Number(payload.outputCount || 1) || 1));
  if (!prompt) return { ok: false, error: 'Enter a Kling video prompt.' };
  const results = [];
  const selectedImages = images.slice(0, 6);
  for (let round = 0; round < outputCount; round += 1) {
    const imageQueue = selectedImages.length ? selectedImages : [{ path: '' }];
    for (const image of imageQueue) {
      const result = await generateOneKlingVideo({
        imagePath: String(image.path || ''),
        prompt,
        modelPreset: payload.modelPreset,
        duration: payload.duration,
        mode: payload.mode,
        cfgScale: payload.cfgScale,
        generateAudio: Boolean(payload.generateAudio),
        resolution: payload.resolution,
        aspectRatio: payload.aspectRatio,
        voiceId: payload.voiceId,
        voiceName: payload.voiceName
      });
      results.push(result);
      if (!result.ok) break;
    }
    if (results.some((entry) => !entry.ok)) break;
  }
  const ok = results.every((entry) => entry.ok);
  return {
    ok,
    results,
    error: ok ? undefined : results.find((entry) => !entry.ok)?.error || 'Kling generation failed.',
    failure: ok ? undefined : results.find((entry) => !entry.ok)
  };
}

async function fetchCloudflareJson(url, options = {}) {
  const token = getCloudflareApiToken();
  if (!token) {
    return {
      ok: false,
      code: 'missing_credentials',
      error: 'Set CLOUDFLARE_API_TOKEN or CF_API_TOKEN before starting MindShare Central.'
    };
  }
  const response = await fetch(url, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...(options.headers || {})
    }
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok || payload.success === false || payload.errors?.length) {
    return {
      ok: false,
      code: 'cloudflare_request_failed',
      status: response.status,
      error: payload.errors?.map((entry) => entry.message).join('; ') || response.statusText || 'Cloudflare request failed.',
      payload
    };
  }
  return { ok: true, payload };
}

function resolveCloudflareAnalyticsRange(rawRange) {
  const range = String(rawRange || process.env.CLOUDFLARE_ANALYTICS_RANGE || '').toLowerCase();
  if (range === '7d' || range === 'week') return { key: '7d', label: '7 days', hours: 7 * 24, days: 7 };
  if (range === '30d' || range === 'month') return { key: '30d', label: '30 days', hours: 30 * 24, days: 30 };
  return { key: '24h', label: '24 hours', hours: Number(process.env.CLOUDFLARE_ANALYTICS_HOURS || 24) || 24, days: 1 };
}

function buildCloudflareTimeSlices(start, end) {
  const slices = [];
  let cursor = new Date(start);
  while (cursor < end) {
    const next = new Date(Math.min(cursor.getTime() + 24 * 60 * 60 * 1000, end.getTime()));
    slices.push({ start: new Date(cursor), end: next });
    cursor = next;
  }
  return slices;
}

async function fetchCloudflareZoneTraffic(zone, query, slices, dailyQuery = null, dailyFilter = null) {
  const totals = { requests: 0, visits: 0, bytes: 0 };
  const errors = [];
  if (dailyQuery && dailyFilter) {
    const analyticsResult = await fetchCloudflareJson('https://api.cloudflare.com/client/v4/graphql', {
      method: 'POST',
      body: JSON.stringify({
        query: dailyQuery,
        variables: {
          zoneTag: zone.id,
          filter: dailyFilter
        }
      })
    });
    if (!analyticsResult.ok) {
      errors.push(analyticsResult.error);
    } else {
      const groups = analyticsResult.payload?.data?.viewer?.zones?.[0]?.httpRequests1dGroups || [];
      for (const group of groups) {
        totals.requests += Number(group.sum?.requests || 0);
        totals.visits += Number(group.uniq?.uniques || 0);
        totals.bytes += Number(group.sum?.bytes || 0);
      }
    }
    return {
      name: zone.name,
      zoneId: zone.id,
      ...totals,
      error: errors.length ? errors.slice(0, 2).join('; ') : undefined
    };
  }
  for (const slice of slices) {
    const analyticsResult = await fetchCloudflareJson('https://api.cloudflare.com/client/v4/graphql', {
      method: 'POST',
      body: JSON.stringify({
        query,
        variables: {
          zoneTag: zone.id,
          filter: {
            datetime_geq: slice.start.toISOString(),
            datetime_leq: slice.end.toISOString()
          }
        }
      })
    });
    if (!analyticsResult.ok) {
      errors.push(analyticsResult.error);
      continue;
    }
    const group = analyticsResult.payload?.data?.viewer?.zones?.[0]?.httpRequestsAdaptiveGroups?.[0] || {};
    totals.requests += Number(group.count || 0);
    totals.visits += Number(group.sum?.visits || 0);
    totals.bytes += Number(group.sum?.edgeResponseBytes || 0);
  }
  return {
    name: zone.name,
    zoneId: zone.id,
    ...totals,
    error: errors.length ? errors.slice(0, 2).join('; ') : undefined
  };
}

async function getCloudflareTopSites(payload = {}) {
  const range = resolveCloudflareAnalyticsRange(payload.range);
  const hours = range.hours;
  const end = new Date();
  const start = new Date(end.getTime() - Math.max(1, hours) * 60 * 60 * 1000);
  const slices = buildCloudflareTimeSlices(start, end);
  const zonesUrl = new URL('https://api.cloudflare.com/client/v4/zones');
  zonesUrl.searchParams.set('per_page', '50');
  zonesUrl.searchParams.set('status', 'active');
  const accountId = process.env.CLOUDFLARE_ACCOUNT_ID || process.env.CF_ACCOUNT_ID || '';
  if (accountId) zonesUrl.searchParams.set('account.id', accountId);

  const zonesResult = await fetchCloudflareJson(zonesUrl.toString());
  if (!zonesResult.ok) return zonesResult;
  const zones = Array.isArray(zonesResult.payload.result) ? zonesResult.payload.result : [];
  if (!zones.length) {
    return {
      ok: true,
      sites: [],
      summary: { requests: 0, visits: 0, bytes: 0, zoneCount: 0, hours, range: range.key },
      updatedAt: end.toISOString(),
      window: { start: start.toISOString(), end: end.toISOString(), hours, range: range.key, label: range.label }
    };
  }

  const query = `
    query ZoneTraffic($zoneTag: string!, $filter: ZoneHttpRequestsAdaptiveGroupsFilter_InputObject) {
      viewer {
        zones(filter: { zoneTag: $zoneTag }) {
          httpRequestsAdaptiveGroups(limit: 1, filter: $filter) {
            count
            sum {
              edgeResponseBytes
              visits
            }
          }
        }
      }
    }
  `;
  const dailyQuery = `
    query ZoneDailyTraffic($zoneTag: string!, $filter: ZoneHttpRequests1dGroupsFilter_InputObject) {
      viewer {
        zones(filter: { zoneTag: $zoneTag }) {
          httpRequests1dGroups(limit: 40, filter: $filter) {
            sum {
              bytes
              requests
            }
            uniq {
              uniques
            }
            dimensions {
              date
            }
          }
        }
      }
    }
  `;
  const dailyStart = new Date(end);
  dailyStart.setUTCDate(dailyStart.getUTCDate() - Math.max(0, range.days - 1));
  const dailyFilter = slices.length > 1
    ? {
        date_geq: dailyStart.toISOString().slice(0, 10),
        date_leq: end.toISOString().slice(0, 10)
      }
    : null;
  const sites = [];
  const zoneQueue = [...zones];
  const workers = Array.from({ length: Math.min(5, zoneQueue.length) }, async () => {
    while (zoneQueue.length) {
      const zone = zoneQueue.shift();
      sites.push(await fetchCloudflareZoneTraffic(zone, query, slices, dailyQuery, dailyFilter));
    }
  });
  await Promise.all(workers);
  const analyticsErrors = sites
    .filter((site) => site.error)
    .map((site) => ({ zone: site.name, error: site.error }));
  const allAnalyticsFailed = sites.length > 0 && sites.every((site) => site.error && site.requests === 0 && site.visits === 0 && site.bytes === 0);
  if (allAnalyticsFailed) {
    const rangeError = analyticsErrors.find((entry) => /time range wider than 1d/i.test(entry.error || ''));
    if (rangeError) {
      return {
        ok: false,
        code: 'analytics_range_failed',
        error: 'Cloudflare rejected the requested analytics range even after daily slicing. Try 24 hours first, then restart MindShare Central if this persists.',
        details: analyticsErrors.slice(0, 3),
        source: {
          credentialsLoaded: Boolean(getCloudflareApiToken()),
          envFilesLoaded: envLoadedFiles.length,
          zoneCount: zones.length
        }
      };
    }
  }
  if (allAnalyticsFailed) {
    return {
      ok: false,
      code: 'analytics_permission_required',
      error: 'Cloudflare zones loaded, but this token cannot read zone analytics. Add Zone:Analytics Read permission for the zones you want in the Top 10 view.',
      details: analyticsErrors.slice(0, 3),
      source: {
        credentialsLoaded: Boolean(getCloudflareApiToken()),
        envFilesLoaded: envLoadedFiles.length,
        zoneCount: zones.length
      }
    };
  }
  const topSites = sites
    .sort((left, right) => right.requests - left.requests)
    .slice(0, 10)
    .map((site, index) => ({ ...site, rank: index + 1 }));
  const summary = topSites.reduce((acc, site) => ({
    requests: acc.requests + site.requests,
    visits: acc.visits + site.visits,
    bytes: acc.bytes + site.bytes,
    zoneCount: zones.length,
    hours,
    range: range.key
  }), { requests: 0, visits: 0, bytes: 0, zoneCount: zones.length, hours, range: range.key });

  return {
    ok: true,
    sites: topSites,
    summary,
    source: {
      credentialsLoaded: Boolean(getCloudflareApiToken()),
      envFilesLoaded: envLoadedFiles.length
    },
    updatedAt: end.toISOString(),
    window: { start: start.toISOString(), end: end.toISOString(), hours, range: range.key, label: range.label }
  };
}

function installOneSkill(rawName) {
  const name = String(rawName || '').trim();
  if (!name || !SKILL_NAME_PATTERN.test(name)) {
    return { name, ok: false, error: 'Invalid skill name.' };
  }
  const source = path.join(skillsSourceRoot, name);
  // Guard against path traversal: resolved source must stay under the source root.
  if (source !== path.join(skillsSourceRoot, name) || !source.startsWith(skillsSourceRoot + path.sep)) {
    return { name, ok: false, error: 'Skill path is not allowed.' };
  }
  if (!fs.existsSync(path.join(source, 'SKILL.md'))) {
    return { name, ok: false, error: 'Skill not found in the app bundle.' };
  }
  try {
    let templates = 0;
    const dests = [];
    for (const root of skillsInstallRoots) {
      const dest = path.join(root, name);
      fs.mkdirSync(root, { recursive: true });
      fs.rmSync(dest, { recursive: true, force: true }); // overwrite existing
      fs.cpSync(source, dest, { recursive: true });
      templates += installRelatedTemplates(dest).length;
      dests.push(dest);
    }
    return { name, ok: true, dests, templates };
  } catch (error) {
    return { name, ok: false, error: error.message || String(error) };
  }
}

function installSkills(names) {
  const list = Array.isArray(names) ? names : [];
  const results = list.map(installOneSkill);
  const installed = results.filter((r) => r.ok).map((r) => r.name);
  const failed = results.filter((r) => !r.ok).map((r) => ({ name: r.name, error: r.error }));
  const templates = results.reduce((sum, r) => sum + ((r.ok && r.templates) || 0), 0);
  return { ok: failed.length === 0, installed, failed, templates, roots: skillsInstallRoots };
}

function createWindow() {
  const window = new BrowserWindow({
    width: 1440,
    height: 960,
    icon: appIconPath,
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      webviewTag: true
    }
  });

  window.maximize();
  const publicRoot = require('node:fs').existsSync(path.join(bundledPublicRoot, 'index.html'))
    ? bundledPublicRoot
    : devPublicRoot;
  window.loadFile(path.join(publicRoot, 'index.html'));
  window.webContents.on('render-process-gone', (_event, details) => {
    console.error('MindShare renderer process exited.', details);
  });
  window.webContents.on('unresponsive', () => {
    console.error('MindShare renderer became unresponsive.');
  });
  window.webContents.on('responsive', () => {
    console.warn('MindShare renderer became responsive again.');
  });
  window.webContents.on('before-input-event', (event, input) => {
    const key = String(input.key || '').toLowerCase();
    const isRefresh = key === 'f5' || (key === 'r' && (input.control || input.meta));
    if (isRefresh) {
      event.preventDefault();
      window.webContents.reloadIgnoringCache();
    }
  });
}

function installApplicationMenu() {
  // No native application menu — removes the View/Edit bar at the top of the window.
  // Refresh (Ctrl+R / F5) is still handled by the before-input-event hook in createWindow.
  Menu.setApplicationMenu(null);
}

ipcMain.handle('mindshare:codex-connect', async (_event, payload) => connectCodex(payload));
ipcMain.handle('mindshare:claude-connect', async (_event, payload) => connectClaude(payload));
ipcMain.handle('mindshare:sessions', async () => listSessions());
ipcMain.handle('mindshare:session-reset', async (_event, payload) => resetProviderSession(payload));
ipcMain.handle('mindshare:role-context', async (_event, payload) => loadRoleContext(payload));
ipcMain.handle('mindshare:conference-room-context', async () => loadConferenceRoomContext());
ipcMain.handle('mindshare:conference-room-invite-candidates', async () => ({
  ok: true,
  inviteCandidates: listConferenceRoomInviteCandidates()
}));
ipcMain.handle('mindshare:tess-level4-automation', async (_event, payload) => runTessLevel4Automation(payload));
ipcMain.handle('mindshare:vik-automation', async (_event, payload) => runVikAutomation(payload));
ipcMain.handle('mindshare:automation-control', async (_event, payload = {}) => {
  const role = String(payload.role || '').toLowerCase();
  const action = String(payload.action || '').toLowerCase();
  if (!['tess', 'vik'].includes(role)) return { ok: false, error: `No automation timer is registered for ${role || 'that role'}.` };
  if (action === 'run') return { ok: true, action, role, result: await runAutomationNow(role) };
  if (action === 'pause') {
    clearAutomationTimer(role);
    return { ok: true, action, role, timerActive: false };
  }
  if (action === 'stop') {
    clearAutomationTimer(role);
    return { ok: true, action, role, timerActive: false };
  }
  if (action === 'resume') {
    startAutomationTimer(role);
    return { ok: true, action, role, timerActive: true };
  }
  return { ok: false, error: `Unsupported automation action: ${action || 'none'}.` };
});
ipcMain.handle('mindshare:codex-message', async (_event, payload) => sendCodexMessage(payload));
ipcMain.handle('mindshare:claude-message', async (_event, payload) => sendClaudeMessage(payload));
ipcMain.handle('mindshare:deepseek-connect', async (_event, payload) => connectDeepSeek(payload));
ipcMain.handle('mindshare:deepseek-message', async (_event, payload) => sendDeepSeekMessage(payload));
ipcMain.handle('mindshare:deepseek-balance', async () => getDeepSeekBalance());
ipcMain.handle('mindshare:configuration-files', async () => getConfigurationFiles());
ipcMain.handle('mindshare:open-configuration-file', async (_event, payload) => openConfigurationFile(payload));
ipcMain.handle('mindshare:microphone-shortcut', async () => triggerWindowsVoiceShortcut());
ipcMain.handle('mindshare:choose-files', async () => {
  const result = await dialog.showOpenDialog({
    title: 'Attach files',
    properties: ['openFile', 'multiSelections']
  });
  if (result.canceled) {
    return { ok: true, files: [] };
  }
  return {
    ok: true,
    files: result.filePaths.map((filePath) => ({
      path: filePath,
      name: path.basename(filePath)
    }))
  };
});
ipcMain.handle('mindshare:choose-image-files', async () => {
  const result = await dialog.showOpenDialog({
    title: 'Choose source images',
    defaultPath: path.join(process.env.USERPROFILE || process.env.HOME || '', 'Pictures'),
    properties: ['openFile', 'multiSelections'],
    filters: [
      { name: 'Images', extensions: ['png', 'jpg', 'jpeg', 'webp', 'gif'] },
      { name: 'All Files', extensions: ['*'] }
    ]
  });
  if (result.canceled) {
    return { ok: true, files: [] };
  }
  return {
    ok: true,
    files: result.filePaths.map((filePath) => ({
      path: filePath,
      name: path.basename(filePath)
    }))
  };
});
ipcMain.handle('mindshare:copy-text', async (_event, payload = {}) => {
  clipboard.writeText(String(payload.text || ''));
  return { ok: true };
});
ipcMain.handle('mindshare:show-file', async (_event, payload = {}) => {
  const filePath = String(payload.path || '');
  if (!filePath) return { ok: false, error: 'No file path provided.' };
  shell.showItemInFolder(filePath);
  return { ok: true };
});
ipcMain.handle('mindshare:install-skill', async (_event, payload = {}) => installSkills([payload.name]));
ipcMain.handle('mindshare:install-skills', async (_event, payload = {}) => installSkills(payload.names));
ipcMain.handle('mindshare:cloudflare-top-sites', async (_event, payload = {}) => getCloudflareTopSites(payload));
ipcMain.handle('mindshare:meetup-dashboard', async (_event, payload = {}) => getMeetupDashboard(payload));
ipcMain.handle('mindshare:kling-generate-video', async (_event, payload = {}) => generateKlingVideo(payload));

app.whenReady().then(() => {
  loadLocalEnvFiles();
  app.setName('MindShare Central');
  if (process.platform === 'win32') {
    app.setAppUserModelId('com.mindshare.central');
  }
  app.on('child-process-gone', (_event, details) => {
    console.error('MindShare child process exited.', details);
  });
  installApplicationMenu();
  refreshConfigurationFileCache();
  createWindow();
  runTessLevel4Automation({ mode: 'scheduled' }).catch((error) => {
    console.warn('Tess Level 4 automation startup run failed.', error);
  });
  startAutomationTimer('tess');
  runVikAutomation({ mode: 'scheduled' }).catch((error) => {
    console.warn('Vik automation startup run failed.', error);
  });
  startAutomationTimer('vik');
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    clearAutomationTimer('tess');
    clearAutomationTimer('vik');
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
