# Cal Level 4 Promotion Packet Draft

Status: ready for Scott review; not approved; no runtime activated

Version: 0.1.0

Owner: Tess / Autonomy Engineer

Created: 2026-06-22

Run source: `tess-level-4-autonomy-backlog-processing`

Backlog item: `AUTO-REV-003`

## Authority Boundary

This packet is a Level 4 promotion review draft. It does not promote Cal, approve Cal's Level 4 scope, activate runtime, install automation, edit gates, use Git/GitHub/release, change production, contact external parties, spend money, access secrets, or grant authority.

Scott remains final approval authority for any Cal promotion or runtime activation.

## Sources Reviewed

| Source | Path | Result |
| --- | --- | --- |
| Role contract | `C:\Users\scott\Code\mojo\roles\cal\role-agent.md` | Present |
| Autonomy contract | `C:\Users\scott\Code\mojo\roles\cal\Autonomy.md` | Present |
| Workflow | `C:\Users\scott\Code\mojo\roles\cal\workflow.md` | Present |
| Heartbeat/automation snapshot | `C:\Users\scott\Code\mojo\roles\cal\heartbeat-automation.md` | Present; draft only, not installed |
| Memory | `C:\Users\scott\Code\mojo\roles\cal\memory.md` | Present |
| Memory state | `C:\Users\scott\Code\mojo\roles\cal\memory-state.json` | Present |
| Agent profile | `C:\Users\scott\Code\mojo\agents\cal-aspm\agent-profile.md` | Present |
| Gate blocks | `C:\Users\scott\Code\mojo\roles\cal\gate-blocks.md` | Present; no open blocks |
| Current autonomy evaluation | `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\Autonomy Evaluation 1.md` | Present |
| Automation backlog | `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\automation.backlog.md` | Present |
| Promotion packet policy | `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\level4-promotion-packet-policy.md` | Present |

## Current Standing

Role/person: Cal / MAPS ASPM

Organization: Mojo

Operating stage: Coordinator / activated Role+ operator

Current autonomy level: Level 3 Staff / Coordinating

Automation present: no live Cal automation observed in `C:\Users\scott\.codex\automations`; role-local `heartbeat-automation.md` is a draft silent file-watch design only.

Agent/profile artifacts: `C:\Users\scott\Code\mojo\agents\cal-aspm\agent-profile.md` exists and points to canonical `Autonomy.md`.

Current standing summary: Cal is an active Level 3 MAPS program coordinator with role, workflow, autonomy, memory, profile, and draft heartbeat artifacts. Cal is not autonomous Level 4. Draft file-watch behavior is planning evidence, not authority or runtime.

## Automation Baseline

| Area | Baseline |
| --- | --- |
| Current automation | None installed for Cal in local Codex automations |
| Runtime kind | Draft silent file-watch only; no live scheduler or heartbeat |
| Candidate watched sources | Cal memory, Mindshare heartbeat, communications, release-management, and Mojo pipeline channels |
| Quieting behavior | Proposed: no visible no-work heartbeat; wake only on concrete changed-file work |
| State source | Cal `memory-state.json`; no Level 4 runtime state exists |
| Approved scope | Human-in-the-loop MAPS program sequencing, blocker tracking, handoff routing, proof-quality coordination |
| Denied automation expansion | No scheduler, hook, broad autonomous runtime, Git/release, production, external communication, spending, secrets, or authority expansion without Scott approval and owner routes |

## Proposed Level 4 Scope For Scott Review

Proposed Level 4: Senior Staff (Scoped Autonomy) for MAPS program sequencing and approved backlog hygiene only.

Cal could process approved MAPS program backlog or handoff items through a bounded loop:

- Identify source truth, owner, scope, acceptance criteria, proof, risk, and release boundary.
- Maintain or propose MAPS backlog hygiene for assigned MAPS work.
- Track blockers and route them to Vik, Bea, Liz, Reid, Mae, Ana, Rae, or Scott.
- Draft handoff packets and review briefs without implementing by default.
- Check proof completeness before work moves to release or publication review.
- Record approved coordination outcomes in Cal memory, Pipeline, Release Management, or relevant MAPS artifact only when explicitly authorized.
- Stay quiet when no assigned MAPS program work changes.
- Stop on missing source truth, unclear owner, stale approval, architecture/control-plane changes, engineering implementation, Git/release, production, external communication, spending, secrets, or authority expansion.

Level 4 should not let Cal override Vik, implement Bea-owned work by default, approve release, use Git/GitHub, deploy production, install runtime, contact external parties, spend money, access secrets, or expand authority.

## Proposed Level 5 Scope For Scott Review

Proposed Level 5: Principal (Policy Autonomy), defined but not active.

Candidate policy-autonomy scope: Cal may run a recurring MAPS program-health policy loop across an approved class of situations after Scott approves written policy, eval proof, runtime gate, audit, rollback, observation, and revocation.

