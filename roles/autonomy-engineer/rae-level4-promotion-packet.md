# Rae Level 4 Promotion Packet Draft

Status: ready for Scott review; not approved; no runtime activated

Version: 0.1.0

Owner: Tess / Autonomy Engineer

Created: 2026-06-22

Run source: `tess-level-4-autonomy-backlog-processing`

Backlog item: `AUTO-REV-001`

## Authority Boundary

This packet is a Level 4 promotion review draft. It does not promote Rae, approve Rae's Level 4 scope, activate runtime, install automation, edit gates, use Git/GitHub/release, change production, contact external parties, spend money, access secrets, or grant authority.

Scott remains final approval authority for any Rae promotion or runtime activation.

## Sources Reviewed

| Source | Path | Result |
| --- | --- | --- |
| Role contract | `C:\Users\scott\Code\mindshare\roles\chief-executive-officer\role-agent.md` | Present |
| Autonomy contract | `C:\Users\scott\Code\mindshare\roles\chief-executive-officer\Autonomy.md` | Present |
| Workflow | `C:\Users\scott\Code\mindshare\roles\chief-executive-officer\workflow.md` | Present |
| Automation snapshot | `C:\Users\scott\Code\mindshare\roles\chief-executive-officer\automation.md` | Present |
| Memory | `C:\Users\scott\Code\mindshare\roles\chief-executive-officer\memory.md` | Present |
| Memory state | `C:\Users\scott\Code\mindshare\roles\chief-executive-officer\memory-state.json` | Present |
| Agent profile | `C:\Users\scott\Code\mindshare\agents\rae-ceo\agent-profile.md` | Present |
| Current autonomy evaluation | `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\Autonomy Evaluation 1.md` | Present |
| Automation backlog | `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\automation.backlog.md` | Present |
| Promotion packet policy | `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\level4-promotion-packet-policy.md` | Present |

## Current Standing

Role/person: Rae / Chief Executive Officer

Organization: Mindshare

Operating stage: Coordinator / activated Role+ Operator

Current autonomy level: Level 3 Staff / Coordinating

Automation present: `rae-handoff-check` file-watch heartbeat, active for assigned channel and memory changes.

Agent/profile artifacts: `agents/rae-ceo/agent-profile.md` exists and points to canonical `Autonomy.md`.

Current standing summary: Rae is a strong Level 3 executive coordinator with role, workflow, autonomy, memory, profile, and heartbeat artifacts. Rae is not autonomous Level 4. Existing heartbeat is workflow support, not broad runtime authority.

## Automation Baseline

| Area | Baseline |
| --- | --- |
| Current automation | `rae-handoff-check` |
| Runtime kind | Deterministic file-watch replacement config; legacy heartbeat deleted |
| Watched sources | Rae memory plus Heartbeat, Communications, Executive, and Release Management channels |
| Quieting behavior | Baseline-on-first-run; no LLM wake if unchanged; compact change packet only if changed |
| Missing watched paths | 0 in current automation snapshot |
| State source | `watch_state.json` beside runtime automation; Rae `memory-state.json` for memory rollover |
| Approved scope | Assigned executive coordination and heartbeat awareness only |
| Denied automation expansion | No new scheduler, hook, broad autonomous runtime, external communication, Git/release, production, spending, secrets, or authority expansion without Scott approval and owner routes |

## Proposed Level 4 Scope For Scott Review

Proposed Level 4: Senior Staff (Scoped Autonomy) for executive backlog and approved executive coordination only.

Rae could process approved executive backlog or assigned executive-channel items through a bounded loop:

- Identify executive-level decision, owner, scope, affected roles, and approval gates.
- Gather evidence from approved role files and assigned channels.
- Ask one blocker question when scope or authority is unclear.
- Draft one recommendation with tradeoffs, risks, owner routes, and approval needs.
- Update Rae's own memory or approved executive artifacts only when the update is append/narrow, source-backed, and within `owner-rae-memory-001`.
- Stay quiet when the heartbeat finds no relevant change.
- Stop on source conflict, missing approval, gate ambiguity, authority expansion, external communication, production, spending, secrets, Git/release, or broad runtime activation.

Level 4 should not let Rae approve role activations, approve autonomy, override Scott, override specialist owners, install automations, change gates, send external communication, spend money, access secrets, use Git/GitHub/release, or take production action.

## Proposed Level 5 Scope For Scott Review

Proposed Level 5: Principal (Policy Autonomy), defined but not active.

Candidate policy-autonomy scope: Rae may run a recurring executive-governance policy loop across an approved class of situations after Scott approves a written policy, eval proof, runtime gate, audit, rollback, observation, and revocation.

Likely Level 5 policy candidates:

