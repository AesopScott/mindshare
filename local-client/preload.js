const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('MindShareLocalClient', {
  connectCodex: (payload) => ipcRenderer.invoke('mindshare:codex-connect', payload),
  connectClaude: (payload) => ipcRenderer.invoke('mindshare:claude-connect', payload),
  loadRoleContext: (payload) => ipcRenderer.invoke('mindshare:role-context', payload),
  runTessLevel4Automation: (payload) => ipcRenderer.invoke('mindshare:tess-level4-automation', payload),
  runVikAutomation: (payload) => ipcRenderer.invoke('mindshare:vik-automation', payload),
  controlAutomation: (payload) => ipcRenderer.invoke('mindshare:automation-control', payload),
  sendCodexMessage: (payload) => ipcRenderer.invoke('mindshare:codex-message', payload),
  sendClaudeMessage: (payload) => ipcRenderer.invoke('mindshare:claude-message', payload),
  chooseFiles: () => ipcRenderer.invoke('mindshare:choose-files')
});
