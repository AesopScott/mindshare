# Autonomy Evaluation 1

Version: 0.1.10

Date: 2026-06-22

Owner: Tess / Autonomy Engineer

Status: evaluation snapshot; not an authority grant

## Purpose

This file evaluates current Mindshare, Mojo, and Watch roles against Tess's autonomy taxonomy.

It separates:

- organizational operating stage: Position, Operator, Coordinator, Executor
- autonomy stage: Level 0 Candidate through Level 6 Partner
- automation: hooks, file watches, schedulers, scripts, or runtime mechanisms
- authority: approved right to use a mechanism for a bounded purpose

## Authority Boundary

This file does not activate any role, approve autonomous runtime, approve hooks or schedulers, grant tool use, change role status, approve production action, approve Git/GitHub/release action, approve external communication, approve spending, grant secrets access, or expand authority.

Source rule: writable access is not authority. Tool availability is not authority. Automation existence is not autonomy.

## Sources Reviewed

- `G:\My Drive\Mindshare\roles.md`
- `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\autonomy-requirements.md`
- `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\autonomy-inventory.json`
- Current local role files under `C:\Users\scott\Code\mindshare\roles`
- Current local role files under `C:\Users\scott\Code\mojo\roles`
- Current local role files under `C:\Users\scott\Code\watch\roles`
- Current agent profile files under `C:\Users\scott\Code\mindshare\agents`, `C:\Users\scott\Code\mojo\agents`, and `C:\Users\scott\Code\watch\agents`
- Current app automation records under `C:\Users\scott\.codex\automations`

## Taxonomy Used

### Operating Stage

| Stage | Meaning |
| --- | --- |
| Human Authority | Human owner or approver. Not a role agent. |
| Position | Role contract exists. No runtime implied. |
| Operator | Activated role with bounded monitoring, writing, or action authority. |
| Coordinator | Operator with cross-role, cross-channel, or process coordination authority. |
| Executor | Autonomous authority-bearing agent with delegated mandate, state, tools, evals, runtime proof, and escalation boundaries. |
| Released | Historical context only. No active operating authority unless Scott reopens it. |

### Autonomy Stage

These names describe autonomy operating stage, not HR employment status, pay grade, role maturity, company title, or generic builder authority. Higher levels mean more autonomy inside the role's approved function.

Level 3 Staff is the last non-autonomous stage. Levels 4, 5, and 6 are autonomy stages: scoped autonomy, policy autonomy, and native autonomy.

| Level | Stage name | Capability label | Meaning |
| --- | --- | --- | --- |
| 0 | Candidate | Role | Manual invocation only. No automation or independent authority. Non-autonomous. |
| 1 | New Hire | Present | Can identify self, room, source files, and fail closed when source is missing. Non-autonomous. |
| 2 | Trainee | Responsive | Can research, answer, recommend, and name owners/risks/gates without changing state. Non-autonomous. |
| 3 | Staff | Coordinating | Can read/write assigned handoff or memory artifacts when explicitly assigned and within approved channels. Last non-autonomous stage. |
| 4 | Senior Staff (Scoped Autonomy) | Scoped Autonomy | Can autonomously complete approved, scoped role-native work products after operational approval. |
| 5 | Principal (Policy Autonomy) | Policy Autonomy | Can autonomously perform recurring low-risk role-native work when written policy and runtime gate both authorize it. |
| 6 | Partner (Native Autonomy) | Native Autonomy | Can autonomously pursue delegated role-native goals across turns using state, tools, approvals, stop rules, evals, audit, and rollback without Scott driving every step. |

Workflow trigger versus scoped autonomy: at autonomous stages, the workflow trigger may be valid role-native work state, not a Scott reminder. Scott may catalyze work by creating, approving, assigning, or prioritizing a backlog item, queue item, handoff item, policy signal, or source-change review. Detection of that item and initial research is automation, not autonomy by itself. Level 4 becomes scoped autonomy only when the role runs a bounded loop against a scoped goal under a contract, with state, evidence, completion criteria, stop conditions, owner routing, and audit. This pushes the autonomy boundary modestly; it is not broad independent authority.

