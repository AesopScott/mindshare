# Org Chart Development Handoff To Vik

## Owner

Vik / Agentic Systems Program Architect.

## Date

2026-06-19.

## Status

Active architecture handoff. Implementation should continue only after confirming the current state of the Mojo MAPS website repo and Scott's desired publication timing.

Role handoff status: `local-implemented`. The Role Handoffs page subtask is closed as published and verified. Matt completed the architecture acceptance review, Vik scoped Org Chart Content Correction, Matt accepted it for build sequencing, and Vik implemented the scoped local content corrections. Do not publish or change authority/activation behavior from this handoff without the authority gates below.

## Shared Channel

`G:\My Drive\Mindshare\05 Role Handoffs\channels\pipeline.md`

## Senders

Vik, Matt.

## Receivers

Vik, Matt.

## Context

Scott is evolving the MAPS website and Mindshare operating model so the org chart is not just a static page. It should become the visible architecture for a role-agent corporation: a set of roles that can eventually become advisors, workflow owners, skills, hooks, loops, active processes, or full agents.

The visible website work belongs in the Mojo/MAPS teaching site. The durable role-agent operating model belongs in the Mindshare project.

Known target routes from prior direction:

- `/maps/org-chart/`
- `/maps/org-chart/roles-versus-agents/`
- `/maps/org-chart/role-maturity/`
- `/maps/org-chart/authority-taxonomy/`
- `/maps/org-chart/operating-cadence/`

## Architectural Decision

The org chart should be owned architecturally by Vik because it defines:

- the difference between a role and an agent
- role maturity
- authority levels and declarations
- operating cadence
- trigger and activation rules
- the shape of future Mindshare role agents

Matt / ASPM should support execution tracking and phase handoffs, but Vik owns the control-plane architecture.

## Current Desired Changes

1. Navigation
   - Use an `Org Chart` dropdown.
   - The dropdown should contain human-readable labels, not public O-number nomenclature.
   - Use:
     - `MAPS Org Chart`
     - `Roles versus Agents`
     - `Role Maturity`
     - `Authority Taxonomy`
     - `Operating Cadence`

2. Roles versus Agents
   - Explain that a role is an organizational responsibility/voice/authority contract.
   - Explain that an agent is an implemented runtime with goal, state, tools, memory, policy, evals, handoffs, escalation, and stop conditions.
   - State clearly that creating a role contract does not automatically create or authorize an agent.

3. Role Maturity
   - Use the professional maturity taxonomy from `/role`:
     - L0 Candidate
     - L1 Trainee
     - L2 Associate
     - L3 Practitioner
     - L4 Senior Practitioner
     - L5 Lead
     - L6 Principal
     - L7 Director
     - L8 Executive
     - L9 Officer
   - Make clear that maturity is separate from authority.
   - Tie org chart colors to status:
     - Red: role does not exist.
     - Blue: role exists but is not mature.
     - Green: role exists and is mature.
   - Preserve the MAPS proprietary role legend.

4. Authority Taxonomy
   - Use the authority taxonomy from `/role`.
   - Include authority levels A0 through A12.
   - Include authority domains:
     - advice and critique
     - artifact creation
     - workflow ownership
     - tool use
     - memory and RAG writes
     - source, evidence, and data handling
     - external communication
     - spending, procurement, or commitments
     - policy, governance, compliance, or risk
     - people, roles, staffing, or performance
     - deployment, production, infrastructure, or runtime operations
     - escalation, approval, veto, or incident response
   - Include a literal checklist of possible role capabilities.
   - Include special declarations such as:
     - `read-only`
     - `recommend-only`
     - `draft-only`
     - `human-approval-required`
     - `role-approval-required`
     - `two-key-approval`
     - `policy-bound`
     - `budget-bound`
     - `time-bound`
     - `scope-bound`
     - `memory-read`
     - `memory-write`
     - `memory-propose`
     - `external-communication`
     - `no-external-communication`
     - `tool-use`
     - `no-tool-use`
     - `production-access`
     - `no-production-access`
     - `veto-right`
     - `escalation-right`
     - `emergency-break-glass`
     - `self-improvement-propose`
     - `self-improvement-write`
     - `revocable`

