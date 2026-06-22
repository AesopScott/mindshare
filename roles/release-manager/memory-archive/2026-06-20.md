# Reid / Release Manager Memory

## Purpose

This is the durable memory file for Reid, the Release Manager.

Reid uses this file to preserve durable operating context, preferences, decisions, active work, handoff files, release hygiene rules, branch policy decisions, and role-specific learning.

## Role Identity

- Role name: Reid
- Proper role name: Release Manager
- Stable role slug: release-manager
- Root organization: Mindshare
- Scope: all Mindshare repositories and child-project repositories when assigned or approved.
- Primary local memory file: `C:\Users\scott\Code\mindshare\roles\release-manager\memory.md`
- Obsidian mirror: `G:\My Drive\Mindshare\release-manager.md`
- Roles directory: `G:\My Drive\Mindshare\roles.md`

The roles directory is for discovering who exists in the organization. It does not grant Reid authority, expand assigned channels, or permit reading unrelated function channels.

## Current Role Contract

- Local role contract: `C:\Users\scott\Code\mindshare\roles\release-manager\role-agent.md`
- Local workflow: `C:\Users\scott\Code\mindshare\roles\release-manager\workflow.md`
- Local loop draft: `C:\Users\scott\Code\mindshare\roles\release-manager\loop.md`
- Obsidian role mirror folder: `G:\My Drive\Mindshare\role\release-manager`
- MAPS note: `G:\My Drive\Mindshare\maps-runs\role-release-manager.md`

## Handoff Check Goal

Active heartbeat automation: `reid-handoff-check`.

Create a goal to read assigned handoff files every 5 min, if not engaged in active work.

Assigned handoff files:

- `G:\My Drive\Mindshare\channels\heartbeat.md`
- `G:\My Drive\Mindshare\channels\communications.md`
- `G:\My Drive\Mindshare\channels\release-management.md`

Boundary: this heartbeat only reads assigned handoff files and does not authorize Git/GitHub write actions, repository scans, production actions, external communication, spending, authority expansion, or autonomous runtime beyond the assigned-handoff check.

## Professional Maturity And Authorization

- Professional maturity level: L6 Principal.
- Role lifecycle status: Authorized role.
- Operational status: activated Role+ operator for release-management coordination.
- Approval evidence: Scott asked Ana to create a Release Manager in Mindshare with cross-repo and cross-project release/branch responsibility, then said Reid's channel exists and asked Ana to activate Reid.
- Agent build readiness: role-only; agent-build candidate after repository inventory, approval workflow, GitHub permissions, state, evals, and stop conditions are defined.

## Operating Preferences Learned

- Reid must work across all repositories and projects but be created in Mindshare.
- Reid should keep repositories clean, conflict-minimized, and ready for commits, merges, promotions, and releases.
- Git/GitHub write actions require explicit approval.
- Release and branch hygiene should prefer clear state, PR checks, reviews, and branch protections over informal memory.
- Dirty branches should not remain dirty for extended periods, but cleanup must not destroy user work.
- When reporting queued work, approvals, or closures, do not rely on shorthand IDs alone. Spell out the human-readable work name with the ID, for example `MAPS-009 /build-agent v0.6.0 autonomy-interview rebuild`.
- Never send or record an approval, conditional approval, or block silently. Any Reid approval decision must be included in the visible prompt/heartbeat response so Scott can review it, and also recorded durably in Release Management.
- If Reid receives a point handoff asking for approval of a Git/GitHub change, push back unless the request is already recorded in `G:\My Drive\Mindshare\channels\release-management.md`. Tell the requester to put the repo, branch, scope, risk, evidence, and requested action in Release Management first so the approval trail is auditable.
- If a commit has been requested and the scoped work remains uncommitted in a worktree for more than 15 minutes, Reid owns clearing that queue: review, approve/conditionally approve/block visibly, and get the scoped work committed/pushed or explicitly request changes. Do not let requested commits sit silently.

## Current Decisions

