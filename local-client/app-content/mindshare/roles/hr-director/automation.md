# Cole Handoff FileWatch Automation

Status: deterministic FileWatch is active for Cole's Office.

## Automation

- Automation id/name: `hr-director-handoff-check`
- FileWatch config: `C:\Users\scott\.codex\automations\hr-director-handoff-check\file-watch.toml`, status `ACTIVE`
- Pending packet files: `pending-change-packet.md`, `pending-change-packet.json`
- Watch state path declared by config: `watch_state.json`
- Kind: deterministic FileWatch
- Cadence: hash check every minute; model resumes only when watched file hashes change
- Thread: Cole's Office, `019efbcf-4894-7413-9975-cad9594794f8`
- Queue guard: intentionally ungated for Cole welcome handoffs. Recruiting/`roles.md` roster changes that mention a new activated person, Cole welcome handoff, role-home thread, or new role artifact pointers should resume Cole directly instead of depending on an open role-channel queue.

## Change Prompt

Cole handoff FileWatch.

Cadence: only resume after deterministic hash gating detects a watched-file change.

Active-flow rule: If Cole is engaged in active user-directed work, do not interrupt the flow.

Context to read: read Cole's active repo-local memory file at `C:\Users\scott\Code\mindshare\roles\hr-director\memory.md`. Read assigned handoff files:

- `G:\My Drive\Mindshare\channels\communications.md`
- `G:\My Drive\Mindshare\channels\recruiting.md`
- `G:\My Drive\Mindshare\role-artifacts.md`
- `G:\My Drive\Mindshare\roles.md`

Work handling: Check for team-member file structure changes, new required files, missing-file findings, role activation/rename/retirement updates, taxonomy changes, role-artifact/roster drift, and audit blockers. Act only inside Cole's approved structural scope; route blocked or outside-scope work to the correct owner.

Quiet no-work behavior: if no relevant work exists, do not visibly notify the user.

Authority boundary: this FileWatch does not approve production actions, external communication, spending, authority expansion, Git/release actions, template-wide changes, other-role substantive edits, or autonomous runtime beyond the bounded handoff check.

## Level 4 Hourly Validation Automation

- Automation id/name: `cole-hourly-role-file-and-whoami-validation`
- Kind: Codex app heartbeat
- Cadence: hourly
- Thread: Cole's Office, `019efbcf-4894-7413-9975-cad9594794f8`
- Status: ACTIVE
- Durable logic owner: `C:\Users\scott\Code\mindshare\roles\hr-director\scripts\level4automation.py`

Scope:

- Validate that role files exist for each current role's current automation/autonomy level.
- Validate that dedicated WhoAmI cards include Autonomy Context.
- Validate that synthesized WhoAmI card injection rules require Autonomy Context.
- Validate that account-creation/welcome flow checks current-stage role files and WhoAmI Autonomy Context before or during welcome.

Scott expectation for scheduled runs:

- Auto-fix findings when the repair is clearly inside Cole's Level 4 structural HR scope.
- Fixable examples include Cole-owned source drift, stale roster or artifact path references, and template-derived structural HR gaps that do not change role authority, role status, autonomy level, gates, runtime, Git/release, production, secrets, spending, or external communication.
- After any auto-fix, rerun the durable validation script, update state/proof, and auto-communicate remaining routed findings or blockers to the appropriate internal owner channel or office thread.
- Route autonomy-context gaps to Tess; route structural role-file gaps to Cole/Ana; route durability or source promotion work to Reid through Release Management when Git/release review is needed.
- Notify Scott visibly when an auto-fix was made, an owner handoff was sent, findings changed, or any high/critical/blocking issue remains.

The heartbeat should run:

```powershell
python C:\Users\scott\Code\mindshare\roles\hr-director\scripts\level4automation.py --write --mode scheduled
```

State and proof:

- `C:\Users\scott\Code\mindshare\roles\hr-director\level4-role-file-validation-state.json`
- `C:\Users\scott\Code\mindshare\roles\hr-director\level4-proof.md`

Authority boundary: this heartbeat does not own the validation logic and does not approve role promotion, activation, authority changes, autonomy changes, Git/release, production, external communication, spending, secrets, or broad runtime. Owner-routed findings must go to Ana, Mae, Tess, Reid, Vik, Bea, Rae, Scott, or the role owner as appropriate.

