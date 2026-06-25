const { app, BrowserWindow, dialog, ipcMain, Menu } = require('electron');
const path = require('node:path');
const { connectCodex, connectClaude, loadRoleContext, runTessLevel4Automation, sendCodexMessage, sendClaudeMessage } = require('./mindshare-local-client');

const bundledPublicRoot = path.join(__dirname, 'app-content', 'mindshare', 'public');
const devPublicRoot = path.join(__dirname, '..', 'public');
const TESS_LEVEL4_INTERVAL_MS = 30 * 60 * 1000;
let tessLevel4Timer = null;

function createWindow() {
  const window = new BrowserWindow({
    width: 1440,
    height: 960,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  window.maximize();
  const publicRoot = require('node:fs').existsSync(path.join(bundledPublicRoot, 'index.html'))
    ? bundledPublicRoot
    : devPublicRoot;
  window.loadFile(path.join(publicRoot, 'index.html'));
}

function installApplicationMenu() {
  const template = [
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' },
        { role: 'pasteAndMatchStyle' },
        { role: 'selectAll' }
      ]
    }
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

ipcMain.handle('mindshare:codex-connect', async (_event, payload) => connectCodex(payload));
ipcMain.handle('mindshare:claude-connect', async (_event, payload) => connectClaude(payload));
ipcMain.handle('mindshare:role-context', async (_event, payload) => loadRoleContext(payload));
ipcMain.handle('mindshare:tess-level4-automation', async (_event, payload) => runTessLevel4Automation(payload));
ipcMain.handle('mindshare:codex-message', async (_event, payload) => sendCodexMessage(payload));
ipcMain.handle('mindshare:claude-message', async (_event, payload) => sendClaudeMessage(payload));
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

app.whenReady().then(() => {
  installApplicationMenu();
  createWindow();
  runTessLevel4Automation({ mode: 'scheduled' }).catch((error) => {
    console.warn('Tess Level 4 automation startup run failed.', error);
  });
  tessLevel4Timer = setInterval(() => {
    runTessLevel4Automation({ mode: 'scheduled' }).catch((error) => {
      console.warn('Tess Level 4 automation scheduled run failed.', error);
    });
  }, TESS_LEVEL4_INTERVAL_MS);
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (tessLevel4Timer) {
      clearInterval(tessLevel4Timer);
    }
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
