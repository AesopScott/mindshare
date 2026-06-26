const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('MindShareLocalClient', {
  connectCodex: (payload) => ipcRenderer.invoke('mindshare:codex-connect', payload),
  connectClaude: (payload) => ipcRenderer.invoke('mindshare:claude-connect', payload),
  listSessions: () => ipcRenderer.invoke('mindshare:sessions'),
  resetSession: (payload) => ipcRenderer.invoke('mindshare:session-reset', payload),
  loadRoleContext: (payload) => ipcRenderer.invoke('mindshare:role-context', payload),
  runTessLevel4Automation: (payload) => ipcRenderer.invoke('mindshare:tess-level4-automation', payload),
  runVikAutomation: (payload) => ipcRenderer.invoke('mindshare:vik-automation', payload),
  controlAutomation: (payload) => ipcRenderer.invoke('mindshare:automation-control', payload),
  sendCodexMessage: (payload) => ipcRenderer.invoke('mindshare:codex-message', payload),
  sendClaudeMessage: (payload) => ipcRenderer.invoke('mindshare:claude-message', payload),
  listConfigurationFiles: () => ipcRenderer.invoke('mindshare:configuration-files'),
  openConfigurationFile: (payload) => ipcRenderer.invoke('mindshare:open-configuration-file', payload),
  triggerMicrophoneShortcut: () => ipcRenderer.invoke('mindshare:microphone-shortcut'),
  chooseFiles: () => ipcRenderer.invoke('mindshare:choose-files'),
  chooseImageFiles: () => ipcRenderer.invoke('mindshare:choose-image-files'),
  copyText: (payload) => ipcRenderer.invoke('mindshare:copy-text', payload),
  showFile: (payload) => ipcRenderer.invoke('mindshare:show-file', payload),
  installSkill: (payload) => ipcRenderer.invoke('mindshare:install-skill', payload),
  installSkills: (payload) => ipcRenderer.invoke('mindshare:install-skills', payload)
});
