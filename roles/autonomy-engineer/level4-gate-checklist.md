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
| Git promotion/durability gate | Any canonical runtime-read source, role `Autonomy.md`, automation prompt, state/proof file, evaluation snapshot, website source mirror, or release-relevant autonomy artifact changed by the promotion has been routed through Reid / Release Management for commit/promotion, or Scott/Reid approved an explicit protected-source alternative. | Promotion source exists only as uncommitted local drift, lacks an owner-filed Release Management request, or website/source mirrors update without the role source being committed or otherwise protected. |
| Script/timer separation gate | Level 4+ recurring work that writes durable state, proof, source files, evaluations, websites, or release-relevant artifacts keeps deterministic logic in a human-readable script where practical; the automation timer/heartbeat acts as trigger, interpreter, live-context router, and escalation path. | Core logic exists only in a long automation prompt, no durable script owns repeatable checks, or file-changing runs lack Release Management routing for Reid. |

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
- Git promotion/durability gate: `level4-processing-state.json` records `release_management_request_present=true` and zero active automation Reid-route gaps.
- Script/timer separation gate: `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\scripts\level4automation.py` owns deterministic Level 4 checks/state/proof; the app cron is being reduced to timer/router behavior.

Failing or unproven gates:

- None currently recorded after the 2026-06-24 manual script proof run. The first scheduled script-backed run remains useful follow-up evidence, but manual proof and durable state currently pass the required gates.

## Changelog

- 2026-06-22 - Created gate checklist after Scott identified that Tess was claiming Level 4 without an operational loop.
- 2026-06-22 - Installed `tess-level-4-autonomy-backlog-processing`, added state/proof files, and moved Tess from approved-not-operational to runtime-installed-pending-proof.
- 2026-06-22 - Recorded first proof observation window with no scheduled proof write; Tess is runtime-configured-scheduler-proof-pending, not operational.
- 2026-06-22 - Recorded scheduled work-loop proof, Rae packet output, state/proof evidence, and pause/resume revocation proof; Tess is Level 4 operational inside approved scope.
- 2026-06-24 - Added Git promotion/durability gate: Level 4+ source changes must be routed through Reid for commit/promotion or approved protected-source handling before operational status is durable; Scott clarified Reid should not clean this class of drift and should require owner-filed Release Management requests.
- 2026-06-24 - Added script/timer separation gate and recorded Tess's script-owned Level 4 proof: deterministic checks now live in `scripts\level4automation.py`, with timer prompts acting as trigger/router only.