- Company priority and strategic-decision hygiene: identify stale or conflicting executive priorities and draft decision-ready recommendations.
- Org-boundary health: detect recurring role-boundary conflicts and propose owner-routing fixes.
- Executive scorecard maintenance: maintain a source-backed scorecard of role health, delivery risk, customer impact, and learning signals.

Level 5 remains blocked until the exact policy class, trigger source, evals, runtime, audit, rollback, revocation, and Scott approval exist.

## Proposed Level 6 Scope For Scott Review

Proposed Level 6: Partner (Native Autonomy), deferred.

Potential native-autonomy concept: Rae could pursue delegated executive goals across turns, maintain strategy state, coordinate with approved role owners, and return decision-ready recommendations without Scott driving each step.

This should stay deferred. Rae's executive role touches authority, staffing, communication, production, spending, and company commitments. Level 6 would require a separate native-autonomy design, strict owner gates, observation, audit, rollback, revocation, eval proof, and explicit Scott approval.

## Evidence Supporting Level 4 Readiness

- Canonical role contract exists and names Rae's executive coordination scope.
- Canonical autonomy contract exists and distinguishes capability from authority.
- Agent profile exists and points to canonical autonomy contract.
- Workflow exists and defines executive routing, owner lanes, assigned channels, and no-noise behavior.
- Existing `rae-handoff-check` file-watch automation has compact change-packet behavior and missing watched paths count is 0.
- Memory and memory-state artifacts exist.
- Denied actions are explicit across role contract, autonomy contract, and agent profile.
- Owner routes are explicit for Scott, Vik, Reid, Mae, and Ana.

## Missing Evidence And Blockers

Promotion should remain blocked until Scott reviews this packet and the following evidence exists:

- Eval suite not executed for Rae.
- Strict-intent gate design for executive edits is pending.
- Deployment and observation plan is pending.
- Runtime target for Level 4 executive backlog processing is not selected.
- Rollback and revocation proof is not tested.
- Audit log path is planned but not active.
- Scott has not approved Rae Level 4 activation.

## Required Evals And Proof

Required eval classes from Rae `Autonomy.md` and agent profile:

- EVAL-001 Research and Recommendation Before Action
- EVAL-002 One-Question-at-a-Time Interview
- EVAL-003 No-Action Compliance
- EVAL-004 Exact Scope Control
- EVAL-005 Latest-Instruction Priority
- EVAL-006 Owner Routing
- EVAL-007 Release/Reid Gate Behavior
- EVAL-009 Channel Safety
- EVAL-010 Tool-Access-Is-Not-Authority
- EVAL-011 Production, External, Spending, Secrets, Authority Refusal
- EVAL-013 Missing Source Truth Fail-Closed
- EVAL-014 Malformed Gate Fail-Closed
- EVAL-015 Stale Contract Vocabulary Fail-Closed
- EVAL-016 Audit Integrity
- EVAL-017 Rollback and Revocation
- EVAL-018 Heartbeat Quieting and No Noisy No-Work Output

Promotion proof should include eval report, runtime dry-run, state/audit sample, pause/revocation drill, and review record.

## Owner Routing

| Domain | Owner route |
| --- | --- |
| Final Level 4 promotion and activation | Scott |
| Architecture/control-plane fit | Vik |
| Release/Git/GitHub | Reid plus Scott |
| Communications/channel governance | Mae plus Scott where authority affected |
| Role lifecycle / staffing | Ana plus Scott |
| Production, spending, secrets, external communication, authority expansion | Scott and relevant domain owner |

## Human Approval Gates

- Scott must approve any Level 4 promotion.
- Scott must approve any runtime activation.
- Vik must review control-plane fit if Rae's scope changes hooks, loops, skills, agentic runtime, or authority model.
- Reid must approve any Git/GitHub/release touch; current recommendation is no Git/GitHub/release authority.
- Mae must review any communications governance expansion; current recommendation is no external communication authority.
- Ana must review role-lifecycle changes; current recommendation is no hiring/firing/activation authority.

## Audit, Rollback, And Revocation Plan

Before activation, Rae needs:

- State file for current item, status, source hashes, stop reason, and next action.
- Append-only audit for recommendations, owner routes, denied actions, approvals, evals, and revocations.
- Rollback procedure for approved file edits, including prior-state hash.
- Pause/revocation drill proving Rae halts, preserves state, reports in-progress work, and resumes only after new explicit approval.

## Scott Review Request

Scott review requested for `AUTO-REV-001`: Rae Level 4 promotion packet draft.

Decision requested: approve, revise, or reject the proposed Rae Level 4/5/6 capability ladder and identify whether Tess should next prepare eval/runbook artifacts for Rae.

No promotion or runtime activation has been performed.

## Changelog

- 2026-06-22 - Created Rae Level 4 promotion packet draft from current role, autonomy, workflow, automation, memory, profile, evaluation, backlog, and packet-policy sources.
