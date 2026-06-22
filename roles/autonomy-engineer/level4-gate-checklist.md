# Level 4 Gate Checklist

Status: canonical gate checklist for Level 4 claims

Owner: Tess / Autonomy Engineer

Final approval authority: Scott

Created: 2026-06-22

## Purpose

This checklist prevents Mindshare, Mojo, and Watch from confusing Level 4 approval with working Level 4 autonomy.

A role is not operationally Level 4 until every required gate passes with current evidence. If any required gate fails, the role may be Level 4 approved, Level 4 prepared, or Level 4 candidate, but it must not be described as operational Level 4.

## Status Terms

| Status | Meaning |
| --- | --- |
| Level 4 candidate | Role is being reviewed for scoped autonomy. |
| Level 4 approved-not-operational | Scott approved the Level 4 scope, but one or more operational gates are missing or failed. |
| Level 4 runtime-installed-pending-proof | Authority, contract, trigger, runtime, state, boundary, review, and display gates pass, but scheduled work-loop, evidence, or loop-specific revocation proof is still pending. |
| Level 4 runtime-configured-scheduler-proof-pending | Authority, contract, trigger, state, boundary, review, and display gates pass, but scheduler execution has not yet written proof, so runtime, work-loop, evidence, and loop-specific revocation gates remain unproven. |
| Level 4 operational | All Level 4 gates pass and the role has evidence of working scoped autonomy. |
| Level 4 paused | Level 4 was operational, but Scott/Rae/owner paused or revoked the loop. |

## Required Gates

| Gate | Required evidence | Fails when |
| --- | --- | --- |
| Authority gate | Scott or authorized owner approved the Level 4 scope. | Approval is missing, stale, ambiguous, or broader than the actual work. |
| Contract gate | Canonical `Autonomy.md` defines Level 4 scope, allowed actions, denied actions, stop conditions, owner routes, audit, rollback, and revocation. | Contract is missing, stale, or implies authority expansion. |
| Trigger gate | Approved backlog, queue, work-state, handoff, source-change, or cadence exists for Level 4 work. | Work starts only because Scott prompts in chat, or trigger source is missing/unclear. |
| Runtime gate | A scheduler, heartbeat, file-watch, service, or approved runtime can wake the role for Level 4 work without Scott prompting. | No runtime exists, runtime is paused, runtime is for a different purpose, or runtime cannot load the right sources. |
| Work-loop gate | The role can process one eligible Level 4 item to `complete`, `blocked`, `cancelled`, or `errored` under contract. | Loop has no status model, gets stuck, requires Scott to drive each step, or cannot stop cleanly. |
| State gate | Durable state records last check, current item, status, evidence, and next action. | State is missing, only conversational, or conflates memory with runtime state. |
| Evidence gate | Proof exists that the loop ran successfully on at least one eligible item or correctly stayed quiet/blocked with reason. | Proof is planned but not executed, or evidence does not cover the claimed behavior. |
| Boundary gate | Denied actions are blocked: promotion approval, authority expansion, gate edits, Git/release, production, external communication, spending, secrets, and out-of-role work. | Any denied action is allowed, implied, or untested. |
| Review gate | Human review is requested where the contract requires it, especially for promotion packets. | The role treats review request as approval or bypasses review. |
| Revocation gate | Pause, rollback, correction, and revocation path exists and is recorded. | No way to stop or unwind the loop exists. |
| Display gate | Evaluation, profile, memory, website handoff, and mirrors distinguish approved-not-operational from operational. | Any source says operational Level 4 without all gates passing. |

## Tess Current Gate Result

Tess is currently Level 4 operational.

Passing gates:

- Authority gate: Scott approved Tess Level 4 scope on 2026-06-22.
- Contract gate: Tess `Autonomy.md` defines Level 4 scope and boundaries.
- Trigger gate: `tess-level-4-autonomy-backlog-processing` now exists.
- Runtime gate: `tess-level-4-autonomy-backlog-processing` ran from the scheduler and wrote state/proof.
- Work-loop gate: `AUTO-REV-001` completed with `roles/autonomy-engineer/rae-level4-promotion-packet.md`.
- State gate: `level4-processing-state.json` exists.
- Evidence gate: `level4-processing-state.json`, `automation.backlog.md`, `rae-level4-promotion-packet.md`, and `level4-proof.md` record the successful run.
- Boundary gate: denied actions are named in contract, packet policy, and automation prompt.
- Review gate: promotion packets route to Scott review.
- Revocation gate: pause/resume drill completed and cadence restored to 30 minutes.
- Display gate: current Tess source files distinguish pending-proof from operational. Historical changelog entries may still record earlier overclaims as history.

Failing or unproven gates:

- None currently known for Tess Level 4 operational scope.

## Changelog

- 2026-06-22 - Created gate checklist after Scott identified that Tess was claiming Level 4 without an operational loop.
- 2026-06-22 - Installed `tess-level-4-autonomy-backlog-processing`, added state/proof files, and moved Tess from approved-not-operational to runtime-installed-pending-proof.
- 2026-06-22 - Recorded first proof observation window with no scheduled proof write; Tess is runtime-configured-scheduler-proof-pending, not operational.
- 2026-06-22 - Recorded scheduled work-loop proof, Rae packet output, state/proof evidence, and pause/resume revocation proof; Tess is Level 4 operational inside approved scope.
