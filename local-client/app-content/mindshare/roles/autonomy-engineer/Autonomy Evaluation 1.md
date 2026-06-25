# Autonomy Evaluation 1

Version: 0.1.53

Date: 2026-06-24

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
- `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\policy-autonomy.md`
- Current local role files under `C:\Users\scott\Code\mindshare\roles`
- Current local role files under `C:\Users\scott\Code\mojo\roles`
- Current local role files under `C:\Users\scott\Code\watch\roles`
- Current agent profile files under `C:\Users\scott\Code\mindshare\agents`, `C:\Users\scott\Code\mojo\agents`, and `C:\Users\scott\Code\watch\agents`
- Current app automation records under `C:\Users\scott\.codex\automations`
- `C:\Users\scott\Code\mindshare\roles\recruiter\recruiting.pipeline.json`

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
| 4 | Senior Staff (Scoped Autonomy) | Scoped Autonomy | Can process the role's approved backlog: autonomously complete approved, scoped role-native backlog items under contract after operational approval. Narrow role-specific follow-through usually belongs here unless a reusable policy/gate is required. |
| 5 | Principal (Policy Autonomy) | Policy Autonomy | Can autonomously perform recurring role-native work across a class of situations only when an approved written policy, runtime gate, eval proof, audit, and revocation path authorize that class of action. |
| 6 | Partner (Native Autonomy) | Native Autonomy | Can autonomously pursue delegated role-native goals across turns using state, tools, approved policies, stop rules, evals, observation, audit, and rollback without Scott driving every step. |

Workflow trigger versus scoped autonomy: every role may have a role-native backlog. At autonomous stages, the workflow trigger may be valid role-native work state, not a Scott reminder. Scott may catalyze work by creating, approving, assigning, or prioritizing a backlog item, queue item, handoff item, policy signal, or source-change review. Detection of that item and initial research is automation, not autonomy by itself. Level 4 becomes scoped autonomy when the role can process approved backlog items through a bounded loop against a scoped goal under a contract, with state, evidence, completion criteria, stop conditions, owner routing, and audit. This pushes the autonomy boundary modestly; it is not broad independent authority.

Policy autonomy correction: Level 5 is not the next larger task after Level 4. Prior role-specific Level 5/6 examples are now treated as reclassification candidates. If the work is direct follow-through from a scoped approved backlog item, fold it into Level 4. If the work requires deciding whether a recurring class of situations is safe to act on, define a Level 5 policy packet first. If the work is self-directed goal pursuit across turns, hold it for Level 6 design review.

## Executive Summary

No current non-human role is approved as Level 6 Partner.

Most active teammates sit at Level 3 Staff, meaning they are not broad autonomous agents. Ana, Tess, Mae, and Cole now have approved Level 4 scoped-autonomy lanes, though Cole is runtime-installed-scheduler-proof-pending rather than fully operational until the hourly validation heartbeat writes scheduler proof and Reid promotion durability is complete. Vik is Level 5 Principal (Policy Autonomy) for completed-research product-recommendation review only; Level 6 and broad autonomous runtime remain inactive. Tess is operational Level 4 only inside the approved automation-baseline and promotion-packet scope: `tess-level-4-autonomy-backlog-processing` has produced review packets for Rae, Cal, Ana, Vik, Liz, Mae, Reid, Bea, Jay, Cole, June, Paige, and Lane, wrote state/proof, passed a pause/resume drill, restored the 30-minute cadence, and now uses `scripts\level4automation.py` as the durable logic owner for backlog/status/Reid-route checks. Mae is operational Level 4 for automation-health/file-watch delivery monitoring with `scripts\level4automation.py` as the durable logic owner; the latest scheduled-mode script proof checked 17 active configs with zero critical findings. Ana's Level 4 recruiting lifecycle heartbeat now uses `scripts\level4automation.py` as the deterministic logic owner; the latest scheduled-mode script proof found no eligible backlog or timed promotions and held all boundaries. No one has approved Level 6 Partner status under the corrected policy-autonomy standard. Ana is approved for internal recruiting backlog processing only; `ana-l4-recruiting-backlog-processing` is active as a heartbeat in Ana's room on the 4-hour steady cadence after three consecutive Level 1 standard proof runs. Cole is approved for Level 4 role-file and WhoAmI injection validation only. June, Paige, and Lane have canonical autonomy contracts and Level 4 review packets, but remain Level 3 until Scott reviews and approves any promotion. Rae, Cal, Liz, Reid, Bea, and Jay also have review packets ready but remain Level 3. Matt is released legacy context.

