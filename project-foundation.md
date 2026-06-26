# Project Foundation

## Kickoff

M0 Project Foundation for `mindshare`, the parent organization for projects under the Mindshare umbrella.

## Project

- Name: mindshare
- Owner: Scott
- Repository: C:\Users\scott\Code\mindshare
- Date: 2026-06-19
- Project type: Parent organization multi-agent project
- Primary customer or operator: Scott
- Desired outcome: Oversee all projects underneath the Mindshare umbrella through a consistent MAPS memory and skill-output structure.

## M0 Preflight Decisions

| Decision | Answer | Confirmed by | Notes |
|---|---|---|---|
| RAG exists? | Yes | Scott | Obsidian itself is the RAG store for now. |
| Notes location | G:\My Drive\Mindshare | Scott | Current `mindshare` project root. |
| Notes access method | filesystem | Scott | Google Drive-backed Obsidian vault. |
| Additional notes locations | None yet | Scott | Not needed for M0. |
| RAG provider/location/index | Obsidian at G:\My Drive\Mindshare | Scott | No separate vector index configured yet. |
| RAG access method | filesystem | Scott | Markdown-first access. |
| Additional RAG/index locations | None yet | Scott | Future explicit indexes can be added later. |
| Canonical store policy | Obsidian is canonical for project-authored notes, durable memory, and RAG. `.maps` is automation state. | Scott | Standard project writes go to the project folder; MAPS-specific writes go to `maps-runs`. |
| Memory root | G:\My Drive\Mindshare | Scott | No separate `memory` folder for now. Durable memory files live at the top level. |
| Memory access method | filesystem | Scott | Markdown files in Obsidian. |
| Sources root | G:\My Drive\Mindshare | Scott | Source material is not separately managed yet. |
| Sources access method | filesystem | Scott | Capture sources in ordinary Obsidian notes until a source workflow is defined. |
| Reuse remembered defaults? | No prior defaults existed | Codex | Fresh project preferences were created. |
| Project identity and type | `mindshare`, parent organization multi-agent project | Scott | Not a downstream product org using MAPS. |
| Project intent | Oversee all projects underneath the Mindshare umbrella | Scott | Parent project control layer. |
| Primary customer/operator | Scott | Scott | Solo operator for now. |
| Update global living template? | Yes | Scott | Future projects should use G:\My Drive\Mindshare\[project]. |

## Customer Story

- As a: Scott, operating the Mindshare parent project
- I need: a durable, Obsidian-centered way to organize MAPS work across all child projects
- So I can: keep project context, skill outputs, memory, and retrieval aligned across the Mindshare umbrella.

## Current Workflow

- Current process: Scott uses Obsidian as the working knowledge base and durable project memory. MAPS skills are invoked from Codex against project repositories.
- Pain points: The default MAPS scaffold assumes separate `notes`, `sources`, and `memory` folders, but Scott wants Obsidian to be the canonical project store with standard project writes in the project folder and MAPS-specific writes in `maps-runs`.
- Workarounds: Record the desired Obsidian contract explicitly in this foundation and in `.maps/foundation-preferences.json`; use `maps-runs` for MAPS-specific outputs and helper-maintained skill notes.
- Evidence: M0 preflight conversation with Scott on 2026-06-19.

## EventStorming Lite

| Domain event | Trigger or command | Actor | Policy or rule | System/data touched | Pain point | Question |
|---|---|---|---|---|---|---|
| Mindshare foundation is created | `/foundation` | Scott, Codex | Ask one question at a time; do not infer foundation defaults without confirmed answers | Codex repo, Obsidian vault | Existing skill wording asks about defaults too early | Should the skill permanently remove the defaults question? |
| MAPS skill run completes | `/shape`, `/define-agent`, etc. | Scott, Codex | Write MAPS-specific output, run summary, and helper-maintained skill note into `maps-runs` | G:\My Drive\Mindshare\maps-runs | Older foundation wording referenced top-level skill folders | Which stale references still need cleanup? |
| Child project is added | New project under Mindshare | Scott | Future projects should write to G:\My Drive\Mindshare\[project] | Obsidian vault, global foundation preferences | Placeholder behavior is policy, not native helper behavior yet | How should `[project]` be resolved automatically? |
| Project context is queried | Scott asks what is known | Scott, Codex | Answer from Obsidian/MAPS memory where appropriate | Obsidian notes, `.maps` state | RAG is Obsidian, not a separate index yet | What retrieval/indexing tool should eventually sit on top of Obsidian? |

## Service Blueprint Lite

| Customer/operator action | Visible agent/system action | Backstage process | Supporting system/data | Evidence/source | Failure point |
|---|---|---|---|---|---|
| Scott invokes a MAPS phase | Codex asks focused preflight questions one at a time | Skill reads project preferences and writes phase output | `.maps/foundation-preferences.json`, Obsidian `maps-runs` folder | M0 conversation | Skill asks abstract defaults questions instead of concrete location questions |
| Scott confirms project memory layout | Codex records Obsidian as canonical | Preferences and foundation contract are updated | G:\My Drive\Mindshare, project foundation file | M0 conversation | Helper scripts assume `notes/sources/memory` scaffold |
| A future project starts | Codex proposes G:\My Drive\Mindshare\[project] as project root | Global foundation preferences are read | C:\Users\scott\.codex\maps\foundation-preferences.json | Scott's clarification | Placeholder may need custom skill support |
| A phase output is completed | Output appears in `maps-runs` | Optional RAG manifest records changed notes | Obsidian, `.maps/rag-updates.json` | This foundation run | Obsidian RAG has no separate reindex mechanism yet |

