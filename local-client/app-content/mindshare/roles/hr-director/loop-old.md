# Cole - HR Director Loop Draft

Status: Level 4 hourly validation loop installed; deterministic logic migrated to script; scheduler proof pending.

## Approved Level 4 Trigger

- Hourly heartbeat `cole-hourly-role-file-and-whoami-validation`.
- Account creation / new role-home / welcome process.
- A role is created, activated, renamed, retired, or migrated.
- A new required role file, autonomy level, WhoAmI card rule, or injection rule is defined.
- `roles.md`, team-member file structure, conference-room protocol, memory-template, role skill templates, or backup expectations change.

## Approved Cadence

Hourly validation plus event-sensitive account-creation/welcome validation. The timer/heartbeat runs `C:\Users\scott\Code\mindshare\roles\hr-director\scripts\level4automation.py`; the script owns deterministic checks and state/proof writes. Full template-wide repair remains owner-gated; this loop validates and routes.

## State

Level 4 validation state tracks:

- last run timestamp
- last audited roster hash
- last audited file-structure standard hash
- last checked WhoAmI injection protocol hash
- checked role count
- dedicated WhoAmI card count
- missing/stale file findings
- missing/stale Autonomy Context findings
- owner and status for each correction
- durable script path and run mode

## Allowed Actions In Level 4 Scope

- Read approved handoff files and Cole memory.
- Read current role roots, role Autonomy files, WhoAmI cards, room injection rules, and Cole's file-structure standard.
- Validate required files for each role's current stage and automation/autonomy level.
- Validate dedicated and synthesized WhoAmI Autonomy Context injection.
- Draft missing-file and stale-card findings.
- Update Cole memory and audit artifacts.
- Route correction requests to the owner.

## Forbidden Actions

- No autonomous file repairs.
- No authority or status changes.
- No gate edits.
- No Git/release actions.
- No production actions.
- No external communication.
- No spending or commitments.

## Stop Conditions

- Missing approval.
- Scope ambiguity.
- Finding affects authority, autonomy, release, production, or external communication.
- Source conflict between role contract, memory, and roster.
- Scott or Rae suspends the loop.