Source reconciliation note: `G:\My Drive\Mindshare\roles.md` current roster row for Ana matches Level 4 scoped autonomy, but the backup-map section still describes Ana's Level 4 backlog automation as being on a 3-minute proof-testing cadence. Current app automation source `C:\Users\scott\.codex\automations\ana-l4-recruiting-backlog-processing\automation.toml` shows the actual cadence is 4 hours. Treat the backup-map cadence text as stale until Ana/roster ownership updates it.

Ana recruiting pipeline note: REC-001 through REC-005 and REC-007 through REC-009 and REC-011 through REC-026 are named, unassigned Level 2 Trainee packets as of 2026-06-24T23:20:00Z. They are not activated operators, have no offices/channels/runtime, and have no state-changing authority; Finn / REC-010 remains the activated Finance Director outside the timed queue.

## Current Standing By Role

| Role | Org | Operating stage | Current autonomy | Automation present | Agent/profile artifacts | Standing |
| --- | --- | --- | --- | --- | --- | --- |
| Scott | Mindshare | Human Authority | Not applicable | Not applicable | Not applicable | Final human approver for activation, autonomy, authority expansion, production, external communication, spending, secrets, and commitments. |
| Rae | Mindshare | Coordinator | Level 3 - Staff | `rae-handoff-check` active per roster | `agents/rae-ceo/agent-profile.md`; role `Autonomy.md`; `roles/autonomy-engineer/rae-level4-promotion-packet.md` exists | Strong Staff. Target Level 4 Senior Staff. Tess prepared Rae's Level 4 packet for Scott review. Needs eval execution and explicit operational approval for Level 4 actions. No autonomous runtime. |
| Ana | Mindshare | Operator | Level 4 Senior Staff (Scoped Autonomy); Level 5 policy defined-not-active; Level 6 deferred | `ana-handoff-check` active for handoff/channel checking; `ana-l4-recruiting-backlog-processing` active heartbeat on 4-hour steady cadence and now calls `scripts\level4automation.py`; `recruiting.backlog.md` and `recruiting.pipeline.json` approved as Level 4 trigger/state sources | `agents/ana-recruiter/agent-profile.md`; role `Autonomy.md`; `recruiting.backlog.md`; `recruiting.pipeline.json`; `level4-lifecycle-state.json`; `level4-lifecycle-proof.md`; `scripts\level4automation.py`; `leadership-role-taxonomy.md`; `roles/autonomy-engineer/ana-level4-level5-review-packet.md`; updated proof/eval artifacts exist | Scott approved Ana's Level 4 scope on 2026-06-22 and expanded it to the scoped internal recruiting lifecycle: backlog to Level 1 New Hire, Level 1 to Level 2 Trainee after 24 hours, and Level 2 to Level 3 Staff after five days. Tess prepared Ana's Level 4 maintenance and Level 5 policy review packet for Scott review. Ana's Level 4 deterministic checks now live in a script; latest proof found no eligible backlog or timed promotions and held boundaries. Ana's Level 5 policy autonomy remains defined but inactive: research positions other companies have that are missing internally and have conversations with existing leaders at leadership-taxonomy Level 5+ to see whether they want to hire anyone. Level 5 requires the leadership-role taxonomy, policy packets, runtime gate, eval proof, audit, rollback, and revocation before activation. Level 6 is intentionally deferred. No external recruiting, human hiring, Git/release, production, spending, secrets, Level 4+ promotion for hired roles, or broad autonomous runtime. |
| Matt | Mojo | Released | No active path | Legacy only | `roles/released-maps-agentic-systems-program-manager/Autonomy.md` legacy block exists | Released by Scott on 2026-06-20. No promotion path active. Use Cal for active MAPS ASPM work. |
| Cal | Mojo | Coordinator | Level 3 - Staff | None observed in roster | `agents/cal-aspm/agent-profile.md`; role `Autonomy.md`; `roles/autonomy-engineer/cal-level4-promotion-packet.md` exists | Active MAPS ASPM coordinator. Strong Staff. Tess prepared Cal's Level 4 packet for Scott review. Target Level 4 Senior Staff after approval. No implementation, Git/release, architecture override, or autonomous runtime authority. |
| Vik | Mojo | Coordinator / architecture lead | Level 5 Principal (Policy Autonomy) active for completed-research product-recommendation review only; Level 6 native loop defined-not-active | `vik-visible-backlog-research` active 30-minute visible backlog heartbeat and now calls `roles/maps-agentic-systems-program-architect/scripts/level5automation.py`; `vik-daily-role-memory-maintenance` active daily cron; `vik-handoff-check` queue/file-watch sidecar paused | `agents/vik-aspa/agent-profile.md`; role `Autonomy.md`; `level5-product-recommendation-policy.md`; `level5-product-recommendation-state.json`; `level5-product-recommendation-proof.md`; `roles/maps-agentic-systems-program-architect/scripts/level5automation.py`; `level6-ai-security-research-loop-policy.md`; `roles/autonomy-engineer/vik-level4-level6-review-packet.md`; eval/deploy/observe/promotion artifacts exist | Scott corrected the stale demotion: Vik is Level 5 Principal for completed-research product-recommendation policy autonomy. Level 4 scoped research backlog loops remain part of Vik's lower-level capability, but Vik's current standing is Level 5. The Level 5 script found 48 completed Level 4 reports and 48 Level 5 reports; after correction, canonical `Autonomy.md` and state no longer treat this as a source conflict. Level 5 means Vik may look across completed research and recommend whether the company would be well served by making, implementing, adopting, integrating, further reviewing, or declining researched products or capabilities. No Level 6 discovery, implementation, procurement, vendor contact, Git/release, production, spending, secrets, external communication, final product decision, broad runtime, or authority expansion. |
| Liz | Mojo | Operator / workflow owner | Level 3 - Staff with policy-scoped `/maps` execution boundary | `liz-handoff-check` active per roster | `agents/liz-training/agent-profile.md`; role `Autonomy.md`; `roles/autonomy-engineer/liz-level4-promotion-packet.md` exists | Training coordinator with bounded heartbeat and site/training mirror scope. Tess prepared Liz's Level 4 packet for Scott review. No production publish, Git/release, or autonomous runtime authority. |
| Mae | Mindshare | Operator | Level 4 Senior Staff (Scoped Autonomy), operational with script-backed proof | `mae-handoff-check` active per roster; `mae-automation-health-check` active 4-hour heartbeat that calls `scripts\level4automation.py` | `agents/mae-communications/agent-profile.md`; role `Autonomy.md`; `roles/autonomy-engineer/mae-level4-promotion-packet.md`; `roles/communications-director/level4-automation-health-state.json`; `roles/communications-director/level4-proof.md`; `scripts\level4automation.py` | Scott formally promoted Mae to Level 4 on 2026-06-24. Proof history records dropped-packet delivery failure routed to Bea, file-watch runner stall routed to Bea, restored state/proof retention, and a 2026-06-24 scheduled-mode script proof checking 17 active configs with zero critical findings. Mae's deterministic checks now live in a human-readable script while the heartbeat handles wakeup, live-thread checks, owner routing, and user-visible reporting. No external communication, authority expansion, Git/release, production, spending, secrets, cadence/target-thread change, or broad autonomous runtime. |
| Reid | Mindshare | Operator | Level 3 - Staff | `reid-handoff-check` active per roster | `agents/reid-release/agent-profile.md`; role `Autonomy.md`; `roles/autonomy-engineer/reid-level4-promotion-packet.md` exists | Release-management coordinator/operator. Tess prepared Reid's Level 4 packet for Scott review. Strong gate owner for release/Git routing, but no Git/GitHub write authority until explicit approval. No autonomous runtime. |
| Tess | Mindshare | Operator | Level 4 Senior Staff (Scoped Autonomy), operational inside approved automation-baseline, promotion-packet, and durable-methodology conversion scope | `tess-autonomy-evaluation` active 4-hour heartbeat for evaluation/Liz handoff only; `tess-level-4-autonomy-backlog-processing` active local cron on 30-minute cadence that calls `scripts\level4automation.py` | `agents/tess-autonomy/agent-profile.md`; role `Autonomy.md`; `automation.backlog.md`; `policy-autonomy.md`; `level4-promotion-packet-policy.md`; `level4-gate-checklist.md`; `level4-processing-state.json`; `level4-proof.md`; `level4-visible-log.md`; `scripts\level4automation.py`; Rae, Cal, Ana, Vik, Liz, Mae, Reid, Bea, Jay, Cole, June, Paige, and Lane packet files exist | Scott approved Tess's Level 4 scope on 2026-06-22. Scheduled runs created review packets for Rae, Cal, Ana, Vik, Liz, Mae, Reid, Bea, Jay, Cole, June, Paige, and Lane; requested Scott review; wrote state/proof; held denied-action boundaries; passed pause/resume drill; restored 30-minute cadence; and now uses durable script-owned checks for backlog counts, Reid-route gaps, state/proof, and conversion queue visibility. Current backlog includes remaining `METH-*` script/timer methodology conversions for Vik, Lane, June, Reid, and FileWatch handoff automations. Level 5 remains inactive and Level 6 is not defined. No broad autonomous runtime, unilateral gate edits, Git/release, production, external comms, spending, secrets, promotion approval, or authority expansion. |
| Cole | Mindshare | Operator | Level 4 Senior Staff (Scoped Autonomy), runtime-installed-with-findings | `hr-director-handoff-check` active per roster; `cole-hourly-role-file-and-whoami-validation` active hourly heartbeat that calls `roles/hr-director/scripts/level4automation.py` | No agent profile observed; role `Autonomy.md`; `roles/autonomy-engineer/cole-level4-promotion-packet.md`; `roles/hr-director/scripts/level4automation.py`; `roles/hr-director/level4-role-file-validation-state.json`; `roles/hr-director/level4-proof.md` | Scott approved Cole Level 4 on 2026-06-24 for validating that role files exist for each current role's current automation/autonomy level and confirming WhoAmI Autonomy Context injection on account creation/welcome and hourly. Tess installed the hourly heartbeat, updated Cole contract/loop/welcome/state/proof, moved the deterministic logic to the standard role-local `scripts/level4automation.py` name, and completed scheduled proof. Do not call Cole fully operational Level 4 until current validation findings and Reid promotion durability pass. No Level 5+, role activation, authority changes, Git/release, production, external communication, spending, secrets, or broad autonomous runtime. |
| June | Mindshare | Operator | Level 3 Staff; canonical `Autonomy.md` exists; Level 4 packet ready for Scott review | `june-writing-nudge` active writing nudge heartbeat | No agent profile observed; role `Autonomy.md`; `roles/autonomy-engineer/june-level4-promotion-packet.md` exists | Activated Staff Writer. Tess prepared June's Level 4 packet for Scott review. June can draft, synthesize, and support Marketing/book work inside approved scope. No public publishing, external communication, production, Git/release, or autonomous runtime authority. |
| Paige | Mindshare | Operator | Level 3 Staff; canonical `Autonomy.md` exists; Level 4 packet ready for Scott review | None observed in roster | No agent profile observed; role `Autonomy.md`; `roles/autonomy-engineer/paige-level4-promotion-packet.md` exists | Activated Executive Assistant under Executive Operations. Tess prepared Paige's Level 4 packet for Scott review. Notes-only scope. No email, Slack, calendar, private-channel, connector, external communication, autonomous runtime, production, Git/release, spending, secrets, or authority-expansion authority. |
| Bea | Mojo | Operator | Level 3 Staff; Level 4 packet ready for Scott review | `bea-handoff-check` active per roster | `agents/bea-maps-engineer/agent-profile.md`; role `Autonomy.md`; `roles/autonomy-engineer/bea-level4-promotion-packet.md` exists | Mojo MAPS engineer for assigned implementation. Tess prepared Bea's Level 4 packet for Scott review. No repository write, Git/GitHub, release, production, external communication, spending, or autonomous agent authority. |
| Imani | Mojo | Operator | Level 3 Staff | None observed | No agent profile observed; role `Autonomy.md`; `roles/data-engineering-director/role-agent.md`; `WhoAmI.md`; `state.json`; Drive mirror exists | Activated Data Engineering Director from REC-006. Staff-level internal data-engineering role; may research, answer, recommend, name owners/risks/gates, and draft assigned internal plans. No production, Git/release, data-system credentials, secrets, external communication, spending, automation, broad runtime, Level 4+, or authority expansion. |
| Lane | Mojo | Operator | Level 3 Staff; canonical `Autonomy.md` exists; Level 4 packet ready for Scott review | `lane-hourly-token-usage-update` active; `lane-daily-token-graph-build` disabled | No agent profile observed; role `Autonomy.md`; `roles/autonomy-engineer/lane-level4-promotion-packet.md` exists | Activated Mojo Lab Operator under Vik on the Mojo MAPS Management Team. Tess prepared Lane's Level 4 packet for Scott review. Maintains a reviewable lab queue for MAPS skill creation, modification, validation, proof capture, handoff routing, and approved token-usage reporting. No broad autonomous runtime, production, Git/GitHub, release, spending, external communication, secrets, connector access, or authority-expansion authority. |
| Jay | Watch | Operator | Level 3 - Staff | `jay-handoff-check` active per roster | `agents/jay-meetup/agent-profile.md`; role `Autonomy.md`; `roles/autonomy-engineer/jay-level4-promotion-packet.md` exists | Customer-success / Meetup operator. Tess prepared Jay's Level 4 packet for Scott review. Can coordinate approved prep. No live Meetup, Zoom distribution, external communication, production, Git/GitHub, spending, or authority expansion without approval. |

