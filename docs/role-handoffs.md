# Role Handoffs

## Purpose

Role handoffs are the durable communication system between Mindshare roles. Commonly communicating roles use shared Markdown channel files to read and write ongoing context. Bounded work becomes a linked handoff packet when it needs status, ownership, evidence, verification, or closeout.

## Architecture Decision

Mindshare uses a shared role communication lane:

- Canonical visible queue: `G:\My Drive\Mindshare\05 Role Handoffs`
- Obsidian queue page: `G:\My Drive\Mindshare\05 Role Handoffs\05 Role Handoffs.md`
- Function channel folder: `G:\My Drive\Mindshare\05 Role Handoffs\channels`
- Role-local source mirror: `roles/<role-slug>/handoffs`
- Obsidian role mirror: `G:\My Drive\Mindshare\role\<role-slug>\handoffs`
- MAPS run memory: `G:\My Drive\Mindshare\maps-runs`

The visible queue is for role communication, intake, status, retrieval, and cross-role coordination. Channel files are named by function, not by the current role pair. Handoff packets hold bounded work items spawned from those function channels. Role-local folders keep handoff packets close to the owning role contract.

## Ownership Model

The sending role owns the clarity of the message: context, request, evidence, authority boundary, expected response, and next owner.

The receiving role owns the response: accept, ask one clarifying question, redirect, escalate, act, review, or close.

Scott remains the approval authority for publication, production changes, authority expansion, autonomous operation, external communication, spending, global installs, and destructive changes.

Matt owns program/build handoff intake when a packet is specifically ready for execution sequencing, build coordination, blocker tracking, verification routing, and closeout.

## Function Channel Files

Functions where roles commonly communicate should have a shared Markdown channel file under `G:\My Drive\Mindshare\05 Role Handoffs\channels`.

Channel files are append-oriented. Each role reads the relevant function channel before acting on shared work and appends meaningful updates after decisions, blockers, handoffs, reviews, or closeouts.

## 5-Minute Handoff Check Goal

Every active role and agent should have a standing goal to check its assigned handoff files for work every 5 minutes while it is operating and not engaged in active work.

Rules:

- Always include `G:\My Drive\Mindshare\05 Role Handoffs\channels\heartbeat.md` as an assigned handoff file for every role.
- Read the relevant function channel and linked active packets.
- Look for new requests, assigned work, blockers, review needs, decisions, escalations, and closeout tasks.
- If work exists, acknowledge it, act inside authority, ask one blocker question, or route it to the correct function channel.
- Append when work is found, status changes, evidence changes, a blocker appears, or a closeout happens.
- Routine no-work checks do not need noisy log entries unless a channel explicitly requires them.
- This goal does not activate autonomous polling, production actions, external communication, spending, or authority expansion without an approved runtime and explicit permission.

Active and planned channels:

| Function | Channel | Participants | Purpose | Status |
| --- | --- | --- | --- | --- |
| Heartbeat | `channels/heartbeat.md` | All roles | Shared liveness, cadence, blockers, cross-role awareness, and operating-state changes. | Active |
| Pipeline | `channels/pipeline.md` | Vik, Matt | Pipeline coordination, phase movement, build sequencing, blockers, verification routing, and closeout. | Active |
| Recruiting | `channels/recruiting.md` | Vik, Matt, Ana | Recruiting, defining, hiring/building, onboarding, and maturing roles. | Active |
| Training | `channels/training.md` | Liz | MAPS education, curriculum, training operations, and learner feedback. | Planned |

Use `role-channel-template.md` for new function channels.

## Statuses

| Status | Meaning | Owner |
| --- | --- | --- |
| `drafting` | Architecture is still being shaped. | Scott and Vik |
| `ready-for-receiver` | Packet or channel request is complete enough for the receiving role to respond. | Sending role |
| `accepted` | Receiving role has accepted ownership or redirected the packet. | Receiving role |
| `in-progress` | Receiving role is acting, reviewing, deciding, escalating, or drafting a response. | Receiving role |
| `blocked` | Work cannot proceed without a decision, access, source, or approval. | Matt |
| `ready-for-review` | Build output exists and needs acceptance review. | Builder and Matt |
| `complete` | Acceptance criteria, verification, and memory updates are done. | Matt |
| `archived` | Closed and no longer active. | Matt |

## Process