5. Operating Cadence
   - Explain how roles are triggered.
   - Explain how agents operate.
   - Include trigger types:
     - explicit invocation
     - session start
     - phase boundary
     - review gate
     - event or signal
     - scheduled cadence
     - incident or escalation
     - memory/RAG update
   - Include a visible agent loop:
     - intake
     - plan
     - act
     - record
     - report
     - stop or continue

## Roles To Represent

The org chart should support Mindshare's first operational role agents:

- Vik / Agentic Systems Program Architect: architecture and control plane.
- Matt / Agentic Systems Program Manager: cadence, phase routing, and handoffs.
- Ana / Recruiter: upcoming owner of `/role`, responsible for hiring/building future roles.
- Liz / Mojo MAPS Training Coordinator: upcoming training coordinator for MAPS education.

Ana and Liz are planned but should not be represented as fully built until their role artifacts exist.

## Acceptance Criteria

- The org chart dropdown uses the final labels above.
- The site avoids public O-number nomenclature unless Scott asks to restore it.
- The org chart pages explain role-agent architecture, not only company hierarchy.
- The authority page contains a real checklist broad enough to cover what a role could do.
- The operating cadence page explains triggers and agent operating loops.
- The org chart distinguishes:
  - roles that do not exist
  - roles that exist but are immature
  - roles that exist and are mature
  - MAPS-proprietary roles
- The page content aligns with the installed `/role` authority and maturity model.
- Any production publish is explicitly approved by Scott and verified after deploy.

## Risks

- Overloading the public website with internal implementation detail.
- Confusing MAPS teaching pages with Mindshare operational source of truth.
- Treating role maturity as authority.
- Treating org-chart presence as role activation.
- Letting Ana, Liz, Matt, or Vik overlap without clear boundaries.

## Recommended Next Step

Vik should inspect the current Mojo MAPS website repo state, compare it with this handoff, and produce a small implementation plan before more page edits. If Scott wants immediate implementation, Vik should coordinate with Matt for publish sequencing and with Ana once `/role` ownership is created.

## Next Scoped Subtask

Subtask: Org Chart Architecture Acceptance Review.

Status: `complete`.

Sender: Vik.

Receiver: Matt.

Shared channel: `G:\My Drive\Mindshare\05 Role Handoffs\channels\pipeline.md`.

Purpose: confirm which remaining org-chart architecture items are already satisfied on the website and which need a new bounded build handoff.

Scope:

- Review production routes:
  - `https://mojoaistudio.com/maps/org-chart/`
  - `https://mojoaistudio.com/maps/org-chart/roles-versus-agents/`
  - `https://mojoaistudio.com/maps/org-chart/role-maturity/`
  - `https://mojoaistudio.com/maps/org-chart/authority-taxonomy/`
  - `https://mojoaistudio.com/maps/org-chart/operating-cadence/`
  - `https://mojoaistudio.com/maps/org-chart/role-handoffs/`
- Compare the routes against the acceptance criteria in this packet.
- Decide whether the next build handoff is content correction, navigation correction, status/legend correction, or closeout.

Non-goals:

- Do not publish new website changes from this review alone.
- Do not change role authority, role lifecycle status, or agent activation.
- Do not expand autonomous behavior.

Authority gates:

- Production publish requires Scott approval unless Scott directly asks for the publish.
- Role authority, activation, automation, external communication, or deployment behavior changes require Scott approval.
- Matt may accept, redirect, or request one blocker clarification; Matt does not override Vik's architecture ownership.

Verification:

- HTTP 200 for each route reviewed.
- Page content checked for the acceptance criteria in this packet.
- Any missing item becomes a new bounded handoff with owner, scope, authority gates, verification, and memory update plan.

Memory updates:

- Update this packet.
- Update `G:\My Drive\Mindshare\05 Role Handoffs\channels\pipeline.md`.
- Update `G:\My Drive\Mindshare\vik.md` for durable Vik decisions.
- Run the shared MAPS memory helper after durable changes.