## Recruiting Pipeline Packet Standing

These entries are not activated employees. They are named, unassigned recruiting pipeline packets maintained by Ana's approved Level 4 scoped lifecycle. Level 2 Trainee means the packet can support research, answers, recommendations, and owner/risk/gate naming inside the packet boundary without changing state. It does not grant office activation, channels, runtime, memory or handoff writes, production, Git/release, spending, secrets, external communication, or authority expansion.

| ID | Assigned name | Title | Org | Current packet level | Operating stage | Authority boundary | Source packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REC-001 | Morgan Vale | Operations Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-001-level2.md |
| REC-002 | Priya Sen | Product Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-002-level2.md |
| REC-003 | Owen Kline | Technology Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-003-level2.md |
| REC-004 | Nia Calder | Engineering Director | Mindshare / Mojo | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-004-level2.md |
| REC-005 | Mateo Ruiz | Platform Engineering Director | Mojo | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-005-level2.md |
| REC-007 | Theo Nakamura | AI Systems Engineering Director | Mojo | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-007-level2.md |
| REC-008 | Harper Quinn | Security Engineering Director | Mindshare / Mojo | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-008-level2.md |
| REC-009 | Sloane Mercer | Revenue Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-009-level2.md |
| REC-011 | June Park | Staff Operations Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-011-level2.md |
| REC-012 | Leon Archer | Executive Operations Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-012-level2.md |
| REC-013 | Mira Patel | PMO Director | Mindshare / Mojo | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-013-level2.md |
| REC-014 | Gabe Rowan | Product Management Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-014-level2.md |
| REC-015 | Elise Hart | Product Operations Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-015-level2.md |
| REC-016 | Nora Voss | Service Design Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-016-level2.md |
| REC-017 | Kai Bennett | Experience Design Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-017-level2.md |
| REC-018 | Amara Hayes | User Research Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-018-level2.md |
| REC-019 | Drew Collins | Sales Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-019-level2.md |
| REC-020 | Celia Grant | Partnerships Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-020-level2.md |
| REC-021 | Jordan Hale | Customer Success Director | Mindshare / Watch / Mojo | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-021-level2.md |
| REC-022 | Samira Knox | Support Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-022-level2.md |
| REC-023 | Mila Chen | People Operations Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-023-level2.md |
| REC-024 | Adrian Moss | Legal Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-024-level2.md |
| REC-025 | Isla Monroe | Compliance Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-025-level2.md |
| REC-026 | Victor Lane | Vendor Management Director | Mindshare | Level 2 Trainee | Position packet / unassigned recruiting pipeline item | Not activated; no office, runtime, channels, handoff/memory writes, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-026-level2.md |

