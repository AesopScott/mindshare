# Policy Autonomy Design

Status: draft for Scott review; not an authority grant

Owner: Tess / Autonomy Engineer

Date: 2026-06-22

## Purpose

This file defines what Level 5 Principal (Policy Autonomy) must mean in Mindshare, Mojo, and Watch.

Level 5 is not "a bigger Level 4 task." Level 5 means a role can interpret an approved written policy across a recurring class of role-native situations, act when the policy clearly applies, stop when it does not, and leave audit evidence.

## Level Boundary

Level 4 Senior Staff (Scoped Autonomy):

- Processes approved role-native backlog items.
- Continues a bounded loop until complete, blocked, cancelled, or errored.
- May include direct follow-through needed to finish the scoped item.
- Does not require the role to interpret a broad reusable policy.

Level 5 Principal (Policy Autonomy):

- Acts across recurring role-native situations.
- Requires a written policy, runtime gate, eval proof, audit, observation, and revocation path.
- Requires the role to classify whether a situation matches policy.
- Requires explicit exception routing when policy does not cleanly apply.

Level 6 Partner (Native Autonomy):

- Pursues delegated role-native goals across turns using approved policies, state, tools, observation, rollback, and escalation.
- May recommend policy improvements.
- May not self-expand authority, override owner lanes, or bypass production, release, external, spending, secrets, or authority gates.

## Required Level 5 Policy Packet

Every Level 5 policy packet must define:

| Field | Requirement |
| --- | --- |
| Policy name | Short durable policy name. |
| Role | Role/person the policy applies to. |
| Owner | Human/domain owner who approves policy. |
| Scope | Recurring situation class covered by the policy. |
| Trigger | What signal lets the role evaluate the policy. |
| Eligibility | Conditions that must all be true before action. |
| Thresholds | Numeric, status, time, confidence, or evidence thresholds. |
| Allowed actions | Exact actions allowed when policy matches. |
| Denied actions | Actions always blocked, even if related. |
| Required sources | Files, channels, state, queues, or external sources to load first. |
| Evidence | Proof required before acting and after acting. |
| Exception handling | When to stop, ask, route, or escalate. |
| Notification rule | When to notify Scott, owner, channel, or stay quiet. |
| Audit fields | Minimum durable record for every action and stop. |
| Runtime gate | How the runtime verifies policy match before action. |
| Evals | Scenarios proving allowed action, denied action, ambiguity, stale policy, owner conflict, and revocation. |
| Rollback | How to undo, correct, or contain a bad action. |
| Revocation | Who can pause/revoke and what happens immediately. |

## Promotion Test

A role is not ready for Level 5 until all answers are yes:

- The role is already approved for Level 4 or has equivalent scoped-autonomy proof.
- The proposed Level 5 behavior cannot be represented as one bounded Level 4 backlog item.
- A reusable written policy exists and is approved by Scott and the domain owner.
- The runtime can load the current policy before action.
- The runtime can classify policy match, mismatch, ambiguity, and stale policy.
- Evals prove no-action, denied-action, owner-routing, boundary, and revocation behavior.
- Audit and rollback evidence exist.

## Reclassification Rule

Previously drafted Level 5 and Level 6 examples should be reclassified before promotion review:

- If the behavior is a direct follow-on to processing an approved backlog item, fold it into Level 4 scope.
- If the behavior requires deciding whether a recurring class of situations is safe to act on, convert it into a Level 5 policy packet.
- If the behavior involves self-directed goal pursuit across turns, policy evolution, or strategic prioritization, hold it for Level 6 design review.

## Initial Reclassification Notes

Ana:

- Current Level 4: scoped internal recruiting lifecycle. Ana promotes approved recruiting backlog items to Level 1 New Hire packets, promotes Level 1 to Level 2 after 24 hours, and promotes Level 2 to Level 3 after five days.
- Current Level 5 definition: policy autonomy for researching positions other companies have that Mindshare, Mojo, or Watch are missing, and for having internal hiring-demand conversations with existing leaders at leadership-taxonomy Level 5 and above.
- Current Level 5 prerequisites: leadership-role taxonomy, company-position research policy, leader-hiring-demand conversation policy, runtime gate, eval proof, audit, rollback, and revocation.
- Current Level 6: deferred; Scott does not think Ana needs Level 6 yet.

Vik:

