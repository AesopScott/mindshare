# Reid Level 4 Promotion Packet Draft

Status: ready for Scott review; not approved; no runtime activated; no Git/GitHub action

Version: 0.1.0

Owner: Tess / Autonomy Engineer

Created: 2026-06-22

Run source: `tess-level-4-autonomy-backlog-processing`

Backlog item: `AUTO-REV-007`

## Authority Boundary

This packet is a Level 4 promotion review draft. It does not promote Reid, approve Reid's Level 4 scope, activate runtime, install automation, edit gates, commit, push, branch, open/merge PRs, release, deploy, change production, contact external parties, spend money, access secrets, or grant authority.

## Current Standing

Role/person: Reid / Release Manager

Organization: Mindshare

Operating stage: Operator

Current autonomy level: Level 3 Staff / Coordinating.

Sources reviewed: Reid role contract, `Autonomy.md`, workflow, loop, automation snapshot, memory/state, agent profile, Tess evaluation, backlog, and packet policy.

Automation baseline: `reid-handoff-check` active file-watch for Reid memory, Heartbeat, Communications, Release Management, and Reid mirror. Missing watched paths: 0. Current automation supports handoff/gate-block awareness only; it does not grant Git/GitHub write authority.

## Proposed Level 4 Scope For Scott Review

Proposed Level 4: scoped release-readiness and branch-hygiene backlog processing.

Reid may process approved release-management review items:

- Read repo/release/branch state for assigned targets.
- Draft dirty-worktree, PR readiness, branch hygiene, merge/release, rollback, and approval-routing reports.
- Track gate-block findings and request scoped approvals.
- Stay quiet when no release-management issue exists.
- Stop before any Git/GitHub write, branch cleanup, destructive action, release publication, production promotion, external communication, spending, secrets, automation expansion, or authority expansion.

## Proposed Level 5 Scope For Scott Review

Proposed Level 5: policy autonomy for recurring read-only release hygiene, not active.

Candidate policies:

- Scheduled read-only cross-repo dirty-worktree/stale-branch review.
- PR readiness scorecard and release-risk routing.
- Gate-block monitoring with concise owner routing.

Requires Scott approval, Vik runtime/control-plane review, repo inventory, eval proof, audit, rollback, observation, and revocation. Git/GitHub writes remain separately approval-gated.

## Proposed Level 6 Scope For Scott Review

Proposed Level 6: deferred. Native release operations across repos should wait until read-only policy autonomy is proven and explicit write authority, rollback, two-key approval, and production boundaries are mature.

## Blockers Before Promotion

- Scott has not approved Reid Level 4 activation.
- Evals not executed.
- Canonical repo inventory and branch/release policy map are incomplete.
- Runtime state/audit path not selected.
- Rollback/revocation proof missing.
- Git/GitHub writes require separate explicit scoped approval even after promotion.

## Scott Review Request

Scott review requested for `AUTO-REV-007`: approve, revise, or reject Reid's proposed Level 4/5/6 capability ladder. No promotion, runtime activation, or Git/GitHub action has been performed.

## Changelog

- 2026-06-22 - Created Reid Level 4 promotion packet from current role, autonomy, workflow, automation, memory, profile, evaluation, backlog, and packet-policy sources.