## Product Intent

- Project purpose: Oversee all projects underneath the Mindshare umbrella.
- User value: Scott gets a consistent project-control layer for MAPS work and project memory.
- Business or mission value: Mindshare can accumulate durable operating context across many projects without scattering phase outputs and decisions.
- Why agents are appropriate: MAPS work involves repeated research, design, build, evaluation, observation, and improvement loops that agents can perform and document consistently.
- Why multiple agents may be needed: The parent project may eventually coordinate distinct roles for project intake, memory maintenance, planning, evaluation, deployment, and review across child projects.

## Scaffold

Create or confirm:

```text
.maps/
  foundation-preferences.json
  rag-updates.json
.env.example
.env.local
G:\My Drive\Mindshare\
  maps-runs/
  daily/
  interviews/
  research/
  decisions/
  docs/
  transcripts/
  screenshots/
  links.md
  project-context.md
  glossary.md
  entity-map.md
```

For future projects, use:

```text
G:\My Drive\Mindshare\[project]\
  maps-runs/
```

## Remembered Foundation Preferences

- Preference source: project
- Notes root: G:\My Drive\Mindshare
- Notes access method: filesystem
- Additional notes locations:
- Sources root: G:\My Drive\Mindshare
- Sources access method: filesystem
- Memory root: G:\My Drive\Mindshare
- Memory access method: filesystem
- RAG provider: Obsidian
- RAG location: G:\My Drive\Mindshare
- RAG index path:
- RAG access method: filesystem
- Additional RAG locations:
- Canonical store policy: Obsidian vault at G:\My Drive\Mindshare is canonical for project-authored notes, durable memory, and RAG. Standard project writes should go to the project folder. MAPS-specific phase outputs, run summaries, and helper-maintained skill notes should go to `G:\My Drive\Mindshare\maps-runs`. MAPS project state in `.maps` is automation state. Source material is not separately managed yet; capture it in ordinary Obsidian notes unless a later source workflow is defined.
- Global default used?: no
- Updated `.maps/foundation-preferences.json`?: yes

## Persistent Memory Contract

| Store | Type | Location | Purpose | Update trigger | Update method | Sync rule | Canonical? | Do not write |
|---|---|---|---|---|---|---|---|---|
| Obsidian project root | Markdown vault | G:\My Drive\Mindshare | Canonical project-authored notes, durable memory, and RAG for `mindshare`. | Any stable project fact, decision, ordinary project note, or retrieval-worthy update. | Create or edit Markdown in the project folder. | Treat `.maps` as automation metadata derived from or pointing back to Obsidian. | Yes | Secrets, unsupported claims, noisy raw logs, or MAPS-specific run artifacts. |
| MAPS runs | Markdown folder | G:\My Drive\Mindshare\maps-runs | MAPS-specific phase outputs, run summaries, and helper-maintained skill notes. | Completion of a MAPS skill phase or MAPS-specific durable output. | Write or append the artifact and run summary in `maps-runs`. | Helper-maintained notes and RAG manifests should point back to `maps-runs`. | Yes for MAPS phase outputs and summaries | Mixed-project notes or unrelated scratch work. |
| Project context | Markdown memory | G:\My Drive\Mindshare\project-context.md | Stable facts about Mindshare, its purpose, structure, and operating context. | Durable project context changes. | Append or revise concise Markdown entries. | Keep aligned with foundation and later phase outputs. | Yes | Temporary brainstorms. |
| Glossary | Markdown memory | G:\My Drive\Mindshare\glossary.md | Shared terms and definitions. | New stable term or changed definition. | Add or update definitions. | Keep terms consistent across skill outputs. | Yes | Ambiguous terms without context. |
| Entity map | Markdown memory | G:\My Drive\Mindshare\entity-map.md | People, projects, systems, and relationships under Mindshare. | New child project, stakeholder, tool, or relationship. | Add concise entity entries and links. | Keep synced with child-project foundations. | Yes | Private personal data beyond project needs. |
| Source material | Ordinary Obsidian notes for now | G:\My Drive\Mindshare | Raw evidence, docs, transcripts, screenshots, or links when they matter. | A source becomes important to project reasoning. | Capture it where it naturally belongs in Obsidian. Define a dedicated source workflow later if needed. | Cite or link source notes from phase outputs. | Yes when captured and cited | Unapproved private material or uncited dumps. |
| RAG | Obsidian | G:\My Drive\Mindshare | Queryable project knowledge. | New or changed approved notes or memory. | Use Obsidian as retrieval corpus; future indexes should derive from it. | Derived indexes must point back to Obsidian notes. | Yes for current retrieval corpus | Separate stale indexes without provenance. |
| MAPS state | JSON state | .maps/foundation-preferences.json | Remembered scaffold and memory routing for future skill runs. | Foundation configuration changes. | Structured JSON update. | Reflect important choices in this document and global defaults when approved. | Yes for automation defaults | Long prose or source evidence. |
| RAG update manifest | JSON state | .maps/rag-updates.json | Append-only record of MAPS outputs needing retrieval awareness. | New or changed MAPS phase output. | Append a structured entry. | Future indexing automation may consume it. | No, derived from canonical stores | Long prose or raw evidence. |

## Git Readiness

