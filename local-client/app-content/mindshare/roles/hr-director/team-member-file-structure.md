# Team-Member File Structure Standard

Owner: Cole / HR Director
Status: active standard for Cole's approved HR file-structure scope.

## Purpose

Define the expected file structure for Mindshare team members so every role can be found, loaded, audited, backed up, and updated consistently.

## Canonical Directory Naming

Canonical role-root directories use the stable role or function slug, not the person's proper name.

Examples:

- `roles/hr-director`, not `roles/cole`
- `roles/recruiter`, not `roles/ana-recruiter`
- `roles/agentic-systems-program-architect`, not `roles/vik-aspa`
- `roles/mojo-maps-engineer`, not `roles/bea`

Proper names, display names, aliases, and invocation names belong inside `name.md`, `WhoAmI.md`, `role-agent.md`, `state.json`, memory, and room cards. A directory rename does not change authority, lifecycle status, autonomy level, runtime, reporting line, or communication permissions.

## Current Required Files For New Mindshare Roles

Ana owns hiring and internal lifecycle movement through Level 2 Trainee. Cole owns the welcome/readiness lane after Ana places a Level 2 Trainee in the correct office: he verifies the required files and context surfaces, welcomes the person to the office, records proof, and may promote the person to Level 3 Staff when the readiness gates pass.

Cole also owns assigning the role image for local app role records. Liz no longer owns image assignment for these people now that the operating surface is the local MindShare app instead of the public website.

For every new Level 2 Trainee role packet, Ana creates:

- `name.md`
- `personality.md`
- `WhoAmI.md`
- `role-agent.md`
- `memory.md`
- `state.json`

For Level 3 Staff readiness, Cole verifies:

- required Level 3 files exist in the role root
- role image assignment in local app assets/display metadata
- Level 3 verification record/proof note
- this `team-member-file-structure.md` standard remains current

For role control-plane structure, Tess owns:

- `workflow.md`
- `gate-blocks.md`

`Autonomy.md`, `loop.md`, automation files, runtime files, and gate/autonomy expansion belong to Tess/autonomy review and tests, not Cole's Level 3 completeness lane.

Each `WhoAmI.md` must include an `Autonomy Context` section with:

- current autonomy level and operating stage
- active autonomy capability summary, or "none active"
- lower-level context the role must keep in mind
- Level 4, Level 5, and Level 6 capabilities only as defined/inactive unless promoted
- canonical `Autonomy.md` source path, or a clear missing-source note
- reminder that the card gives awareness, not authority

Cole's Level 4 automation validates current Who Am I surfaces, not only the local source file:

- local role-root `WhoAmI.md`
- `G:\My Drive\Mindshare\role\<role-slug>\WhoAmI.md` when Mindshare is the mirror root
- `G:\My Drive\Mindshare\role\who-am-i-cards\<proper-name>.md`
- role-slug room-card aliases when present

The local role-root `WhoAmI.md` is the primary source. G Drive role mirrors and room cards must stay current enough to carry the same Autonomy Context, even when their surrounding compiled text differs.

When the role owns a workflow, Tess defines or reviews `workflow.md` before it is treated as canonical.

When the role has proposed or active automation, Tess owns and verifies the automation file set:

- Automation Definition and Contract: `/roles/<role name>/automation/automation.md`
- Automation Schedule and Goal: `/roles/<role name>/automation/loop.md`
- Automation Workflow: `/roles/<role name>/automation/scripts/levelXautomation.py`
- Automation State: `/roles/<role name>/state.json` role file
- Automation Evaluations: `/roles/<role name>/automation/automationproofs.md`
- Automation Triggers:
  - `C:\Users\scott\.codex\hooks.json` for Codex
  - `%APPDATA%\Claude\hooks.json` for Claude Desktop
  - `/roles/<role name>/automation/hooks/<hook function>` for role-owned hook functions
- Prompt Automation: `/roles/<role name>/WhoAmI.md`

When the role is activated:

- role-home session record or session id in memory/roster
- Who Am I card injected or confirmed in the role-home session
- FileWatch configuration only when approved
- assigned handoff files in memory and contract
- Communications announcement when activation is approved
- entry in `G:\My Drive\Mindshare\role-artifacts.md`

Primary team-member source files must live in local role roots under the owning repo, not on G Drive. G Drive is for mirrors, rosters, channels, cards, and inventory/index files unless Scott explicitly approves another source-of-truth location.

When the role has an agent build path:

- `agents\<role-slug>\agent-brief.md`
- `agents\<role-slug>\agent-profile.md`
- later MAPS phase artifacts only when approved

## Obsidian Mirrors

When Mindshare is the memory root, each role should have:

- `G:\My Drive\Mindshare\<proper-name-or-role-slug>.md`
- `G:\My Drive\Mindshare\role\<role-slug>\name.md`
- `G:\My Drive\Mindshare\role\<role-slug>\personality.md`
- `G:\My Drive\Mindshare\role\<role-slug>\WhoAmI.md`
- `G:\My Drive\Mindshare\role\<role-slug>\role-agent.md`

## Audit Categories

- Missing file.
- Stale file.
- Wrong role status.
- Missing Obsidian mirror.
- Roster mismatch.
- Role-stage mismatch.
- Missing role-artifacts inventory entry.
- Missing source pointer.
- Missing or stale WhoAmI Autonomy Context.
- Missing WhoAmI injection evidence in an active role-home session.
- Missing Level 2 to Level 3 readiness proof after Ana office placement.
- Missing Level 3 completeness checklist or required Level 3 baseline file.
- Missing or unassigned role image in the local app asset/display metadata.
- Unapproved authority implied by file text.
- New structure not rolled into templates or backup expectations.

## Correction Routing

- Cole may create missing Level 3 verification records when the requirement is clear, file content is template-derived, and the action does not change role authority, lifecycle, autonomy, Git/release, production, external communication, spending, secrets, or another owner's substantive content.
- Cole owns Level 3 completeness file verification and may create missing verification records and local app role-image assignments when the requirement is clear and the action does not change role authority, lifecycle, autonomy, Git/release, production, external communication, spending, secrets, or another owner's substantive content.
- Cole may assign or update local app role images and corresponding display metadata when doing onboarding/readiness work, as long as the image assignment does not imply authority, autonomy, external publication, production release, or identity verification beyond the approved role record.
- Cole may promote an Ana-hired Level 2 Trainee to Level 3 Staff only after welcome, file-readiness, WhoAmI/Autonomy Context, owner-route, and proof gates pass. This promotion does not grant autonomy, production, external communication, Git/release, spending, secrets, or authority beyond Level 3 Staff.
- Cole may send an internal role-home context-repair prompt when an active office lacks current WhoAmI/Autonomy Context evidence. The prompt may only ask the role to load its WhoAmI card and confirm identity, autonomy level, active boundaries, and canonical autonomy source in first person; it must not grant authority, activate runtime, approve promotion, or change role status.
- Role lifecycle, roster, or `/role` output: Ana.
- Organization notice or channel guidance: Mae.
- Autonomy, gate, FileWatch, Automation, hook, loop, runtime, or authority implication: Tess and Vik.
- Git, release, branch, PR, or promotion file: Reid.
- Backup expectation: Bea.
- Public/training website publication: Liz when in scope; local role/person image assignment: Cole.
- Final approval or authority expansion: Scott.

## Boundary

This standard describes expected structure and Scott-approved HR gap filling for required structural files. It does not approve role activation, authority changes, autonomous runtime, Git/release actions, production actions, spending, external communication, secrets access, or broad access to every role's private context.