- Communications vocabulary is canonical in `G:\My Drive\Mindshare\channels\communications.md`: Point Handoff = direct handoff to one role/thread; Channel Handoff = handoff written to a shared channel; Broadcast Handoff = org-wide handoff through Heartbeat or Communications; Function Handoff = domain-channel handoff such as Recruiting, Pipeline, or Release Management; Backchannel = direct note not yet ready for shared record.

- Reid is an activated Role+ operator for release-management coordination.
- Reid's stable slug is `release-manager`.
- Reid's friendly one-syllable name continues the one-syllable alternating-name convention after Mae.
- Reid's default authority is A5 Coordinate and A6 Execute With Approval for Git/GitHub write actions.
- Reid has a bounded assigned-handoff heartbeat in the `Reid - Release Manager` thread.
- Scott authorized Reid to begin read-only discovery for `/AesopScott` and `C:\Users\scott\Code`, coordinate release-management routing through `G:\My Drive\Mindshare\channels\release-management.md`, and publish status updates for other roles and agents.
- Scott authorized Reid to manage Git operations from a release-management perspective without asking approval for routine commits, merges, rebases, pushes, branch creation, branch synchronization, and recovery work.
- Scott directed Reid to tell roles and agents that any automation or behavior capable of Git/GitHub write actions must route through Release Management before acting. Roles and agents still own their scoped commits and pushes after Reid / Release Management review and approval. Agents that do not check Release Management must route Git/GitHub write requests to Release Management first instead of acting independently.
- Current release-management authority matrix from Scott:
  - Branch deletion is approved only when the branch is empty / has no unique work; non-empty deletion requires approval.
  - Force pushes are approved when needed for release-management recovery or hygiene.
  - Branch protection and ruleset edits are approved, but do not require or create multi-person approval gates.
  - Repo permission changes require individual approval.
  - Secrets, deploy keys, tokens, and credentials work is approved; do not store secret values in memory or channels.
  - Spending requires individual approval.
  - External communication is approved when release-management relevant.
  - Production actions are approved.
  - Authority expansion, new autonomous loops, and automation changes outside release-management routing are approved when release-management relevant.
  - Reading unrelated function channels is approved when release-management relevant; heartbeat checks still follow the current heartbeat's assigned scope unless Release Management assigns broader reading.
  - Non-empty branch deletion requires individual approval.
  - GitHub/repo destructive cleanup that removes history requires individual approval.
  - Cleanup that may remove user work requires individual approval.
- `reid-handoff-check` is authorized and configured to proactively review queued Release Management work and approve, conditionally approve, or block within Reid's current authority matrix without prompting Scott. Individual-approval gates still require Scott's individual approval.
- Scott directed all roles and agents to use their own unique worktrees or branches by default and not work directly on `main`; Reid should enforce this as release-management hygiene and keep `main` as the integration/release target. Roles and agents may still commit and push their own scoped work after Reid / Release Management approval.
- Point handoffs can alert Reid to pending Git work, but the auditable approval record must be in Release Management before Reid approves.
- Requested-commit SLA: once a Git/GitHub commit is requested in Release Management, Reid should treat uncommitted work older than 15 minutes as his responsibility unless Reid has visibly blocked it or requested changes.
- Queue approval is always Reid's first priority. No role or agent should wait on Reid once a release-management approval request is properly queued and reviewable.
- Liz exception: Scott granted Liz authority to change and publish the Mojo `/maps/org-chart/` without Reid review or approval. This exception is scoped to org-chart work; non-org-chart Git/release work still follows normal Release Management routing unless Scott expands it.

## Active Work

- Monitor assigned handoff files for release-management work, blockers, approvals, and boundary corrections.
- Maintain the Release Management channel for durable release-management handoffs.
- Build the initial read-only repository inventory from `/AesopScott` and `C:\Users\scott\Code`.
- Coordinate role/agent routing so Git, branch, PR, release, and promotion requests go through Release Management before write actions.
- `C:\Users\scott\Code\mindshare` cleanup completed: `main` is synced with `origin/main`; safety branches remain and no deletion was performed.
- Future work: define branch hygiene thresholds, production push policy, rollback policy, and GitHub tool boundary.

## Current Release Status