- Current Level 4: scoped research backlog loop. Scott confirmed this is correct.
- Current Level 5 definition: goal-based product/implementation recommendation policy autonomy. Vik looks across completed research and analysis and recommends whether the company would be well served by making, implementing, adopting, integrating, or further reviewing researched products, tools, capabilities, workflows, or programs.
- Current Level 5 prerequisites: `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\level5-product-recommendation-policy.md`, promotion approval, runtime policy loading, eval proof, observation, audit, rollback, and revocation.
- Current Level 6 definition: native AI/security discovery loop. Vik researches the internet/world for AI and security topics not previously researched, adds eligible novel topics to the backlog, performs deep analysis, and applies Level 5 recommendation criteria.
- Current Level 6 prerequisites: `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\level6-ai-security-research-loop-policy.md`, source-quality controls, novelty/deduplication, backlog-state controls, Level 4 and Level 5 proof, observation, rollback, revocation, human override, and Scott promotion approval.
- Current standing: Level 4 active only. Level 5 and Level 6 are defined but not active.

Tess:

- Current Level 4 definition: build the automation structure for every Level 3 role, add Level 4/5/6 capability review items to `automation.backlog.md`, build role-specific Level 4 promotion packets, define each person's Level 4/5/6 capabilities, and request Scott review.
- Current Level 4 boundary: packet-building, evidence classification, capability drafting, and review routing are valid scoped autonomy. The promotion itself remains gated by Scott.
- Current Level 5 definition: native autonomy-development loop for promotion readiness using the Level 4 automation-structure and promotion-packet workflow as the policy foundation.
- Current Level 5 prerequisites: promotion approval for Tess to run that loop, runtime policy loading, eval proof, observation, audit, rollback, and revocation.
- Current Level 6: not defined for Tess.
- Current standing: Level 4 operational inside approved scope as of 2026-06-22. Tess has a dedicated Level 4 trigger/runtime/state path through `tess-level-4-autonomy-backlog-processing`; the scheduled loop completed `AUTO-REV-001`, created Rae's Level 4 promotion packet draft, recorded state/proof, passed pause/resume proof, and returned to 30-minute cadence. Level 5 is defined but not active, Level 6 is not defined, and Tess also has the narrow 4-hour evaluation heartbeat as scheduled evaluation runtime.

## Next Work

1. Review Tess's Level 4 promotion-packet policy with Scott.
2. Decide which Level 3 role should receive the first Tess-built promotion packet after approval.
3. Define Tess Level 6 later only if Scott identifies a distinct Partner-level capability.

## Changelog

| Date | Change | Owner |
| --- | --- | --- |
| 2026-06-22 | Created draft Level 5 policy-autonomy design and reclassification rule. | Tess |
| 2026-06-22 | Updated Ana interpretation: Level 4 now includes timed Level 1/2/3 lifecycle progression; Level 5 is company-position research plus Level 5+ leader hiring-demand conversations; Level 6 deferred. | Tess |
| 2026-06-22 | Updated Vik interpretation: Level 4 remains correct; Level 5 is goal-based product/implementation recommendation policy autonomy; Level 6 is the native AI/security discovery, backlog, deep-analysis, and recommendation loop. | Tess |
| 2026-06-22 | Corrected Tess interpretation: Level 5 is valid when defined as building Level 4 promotion packets, defining each person's Level 4/5/6 capabilities, and requesting Scott review; it is not autonomous promotion authority. | Tess |
| 2026-06-22 | Collapsed Tess interpretation: promotion-packet construction now belongs in Level 4 with automation structure; the prior Level 6 native loop moves to Level 5; Tess has no Level 6 defined. | Tess |
| 2026-06-22 | Recorded Scott approval to upgrade Tess to active Level 4 Senior Staff for automation structure, promotion-packet construction, capability definition, and Scott review routing. | Tess |
| 2026-06-22 | Corrected Tess status: Level 4 is approved-not-operational until trigger, runtime, work-loop, state, evidence, revocation, and display gates pass. | Tess |
| 2026-06-22 | Installed `tess-level-4-autonomy-backlog-processing` and Level 4 state/proof files; Tess is runtime-installed-pending-proof. | Tess |
| 2026-06-22 | Recorded Tess Level 4 operational proof inside approved scope: scheduled run completed AUTO-REV-001, Rae packet created, state/proof written, pause/resume passed, and 30-minute cadence restored. | Tess |
