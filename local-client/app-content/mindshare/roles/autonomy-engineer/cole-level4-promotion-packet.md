# Cole Level 4 Promotion Packet Draft

Status: Scott approved Level 4 scope; runtime installed; scheduler proof pending

Version: 0.2.0

Owner: Tess / Autonomy Engineer

Created: 2026-06-22

Backlog item: `AUTO-REV-009`

## Authority Boundary

This packet records Scott's Level 4 approval and Tess's implementation state. It does not grant Level 5+, change role authority beyond the approved Level 4 scope, edit gates, use Git/release, change production, contact external parties, spend money, access secrets, or grant authority.

## Sources Reviewed

Cole role contract, workflow, loop, automation snapshot, memory/state, newly created `Autonomy.md`, Tess evaluation, backlog, and packet policy.

## Automation Baseline

- `hr-director-handoff-check` active deterministic FileWatch for Cole assigned handoff/files. Scope: HR file-structure monitoring and owner-routed correction only.
- `cole-hourly-role-file-and-whoami-validation` active hourly heartbeat in Cole's office. Scope: validate role files exist for current automation/autonomy level and confirm WhoAmI Autonomy Context injection on account creation/welcome and hourly.

## Proposed Capability Ladder

Level 4: validate role files exist for current automation/autonomy level; confirm WhoAmI Autonomy Context injection in dedicated/synthesized cards; run this validation during account creation/welcome and hourly; create clearly required template-derived structural files only inside Cole scope; draft owner-routed correction packets; stop before authority/status/autonomy changes.

Level 5: recurring role-file health audit policy with low-risk structural repair only under written policy, evals, audit, rollback, observation, and revocation.

Level 6: deferred native HR file-governance autonomy.

## Blockers

First scheduler-triggered hourly proof is pending. Git promotion/durability through Reid is pending. Finn is missing expected canonical `Autonomy.md` and should be routed as a structural/autonomy finding.

## Scott Review Request

Scott approved Cole Level 4 scope on 2026-06-24. Next proof gate: observe `cole-hourly-role-file-and-whoami-validation` write scheduler evidence to `roles/hr-director/level4-proof.md`, then mark operational only if all Level 4 gates pass and Reid promotion durability is complete.

## Changelog

| Date | Version | Change | Owner |
| --- | --- | --- | --- |
| 2026-06-24 | 0.2.0 | Recorded Scott approval and installed hourly validation heartbeat; scheduler proof pending. | Tess |
| 2026-06-22 | 0.1.0 | Created Cole Level 4 promotion packet draft for Scott review. | Tess |
