# MindShare Native Host

This is the local machine side of the MindShare Chrome extension.

Chrome cannot let a normal web page launch local programs. Chrome Native Messaging is the approved bridge:

`MindShare website -> Chrome extension -> native host -> local Codex CLI`

## Register For Chrome

1. Load the Chrome extension from `%USERPROFILE%\MindShare\local-client\chrome-extension`.
2. Register this native host:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\MindShare\local-client\install-mindshare-local.ps1"
```

The installer writes a Chrome Native Messaging registry entry under the current user only.
