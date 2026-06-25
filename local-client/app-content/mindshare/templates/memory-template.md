# [proper-role-name] Memory

Last reviewed: [last-reviewed-date]
Last rollover: [last-rollover-date]
Full archive: `C:\Users\scott\Code\mindshare\roles\[role-name]\memory-archive\[date].md` when archived

## Purpose

This is the compact active memory file for [proper-role-name].

[proper-role-name] uses this file for prompt-loadable operating context only: identity, standing rules, current decisions, active work, same-day notes, and archive pointers. Full history belongs in dated archives, source artifacts, channels, MAPS run notes, or Obsidian notes.

## Role Identity

- Role name: [role-name]
- Proper role name: [proper-role-name]
- Root organization: Mindshare
- Memory file: `G:\My Drive\Mindshare\[role-name].md`

## Current Role Contract

- Local role contract: `C:\Users\scott\Code\mindshare\roles\[role-name]\role-agent.md`
- Local workflow: `C:\Users\scott\Code\mindshare\roles\[role-name]\workflow.md`
- Local gate-block tracker: `C:\Users\scott\Code\mindshare\roles\[role-name]\gate-blocks.md`
- Obsidian role mirror: `G:\My Drive\Mindshare\maps-runs\role-[role-name].md`

## Daily Memory Rollover

- Active memory target size: keep under about 1,500 words when possible; warn above 2,000 words; rollover required above 3,000 words unless the role is blocked from archiving.
- Retain in active memory: durable identity, source pointers, standing rules, unresolved decisions, active work, same-day notes, and archive pointers.
- Archive from active memory: completed run logs, long decision history, old heartbeat evidence, raw transcripts, obsolete status, and detailed proof already recorded elsewhere.
- Rollover cadence: a daily maintenance heartbeat may call the shared role-memory rollover script once per local day. The script must archive before compacting and must skip if `memory-state.json` shows the role already rolled over that day.
- Rollover state: write `C:\Users\scott\Code\mindshare\roles\[role-name]\memory-state.json` with `last_rollover_date`, `last_rollover_at`, `last_archive`, old word count, and new word count.

## Handoff Check Goal

Create a goal to read your assigned handoff files every 5 min, if not engaged in active work.

Assigned handoff files:

- `G:\My Drive\Mindshare\05 Role Handoffs\channels\heartbeat.md`
- `[assigned-handoff-file]`

## Professional Maturity And Authorization

- Professional maturity level: [professional-maturity-level]
- Role lifecycle status: [role-lifecycle-status]
- Approval evidence: [approval-evidence]
- Agent build readiness: [agent-build-readiness]

## Operating Preferences Learned

- [operating-preference]
- Gate-block habit: when blocked by the Codex tool gate, add an open entry to `C:\Users\scott\Code\mindshare\roles\[role-name]\gate-blocks.md` with time, blocked action, target path or command, approval needed, and current owner; route the block to `G:\My Drive\Mindshare\channels\release-management.md` when Reid or Scott visibility is needed; when the gate clears, remove the open entry and add a short cleared note.

## Worktree Discipline

- Default Git working surface: use a unique role/work item worktree or branch, not `main`.
- `main` is the integration/release target, not the normal working branch.
- Before starting repo work, create or use a role-specific worktree/branch named clearly for the role and task, such as `<role>/<short-task>-YYYYMMDD`.
- Do not commit directly on `main` unless Reid / Release Management explicitly approves the scoped action or the task is an emergency release action inside Reid's authority.
- Route commits, pushes, merges, promotions, production deploys, branch cleanup, and worktree cleanup through Release Management before acting.
- After Reid / Release Management approves a scoped Git/GitHub action, the owning role or agent may commit and push its own approved work unless the approval says otherwise.
- If waiting more than 15 minutes for Reid review or approval on changes already routed through Release Management, send a Point Handoff directly to Reid for escalation while keeping the approval record in Release Management.
- Keep unrelated dirty files out of staged changes. If unrelated work is present, use selective staging or a separate worktree.

## Current Decisions

- [decision]

## Active Work

- [active-work-item]

## Loading Proposal

This memory file is not automatically loaded unless project or role instructions explicitly say so.

Candidate loading rule:

- When [proper-role-name] is invoked or assigned work, read `G:\My Drive\Mindshare\[role-name].md` after project foundation context and before substantive role recommendations.
- If the question is specifically about Obsidianify injected graph memory, follow the Obsidianify packet rule first.
- Keep this memory concise. Move completed run evidence into role artifacts, lab history, handoff files, or MAPS run notes instead of storing large transcripts here.

## Privacy And Retention

- Do not store secrets, credentials, private raw logs, or unsupported personal claims here.
- Store durable operating preferences, decisions, active work, handoff state, and proven patterns.
- Prefer links to source artifacts over duplicating long content.

## Today

- [date]: Created [proper-role-name] active memory file from `memory-template.md`.

## Archive Pointers

- Full memory archive folder: `C:\Users\scott\Code\mindshare\roles\[role-name]\memory-archive`
- Daily rollover state: `C:\Users\scott\Code\mindshare\roles\[role-name]\memory-state.json`
- Keep detailed history in dated archives or source artifacts instead of this active file.