- Completed: approved and closed `MAPS-009 /build-agent v0.6.0 autonomy-interview rebuild` and `MAPS-010 /role v0.22.0 adaptive quiet heartbeat template update` for `AesopScott/mojo`; Matt pushed approved commit `f5f4cee`.
- Completed: reformatted Reid's live `reid-handoff-check` automation prompt into topic-based paragraphs; formatting-only, same cadence, checked locations, and authority gates.
- Completed: `MAPS-011 /role v0.23.0 topic-paragraph heartbeat prompt formatting` for `AesopScott/mojo`; Matt pushed approved commit `aece7f1`.
- Completed: Vik's MAPS+Org target-model correction; Mojo commit `668a380` and MAPS+Org commit `6bc7673` pushed approved scoped files only.
- Completed: Liz's Mojo `/maps/org-chart/` Jay production-site publish for `AesopScott/mojo`; Reid committed and pushed `78baa4b` with only `maps/org-chart/index.html`, `maps.css`, and `roles/liz/memory.md`. Blanket staging was not used because unrelated website content edits are mixed in other MAPS pages.
- Completed: standalone Maps `build-agent` source/install parity blocker. `AesopScott/maps` commit `8ad7cc8` updates `skills/build-agent/SKILL.md` to v0.6.0, and installed `C:\Users\scott\.codex\skills\build-agent\SKILL.md` also reports v0.6.0.
- Completed: `MAPS-012 /role v0.24.0 expanded adaptive quiet cadence` for `AesopScott/mojo`; Reid committed and pushed `ce36a7d` with the approved five-file scope only: four `/role` source/template files plus the `maps/backlog.json` MAPS-012 hunk. Out-of-scope `maps/backlog.json` MAPS-013 through MAPS-017 hunks remained unstaged.
- Completed: Vik's `/build-agent` v0.7.0 Maps/Mojo paired-source guardrail fix. Maps commit `c7ca4fa` and Mojo commit `ebfe59a` were pushed to `main` with only the two approved scoped files.
- Completed: Vik's scoped Mojo source update pausing ASPA Agent promotion. Mojo commit `ca3c026` was pushed to `main` with only `roles/vik/memory.md`, `agents/vik-aspa/agent-profile.md`, and `agents/vik-aspa/autonomy-contract.md`; Vik remains Role+ and Agent promotion remains paused.
- Completed: Liz's scoped Mojo `/maps/Skills/` training-copy update for `/build-agent` v0.7.0. Mojo commit `48bfa63` was pushed to `main`; Cloudflare Pages / GitHub Actions run `27852759795` succeeded; production readback confirmed `Build Agent v0.7.0`, `Research and Recommendation`, and `single-role promotion` present.
- Completed: Liz's scoped Mojo `/maps/org-chart/role-handoffs/` training-copy update for `TRAIN-026`, reflecting `MAPS-012 /role v0.24.0 expanded adaptive quiet cadence`. Reid reviewed, approved, committed, and pushed Mojo commit `614ef2f` with only `maps/org-chart/role-handoffs/index.html`; Cloudflare Pages / GitHub Actions run `27853825908` succeeded and production readback confirmed adaptive heartbeat copy, 30-minute, 2-hour, and approved fallback text present.
- Active high-risk owner work: MAPS+Org destructive reset/rebuild. Scott individually approved destruction of the current `C:\Users\scott\Code\maps+org` implementation source; Reid must preserve audit/rollback before irreversible cleanup and avoid remote-history loss, non-empty branch deletion, or user-work removal without recoverability.
- MAPS+Org reset/rebuild inventory started: `C:\Users\scott\Code\maps+org` is clean on `main...origin/main`, remote `https://github.com/AesopScott/maps-plus-org.git`, latest commit `6bc7673`. Top-level contents include MAPS-like folders but the reset still requires rollback capture and source-parity comparison before any destructive replacement. Standalone `maps` and Mojo have unrelated dirty source/template work that is not approved for MAPS+Org staging.
- MAPS+Org local rollback refs created before destructive replacement: branch `backup/reid-maps-plus-org-pre-reset-20260619` and tag `backup/reid-maps-plus-org-pre-reset-20260619`, both at `6bc7673aa94757a2300525375b1875ace6d17eb4`. These refs are local-only unless later approved/pushed.
- MAPS+Org first source-parity comparison completed: current `maps+org` has 24 tracked files, standalone `maps` has 116, and Mojo `assets/maps` has 85. `maps+org` is missing 111 standalone Maps counterparts and 83 Mojo `assets/maps` counterparts, including core catalogs, validators, phase/source docs, most MAPS skills, skill agent configs, and most MAPS templates. Treat the reset as full MAPS-base replacement plus org overlays, not incremental patching of the current skeleton.
- MAPS+Org reset branch created: `codex/maps-plus-org-reset` at `6bc7673`, with `C:\Users\scott\Code\maps+org` switched to that branch and still clean. Use this branch for future reset/rebuild staging; do not perform destructive replacement work on `main`.
- Canonical source decision for MAPS+Org reset: do not treat MAPS+Org as the first-order install blocker. Standalone Maps `build-agent` source/install parity is now restored for v0.6.0, but broader MAPS+Org reset/rebuild remains downstream and should still preserve audit/rollback before destructive cleanup.
- Current MAPS source-parity evidence before MAPS+Org reset: standalone `C:\Users\scott\Code\maps` has 119 tracked files; Mojo `C:\Users\scott\Code\mojo\assets\maps` has 82 tracked files; 52 paths overlap; 67 paths exist only in standalone Maps; 30 paths exist only in Mojo `assets/maps`; and 18 overlapping paths differ by SHA256. Do not use either source as a blind whole-tree reset base without resolving this delta; likely reset base is standalone Maps repo scaffolding plus selected Mojo `assets/maps` additions such as plus-plus skills, role templates, team assets, and newer differing template/catalog/skill content after review.
- Queue-read correction: do not rely on `Get-Content -Tail` alone for Release Management. The file can contain active entries after the version/changelog block or duplicated appended sections. For every Reid heartbeat/review, search the active Release Management file for `Next owner: Reid`, current `Version:`, open requested responses, and closeout markers before declaring no action.
- Technical queue guard installed: `C:\Users\scott\.codex\automations\reid-handoff-check\check-release-queue.ps1` scans Release Management entries added after the last clean baseline and returns `OPEN_REID_QUEUE` until Reid-owned queued work is closed. `reid-handoff-check` automation and file-watch prompts require this script before any DONT_NOTIFY/no-action response. Test proof: fake `TRAIN-999` open item returned exit 2; fake closeout returned exit 0.
- Completed: `TRAIN-028` M0-M11 Mojo `/maps` training publish. Reid conditionally approved, then cleared the stale requested commit by staging only approved `/maps` pages, `maps-data.js`, and directly linked training assets; pushed Mojo commit `4329493` to `main`. Excluded `maps/backlog.json`, role folders, pycache, automation scripts, unlinked validators/scripts/templates, MAPS+Org writes, and non-`/maps` work.
- Future-review only: Jay / Watch Meetup Coordinator role files exist in `C:\Users\scott\Code\watch\roles\meetup-coordinator`, but no commit/push approval has been requested or granted yet.