Requested response from Matt: completed 2026-06-19 09:56; next handoff should be content correction, not closeout.

Review result:

- All six production routes returned HTTP 200.
- The org-chart navigation labels were present across reviewed routes.
- Public O-number nomenclature was not detected.
- The next handoff should be content correction because several acceptance criteria are not fully satisfied.

Missing or weak acceptance evidence:

- Authority Taxonomy page: missing required authority-domain wording for `tool use`, `spending`, `procurement`, and `deployment`.
- Operating Cadence page: missing the trigger type `memory/RAG update`.
- MAPS Org Chart page: status colors were present, but MAPS-proprietary role legend evidence was not found.
- Roles versus Agents page: role/agent distinction exists, but explicit wording that creating a role contract does not automatically create or authorize an agent should be strengthened.

## Progress Updates

### 2026-06-19 - Matt completed architecture acceptance review

Matt completed the Org Chart Architecture Acceptance Review. Production routes checked:

- `https://mojoaistudio.com/maps/org-chart/`
- `https://mojoaistudio.com/maps/org-chart/roles-versus-agents/`
- `https://mojoaistudio.com/maps/org-chart/role-maturity/`
- `https://mojoaistudio.com/maps/org-chart/authority-taxonomy/`
- `https://mojoaistudio.com/maps/org-chart/operating-cadence/`
- `https://mojoaistudio.com/maps/org-chart/role-handoffs/`

All returned HTTP 200. The review did not support closeout because content gaps remain. Next bounded handoff should be `Org Chart Content Correction`.

## Next Scoped Subtask

Subtask: Org Chart Content Correction.

Status: `local-implemented`.

Owner: Vik.

Receiver: Matt.

Purpose: correct production org-chart content so the pages satisfy the acceptance criteria in this packet.

Scope:

- Add or strengthen explicit wording that creating a role contract does not automatically create or authorize an agent.
- Add missing authority-domain wording for `tool use`, `spending`, `procurement`, and `deployment`.
- Add `memory/RAG update` as an Operating Cadence trigger type.
- Restore or make visible the MAPS-proprietary role legend on the org-chart surface.

Non-goals:

- Do not publish from this review alone.
- Do not change role authority, role lifecycle status, agent activation, or automation behavior.
- Do not add new website routes unless Vik scopes that separately.

Authority gates:

- Production publish requires Scott approval unless Scott directly asks for the publish.
- Role authority, activation, automation, external communication, or deployment behavior changes require Scott approval.
- Vik owns architecture; Matt owns sequencing and intake readiness.

Requested response from Matt: accept the scoped correction, redirect it, or ask one blocker question before build intake.

Matt response: accepted 2026-06-19 09:58. The handoff is intake-ready for scoped local content correction. This acceptance does not authorize production publish, role authority changes, role lifecycle changes, agent activation, or automation expansion.

Implementation response from Vik: completed local implementation 2026-06-19 10:00. The correction is ready for Matt review and publish approval routing before any production deploy.

Verification:

- HTTP 200 for edited routes after implementation.
- Page content includes the missing authority-domain wording.
- Operating Cadence includes `memory/RAG update`.
- Org chart includes MAPS-proprietary role legend evidence.
- Roles versus Agents explicitly says role contracts do not automatically create or authorize agents.

Memory updates:

- Update this packet.
- Update `G:\My Drive\Mindshare\05 Role Handoffs\channels\pipeline.md`.
- Update `G:\My Drive\Mindshare\vik.md`.
- Update `G:\My Drive\Mindshare\matt.md` if Matt sequencing changes.

### 2026-06-19 - Vik scoped Org Chart Content Correction

Vik promoted the content-correction candidate to the next scoped subtask and routed it to Matt for sequencing/intake readiness. The scoped correction is limited to missing page content from Matt's acceptance review: explicit no-auto-agent wording, authority-domain wording for `tool use`, `spending`, `procurement`, and `deployment`, the `memory/RAG update` trigger, and visible MAPS-proprietary role legend evidence.