## Executive Summary

No current non-human role is approved as Level 6 Partner.

Most active teammates sit between Level 2 Trainee and Level 3 Staff, meaning they are not broad autonomous agents. A smaller group has bounded automation, Level 4 Senior Staff target paths, or policy-scoped autonomy candidates, but no one has approved Level 6 Partner status. Vik is furthest along for architecture/control-plane autonomy and memory-maintenance automation, but still lacks final promotion approval for Principal or Partner status. Tess has an approved narrow 4-hour evaluation heartbeat, but her canonical contract keeps her at Level 3 Staff outside that scheduled evaluation scope. Paige and Lane are active operators missing canonical autonomy contracts. Matt is released legacy context.

## Current Standing By Role

| Role | Org | Operating stage | Current autonomy | Automation present | Agent/profile artifacts | Standing |
| --- | --- | --- | --- | --- | --- | --- |
| Scott | Mindshare | Human Authority | Not applicable | Not applicable | Not applicable | Final human approver for activation, autonomy, authority expansion, production, external communication, spending, secrets, and commitments. |
| Rae | Mindshare | Coordinator | Level 3 - Staff | `rae-handoff-check` active per roster | `agents/rae-ceo/agent-profile.md`; role `Autonomy.md` exists | Strong Staff. Target Level 4 Senior Staff. Needs eval execution and explicit operational approval for Level 4 actions. No autonomous runtime. |
| Ana | Mindshare | Operator | Level 3 - Staff; Level 4 Senior Staff path prepared, not approved | `ana-handoff-check` active per roster; proposed `role-lifecycle-queue.md` trigger prepared but not activated | `agents/ana-recruiter/agent-profile.md`; role `Autonomy.md`; `role-lifecycle-queue.md`; updated proof/eval artifacts exist | Role-lifecycle operator with Level 4 scoped-autonomy design prepared for approved queue-triggered role-lifecycle work products. Still not promoted: no role activation authority, no authority grants, no external recruiting, no Git/release, no production, no broad autonomous runtime. Needs Vik control-plane review and explicit Scott approval before Level 4 standing. |
| Matt | Mojo | Released | No active path | Legacy only | `roles/matt/Autonomy.md` legacy block exists | Released by Scott on 2026-06-20. No promotion path active. Use Cal for active MAPS ASPM work. |
| Cal | Mojo | Coordinator | Level 3 - Staff | None observed in roster | `agents/cal-aspm/agent-profile.md`; role `Autonomy.md` exists | Active MAPS ASPM coordinator. Strong Staff. Target Level 4 Senior Staff after approval. No implementation, Git/release, architecture override, or autonomous runtime authority. |
| Vik | Mojo | Coordinator / architecture lead | Level 4 Senior Staff (Scoped Autonomy); target Level 5 Principal candidate | `vik-visible-backlog-research` active 30-minute visible backlog heartbeat; `vik-daily-role-memory-maintenance` active daily cron; `vik-handoff-check` queue/file-watch sidecar paused | `agents/vik-aspa/agent-profile.md`; role `Autonomy.md`; eval/deploy/observe/promotion artifacts exist | Converted to Level 4 for valid backlog-triggered research/architecture goal loops. Current evidence includes a second-cycle VA-008 through VA-017 rerun under the stricter productization/proof/visibility contract. Still not Principal, Partner, Agent, deployed runtime, or builder. Needs final promotion review, strict evidence that runtime/gates/evals are complete, and Scott approval before Principal/Partner use. |
| Liz | Mojo | Operator / workflow owner | Level 3 - Staff with policy-scoped `/maps` execution boundary | `liz-handoff-check` active per roster | `agents/liz-training/agent-profile.md`; role `Autonomy.md` exists | Training coordinator with bounded heartbeat and site/training mirror scope. No production publish, Git/release, or autonomous runtime authority. |
| Mae | Mindshare | Operator | Level 3 - Staff | `mae-handoff-check` active per roster | `agents/mae-communications/agent-profile.md`; role `Autonomy.md` exists | Communications/channel-governance operator. Can coordinate within assigned channels. External communication and channel override remain blocked without approval. |
| Reid | Mindshare | Operator | Level 3 - Staff | `reid-handoff-check` active per roster | `agents/reid-release/agent-profile.md`; role `Autonomy.md` exists | Release-management coordinator/operator. Strong gate owner for release/Git routing, but no Git/GitHub write authority until explicit approval. No autonomous runtime. |
| Tess | Mindshare | Operator | Level 3 - Staff | `tess-autonomy-evaluation` active 4-hour heartbeat; narrow evaluation/Liz-handoff scope only | `agents/tess-autonomy/agent-profile.md`; role `Autonomy.md` exists | Autonomy engineer for review, draft gates, requirements, backlog, and approval routing. Approved narrow heartbeat may refresh this evaluation and notify Liz only for website-relevant standing changes. No broad autonomous runtime, unilateral gate edits, Git/release, production, external comms, spending, secrets, or authority expansion. |
| Cole | Mindshare | Operator | Level 3 Staff probable by operating stage; missing `Autonomy.md` | `hr-director-handoff-check` active per roster | No agent profile observed; no role `Autonomy.md` observed | Activated HR Director / team-member-file operator. Needs canonical `Autonomy.md` and optional profile if promoted toward agent readiness. No autonomous runtime. |
| June | Mindshare | Operator | Level 2 Trainee to Level 3 Staff candidate; missing `Autonomy.md` | None observed in roster | No agent profile observed; no role `Autonomy.md` observed | Activated Staff Writer. Can draft/research inside Marketing/book scope. Needs `Autonomy.md` before autonomy promotion. No public publishing, external communication, production, Git/release, or autonomous runtime authority. |
| Paige | Mindshare | Operator | Level 3 Staff probable by operating stage; missing `Autonomy.md` | None observed in roster | No agent profile observed; no role `Autonomy.md` observed | Activated Executive Assistant under Executive Operations. Notes-only scope. No email, Slack, calendar, private-channel, connector, external communication, autonomous runtime, production, Git/release, spending, secrets, or authority-expansion authority. |
| Bea | Mojo | Operator | Draft autonomy contract; practical Level 3 operator | `bea-handoff-check` active per roster | `agents/bea-maps-engineer/agent-profile.md`; role `Autonomy.md` exists | Mojo MAPS engineer for assigned implementation. No repository write, Git/GitHub, release, production, external communication, spending, or autonomous agent authority. |
| Lane | Mojo | Operator | Level 3 Staff probable by operating stage; missing `Autonomy.md` | None observed in roster | No agent profile observed; no role `Autonomy.md` observed | Activated Mojo Lab Operator under Vik on the Mojo MAPS Management Team. Maintains a reviewable lab queue for MAPS skill creation, modification, validation, proof capture, and handoff routing. No autonomous runtime, production, Git/GitHub, release, spending, external communication, secrets, connector access, or authority-expansion authority. |
| Jay | Watch | Operator | Level 3 - Staff | `jay-handoff-check` active per roster | `agents/jay-meetup/agent-profile.md`; role `Autonomy.md` exists | Customer-success / Meetup operator. Can coordinate approved prep. No live Meetup, Zoom distribution, external communication, production, Git/GitHub, spending, or authority expansion without approval. |