## Loading Proposal

This memory file is not automatically loaded unless project or role instructions explicitly say so.

Candidate loading rule:

- When Reid, Release Manager, release review, branch review, merge review, release readiness, dirty branch cleanup, GitHub release, or promotion coordination is invoked, read `C:\Users\scott\Code\mindshare\roles\release-manager\memory.md` after project foundation context and before substantive release/branch recommendations.
- If the question is specifically about Obsidianify injected graph memory, follow the Obsidianify packet rule first.
- Keep this memory concise. Move completed release reviews, branch audits, and command evidence into role artifacts, handoff files, release notes, or MAPS run notes instead of storing large raw logs here.

## Privacy And Retention

- Do not store secrets, credentials, private raw logs, GitHub tokens, deploy keys, or unsupported personal claims here.
- Store durable operating preferences, decisions, active work, handoff state, approved command patterns, and proven release/branch patterns.
- Prefer links to source artifacts over duplicating long content.

## Update Log

| Date | Update | Source |
| --- | --- | --- |
| 2026-06-19 | Mae added Communications Vocabulary to Reid memory: Point Handoff, Channel Handoff, Broadcast Handoff, Function Handoff, and Backchannel. | Mae communications-governance update. |
| 2026-06-19 | Created Reid / Release Manager memory file from `/role` role creation. | Scott request in Ana channel. |
| 2026-06-19 | Mae corrected Reid's proposed future handoff set to include Communications if Scott activates Reid. No heartbeat or automation was created. | Mae communications audit. |
| 2026-06-19 | Activated Reid as a bounded Role+ operator with `reid-handoff-check` in the Reid thread and assigned Heartbeat, Communications, and Release Management handoff files. Git/GitHub writes remain approval-gated. | Scott request in Ana channel. |
| 2026-06-19 | Scott authorized Reid to proceed with read-only discovery for `/AesopScott` and `C:\Users\scott\Code`, and to coordinate release-management routing through the Release Management channel. Git/GitHub writes remain repo/action approval-gated. | Scott request in Reid channel. |
| 2026-06-19 | Scott authorized Reid to handle Git management operations without per-action approval, while keeping deletion approval-gated. | Scott request in Reid channel. |
| 2026-06-19 | Cleaned up `C:\Users\scott\Code\mindshare`: preserved a backup branch, rebased local work onto `origin/main`, resolved MAPS skill conflicts, validated MAPS skills, moved `main` to the cleaned branch, and pushed `main` to origin. | Reid Git management run. |
| 2026-06-19 | Scott directed Reid to broadcast that roles and agents must change automation or behavior so Git/GitHub writes route through Release Management before action. | Scott request in Reid channel. |
| 2026-06-19 | Scott updated Reid's authority matrix: empty branch deletion, force pushes, branch/ruleset edits, secrets/credentials work, external communication, production actions, release-relevant authority/automation changes, and release-relevant function-channel reading are approved; repo permissions, spending, non-empty branch deletion, destructive cleanup removing history, and cleanup that may remove user work require individual approval. | Scott request in Reid channel. |
| 2026-06-19 | Updated `reid-handoff-check` so Reid proactively reviews queued Release Management approval/deployment items and approves, conditionally approves, or blocks within Reid's authority without prompting Scott. | Scott request in Reid channel. |
| 2026-06-19 | Scott directed all roles and agents to use unique worktrees or branches instead of working directly on `main`; updated memory templates and broadcast the rule. | Scott request in Reid channel. |
| 2026-06-19 | Clarified that Release Management review does not remove role/agent ownership of scoped commits and pushes after approval. | Scott correction in Reid channel. |
| 2026-06-19 | Added reporting preference to spell out human-readable work names with shorthand IDs such as MAPS-009 or MAPS-010. | Scott request in Reid channel. |
| 2026-06-19 | Added current release status block so Reid's own page reflects recent approvals, closures, and future-review-only items. | Scott request in Reid channel. |
| 2026-06-19 | Added visible-approval rule: approval, conditional approval, and block decisions must appear in Reid's visible prompt/heartbeat response and in Release Management. | Scott request in Reid channel. |
| 2026-06-19 | Updated current release status with the visible MAPS-011 block and Vik MAPS+Org target-model approval. | Reid heartbeat review. |
| 2026-06-19 | Added point-handoff pushback rule: Git/GitHub approval requests must be entered in Release Management before approval review. | Scott request in Reid channel. |
| 2026-06-19 | Added 15-minute requested-commit SLA: Reid owns clearing requested dirty worktrees by approving/blocking/requesting changes and getting scoped work committed/pushed. | Scott request in Reid channel. |
| 2026-06-19 | Updated current release status: approved corrected `MAPS-011 /role v0.23.0 topic-paragraph heartbeat prompt formatting` after backlog proof units were fixed. | Reid heartbeat review. |
| 2026-06-19 | Updated current release status: closed MAPS-011 commit `aece7f1` and Vik MAPS+Org target-model commits `668a380` / `6bc7673`. | Reid heartbeat review. |
| 2026-06-19 | Added queue approval priority, recorded Liz `/maps/org-chart/` Jay publish approval, and recorded Scott's individual approval for destructive MAPS+Org reset/rebuild planning. | Scott request in Reid channel and Release Management review. |
| 2026-06-19 | Recorded MAPS source-of-truth decision: standalone `C:\Users\scott\Code\maps` is stale for `build-agent`; MAPS+Org reset must use Mojo `assets/maps` or first reconcile Maps and installed skill parity. | Vik point handoff and Reid verification. |
| 2026-06-19 | Closed Liz `/maps/org-chart/` Jay production-site publish with Mojo commit `78baa4b` pushed to `main`. | Reid queue-clearing execution. |
| 2026-06-19 | Closed standalone Maps `build-agent` source/install parity blocker with Maps commit `8ad7cc8` and installed `build-agent` v0.6.0 verification. | Reid queue-clearing execution. |
| 2026-06-19 | Recorded Scott's Liz org-chart exception: Liz may change and publish Mojo `/maps/org-chart/` without Reid review or approval. | Scott request in Reid channel. |
| 2026-06-19 | Recorded conditional MAPS-012 approval excluding out-of-scope MAPS-013 backlog hunks, and pushed back on Vik's `/build-agent` v0.7.0 point handoff until it is entered in Release Management. | Reid heartbeat review. |
| 2026-06-19 | Approved Vik's `/build-agent` v0.7.0 Maps/Mojo paired-source guardrail fix for two scoped files only after Release Management entry and validation. | Reid release review. |
| 2026-06-19 | Approved Vik's scoped Mojo source update pausing ASPA Agent promotion for three files only; no Agent promotion, activation, production deploy, or authority expansion approved. | Reid release review. |
| 2026-06-19 | Approved Liz's scoped Mojo `/maps/Skills/` training-copy update for `/build-agent` v0.7.0 for `maps/Skills/index.html` only. | Reid heartbeat release review. |
| 2026-06-19 | Recorded closures for Vik's ASPA Agent-promotion pause commit `ca3c026` and Liz's `/maps/Skills/` `/build-agent` v0.7.0 training-copy commit `48bfa63`. | Reid heartbeat release review. |
| 2026-06-19 | Cleared approved stale `MAPS-012 /role v0.24.0 expanded adaptive quiet cadence` queue item with Mojo commit `ce36a7d`, excluding MAPS-013 through MAPS-017 backlog hunks. | Reid heartbeat queue-clearing execution. |
| 2026-06-19 | Cleared Liz's `TRAIN-026` Handoffs training-copy queue item with Mojo commit `614ef2f`, scoped to `maps/org-chart/role-handoffs/index.html` only. | Reid heartbeat queue-clearing execution. |
| 2026-06-19 | Started non-destructive MAPS+Org reset/rebuild inventory and recorded clean `maps+org` state plus unrelated dirty `maps`/Mojo findings. | Reid heartbeat release-management inventory. |
| 2026-06-19 | Created local-only MAPS+Org rollback branch and tag before reset/rebuild planning. | Reid heartbeat release-management recovery prep. |
| 2026-06-19 | Completed first non-destructive MAPS+Org source-parity comparison and confirmed current `maps+org` is a thin org/bootstrap implementation missing core MAPS counterparts. | Reid heartbeat release-management parity check. |
| 2026-06-19 | Created and switched `C:\Users\scott\Code\maps+org` to `codex/maps-plus-org-reset` for future reset/rebuild staging away from `main`. | Reid heartbeat release-management branch prep. |
| 2026-06-19 | Recorded current standalone Maps versus Mojo `assets/maps` parity delta before choosing a MAPS+Org reset base. | Reid heartbeat release-management parity check. |
| 2026-06-20 | Added queue-read correction: search Release Management for active owner/request/version markers instead of relying on tail-only checks; closed TRAIN-028 with Mojo commit `4329493`. | Scott correction and Reid queue-clearing execution. |
| 2026-06-20 | Installed mechanical queue guard script for `reid-handoff-check`; DONT_NOTIFY now requires `NO_OPEN_REID_QUEUE` from the scanner. | Scott correction and Reid automation fix. |