1. Every 5 minutes while operating and not engaged in active work, the role checks assigned handoff files, always including `channels/heartbeat.md`, plus relevant function channels and linked packets.
2. A role reads the shared channel file before acting on shared work.
3. The sending role appends context, request, evidence, authority boundary, and expected response.
4. If the work is bounded, risky, multi-step, or reviewable, the sending role creates a handoff packet and links it from the channel.
5. The receiving role appends acceptance, one clarifying question, redirect, escalation, or blocker.
6. The receiving role acts inside its authority, reviews, decides, drafts, escalates, or hands work onward.
7. The receiving role records changed artifacts, decisions, evidence, verification, and memory updates in the channel or packet.
8. The packet closes when the receiving condition is met, or continues through another channel or packet.

## Handoff Packet Requirements

Every role handoff must include:

- Clear sender role and receiving role.
- Handoff type.
- Shared function channel file.
- Current status.
- Context and problem statement.
- Request, message, or decision needed.
- Scope and non-goals.
- Authority gates and approvals required.
- Source files, target files, routes, or artifacts.
- Acceptance criteria.
- Verification plan.
- Memory update plan.
- Open questions, with no more than one active blocker question at a time.

## Guardrails

- A handoff is not approval to publish, deploy, spend, communicate externally, expand authority, or activate autonomy.
- A role's maturity does not grant authority.
- A handoff packet may create build work, but it does not create an agent runtime.
- Matt may coordinate execution, but Vik remains architecture owner for control-plane decisions.
- If the handoff changes authority, production behavior, global installation, external communication, or autonomous loops, stop for Scott approval.

## Active Handoffs

| Handoff | Senders | Receivers | Status | Canonical role-local path | Visible queue path |
| --- | --- | --- | --- | --- | --- |
| Org Chart Development | Vik, Matt | Vik, Matt | `drafting` | `roles/vik-aspa/handoffs/org-chart-development-2026-06-19.md` | `G:\My Drive\Mindshare\05 Role Handoffs\org-chart-development-2026-06-19.md` |
| Recruiting Handoff | Vik, Matt, Ana | Vik, Matt, Ana | `active` | `G:\My Drive\Mindshare\05 Role Handoffs\channels\recruiting.md` | `G:\My Drive\Mindshare\05 Role Handoffs\channels\recruiting.md` |

## Handoffs By Function

| Function | Channel | Active handoffs | Senders | Receivers | Status |
| --- | --- | --- | --- | --- | --- |
| Heartbeat | `channels/heartbeat.md` | Heartbeat Channel | All roles | All roles | `active` |
| Pipeline | `channels/pipeline.md` | Org Chart Development | Vik, Matt | Vik, Matt | `drafting` |
| Recruiting | `channels/recruiting.md` | Recruiting Handoff | Vik, Matt, Ana | Vik, Matt, Ana | `active` |
| Training | `channels/training.md` | None yet | Liz | Liz | `planned` |

## Obsidian Queue Files

- Queue page: `G:\My Drive\Mindshare\05 Role Handoffs\05 Role Handoffs.md`
- Filesystem README: `G:\My Drive\Mindshare\05 Role Handoffs\README.md`
- Function channel folder: `G:\My Drive\Mindshare\05 Role Handoffs\channels`
- Channel template: `G:\My Drive\Mindshare\05 Role Handoffs\role-channel-template.md`
- Packet template: `G:\My Drive\Mindshare\05 Role Handoffs\role-handoff-template.md`

## Version And Changelog

Version: 0.6.0

| Date | Version | Change |
| --- | --- | --- |
| 2026-06-19 | 0.1.0 | Created shared role-handoff process so Vik can architect and Matt can build from explicit packets. |
| 2026-06-19 | 0.2.0 | Reframed role handoffs as durable Markdown communication channels between commonly communicating roles, with bounded handoff packets linked from channels. |
| 2026-06-19 | 0.3.0 | Renamed channels by communication function, making Pipeline the first active channel instead of a Vik-Matt role-pair channel. |
| 2026-06-19 | 0.4.0 | Added the standing 3-minute handoff check goal for active roles and agents. |
| 2026-06-19 | 0.5.0 | Added Recruiting as the second active function channel and changed sender/receiver tables to names only. |
| 2026-06-19 | 0.6.0 | Added Heartbeat as the mandatory shared channel for all roles and aligned routine checks to the 5-minute heartbeat cadence. |
