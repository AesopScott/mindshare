# Liz Level 4 Promotion Packet Draft

Status: ready for Scott review; not approved; no runtime activated

Version: 0.1.0

Owner: Tess / Autonomy Engineer

Created: 2026-06-22

Run source: `tess-level-4-autonomy-backlog-processing`

Backlog item: `AUTO-REV-005`

## Authority Boundary

This packet is a Level 4 promotion review draft. It does not promote Liz, approve Liz's Level 4 scope, activate runtime, install automation, edit gates, use Git/GitHub/release, change production, contact external parties, spend money, access secrets, or grant authority.

## Sources Reviewed

| Source | Path | Result |
| --- | --- | --- |
| Role contract | `C:\Users\scott\Code\mojo\roles\mojo-website-manager\role-agent.md` | Present |
| Autonomy contract | `C:\Users\scott\Code\mojo\roles\mojo-website-manager\Autonomy.md` | Present |
| Workflow | `C:\Users\scott\Code\mojo\roles\mojo-website-manager\workflow.md` | Present |
| Automation snapshot | `C:\Users\scott\Code\mojo\roles\mojo-website-manager\automation.md` | Present |
| Memory/state | `C:\Users\scott\Code\mojo\roles\mojo-website-manager\memory.md`; `memory-state.json` | Present |
| Agent profile | `C:\Users\scott\Code\mojo\agents\liz-training\agent-profile.md` | Present |
| Evaluation/backlog/policy | Tess autonomy evaluation, backlog, packet policy | Present |

## Current Standing

Role/person: Liz / Mojo Website Manager

Organization: Mojo

Operating stage: Operator / workflow owner

Current autonomy level: Level 3 Staff with policy-scoped website execution boundary.

Automation baseline: `liz-handoff-check` active file-watch. Watched paths include Liz memory, Heartbeat, Mojo Pipeline, Communications, Release Management, `mapstraining.md`, Mojo org chart, Obsidian index, and roles directory. Missing watched paths: 0. Existing production-push authority is limited to verified, scoped, approved Mojo website commits from Liz's training room; broader release/production changes route to Reid and Scott.

## Proposed Level 4 Scope For Scott Review

Proposed Level 4: scoped Mojo website/training backlog processing.

Liz may process approved website/training backlog or source-change items through a bounded loop:

- Confirm source authority from repo-local role/source records and approved training notes.
- Draft or update approved Mojo website/training artifacts inside Liz's site-management lane.
- Maintain org-chart/status mirrors only from approved source records.
- Record proof, owner route, and release boundary.
- Stay quiet when no relevant source change exists.
- Stop on source conflict, mirror-as-authority risk, external communication, broad production/release change, spending, secrets, automation expansion, or authority expansion.

## Proposed Level 5 Scope For Scott Review

Proposed Level 5: policy autonomy for recurring website/source-coherence maintenance, not active.

Candidate policies:

- Stale website/source drift review across Mojo site surfaces.
- MAPS training reflection policy from approved source notes.
- Org-chart/status mirror maintenance when source records change.

Level 5 requires Scott approval, Vik runtime/control-plane review, Reid release boundary, eval proof, audit, rollback, observation, and revocation.

## Proposed Level 6 Scope For Scott Review

Proposed Level 6: deferred. Native website product/learning-surface stewardship across turns should wait until Level 5 policies are proven and release/production boundaries are mature.

## Blockers Before Promotion

- Scott has not approved Liz Level 4 activation.
- Evals not executed.
- Runtime target and state/audit path for Level 4 backlog processing not selected.
- Release-sensitive and production boundary must be explicitly gated with Reid/Scott.
- Rollback/revocation proof missing.

## Scott Review Request

Scott review requested for `AUTO-REV-005`: approve, revise, or reject Liz's proposed Level 4/5/6 capability ladder. No promotion or runtime activation has been performed.

## Changelog

- 2026-06-22 - Created Liz Level 4 promotion packet from current role, autonomy, workflow, automation, memory, profile, evaluation, backlog, and packet-policy sources.
