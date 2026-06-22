# Ana Role-Lifecycle Queue

Status: Level 4 readiness queue; not an authority grant

Owner: Ana / Recruiter

Final authority: Scott

Created: 2026-06-22

## Purpose

This queue defines the role-native work state that can eventually trigger Ana's Level 4 scoped autonomy.

Queue occupancy may trigger Ana to carry an approved role-lifecycle work item through intake, research, recommendation, draft artifact preparation, proof capture, and handoff. It does not authorize role activation, authority grants, autonomous agent activation, external communication, production, Git/GitHub, spending, secrets access, hook installation, scheduler installation, or global `/role` behavior changes.

## Status Vocabulary

Use exactly these item states:

- `backlog`: eligible for Ana scoped role-lifecycle work when operational approval exists.
- `blocked`: waiting on a missing answer, owner routing decision, approval, or source conflict.
- `complete`: role-lifecycle work product is visibly delivered and proof is recorded.
- `cancelled`: Scott or the owning authority cancelled the item.
- `errored`: work failed with a durable, concrete failure that needs review.

Do not use `open`, `seen`, `in_progress`, or implied states.

## Level 4 Loop Contract

For each eligible item, Ana may:

1. Load canonical role, workflow, autonomy, profile, state, and roster sources.
2. Confirm the item is role-lifecycle work inside Ana's lane.
3. Ask exactly one blocking question if required inputs are missing.
4. Research and recommend when the minimum intake is available.
5. Draft approved role artifacts or handoffs only within the approved scope.
6. Record proof in the item row, state, memory, or approved run note.
7. Route architecture/control-plane issues to Vik.
8. Route channel/external-communication issues to Mae.
9. Route Git/release/publication issues to Reid.
10. Route role activation, authority, hiring, spending, production, secrets, or autonomy approval to Scott.
11. Stop when the scoped work product is complete, blocked, cancelled, errored, or requires approval.

## Completion Proof

A completed item must include:

- Output artifact path or visible completion note.
- Role status label: candidate draft, authorized role, activated operator, agent-ready candidate, or released/suspended.
- Explicit authority boundary.
- Activation status.
- Owner routing.
- Proof scenario or checklist result.
- Next skill or next approval.
- Statement that completion does not activate or grant authority unless Scott separately approved that exact action.

## Queue Items

| ID | Work item | Question | Expected output | Owner route | Priority | Status | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ANA-L4-001 | Define Ana Level 4 scoped role-lifecycle queue | What exact work state should trigger Ana scoped autonomy without granting activation authority? | Queue contract, autonomy contract update, eval update, approval packet | Tess drafts; Ana owns role-lifecycle; Vik reviews control-plane fit; Scott approves promotion | P0 | complete | Created `role-lifecycle-queue.md`; updated `Autonomy.md`, `loop.md`, `agent-profile.md`, `runtime-proof-plan.md`, and `eval-suite.md`; no promotion or authority grant |

## Approval Boundary

This queue authorizes planning and readiness work only until Scott explicitly approves Ana Level 4 scoped autonomy.

The exact approval sentence should name:

- Ana
- Level 4 Senior Staff / Scoped Autonomy
- Approved trigger source
- Approved queue path
- Approved role-lifecycle work products
- Explicit blocked domains
- Visibility and proof requirements
- Revocation path

## Changelog

- 2026-06-22 - v0.1.0 - Created Level 4 readiness queue for Ana scoped role-lifecycle autonomy.