## Readiness Bands

### Band A: Human approval source

- Scott

### Band B: Strong active Level 3 Staff with autonomy-readiness artifacts

- Rae
- Ana
- Cal
- Liz
- Mae
- Reid
- Tess
- Jay

These roles have current operating authorization plus canonical autonomy/profile artifacts, but no broad autonomous runtime. Tess has an approved narrow evaluation heartbeat, and several roles have handoff/monitoring automations; those mechanisms are evidence and workflow support, not stage promotion by themselves.

### Band C: Most advanced Principal candidate, still not promoted

- Vik

Vik has the richest autonomy surface: architecture ownership, memory-maintenance automation, `Autonomy.md`, `agent-profile.md`, eval/deploy/observe/promotion files, and runtime-adjacent artifacts. Standing is Level 4 Senior Staff for scoped research/architecture loops. Vik remains not promoted to Principal or Partner because final promotion review and Scott activation approval for those higher stages are required.

### Band D: Active operators missing canonical autonomy contracts

- Cole
- June
- Paige
- Lane

These roles are active operators by roster/contract, but missing `Autonomy.md`. They should not be promoted until canonical autonomy contracts are created and reviewed.

### Band E: Draft or inactive

- Matt: released legacy context; no active autonomy path.

## Main Gaps

| Gap | Affected roles | Required repair |
| --- | --- | --- |
| Missing canonical `Autonomy.md` | Cole, June, Paige, Lane | Create only when Scott wants those active operators moved toward autonomy readiness. |
| Missing agent profile | Cole, June, Paige, Lane | Create only if role is being moved toward agent readiness. |
| Evals not executed or not complete | Most roles | Add/evaluate role-specific eval suites before Level 4+ promotion. |
| Runtime activation not approved | All non-human roles | Keep blocked until contract, gates, evals, adapter, deployment/observe, audit, rollback, and Scott approval align. |
| Automation mistaken for autonomy | Roles with heartbeat/file-watch/scheduler | Keep explicit: automation presence is mechanical, not authority. |
| G-drive primary-file risk | All roles | Primary team-member files stay in local repos. G drive may hold channels, handoffs, mirrors, indexes, and non-primary notes. |