| Item | Status | Notes |
|---|---|---|
| Git available | yes | `git` is available in the project environment. |
| Local repository initialized | yes | `.git/` exists in `C:\Users\scott\Code\mindshare`. This only means local Git state exists. |
| Remote repository | not confirmed for mindshare | `origin` currently points to `https://github.com/AesopScott/maps.git`, which is not recorded as a Mindshare remote. |
| Git initialization action | skipped | No local initialization was needed. |
| Foundation artifact status | untracked | `.maps/`, `project-foundation.md`, and `.env.example` are new/untracked until Scott commits them. |

## Env/Secrets Scaffold

| Item | Status | Notes |
|---|---|---|
| `.env.example` | created | Placeholder keys only; no real secret values. |
| `.env.local` | created | Local ignored secrets file created after Scott confirmed. |
| `.gitignore` env rules | updated | Added `.env`, `.env.*`, `!.env.example`, `*.local`, and `.maps/tmp/`. |
| Real secret handling | configured | Real secrets should live in ignored local env files or a platform secrets manager, never in tracked files. |

## MAPS Skill Run Log

| Timestamp | Skill | Phase | Output | Memory updates | Notes |
|---|---|---|---|---|---|
| 2026-06-19T02:10:00+00:00 | /foundation | M0 | project-foundation.md; G:\My Drive\Mindshare\foundation\foundation.md | Created project foundation, project preferences, global defaults, Obsidian skill folders, and initial memory contract | Helper apply had a Windows backslash escaping issue; Markdown artifacts were written directly. |
| 2026-06-19T02:36:49+00:00 | /role | Role | roles/agentic-systems-program-manager/role-agent.md | Created Agentic Systems Program Manager role contract and workflow; added AGENTS.md automatic activation hook; mirrored role artifacts to G:\My Drive\Mindshare\role\agentic-systems-program-manager. | Role implemented as workflow owner with advisory auto-trigger for MAPS pipeline and skill-development prompts. |
| 2026-06-19T03:03:34+00:00 | /role | Role | roles/agentic-systems-program-manager/role-agent.md | Added Matt as the friendly/manual invocation name for the Agentic Systems Program Manager role; synced local and Obsidian role artifacts. | Manual call names now include Matt, ask Matt, Matt's review, ASPM review, and Agentic Systems Program Manager review. |
| 2026-06-19T03:15:08+00:00 | /shape | M1 | G:\My Drive\Mindshare\maps-runs\system-shape.md | Created M1 system shape; moved MAPS-specific output to `maps-runs`; updated G:\My Drive\Mindshare\project-context.md and G:\My Drive\Mindshare\entity-map.md; helper updated maps-runs shape note and .maps rag manifest. | M1 selected Multi-Agent / MAPS with flexible staged authority and Matt's accepted failure/escalation baseline. |
| 2026-06-19T03:18:20+00:00 | /foundation | M0 | C:\Users\scott\Code\mindshare\project-foundation.md | Corrected standard project vs MAPS-specific write routing; updated project and global foundation preferences; moved M1 shape artifact to maps-runs. | Scott clarified the canonical routing split after M1 shape. |
| 2026-06-19T04:38:26Z | /foundation | M0 incremental audit | project-foundation.md; .env.example; .env.local; .gitignore | Added env/secrets scaffold status, missing Obsidian working folders, links placeholder, and precise Git readiness wording. | Local Git exists; remote is not confirmed for Mindshare and currently points to maps.git. |
| 2026-06-19T13:06:40+00:00 | /role | Role | roles/lab-operator/role-agent.md | Created Lab Operator role contract, workflow, lab memory file, Matt memory file, and Mindshare lab queue. | Lab Operator created as workflow owner for lab.md with bounded authority and no autonomous loop until Scott approves a monitor goal. |
| 2026-06-19T08:05:53-06:00 | /role | Role | roles/agentic-systems-program-architect/role-agent.md | Created Vik / Agentic Systems Program Architect role contract, workflow, loop, hook spec, draft skill, state file, and AGENTS.md activation rule; mirrored role artifacts to Obsidian. | Vik is the Mindshare architecture owner; Matt remains the program cadence and handoff owner. |
| 2026-06-19T08:10:00-06:00 | /role | Role-Handoff | roles/agentic-systems-program-architect/handoffs/org-chart-development-2026-06-19.md | Added org chart development handoff to Vik; mirrored handoff and updated Vik state in Obsidian. | Vik owns org-chart architecture; Matt supports sequencing; Ana and Liz are planned roles, not yet built. |
| 2026-06-19T08:08:24-06:00 | /role | Role | roles/recruiter/role-agent.md | Created Ana / Recruiter role contract, workflow, loop spec, draft skill, state file, AGENTS.md activation rule, and /role skill ownership declaration; mirrored role artifacts to Obsidian. | Ana owns role intake and /role; Vik reviews architecture/control-plane fit; Matt supports sequencing; Scott approves activation and authority. |
| 2026-06-19T08:35:00-06:00 | /role-handoff | Role-Handoff | docs/role-handoffs.md | Created G:\My Drive\Mindshare\05 Role Handoffs, added visible handoff queue README, copied org-chart handoff into the queue, updated Vik state, and added repo handoff process/template. | Vik owns architecture packets; Matt owns build intake and cadence from explicit handoffs. |
| 2026-06-19T08:42:00-06:00 | /role-handoff | Role-Handoff | docs/role-handoffs.md | Finalized Role Handoffs queue and process, including Obsidian queue page, queue README, packet template, active org-chart packet, repo process, repo template, Vik state update, and RAG manifest entry. | Role Handoffs is now the intake bridge: Vik architects packets; Matt builds from ready-for-matt-intake packets. |
| 2026-06-19T08:18:00-06:00 | /define-agent | A1-skill-update | skills/define-agent/SKILL.md | Updated installed and Mindshare-local /define-agent skill files; added installed and local agent-definition templates; updated Mindshare root agent-definition template; recorded run in MAPS memory. | This was skill-development work, not a run defining a specific agent. |
| 2026-06-19T08:55:00-06:00 | /role-handoff | Role-Handoff | roles/agentic-systems-program-architect/handoffs/org-chart-development-2026-06-19.md | Updated org-chart handoff progress in local Vik handoff, Obsidian Vik handoff mirror, visible 05 Role Handoffs queue, maps-runs role-handoff note, project-foundation run log, and RAG manifest. | Vik bridged the missing website-builder role for a local draft only; Matt should sequence any publish. |
| 2026-06-19T09:08:00-06:00 | /role-handoff | Role-Handoff | docs/role-handoffs.md | Updated role handoff process docs, Obsidian 05 Role Handoffs queue notes, role channel template, packet template, Vik-Matt channel, maps-runs role-handoff note, project-foundation run log, and RAG manifest. | Scott clarified that handoffs are how all roles communicate; channel MD files are now the durable read/write substrate between common role pairs. |
| 2026-06-19T14:32:13+00:00 | /define-agent | A1-skill-update | skills/define-agent/SKILL.md | Updated Mindshare local define-agent skill, installed global define-agent skill, and MAPS run notes. | Role-to-agent conversion now belongs in /define-agent; role creation and qualification stays with Ana / /role. |
| 2026-06-19T09:18:00-06:00 | /role-handoff | Role-Handoff | docs/role-handoffs.md | Updated website page, repo role-handoff docs, Obsidian 05 Role Handoffs notes, channel README, channel template, handoff template, created channels/pipeline.md, removed channels/vik-matt.md, and updated maps-runs/project foundation/RAG manifest. | Scott clarified channels should be by function, not role pair; first function channel is pipeline.md. |
| 2026-06-19T09:28:00-06:00 | /role-handoff | Role-Handoff | docs/role-handoffs.md | Updated website Role Handoffs page, repo role-handoff docs, Obsidian 05 Role Handoffs notes, Pipeline channel, channel template, maps-runs role-handoff note, project-foundation run log, and RAG manifest. | 3-minute handoff checks are now an operating goal, not an active scheduler. |
| 2026-06-19T14:41:16+00:00 | /define-agent | A1 | agents/ana-recruiter/agent-brief.md | Created Ana agent brief; updated define-agent MAPS run note, project foundation run log, and RAG manifest. | Defined Ana / Recruiter as an approval-gated human-in-the-loop agent candidate. Next skill: /design-agent. |
| 2026-06-19T14:46:46+00:00 | /define-agent | A1-profile-fix | agents/ana-recruiter/agent-profile.md | Updated Mindshare agent profile artifact, define-agent skill instructions/templates, MAPS run log, and RAG manifest. | Ana now has both agent-brief.md and agent-profile.md. Define Agent now treats profile settings as required output, not optional website polish. |
| 2026-06-19T14:59:25+00:00 | /role | Role-skill-update | skills/role/SKILL.md | Updated global and Mindshare /role skill files, role templates, Mindshare AGENTS role hooks, active role artifacts, project foundation run log, MAPS role run note, and RAG manifest. | Accidental queuing behavior edits were backed out. Queuing prompt default cannot be toggled from repo files; no role behavior change for queuing was retained. |
| 2026-06-19T15:11:13+00:00 | /define-agent | A1-skill-update | skills/define-agent/SKILL.md | Updated the global installed /define-agent skill and the Mindshare local /define-agent copy. The full interview list is now an internal risk checklist, not an upfront form. | Scott flagged that Define Agent should use Research and Recommend instead of asking the wrong questions. The corrected behavior is source role first, R&R second, one question third. |
| 2026-06-19T15:11:13+00:00 | /design-agent | A2-skill-update | skills/design-agent/SKILL.md | Updated the global installed /design-agent skill and the Mindshare local /design-agent copy. The required interview is now explicitly an internal risk checklist, not a design form to ask upfront. | Scott flagged that Design Agent should use Research and Recommend instead of asking the wrong questions. The corrected behavior is source brief first, R&R second, one question third. |
| 2026-06-19T15:11:20+00:00 | /role-handoff | Role-Handoff | docs/role-handoffs.md | Updated G:\My Drive\Mindshare\05 Role Handoffs, channels/pipeline.md, channels/recruiting.md, role-channel-template.md, active role memory notes, project foundation run log, and RAG awareness manifest. |  |
| 2026-06-19T15:11:28+00:00 | /role | Role-skill-handoff-update | skills/role/SKILL.md | Updated skills/role/SKILL.md and skills/role/templates/role-agent.md; active role artifacts and memory notes now carry assigned handoff file goals. |  |
| 2026-06-19T15:13:03+00:00 | /role-handoff | Role-Handoff-finalize | docs/role-handoffs.md | Updated role-channel templates and role-handoff memory run log after final wording cleanup. |  |
| 2026-06-19T15:45:02+00:00 | /role | Role-memory-update | G:\My Drive\Mindshare\vik.md | Created G:\My Drive\Mindshare\vik.md; updated local and Obsidian Vik role-agent contracts; project foundation run log and RAG awareness manifest updated. |  |
| 2026-06-19T15:50:00+00:00 | /role | Role-memory-update | G:\My Drive\Mindshare\ana.md | Created Ana's durable working memory file; updated local and Obsidian Ana state files with memory pointers; updated Ana role memory note. | Scott requested Ana have a memory file like Matt. |
| 2026-06-19T15:51:27+00:00 | /role | Vik-handoff-goal | G:\My Drive\Mindshare\vik.md | Created heartbeat automation vik-handoff-check; created active thread goal; updated G:\My Drive\Mindshare\vik.md; project foundation run log and RAG awareness manifest updated. |  |
| 2026-06-19T15:51:33+00:00 | /role | Role-memory-template-update | C:\Users\scott\Code\mindshare\skills\role\SKILL.md | Created memory-template.md in Obsidian, repo templates, and installed /role templates; updated installed and repo /role skill contracts so every new role receives a required role memory file from memory-template.md; recorded boundary that memory creation does not grant loading, operating authorization, or agent status. |  |
| 2026-06-19T15:52:46+00:00 | /role-handoff | Vik-handoff-check | G:\My Drive\Mindshare\05 Role Handoffs\org-chart-development-2026-06-19.md | Updated G:\My Drive\Mindshare\05 Role Handoffs\channels\pipeline.md, G:\My Drive\Mindshare\05 Role Handoffs\org-chart-development-2026-06-19.md, G:\My Drive\Mindshare\role\agentic-systems-program-architect\handoffs\org-chart-development-2026-06-19.md, G:\My Drive\Mindshare\vik.md, project foundation run log, and RAG awareness manifest. |  |
| 2026-06-19T15:55:14+00:00 | /role-handoff | Vik-handoff-check | G:\My Drive\Mindshare\05 Role Handoffs\org-chart-development-2026-06-19.md | Updated G:\My Drive\Mindshare\05 Role Handoffs\channels\pipeline.md, G:\My Drive\Mindshare\05 Role Handoffs\org-chart-development-2026-06-19.md, G:\My Drive\Mindshare\role\agentic-systems-program-architect\handoffs\org-chart-development-2026-06-19.md, G:\My Drive\Mindshare\vik.md, project foundation run log, and RAG awareness manifest. |  |
| 2026-06-19T15:57:13+00:00 | /role-handoff | Role-Handoff-org-chart-acceptance-review | G:\My Drive\Mindshare\05 Role Handoffs\org-chart-development-2026-06-19.md | Matt accepted and completed Org Chart Architecture Acceptance Review; all six production org-chart routes returned HTTP 200; content gaps require Org Chart Content Correction handoff for authority-domain wording, memory/RAG trigger, MAPS-proprietary legend, and explicit no-auto-agent wording; updated Pipeline channel, org-chart packet, Matt memory, and Vik memory. |  |
| 2026-06-19T15:58:34+00:00 | /role-handoff | Vik-handoff-check | G:\My Drive\Mindshare\05 Role Handoffs\org-chart-development-2026-06-19.md | Updated Pipeline channel, Org Chart Development handoff packet, Vik memory, and Vik role handoff mirrors. No production publish, authority change, role lifecycle change, agent activation, or automation expansion authorized. |  |
| 2026-06-19T15:59:08+00:00 | /role-handoff | Vik-handoff-check | G:\My Drive\Mindshare\vik.md | Updated G:\My Drive\Mindshare\vik.md. No Pipeline or Recruiting state change; Matt remains owner for Org Chart Content Correction response. |  |
| 2026-06-19T15:59:35+00:00 | /role-handoff | Role-Handoff-org-chart-content-correction-intake | G:\My Drive\Mindshare\05 Role Handoffs\org-chart-development-2026-06-19.md | Matt accepted Vik's scoped Org Chart Content Correction handoff for build sequencing; local content implementation is intake-ready for explicit no-auto-agent wording, authority-domain wording, memory/RAG trigger, and MAPS-proprietary legend evidence; production publish, authority changes, lifecycle changes, agent activation, and automation expansion remain gated by Scott approval; updated Pipeline channel, org-chart packet, Matt memory, and Vik memory. |  |
| 2026-06-19T16:01:50+00:00 | /role-handoff | Vik-handoff-check | G:\My Drive\Mindshare\05 Role Handoffs\org-chart-development-2026-06-19.md | Updated Pipeline channel, Org Chart Development handoff packet, Vik memory, Matt memory, Vik handoff mirrors, and maps-runs role-handoff note. Production publish remains gated by Scott approval. |  |
| 2026-06-19T16:02:10+00:00 | /role-handoff | Vik-handoff-check | G:\My Drive\Mindshare\vik.md | Updated G:\My Drive\Mindshare\vik.md after implementing scoped local Org Chart Content Correction and routing review back to Matt. |  |
| 2026-06-19T16:02:54+00:00 | /role-handoff | Role-Handoff-org-chart-content-correction-review | G:\My Drive\Mindshare\05 Role Handoffs\org-chart-development-2026-06-19.md | Matt updated his active handoff-check rule to every 5 minutes when not engaged in active work and to keep routine no-work checks invisible unless there is work to complete. Matt reviewed Vik's local Org Chart Content Correction; local static routes returned HTTP 200 and contained all scoped correction evidence; production routes returned HTTP 200 but still lacked the corrected strings, so publish remains gated by Scott approval and the handoff is ready-for-review rather than complete. Updated Pipeline channel, org-chart handoff packet, Matt memory, and Vik memory. |  |
| 2026-06-19T16:14:48+00:00 | /role-handoff | Vik-handoff-check | G:\My Drive\Mindshare\vik.md | Updated G:\My Drive\Mindshare\vik.md to record restored vik-handoff-check automation on the 5-minute cadence. |  |
| 2026-06-19T16:26:29+00:00 | /role-handoff | Role-Handoff | G:\My Drive\Mindshare\05 Role Handoffs\agent-profile-runtime-integration-2026-06-19.md | Created Agent Profile Runtime Integration design in Obsidian maps-runs; created bounded handoff packet; updated Pipeline channel and Vik memory; routed to Matt for intake. |  |
| 2026-06-19T16:28:37+00:00 | /role | Role-heartbeat-channel-update | G:\My Drive\Mindshare\05 Role Handoffs\channels\heartbeat.md | Created shared Heartbeat channel at G:\My Drive\Mindshare\05 Role Handoffs\channels\heartbeat.md; updated /role instructions and templates so every role always includes Heartbeat in assigned handoff files; updated active role memories and existing 5-minute heartbeat automations for Matt, Vik, and Ana to read Heartbeat. |  |
| 2026-06-19T16:31:03+00:00 | /role-handoff | Role-Handoff-agent-profile-runtime-integration-intake | G:\My Drive\Mindshare\05 Role Handoffs\agent-profile-runtime-integration-2026-06-19.md | Matt accepted Vik's Agent Profile Runtime Integration handoff into Pipeline sequencing; split the integration into five slices; routed Slice 1 (/design-agent and agent profile template contract updates) to Scott for approval before repo skill edits; updated Pipeline, Heartbeat, Matt memory, and Vik memory. |  |
| 2026-06-19T16:35:06+00:00 | /role-handoff | Role-Handoff | G:\My Drive\Mindshare\05 Role Handoffs\mojo-role-migration-vik-matt-2026-06-19.md | Created Mojo Role Migration handoff for Vik and Matt; updated Pipeline and Heartbeat channels; updated Vik memory; paused Agent Profile Runtime Integration Slice 1 pending target Mojo structure confirmation. |  |
| 2026-06-19T16:36:40+00:00 | /role-handoff | Role-Handoff-matt-vik-migration-to-mojo-sequencing | G:\My Drive\Mindshare\05 Role Handoffs\matt-vik-migration-to-mojo-2026-06-19.md | Created Matt's sequencing companion handoff for migrating Matt and Vik from Mindshare parent structure to Mojo DBA company structure; linked Vik's migration packet as canonical architecture source; updated Pipeline and Matt memory; migration remains blocked pending Scott confirmation of canonical Mojo memory root. |  |
| 2026-06-19T16:38:07+00:00 | /role-handoff | Role-Handoff | G:\My Drive\Mindshare\05 Role Handoffs\channels\pipeline.md | Vik heartbeat check recorded Matt sequencing companion packet for Mojo Role Migration; corrected Pipeline channel version to 0.10.0; updated Vik memory. Migration remains blocked on Scott confirming canonical Mojo memory root. |  |
| 2026-06-19T16:50:27+00:00 | /role-handoff | Role-Handoff | G:\My Drive\Mojo\05 Role Handoffs\mojo-role-migration-vik-matt-2026-06-19.md | Migrated Vik and Matt active role artifacts and memory from Mindshare source to Mojo destination at G:\My Drive\Mojo and C:\Users\scott\Code\mojo; updated Mojo AGENTS role hooks; updated Vik heartbeat automation to Mojo paths; Matt heartbeat automation update remains pending due current-thread heartbeat constraint; Mindshare copies remain historical until cleanup approval. |  |
| 2026-06-19T16:51:18+00:00 | /role-handoff | Role-Handoff | G:\My Drive\Mojo\05 Role Handoffs\channels\pipeline.md | Verified Vik and Matt copied from Mindshare to Mojo; Mojo AGENTS, role folders, Obsidian memories, handoff channels, and Vik JSON state verified; Vik heartbeat automation updated to Mojo paths; Matt heartbeat automation remains pending from correct thread/context. |  |
| 2026-06-19T17:04:45+00:00 | /role | Role-memory-move | C:\Users\scott\Code\mindshare\roles\recruiter\memory.md | C:\Users\scott\Code\mindshare\roles\recruiter\memory.md; G:\My Drive\Mindshare\ana.md; G:\My Drive\Mindshare\role\recruiter\state.json; G:\My Drive\Mindshare\maps-runs\role-ana-recruiter.md; G:\My Drive\Mindshare\05 Role Handoffs\channels\recruiting.md; ana-handoff-check automation | Scott asked Ana to move her memory file into the role configuration folder like Matt's local role memory pattern. |
| 2026-06-19T18:17:22+00:00 | /role | Role | C:\Users\scott\Code\mindshare\roles\communications-director\role-agent.md | C:\Users\scott\Code\mindshare\roles\communications-director\role-agent.md; C:\Users\scott\Code\mindshare\roles\communications-director\memory.md; C:\Users\scott\Code\mindshare\roles\communications-director\workflow.md; C:\Users\scott\Code\mindshare\roles\communications-director\loop.md; C:\Users\scott\Code\mindshare\roles\communications-director\heartbeat-automation.md; C:\Users\scott\Code\mindshare\roles\communications-director\state.json; G:\My Drive\Mindshare\channels\communications.md; G:\My Drive\Mindshare\channels\heartbeat.md; G:\My Drive\Mindshare\channels\recruiting.md; G:\My Drive\Mindshare\communications-director.md; G:\My Drive\Mindshare\role\communications-director | Scott asked Ana to create a Communications Director role to ensure roles and agents monitor correct channels, respond appropriately, and stay within boundaries. |
| 2026-06-19T18:22:11+00:00 | /role | Role-taxonomy-memory-update | C:\Users\scott\Code\mindshare\roles\recruiter\memory.md | C:\Users\scott\Code\mindshare\roles\recruiter\memory.md; G:\My Drive\Mindshare\ana.md; G:\My Drive\Mindshare\channels\heartbeat.md | Scott clarified Ana owns this process and should reference the taxonomy appropriately; Matt should update the /role skill to reflect it. |
| 2026-06-19T18:35:22+00:00 | /role | Role Directory | G:\My Drive\Mindshare\roles.md | G:\My Drive\Mindshare\roles.md; C:\Users\scott\Code\mindshare\roles\recruiter\memory.md; G:\My Drive\Mindshare\ana.md; G:\My Drive\Mindshare\channels\heartbeat.md | Directory is a roster only, not an authority grant or channel assignment expansion. |
| 2026-06-19T18:57:50+00:00 | /role | Role | C:\Users\scott\Code\mindshare\roles\release-manager\role-agent.md | C:\Users\scott\Code\mindshare\roles\release-manager\role-agent.md; C:\Users\scott\Code\mindshare\roles\release-manager\memory.md; C:\Users\scott\Code\mindshare\roles\release-manager\workflow.md; C:\Users\scott\Code\mindshare\roles\release-manager\loop.md; G:\My Drive\Mindshare\release-manager.md; G:\My Drive\Mindshare\role\release-manager; G:\My Drive\Mindshare\roles.md; G:\My Drive\Mindshare\channels\heartbeat.md; G:\My Drive\Mindshare\channels\recruiting.md | Created Reid / Release Manager as a Mindshare candidate draft for cross-repository release and branch hygiene. No Git/GitHub write authority, activation, or heartbeat was granted. |
| 2026-06-19T19:08:09+00:00 | /design-agent | A2 | C:\Users\scott\Code\mindshare\agents\ana-recruiter\agent-design.md | Created Ana A2 design proof and backlog in Mindshare beside Ana agent files; updated Ana profile safe design sync fields; validated Mojo website mirror as mirror only. |  |
| 2026-06-19T19:00:32Z | /role | Role activation | C:\Users\scott\Code\mindshare\roles\release-manager\role-agent.md | C:\Users\scott\Code\mindshare\roles\release-manager\memory.md; G:\My Drive\Mindshare\release-manager.md; G:\My Drive\Mindshare\role\release-manager; G:\My Drive\Mindshare\roles.md; G:\My Drive\Mindshare\channels\heartbeat.md; G:\My Drive\Mindshare\channels\recruiting.md; G:\My Drive\Mindshare\channels\communications.md; G:\My Drive\Mindshare\channels\release-management.md; C:\Users\scott\Code\mindshare\roles\recruiter\memory.md; G:\My Drive\Mindshare\ana.md | Activation requested by Scott in Ana channel after Reid channel became available. Reid remains approval-gated for commits, merges, pushes, tags, releases, promotions, branch deletion, force pushes, branch protection/ruleset edits, production actions, authority expansion, and broader repo scans. |
| 2026-06-19T19:17:36+00:00 | /evaluate-agent | A5 | C:\Users\scott\Code\mindshare\agents\ana-recruiter\eval-report.md | Completed Ana specification-mode role-to-agent proof pass for Role As Agent Implementation Confidence Slice 5; eval suite and report confirm Ana is profile/design-ready only, not implemented Agent, with runtime release blocked until Build creates executable loop evidence. |  |
| 2026-06-21T23:17:53+00:00 | /role | Conference Room | rooms/conference-room.md | Created G:\My Drive\Mindshare\conference-room.md; updated project AGENTS.md; added room artifacts under rooms/ and templates/. | Workflow-backed room only; no autonomous runtime, role activation, channel access expansion, external communication, spending, production action, or authority expansion was approved. |
| 2026-06-22T12:23:12-06:00 | /role | Role-Level4-Backlog-Proof | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-proof\2026-06-22-run-001.md | C:\Users\scott\Code\mindshare\roles\recruiter\memory.md; C:\Users\scott\Code\mindshare\roles\recruiter\state.json; C:\Users\scott\Code\mindshare\roles\recruiter\recruiting.backlog.md; G:\My Drive\Mindshare\ana.md; G:\My Drive\Mindshare\recruiting.backlog.md | No office activation, authority grant, external recruiting, Git/GitHub/release, production/website edit, spending, secrets, hooks/global skill changes, Level 5/6 activity, or broad runtime. |
| 2026-06-22T18:46:45+00:00 | /role | Role-skill-update | C:\Users\scott\Code\mindshare\skills\role\SKILL.md | Updated repo-local and installed /role skill rules, role-agent templates, and role-research-sources references for mandatory title-to-role research. |  |
| 2026-06-22T19:32:30+00:00 | /role | Role-skill-update | C:\Users\scott\Code\mindshare\skills\role\SKILL.md | Updated /role Level 1 visibility rule; updated roles.md with 26 non-activated Level 1 packet entries; wrote Liz training handoff; updated Ana memory mirror. |  |
## Evidence Index