Finn / REC-010 is excluded from this unassigned packet table because Scott separately activated Finn as Finance Director / Level 3 Staff operator outside the timed queue.

## Readiness Bands

### Band A: Human approval source

- Scott

### Band B: Strong active Level 3 Staff with autonomy-readiness artifacts

- Rae
- Cal
- Liz
- Reid
- Jay

These roles have current operating authorization plus canonical autonomy/profile artifacts, but no broad autonomous runtime. Several roles have handoff/monitoring automations; those mechanisms are evidence and workflow support, not stage promotion by themselves.

### Band C: Approved Level 4 scoped autonomy

- Ana

Ana is approved only inside a narrow role-native scope. Ana may process approved recruiting backlog items through internal role-lifecycle preparation. Ana does not have active Level 5/6, external communication, production, Git/release, spending, secrets, promotion approval, or broad runtime authority.

### Band C2: Level 4 operational after proof

- Tess
- Mae

Tess has approval, contract, trigger, runtime, work-loop, state, evidence, boundary, review, revocation, display proof, and script/timer separation proof for the approved Level 4 scope. Tess may be displayed as operational Level 4 only for automation-baseline, promotion-packet, and durable-methodology conversion work; this does not grant Level 5, Level 6, promotion approval, broad runtime, gate-edit, Git/release, production, external communication, spending, secrets, or authority expansion.

