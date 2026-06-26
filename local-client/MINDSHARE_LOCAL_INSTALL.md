# MindShare Local Development Install

This is the current development path for connecting the MindShare office UI to local Codex CLI.

## Preferred Local Path

Run the local Electron app:

```powershell
cd C:\Users\scott\Code\mindshare\local-client
npm install
npm start
```

The app loads:

- `C:\Users\scott\Code\mindshare\public\departments\index.html`
- `preload.js`, which exposes `window.MindShareLocalClient`
- `mindshare-local-client.js`, which checks Codex install/login state and sends prompts through local Codex CLI

## Authentication

Codex CLI must be installed and logged in locally. The app checks:

- whether Codex can be launched
- whether `codex login status` reports local ChatGPT login
- whether `codex exec` can produce a reply

## Product Note

The Chrome extension/native-host files are retained as experimental reference, not as the preferred product path. The clean local product is an app that owns the local process boundary directly.