| Evidence | Source | What it supports | Confidence |
|---|---|---|---|
| Scott named the project `mindshare` and owner Scott | M0 preflight conversation | Project identity | High |
| Scott described the project as a parent org multi-agent project | M0 preflight conversation | Project type | High |
| Scott said the purpose is to oversee all projects underneath the Mindshare umbrella | M0 preflight conversation | Project intent | High |
| Scott said the primary customer/operator is likely just Scott | M0 preflight conversation | Primary operator | High |
| Scott identified Obsidian at G:\My Drive\Mindshare as notes, memory, and RAG | M0 preflight conversation | Memory/RAG architecture | High |
| Scott clarified future projects should write to a `[project]` folder | M0 preflight conversation | Global default pattern | High |

## Source Inventory

| Source | Type | Location | Owner | RAG ready? | Notes |
|---|---|---|---|---|---|
| M0 preflight conversation | Conversation | Current Codex thread | Scott | Yes | Primary evidence for this foundation. |
| Obsidian vault | Markdown filesystem | G:\My Drive\Mindshare | Scott | Yes | Canonical project store. |
| Project preferences | JSON | .maps/foundation-preferences.json | Scott | Yes for automation | Project-local routing. |
| Global preferences | JSON | C:\Users\scott\.codex\maps\foundation-preferences.json | Scott | Yes for automation | Future project pattern. |
| Env template | Text | .env.example | Scott | No | Placeholder environment variable names only. |
| Local env file | Text | .env.local | Scott | No | Ignored local secrets file; no real values were written by M0. |

