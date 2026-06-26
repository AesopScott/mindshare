# MindShare Chrome Extension

This extension lets the MindShare website talk to the local MindShare native host, which then talks to the locally authenticated Codex CLI.

The website does not receive Codex credentials and does not call localhost directly. The browser extension owns the browser bridge. The native host owns local machine access.

Development extension ID:

```text
fomlcadcldjpnlbapddpmlikinmdiiji
```

## Development Install

1. Open Chrome and go to `chrome://extensions`.
2. Turn on Developer mode.
3. Click Load unpacked.
4. Select this folder: `%USERPROFILE%\MindShare\local-client\chrome-extension`.
5. Register the native host:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\MindShare\local-client\install-mindshare-local.ps1"
```

7. Make sure Codex CLI is installed and logged in locally:

```powershell
codex login status
```

8. Open the MindShare site and click `Connect Codex`.

## What It Does

- Injects `window.MindShareLocalClient` into approved MindShare pages.
- Forwards `connectCodex` and `sendCodexMessage` requests to Chrome's background service worker.
- Uses Chrome Native Messaging to call the local MindShare native host.
- The native host calls the local Codex CLI using the local subscription login.

## Current Scope

- Codex is wired.
- Claude is intentionally not wired yet.
- This is a development install. A packaged public install flow still needs a signed Chrome Web Store extension or enterprise/policy distribution.
