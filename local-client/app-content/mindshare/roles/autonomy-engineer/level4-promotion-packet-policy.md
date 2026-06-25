# Tess Level 4 Promotion Packet Policy

Status: approved Level 4 policy; operational proof recorded

Owner: Scott

Role: Tess / Autonomy Engineer

Created: 2026-06-22

## Purpose

This policy defines Tess's proposed Level 4 Senior Staff (Scoped Autonomy) promotion-packet behavior.

At Level 4, Tess may build a role-specific promotion packet to Level 4 for each eligible person, define that person's Level 4, Level 5, and Level 6 capabilities, and request Scott's review.

This policy does not let Tess approve the packet or promote the person. The autonomous work is packet construction and review routing. Scott remains the approval gate before a person moves to Level 4.

## Trigger

Tess may build a Level 4 promotion packet when:

- A role is evaluated as Level 3 Staff.
- The role has enough source material to define a role-specific autonomy contract.
- The role appears in `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\automation.backlog.md` or another approved autonomy-review queue.
- The newest Scott instruction has not paused, narrowed, or revoked the work.

## Required Sources

Before building a packet, Tess must review available:

- Role contract and role-agent files.
- Workflow and loop files.
- Memory and state files.
- Agent profile, if one exists.
- Current `Autonomy.md`, if one exists.
- Current autonomy evaluation.
- Automation baseline and current automations.
- Relevant backlog, queue, handoff, or channel evidence.
- Owner lanes and approval gates.

## Packet Contents

Each promotion packet must include:

- Role/person name and organization.
- Current autonomy level and operating stage.
- Proposed Level 4 scope.
- Proposed Level 5 policy-autonomy scope.
- Proposed Level 6 native-autonomy scope, or explicit deferral.
- Evidence supporting Level 4 readiness.
- Missing evidence and blockers.
- Required evals and proof.
- Runtime or automation requirements.
- Allowed actions and denied actions.
- Owner routing.
- Human approval gates.
- Audit, rollback, and revocation plan.
- Scott review request.

## Allowed Actions

When active and policy-matched, Tess may:

- Create or update promotion-packet drafts.
- Define role-specific Level 4, Level 5, and Level 6 capability proposals.
- Add review items to the automation backlog.
- Request Scott review through approved internal handoff or visible report paths.
- Route architecture/control-plane issues to Vik.
- Route role-lifecycle issues to Ana.
- Route website-relevant display changes to Liz after Scott-approved standing changes.

## Denied Actions

This policy does not authorize Tess to:

- Approve promotion packets.
- Promote anyone to Level 4, Level 5, or Level 6.
- Activate runtime, hooks, file watches, or automations.
- Edit gates unilaterally.
- Change Git, GitHub, release, production, or deployment state.
- Contact external parties.
- Spend money.
- Access or mutate secrets.
- Expand authority for Tess or any other person.

## Exception Handling

Tess must stop and ask or route when:

- Required source files conflict.
- Current level or operating stage is unclear.
- Proposed scope affects architecture/control-plane fit.
- Proposed scope affects role lifecycle ownership.
- Proposed scope would require gate edits, release work, production, external communication, spending, secrets, or authority expansion.
- Evidence is stale, missing, or ambiguous.

## Audit

Every packet must record:

- Trigger.
- Sources reviewed.
- Capability proposal.
- Eligibility result.
- Evidence and blockers.
- Owner routes.
- Denied actions.
- Scott review request.
- Remaining risks.

## Activation Status

Scott approved Tess for Level 4 packet-building scope on 2026-06-22. Tess now has the `tess-level-4-autonomy-backlog-processing` trigger/runtime, Level 4 state/proof files, successful scheduled work-loop proof, Rae packet output, and pause/resume proof. This policy is operational only inside Tess's approved Level 4 scope and does not approve promotions or runtime activation for other roles.

This activation does not approve broad runtime, Level 5, Level 6, promotion approval authority, gate edits, Git/release, production, external communication, spending, secrets, or authority expansion.

## Rename Note

Scott moved this capability from Tess Level 5 to Tess Level 4 on 2026-06-22. Scott approved renaming the file from `level5-promotion-packet-policy.md` to `level4-promotion-packet-policy.md`; the current filename now matches the active Level 4 capability.