## Assumptions

| Assumption | Why it matters | How to test | Status |
|---|---|---|---|
| Obsidian can serve as RAG without a separate index for now | Determines whether additional vector/index setup is needed | Ask retrieval questions against Obsidian-backed memory | Accepted for M0 |
| MAPS-specific writes belong in `maps-runs`; standard project writes belong in the project folder | Determines phase-output routing | Run the next MAPS skill and inspect output placement | Accepted after M1 correction |
| Source material does not need a dedicated folder yet | Avoids imposing structure Scott has not chosen | Revisit when source volume becomes painful | Open |
| Future projects should use G:\My Drive\Mindshare\[project] | Establishes global default pattern | Start the next project foundation and confirm route | Accepted for M0 |

## Decisions

| Decision | Rationale | Date | Owner |
|---|---|---|---|
| Use Obsidian at G:\My Drive\Mindshare as canonical for `mindshare` | Scott already treats Obsidian as notes, memory, and RAG | 2026-06-19 | Scott |
| Use `maps-runs` for MAPS-specific writes | Scott clarified that standard project writes go to the project folder and MAPS-specific writes go to `maps-runs` | 2026-06-19 | Scott |
| Do not create separate `notes`, `sources`, or `memory` folders for `mindshare` | Scott wants everything in the top-level project folder | 2026-06-19 | Scott |
| Use G:\My Drive\Mindshare\[project] for future projects | Keeps child projects separated under the Mindshare umbrella | 2026-06-19 | Scott |
| Promote this layout to global defaults | Scott explicitly approved reuse for future `/foundation` runs | 2026-06-19 | Scott |
| Create `.env.local` | Scott confirmed a local ignored secrets file should exist | 2026-06-19 | Scott |