Mae has approval, contract, trigger, runtime, state, evidence, boundary, review, display proof, and script/timer separation proof for the approved Level 4 automation-health scope. Mae may be displayed as operational Level 4 only for file-watch/process health monitoring, bounded safe mechanical repair/routing, and owner escalation. This does not grant external communication, authority expansion, Git/release, production, spending, secrets, cadence/target-thread changes, or broad autonomous runtime.

### Band D: Level 5 Principal policy autonomy

- Vik

Vik has the richest autonomy surface: architecture ownership, memory-maintenance automation, `Autonomy.md`, `agent-profile.md`, eval/deploy/observe/promotion files, and runtime-adjacent artifacts. Standing is Level 5 Principal for completed-research product-recommendation policy autonomy. Scott corrected the stale Level 4 downgrade on 2026-06-24. Level 6 remains inactive: the full AI/security internet discovery, backlog creation, deep analysis, and Level 5 recommendation loop still requires final promotion review, runtime gates, eval proof, observation, rollback, revocation, and Scott activation approval.

### Band E: Active operators with new autonomy contracts, pending review

- June
- Paige
- Lane

These roles are active operators by roster/contract. Their canonical `Autonomy.md` files and Level 4 review packets now exist, but they should not be promoted to Level 4+ until Scott reviews the packets and required eval/runtime/audit/rollback/revocation proof exists.

