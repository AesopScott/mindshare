# MindShare Local

MindShare Local is the desktop/local implementation for role-office chat.

The public website can stay visual and informational. Local CLI access belongs here, because a normal browser page cannot directly launch or control Codex CLI or Claude CLI.

## Current Working Path

Run the Departments office inside Electron:

```powershell
npm install
npm start
```

The Electron preload exposes:

- The page calls `window.MindShareLocalClient.connectCodex()`.
- The local client checks whether Codex CLI is installed.
- The local client checks `codex login status`.
- The local client asks the user to install or log in when needed.
- The local client sends chat messages through the locally authenticated Codex CLI.

This keeps ChatGPT subscription authentication local. No API key or token belongs in the page.

## Verified Locally

The Node adapter can connect to local Codex CLI and receive a response through `codex exec` using local ChatGPT authentication.

## Not The Product Path

The Chrome extension/native-host experiment remains in this folder as reference material, but it is not the preferred local implementation. It is too brittle for the office experience Scott wants.