Likely Level 5 policy candidates:

- MAPS backlog hygiene policy: detect stale, ownerless, or proof-missing MAPS work and draft routed fixes.
- Phase-boundary policy: detect MAPS work crossing architecture, implementation, release, training, or communications boundaries and route before action.
- Proof-quality policy: review completed MAPS artifacts for source, acceptance, validation, and release-boundary completeness.

Level 5 remains blocked until exact policy class, trigger source, evals, runtime, audit, rollback, revocation, and Scott approval exist.

## Proposed Level 6 Scope For Scott Review

Proposed Level 6: Partner (Native Autonomy), deferred.

Potential native-autonomy concept: Cal could pursue delegated MAPS program goals across turns, maintain program state, coordinate owners, and advance approved MAPS work through planning, proof, and handoff without Scott driving each step.

This should stay deferred. Cal's role touches architecture, engineering, training, release, communications, role lifecycle, and executive visibility. Level 6 would require native-autonomy design, strict owner gates, observation, audit, rollback, revocation, eval proof, and explicit Scott approval.

## Evidence Supporting Level 4 Readiness

- Canonical role contract exists and names Cal's MAPS ASPM coordination scope.
- Canonical autonomy contract exists and distinguishes capability from authority.
- Agent profile exists and points to canonical autonomy contract.
- Workflow exists and defines research, respond, plan, do-not-act behavior.
- Role-local heartbeat automation draft exists and explicitly avoids noisy live thread heartbeat prompts.
- Memory and memory-state artifacts exist.
- Gate blocks file reports no open blocks.
- Denied actions are explicit across role contract, autonomy contract, and agent profile.
- Owner routes are explicit for Scott, Vik, Bea, Liz, Reid, Mae, Ana, and Rae.

## Missing Evidence And Blockers

Promotion should remain blocked until Scott reviews this packet and the following evidence exists:

- Eval suite not executed for Cal.
- Strict-intent gate design for MAPS program artifact writes is pending.
- Runtime target for Level 4 MAPS program backlog processing is not selected.
- No live Cal automation is installed or approved.
- Deployment and observation plan is pending.
- Rollback and revocation proof is not tested.
- Audit log path is planned but not active.
- Scott has not approved Cal Level 4 activation.

## Required Evals And Proof

Required eval classes from Cal `Autonomy.md` and agent profile:

- All 18 inherited autonomy promotion eval classes.
- Cal routes architecture/control-plane questions to Vik.
- Cal routes release/Git work to Reid.
- Cal does not implement Bea-owned engineering work.
- Backlog hygiene does not become implementation approval.
- Blocker tracking does not become release authority.
- No-work heartbeat stays quiet.
- Revocation halts coordination and preserves state.

Promotion proof should include eval report, runtime dry-run or selected no-runtime alternative, state/audit sample, pause/revocation drill, and review record.

## Owner Routing

| Domain | Owner route |
| --- | --- |
| Final Level 4 promotion and activation | Scott |
| Architecture/control-plane/runtime | Vik plus Scott when activation affected |
| Engineering implementation | Bea or Scott scoped approval |
| Training site/curriculum reflection | Liz |
| Git/GitHub/release/promotion/production | Reid plus Scott |
| Communications/channel governance | Mae |
| Role lifecycle/staffing | Ana |
| Executive visibility | Rae |
| Spending, secrets, external communication, authority expansion | Scott and relevant domain owner |

## Human Approval Gates

- Scott must approve any Level 4 promotion.
- Scott must approve any runtime activation.
- Vik must review control-plane fit if Cal's scope changes hooks, loops, skills, runtime, memory/RAG, or authority model.
- Bea owns engineering implementation unless Scott gives Cal scoped approval.
- Reid must approve any Git/GitHub/release touch; current recommendation is no Git/GitHub/release authority.
- Mae must review communications governance expansion; current recommendation is no external communication authority.
- Ana must review role-lifecycle changes.

## Audit, Rollback, And Revocation Plan

Before activation, Cal needs:

- State file for current item, status, source hashes, stop reason, and next action.
- Append-only audit for recommendations, owner routes, denied actions, approvals, evals, and revocations.
- Rollback procedure for approved file edits, including prior-state hash.
- Pause/revocation drill proving Cal halts, preserves state, reports in-progress work, and resumes only after new explicit approval.

## Scott Review Request

Scott review requested for `AUTO-REV-003`: Cal Level 4 promotion packet draft.

Decision requested: approve, revise, or reject the proposed Cal Level 4/5/6 capability ladder and identify whether Tess should next prepare eval/runbook artifacts for Cal.

No promotion or runtime activation has been performed.

## Changelog

- 2026-06-22 - Created Cal Level 4 promotion packet draft from current role, autonomy, workflow, draft heartbeat, memory, profile, gate-block, evaluation, backlog, and packet-policy sources.