### Band E2: Level 4 runtime installed, scheduler proof pending

- Cole

Cole has Scott-approved Level 4 scoped autonomy for role-file existence validation and WhoAmI Autonomy Context injection validation only. Runtime is installed as an hourly heartbeat in Cole's office, and first manual proof exists. Standing remains runtime-installed-scheduler-proof-pending until scheduler-triggered proof writes current state/proof and Reid promotion durability is complete.

### Band F: Draft or inactive

- Matt: released legacy context; no active autonomy path.

## Main Gaps

| Gap | Affected roles | Required repair |
| --- | --- | --- |
| Level 4 review packets pending Scott review | Rae, Cal, Liz, Reid, Bea, Jay, June, Paige, Lane | Scott review packets; no promotion until eval/runtime/audit/rollback/revocation proof exists. |
| Level 4 scheduler proof pending | Cole | Wait for `cole-hourly-role-file-and-whoami-validation` to write scheduler-triggered state/proof, then validate all Level 4 gates and Reid durability before marking operational. |
| Missing agent profile | Cole, June, Paige, Lane | Create only if role is being moved toward agent readiness. |
| Evals not executed or not complete | Most roles | Add/evaluate role-specific eval suites before Level 4+ promotion. |
| Broad runtime activation not approved | All non-human roles | Keep broad runtime blocked until contract, gates, evals, adapter, deployment/observe, audit, rollback, and Scott approval align. Vik has approved narrow Level 5 policy autonomy only; Ana, Tess, Mae, and Cole have approved narrow Level 4 scopes only. |
| New Level 4 gate must be applied retroactively | Ana, Vik, Tess, Mae, Cole, future Level 4 candidates | Recheck every Level 4 claim against `level4-gate-checklist.md`; do not call a role operational Level 4 unless all gates pass. |
| Level 4 script/timer conversion pending | Ana, Vik, Lane, June, Reid, FileWatch handoff automations | Process `METH-*` rows in `automation.backlog.md`; deterministic repeatable logic should move to human-readable scripts where practical, with timers acting as wakeups/routers and Reid receiving Release Management requests for changed durable files. |
| Level 4 proof cadence restored | Tess, Mae | Tess's 30-minute backlog cron and Mae's 4-hour health heartbeat are now script-first. Continue monitoring state/proof/visible log and do not expand scope. |
| Roster backup-map cadence stale | Ana | Current automation source shows `ana-l4-recruiting-backlog-processing` runs every 4 hours; `G:\My Drive\Mindshare\roles.md` backup-map section still says 3-minute proof-testing cadence. Roster owner should correct the backup-map text; no standing change. |
| Automation mistaken for autonomy | Roles with heartbeat/file-watch/scheduler | Keep explicit: automation presence is mechanical, not authority. |
| G-drive primary-file risk | All roles | Primary team-member files stay in local repos. G drive may hold channels, handoffs, mirrors, indexes, and non-primary notes. |

## Recommendations

1. Keep current global claim: no current non-human role is Level 6 Partner.
2. Review June, Paige, and Lane Level 4 packets before any promotion; their `Autonomy.md` files now exist but are not approval grants. Cole's Level 4 scope has been approved and installed, but remains scheduler-proof/durability pending before operational display.
3. Redesign Level 5 around policy-backed loops before promoting anyone to Principal. Tess's packet-building and Scott-review routing now belongs in Level 4, not Level 5.
4. Treat Vik as the active Level 5 Principal policy-autonomy holder for completed-research product-recommendation review only; do not downgrade him to Level 4 from stale source text.
5. Do not create more autonomous runtime until strict-intent gate, source loader, contract validator, runtime adapter, audit/state, backup/restore, and promotion review remain green.