No production publish, role authority change, role lifecycle change, agent activation, or automation expansion is authorized by this routing.

### 2026-06-19 - Matt accepted Org Chart Content Correction

Matt accepted the scoped content-correction handoff for build sequencing. The next work is local implementation of the four bounded content corrections, followed by review and explicit publish approval before any production deploy.

### 2026-06-19 - Vik implemented local content corrections

Vik implemented the four scoped local content corrections in the Mojo repo:

- Strengthened Roles versus Agents wording so role contracts do not automatically create or authorize agents.
- Added authority-domain wording for `tool use`, `spending`, `procurement`, and `deployment`.
- Added `memory/RAG update` as an Operating Cadence trigger type.
- Added visible MAPS-proprietary role legend evidence to the org-chart legend.

Local verification:

- `http://127.0.0.1:8765/maps/org-chart/` returned HTTP 200 and included `MAPS-proprietary roles`.
- `http://127.0.0.1:8765/maps/org-chart/roles-versus-agents/` returned HTTP 200 and included `does not automatically create or authorize an agent`.
- `http://127.0.0.1:8765/maps/org-chart/authority-taxonomy/` returned HTTP 200 and included `tool use`, `spending`, `procurement`, and `deployment`.
- `http://127.0.0.1:8765/maps/org-chart/operating-cadence/` returned HTTP 200 and included `Memory/RAG update`.

Production publish remains gated by Scott approval.

### 2026-06-19 - Role Handoffs page published

Scott asked Vik to publish the Role Handoffs page to the website using git. Vik committed and pushed `060e204` (`Update role handoffs page`) to `origin/main` in the Mojo repo.

Verification: local static route `/maps/org-chart/role-handoffs/` returned HTTP 200; production `https://mojoaistudio.com/maps/org-chart/role-handoffs/` returned HTTP 200 and included `channels/recruiting.md`, `Vik, Matt`, and `Vik, Matt, Ana`. The old `channels/vik-matt.md` text was absent.

Publication status: published and verified for the Role Handoffs page. The broader org-chart architecture handoff remains `drafting` until Vik and Matt decide whether additional org-chart work remains in this packet.

### 2026-06-19 - Matt accepted architecture acceptance review

Matt accepted the Org Chart Architecture Acceptance Review subtask. The review will check production HTTP status and compare the org-chart routes against the acceptance criteria in this packet. No publish, authority change, role activation, or automation expansion is authorized by this acceptance.

### 2026-06-19 - Matt closeout decision for Role Handoffs subtask

Matt closed the Role Handoffs page subtask as published and verified. The broader org-chart architecture packet remains open in `drafting` for remaining work on roles versus agents, role maturity, authority taxonomy, and operating cadence. Vik should scope the next bounded org-chart subtask before routing it to Matt build intake.

### 2026-06-19 - Handoff channel correction

Scott clarified that Pipeline is one function channel inside the broader Handoffs system. Pipeline senders and receivers are Vik and Matt, and both names should be listed without role titles in handoff tables.

### 2026-06-19 - Local role handoffs website draft

Scott asked to make the new Role Handoffs process visible on the org chart website before continuing deeper org-chart architecture. Vik bridged the missing website-builder role and added a local draft route at `/maps/org-chart/role-handoffs/` in the Mojo repo. The Org Chart dropdown now includes `Role Handoffs`, and the main org chart links to the new page.

Verification: local static server returned HTTP 200 for `/maps/org-chart/role-handoffs/`; Playwright checked desktop and mobile viewports for title, dropdown link, handoff-process heading, packet-requirements heading, and no horizontal overflow.

Publication status: superseded by the 2026-06-19 Role Handoffs page published update above.

## Memory Updates

This handoff should be recorded in:

- `roles/agentic-systems-program-architect/handoffs/org-chart-development-2026-06-19.md`
- `G:\My Drive\Mindshare\role\agentic-systems-program-architect\handoffs\org-chart-development-2026-06-19.md`
- `G:\My Drive\Mindshare\maps-runs\role-vik-aspa.md`
