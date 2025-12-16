// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  onDisplayMetricsChanged: (cb) => ipcRenderer.on('display-metrics-changed', cb),
  onWindowMoved: (cb) => ipcRenderer.on('window-moved', cb),
  // Expose login function that will call Node-side selenium logic via ipc
  performLogin: (emailLocalPart, password) => ipcRenderer.invoke('perform-login', { emailLocalPart, password })
});