## Changelog

| Date | Version | Change | Owner |
| --- | --- | --- | --- |
| 2026-06-24 | 0.1.53 | Activated Imani / Data Engineering Director from REC-006 as Level 3 Staff / activated Operator and removed REC-006 from the unassigned Level 2 packet table. | Tess / Ana |
| 2026-06-24 | 0.1.52 | Restored Vik to Level 5 Principal policy autonomy for completed-research product-recommendation review only after Scott corrected the stale Level 4 downgrade; Level 6 and broad runtime remain inactive. | Tess / Ana |
| 2026-06-24 | 0.1.51 | Assigned human display names to all 24 unactivated Level 2 Trainee director packets and updated the recruiting pipeline packet standing table; Finn / REC-010 remains activated Finance Director outside the timed queue. | Tess / Ana |
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
| 2026-06-22 | 0.1.10 | Recorded Ana Level 4 scoped-autonomy path as prepared but not approved; added initial role-lifecycle trigger evidence and remaining Vik/Scott approval gates. | Tess |
| 2026-06-22 | 0.1.11 | Clarified the general Level 4 rule: every role may have a backlog, and Senior Staff means processing approved role-native backlog items under the role's `Autonomy.md`. Updated Ana evidence to treat `recruiting.backlog.md` as the backlog source and role `Autonomy.md` as the capability contract. | Tess |
| 2026-06-22 | 0.1.12 | Recorded Scott-defined Vik Level 4/5/6 capability ladder while keeping Vik at current Level 4 standing only. | Tess |
| 2026-06-22 | 0.1.13 | Recorded Scott-defined Tess Level 4/5/6 capability ladder and created `automation.backlog.md`; Level 4 applies to Level 3 roles only; Tess remains Level 3 except for the narrow approved evaluation heartbeat. | Tess |
| 2026-06-22 | 0.1.14 | Promoted Ana standing to Level 4 Senior Staff scoped autonomy for approved recruiting backlog processing only; Level 5/6 remain blocked; proposed local 30-minute backlog automation for review. | Tess |
| 2026-06-22 | 0.1.15 | Activated Ana backlog processing automation on 3-minute proof-testing cadence with three consecutive Ana-owned proof requirement, then 4-hour steady cadence; processing continues until backlog empty or blocked. | Tess |
| 2026-06-22 | 0.1.16 | Changed Ana Level 4 output target to Level 1 New Hire packets; reopened REC-001 through REC-026 for reprocessing and reset proof streak to 0 of 3 under the new standard. | Tess |
| 2026-06-22 | 0.1.17 | Recorded Ana Level 1 New Hire packet proof run 1 of 3 after Ana reprocessed REC-001 through REC-026 and held Level 4 boundaries. | Tess |
| 2026-06-22 | 0.1.18 | Recorded Ana Level 1 proof streak 3 of 3 and moved Ana's Level 4 recruiting backlog automation to the 4-hour steady cadence. | Tess |
| 2026-06-22 | 0.1.19 | Corrected June to Level 3 Staff and corrected Level 5 interpretation: old Level 5/6 task ladders are reclassification candidates; real Principal autonomy requires approved policy packets and runtime/eval proof. | Tess |
| 2026-06-22 | 0.1.20 | Recorded Scott's updated Ana ladder: Level 4 scoped lifecycle now covers backlog to Level 1, Level 1 to Level 2 after 24 hours, and Level 2 to Level 3 after five days; Level 5 policy autonomy is defined but inactive; Level 6 is deferred. | Tess |
| 2026-06-22 | 0.1.21 | Recorded Scott's updated Vik ladder: Level 4 remains correct and active; Level 5 is goal-based product/implementation recommendation policy autonomy; Level 6 is the full AI/security discovery, backlog, deep-analysis, and Level 5 recommendation loop. Vik remains Level 4 only until higher promotion is approved and proven. | Tess |
| 2026-06-22 | 0.1.22 | Corrected Tess ladder: Level 4 builds automation structure for Level 3 roles; Level 5 builds role-specific Level 4 promotion packets, defines each person's Level 4/5/6 capabilities, and requests Scott review; Level 6 becomes possible from the defined Level 5 policy. Tess remains Level 3 until promotion approval. | Tess |
| 2026-06-22 | 0.1.23 | Collapsed Tess ladder per Scott: promotion-packet construction moves into Level 4 alongside automation structure; the former Level 6 native loop becomes Level 5; Tess has no Level 6 capability currently defined. | Tess |
| 2026-06-22 | 0.1.24 | Recorded Scott approval to upgrade Tess to Level 4 Senior Staff (Scoped Autonomy) for automation structure, promotion-packet construction, capability definition, and Scott review routing. Level 5 remains inactive and Level 6 remains undefined. | Tess |
| 2026-06-22 | 0.1.25 | Corrected Tess status after Level 4 gate review: Tess is Level 4 approved-not-operational, not operational Level 4, because trigger/runtime/work-loop/state/evidence gates do not pass. Added requirement to recheck all Level 4 claims against the new gate. | Tess |
| 2026-06-22 | 0.1.26 | Installed Tess Level 4 local cron `tess-level-4-autonomy-backlog-processing` plus state/proof files; Tess is runtime-installed-pending-proof, not operational Level 4 until scheduled work-loop evidence passes. | Tess |
| 2026-06-22 | 0.1.27 | Recorded first Tess Level 4 proof-testing observation window: scheduler is configured, but no scheduled proof write was observed; Tess remains not operational Level 4. | Tess |
| 2026-06-22 | 0.1.28 | Recorded successful Tess Level 4 scheduled proof: `AUTO-REV-001` completed, Rae packet created for Scott review, state/proof written, pause/resume drill passed, and cadence restored to 30 minutes. | Tess |
| 2026-06-22 | 0.1.29 | Added Tess Level 4 visibility requirement: every non-noop backlog-processing run must write local visible log and Heartbeat entry. | Tess |
| 2026-06-22 | 0.1.30 | Recorded new Tess Level 4 evidence: review packets completed for Ana, Vik, Liz, and Mae, plus prior Rae and Cal packets; standings unchanged and no authority expanded. | Tess |
| 2026-06-22 | 0.1.31 | Created canonical `Autonomy.md` contracts and Level 4 review packets for Cole, June, Paige, and Lane after Scott clarified that missing contracts should be repaired during readiness processing; no promotions or runtime activations performed. | Tess |
| 2026-06-22 | 0.1.32 | Normalized packet evidence across all completed Tess Level 4 review items: Rae, Cal, Ana, Vik, Liz, Mae, Reid, Bea, Jay, Cole, June, Paige, and Lane. No standings changed. | Tess |
| 2026-06-22 | 0.1.33 | Reconciled source evidence: Ana's live Level 4 automation is on the 4-hour steady cadence, while the `roles.md` backup-map section still says 3-minute proof-testing cadence. Marked backup-map text stale; no standings changed. | Tess |
| 2026-06-24 | 0.1.44 | Restored Mae standing after proof-retention check. Mae remains Level 4 operational with only two verifiable prior automation-health results and a restored state/proof store; next scheduled run must prove continuity. | Tess |
| 2026-06-24 | 0.1.45 | Recorded Scott-approved Cole Level 4 scope for role-file existence and WhoAmI Autonomy Context injection validation. Installed hourly heartbeat and state/proof; Cole is runtime-installed-scheduler-proof-pending until hourly proof and Reid durability pass. | Tess |
| 2026-06-24 | 0.1.46 | Added recruiting pipeline packet standing table showing REC-001 through REC-005 and REC-007 through REC-009 and REC-011 through REC-026 as unassigned Level 2 Trainee packets; Finn / REC-010 remains activated Finance Director outside the timed queue. | Tess / Ana |
| 2026-06-24 | 0.1.47 | Recorded script/timer methodology conversion for Tess and Mae. Mae is now operational Level 4 with script-backed proof; Tess has queued remaining `METH-*` conversions for Ana, Vik, Lane, June, Reid, and FileWatch handoff automations. | Tess |
| 2026-06-24 | 0.1.48 | Recorded Ana script/timer methodology conversion. Ana's Level 4 standing is unchanged, but the canonical logic/proof sources now include `scripts\level4automation.py`, `level4-lifecycle-state.json`, and `level4-lifecycle-proof.md`. | Tess |
| 2026-06-24 | 0.1.49 | Standardized current Level 4 Python scripts to each role's `scripts\level4automation.py` path for Cole, Tess, Mae, and Ana; no autonomy standing was expanded. | Tess |
| 2026-06-24 | 0.1.50 | Added Vik Level 5 role-local script evidence: `roles/maps-agentic-systems-program-architect/scripts/level5automation.py` writes Level 5 state/proof and flags that Level 5 reports exist while Vik's canonical `Autonomy.md` still says Level 5 is not active. | Tess |