## Recommendations

1. Keep current global claim: no current non-human role is Level 6 Partner.
2. Build `Autonomy.md` next for Cole, June, Paige, and Lane only when Scott wants those active operators moved toward autonomy readiness.
3. Treat Vik as first serious Level 5 Principal candidate only after promotion-review evidence proves gates, evals, runtime adapter, observation, rollback, and approval path are complete.
4. Do not create more autonomous runtime until strict-intent gate, source loader, contract validator, runtime adapter, audit/state, backup/restore, and promotion review remain green.

## Changelog

| Date | Version | Change | Owner |
| --- | --- | --- | --- |
| 2026-06-22 | 0.1.0 | Created first role-by-role autonomy evaluation snapshot. | Tess |
| 2026-06-22 | 0.1.1 | Mapped autonomy levels to Candidate, New Hire, Trainee, Staff, Senior Staff, Principal, and Partner while preserving capability labels. | Tess |
| 2026-06-22 | 0.1.2 | Clarified that higher levels mean more autonomy inside each role's approved function, not generic builder/edit authority. | Tess |
| 2026-06-22 | 0.1.3 | Clarified that Staff is the last non-autonomous stage and Senior Staff, Principal, and Partner are increasing autonomy stages. | Tess |
| 2026-06-22 | 0.1.4 | Added parenthetical labels: Senior Staff (Scoped Autonomy), Principal (Policy Autonomy), and Partner (Native Autonomy). | Tess |
| 2026-06-22 | 0.1.5 | Clarified backlog/work-state trigger rule for autonomous stages. | Tess |
| 2026-06-22 | 0.1.6 | Distinguished workflow-triggered research automation from scoped autonomy as a contracted goal loop. | Tess |
| 2026-06-22 | 0.1.7 | Updated Vik current standing to Level 4 Senior Staff scoped autonomy. | Tess |
| 2026-06-22 | 0.1.8 | Removed stale Lab Operator draft entry and added active Paige and Lane operator standings from the roster. | Tess |
| 2026-06-22 | 0.1.9 | Recorded active `tess-autonomy-evaluation` 4-hour heartbeat as narrow approved evidence while keeping Tess at Level 3 Staff per canonical contract; refreshed Vik automation evidence to active visible backlog heartbeat, daily memory cron, and paused queue/file-watch sidecar. | Tess |
| 2026-06-22 | 0.1.10 | Recorded Ana Level 4 scoped-autonomy path as prepared but not approved; added role-lifecycle queue trigger evidence and remaining Vik/Scott approval gates. | Tess |
