# Bea Level 4 Promotion Packet Draft

Status: ready for Scott review; not approved; no runtime activated; no repo-write authority granted

Version: 0.1.0

Owner: Tess / Autonomy Engineer

Created: 2026-06-22

Run source: `tess-level-4-autonomy-backlog-processing`

Backlog item: `AUTO-REV-012`

## Authority Boundary

This packet is a Level 4 promotion review draft. It does not promote Bea, approve Bea's Level 4 scope, activate runtime, install automation, edit gates, grant repository write authority, commit, push, open PRs, release, deploy, change production, contact external parties, spend money, access secrets, or grant authority.

## Current Standing

Role/person: Bea / Mojo MAPS Engineer

Organization: Mojo

Operating stage: Operator

Current autonomy level: practical Level 3 Staff operator with draft autonomy contract and approval-gated engineering work.

Sources reviewed: Bea role contract, `Autonomy.md`, workflow, loop, automation snapshot, memory/state, agent profile, Tess evaluation, backlog, and packet policy.

Automation baseline: `bea-handoff-check` active file-watch for Bea memory, Heartbeat, Mojo Pipeline, Communications, Release Management, and Bea mirror. Missing watched paths: 0. Current automation supports handoff checking only; it does not authorize implementation, repo writes, Git/GitHub, release, or production.

## Proposed Level 4 Scope For Scott Review

Proposed Level 4: scoped MAPS engineering planning backlog processing.

Bea may process approved engineering-planning backlog items:

- Read assigned backlog item and relevant source files.
- Research implementation surface and constraints.
- Draft implementation plan, acceptance criteria, proof plan, owner routes, and release handoff.
- Update planning artifacts only when approved policy permits.
- Stop before implementation patches unless Scott or routed approval grants the exact build scope.
- Stop before Git/GitHub/release, production, external communication, spending, secrets, automation expansion, or authority expansion.

## Proposed Level 5 Scope For Scott Review

Proposed Level 5: policy autonomy for recurring planning-ready backlog work, not active.

Candidate policies:

- Convert assigned MAPS backlog items into implementation plans without build action.
- Maintain planning status and blocker routing.
- Prepare validation and release handoff templates.

Requires Scott approval, Vik/Cal owner fit, Reid release boundary, eval proof, audit, rollback, observation, and revocation.

## Proposed Level 6 Scope For Scott Review

Proposed Level 6: deferred. Native implementation autonomy should wait until planning policy is proven and explicit build, repo-write, test, release, rollback, and human-override gates exist.

## Blockers Before Promotion

- Scott has not approved Bea Level 4 activation.
- Evals not executed.
- Runtime state/audit path not selected.
- Current `Autonomy.md` is still marked draft.
- Exact policy for planning-file writes is not approved.
- Rollback/revocation proof missing.

## Scott Review Request

Scott review requested for `AUTO-REV-012`: approve, revise, or reject Bea's proposed Level 4/5/6 capability ladder. No promotion, runtime activation, repo write, or Git/GitHub action has been performed.

## Changelog

- 2026-06-22 - Created Bea Level 4 promotion packet from current role, autonomy, workflow, automation, memory, profile, evaluation, backlog, and packet-policy sources.
