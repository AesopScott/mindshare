# Mindshare Central Packaging Manifest

Version: 0.1.0
Last updated: 2026-06-26
Owner: Tess / Autonomy Engineer

## Purpose

This manifest defines what belongs in Mindshare Central as an installed desktop product, what is bundled as role/content data, what is development-only, and what must remain outside the packaged app as user/runtime data.

The repo may contain more than the product while Mindshare Central is being built. The installer package should not.

## Product Boundary

Mindshare Central is the local Electron app for:

- Navigating Mindshare offices and departments.
- Loading role context, WhoAmI cards, role files, and bundled MAPS/org content.
- Connecting role sessions to local Codex CLI and Claude CLI installations.
- Hosting local tool webviews and role-office UI.
- Running app-owned local automation controls after we migrate them out of Codex automations.

Mindshare Central is not:

- The whole Mindshare source repo.
- A raw mirror of Scott's local filesystem.
- A package for Codex/Claude authentication state.
- A package for secrets, API keys, Git metadata, logs, caches, or runtime proof output.

## Ship In The App

These are product-owned files that should be packaged into the installed app.

| Area | Source | Package destination | Notes |
| --- | --- | --- | --- |
| Electron shell | `local-client/main.js`, `local-client/preload.js`, `local-client/mindshare-local-client.js` | app root | Core desktop runtime. |
| App metadata | `local-client/package.json`, `local-client/package-lock.json` | app root | Required for build and dependency lock. |
| App assets | `local-client/assets/` | app assets | Icons and app-owned static assets. |
| App scripts | `local-client/scripts/` | app scripts | Build/sync scripts; runtime scripts only when explicitly marked. |
| Public UI | `public/` | `app-content/mindshare/public/` | Home, departments, offices, tools, contact, and website-derived UI used by Central. |
| Mindshare role content | selected `roles/` | `app-content/mindshare/roles/` | Role files needed for offices and context loading. Exclude volatile proof/state unless promoted to app state. |
| Mindshare agent content | selected `agents/` | `app-content/mindshare/agents/` | Only active/needed role-office support files. Deprecated agent profile/brief files should not be bundled unless still referenced. |
| Global org files | selected global files | `app-content/mindshare/global/` | Roster, role artifacts, autonomy taxonomy, and app-level manifest files. |
| MAPS/org docs | selected `docs/`, `catalogs/`, `phases/`, `rooms/`, `templates/` | `app-content/mindshare/...` | Only docs used by Central, role context, configuration, or tools. |
| Mojo MAPS content | selected `C:\Users\scott\Code\mojo\assets\maps`, `maps`, roles, agents | `app-content/mojo/...` | Only content needed by Central UI and role offices. |
| Watch content | selected Watch roles/agents | `app-content/watch/...` | Only active roles/offices that Central can load. |
| README | `local-client/README.md`, installer README | app/release root | User-facing install/run guidance. |

## Do Not Ship

These should not be included in the installed app package.

| Area | Examples | Reason |
| --- | --- | --- |
| Git data | `.git/`, worktrees, branch metadata | Source control only. |
| Local AI state | `.claude/`, `.codex/`, session logs | User-machine state, often large or private. |
| Obsidian/Graph caches | `.obsidian-memory/`, `graphify-out/` | Development/retrieval cache, not product runtime. |
| Node dependencies in source | `node_modules/` | Rebuilt by package tooling, not source manifest. |
| Build caches | `.pytest_cache/`, `__pycache__/`, temp folders | Not product data. |
| Secrets/config | `.env`, `.env.local`, keys, certs, tokens | Must never ship. |
| Logs | `*.log` | Runtime output, not installer input. |
| Old browser experiment | `local-client/chrome-extension/`, `native-host/`, CRX/PEM/update XML | Deprecated local-client path unless explicitly revived. |
| Raw Stitch drafts | non-canonical `docs/stitch-artifacts/**` drafts | Keep only current source pages or curated design references. |
| Runtime proof/state | `*-state.json`, `*-proof.md`, visible logs | Move to app data or regenerate; do not bake stale operational truth into installer. |
| Personal docs | training outlines, employee guidelines, finance docs | Not part of Central unless explicitly promoted to product docs. |

## Runtime Data Outside The App

These belong in a writable user-data location such as:

`%APPDATA%\Mindshare Central\`

| Runtime data | Reason |
| --- | --- |
| User sessions | Should survive app updates but be clearable. |
| Role chat transcripts | User-specific, not installer content. |
| Automation run state | Mutable operational state. |
| Proof logs | Generated evidence, not packaged truth. |
| User config/preferences | Per-machine/per-user. |
| Tool webview auth/cookies | Owned by local browser/session storage. |
| Generated images/assets | Created by user or roles after install. |

## External Requirements

The installer may check for these, but should not bundle credentials or authenticated state.

- Codex CLI installed and authenticated locally.
- Claude CLI installed and authenticated locally.
- Optional browser/webview logins for tools such as OpenAI Images Playground or Purelymail.

## Current Cleanup Decisions

- The Chrome extension/native-host path is deprecated for Mindshare Central and should be excluded from installer builds.
- `local-client/app-content/` is generated content. It may exist in the repo while we are iterating, but installer packaging should treat it as build output from this manifest, not hand-maintained source.
- Canonical app UI currently lives in `public/` and is synced into `local-client/app-content/mindshare/public/`.
- We should shrink the sync script before building the installer so it copies only manifest-approved paths.

## Maintenance Rules

- When a new file/folder is needed by the installed app, add it here before relying on it.
- When a file/folder is only needed for development, exclude it here before installer work.
- When a role file becomes mutable runtime state, move it to the runtime-data section instead of baking it into the app.
- Every installer build should report which manifest entries were included, excluded, missing, and generated.

## Changelog

| Date | Version | Change |
| --- | --- | --- |
| 2026-06-26 | 0.1.0 | Created initial product packaging boundary for Mindshare Central. |
