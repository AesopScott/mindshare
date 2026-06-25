const { app, BrowserWindow, dialog, ipcMain, Menu } = require('electron');
const path = require('node:path');
const { connectCodex, connectClaude, loadRoleContext, sendCodexMessage, sendClaudeMessage } = require('./mindshare-local-client');

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
  window.loadFile(path.join(__dirname, '..', 'public', 'index.html'));
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
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
