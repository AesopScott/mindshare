# MindShare Local

MindShare Local is the desktop/local implementation for role-office chat.

The public website can stay visual and informational. Local CLI access belongs here, because a normal browser page cannot directly launch or control Codex CLI or Claude CLI.

## Current Working Path

Run the Departments office inside Electron:

```powershell
npm install
npm run sync-content
npm start
```

`npm run sync-content` refreshes generated runtime content into `local-client/app-content` while preserving the canonical app UI at `local-client/app-content/mindshare/public`. The repo-level `public/` collection is mirror or backup only.

## Build The Installer

From `C:\Users\scott\Code\mindshare\local-client`:

```powershell
npm install
npm run dist:win
npm run verify:package
```

`npm run dist:win` runs the Windows package build and automatically refreshes `app-content` first through `prepack:win`. It creates:

- `release\MindShare Central Setup 0.1.0.exe` - Windows installer.
- `release\MindShare Central 0.1.0.exe` - portable Windows executable.
- `release\win-unpacked\MindShare Central.exe` - unpacked runtime build.

`npm run verify:package` confirms the expected build outputs exist and that the packaged runtime includes the bundled MindShare Central content.

Do not commit the generated `release/` files. They are build artifacts and are intentionally ignored by Git.

The bundled content currently includes:

- MindShare Central UI from `local-client/app-content/mindshare/public/`, plus centralized roles, agents, catalogs, docs, phases, rooms, scripts, skills, templates, `AGENTS.md`, and `project-foundation.md`
- MindShare global roster files copied into `app-content/mindshare/global/`
- Mojo MAPS content from `assets/maps/`
- Mojo MAPS web pages from `maps/`
- Mojo agent files and MAPS content; Mojo role files are copied into centralized MindShare roles before packaging
- Watch agent files; Watch role files are copied into centralized MindShare roles before packaging

The sync is exact for generated app-content areas, but it deliberately preserves `app-content/mindshare/public` because that tree is the canonical app UI. The script verifies paths are inside `local-client` and then copies fresh generated content while excluding Git data, local CLI state, node modules, cache folders, env files, logs, and common key/certificate files.

`app-content/manifest.json` records the bundled content using portable paths so the executable does not carry Scott's machine paths as runtime dependencies.

## Packaging Boundary

The product packaging boundary is tracked in:

- `PACKAGING_MANIFEST.md` for the human-readable source of truth.
- `packaging-manifest.json` for future script/build enforcement.

Update those files before adding new app-bundled content, excluding development-only folders, or moving mutable state into `%APPDATA%\Mindshare Central\`.

The Electron preload exposes:

- The page calls `window.MindShareLocalClient.connectCodex()`.
- The page calls `window.MindShareLocalClient.connectClaude()`.
- The local client checks whether Codex CLI is installed.
- The local client checks `codex login status`.
- The local client asks the user to install or log in when needed.
- The local client sends chat messages through the locally authenticated Codex or Claude CLI.

This keeps ChatGPT and Claude subscription authentication local. No API key or token belongs in the page.

## Verified Locally

The Node adapter can connect to local Codex CLI and Claude CLI and receive responses using local subscription authentication.

## Not The Product Path

The Chrome extension/native-host experiment remains in this folder as reference material, but it is not the preferred local implementation. It is too brittle for the office experience Scott wants.