## Open Questions

- Should the Foundation skill be updated so it asks concrete location questions instead of asking whether to use defaults?
- Which generated artifacts or templates still need routing review after the `maps-runs` correction?
- When source material becomes important, should it get its own Obsidian convention or remain ordinary linked notes?
- Should a separate vector index eventually be created from Obsidian, or is Obsidian-native retrieval enough?
- What child projects currently belong under the Mindshare umbrella?
- Should `origin` be changed from `https://github.com/AesopScott/maps.git` to a dedicated Mindshare remote?
- Which environment variables will `mindshare` actually need beyond the placeholder template?

## RAG Readiness

- Source types to index: Obsidian Markdown notes, MAPS phase outputs under `maps-runs`, project-context.md, glossary.md, entity-map.md, and later source notes when defined.
- Required metadata: project name, skill slug, phase, owner, date, source/evidence links, canonical path.
- Privacy or access limits: do not write secrets, raw private data, or uncited dumps into shared retrieval notes.
- Citation requirements: phase outputs should link back to source notes or name the conversation/source that supports claims.
- Freshness rules: update memory when durable facts change; treat `.maps/rag-updates.json` as a reindex/awareness manifest.
- Exclusions: temporary scratch notes, noisy logs, unrelated project material, and separate stale indexes without provenance.

## Next Path

- Scope First: Useful if the next step is cataloging all Mindshare child projects and deciding what the parent org must coordinate.
- Single-Agent / APS: Too narrow for the stated parent-org oversight purpose.
- Multi-Agent / MAPS: Best fit because the umbrella may require distinct project intake, memory maintenance, planning, evaluation, deployment, observation, and improvement responsibilities.
- Recommendation: Multi-Agent / MAPS, with an M1 Scope/Shape pass next to identify child projects, workflows, roles, memory boundaries, and coordination needs.

## M1 Handoff Questions

- What projects currently live under the Mindshare umbrella?
- What does "oversee" mean operationally: planning, status, memory, review, resource allocation, execution, or all of these?
- Which project events should the parent org remember?
- Which child-project artifacts should roll up into Mindshare memory?
- Which roles need separate tools, permissions, or memory?
- What source material already exists outside Obsidian and should be imported?
- What can run in parallel across child projects?
- What failure modes would require escalation to Scott?
