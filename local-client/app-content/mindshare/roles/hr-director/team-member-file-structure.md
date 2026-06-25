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

For every new role draft:

- `name.md`
- `personality.md`
- `WhoAmI.md`
- `gate-blocks.md`
- `role-agent.md`
- `memory.md`
- `state.json`

For every current role, Cole validates the required file set for the role's current stage. Level 4+, autonomy, runtime, FileWatch, heartbeat, or Role+ records must also have a canonical `Autonomy.md` source unless Scott and Tess explicitly record a different autonomy source.

Each `WhoAmI.md` must include an `Autonomy Context` section with:

- current autonomy level and operating stage
- active autonomy capability summary, or "none active"
- lower-level context the role must keep in mind
- Level 4, Level 5, and Level 6 capabilities only as defined/inactive unless promoted
- canonical `Autonomy.md` source path, or a clear missing-source note
- reminder that the card gives awareness, not authority

Cole validates all current Who Am I surfaces, not only the local source file:

- local role-root `WhoAmI.md`
- `G:\My Drive\Mindshare\role\<role-slug>\WhoAmI.md` when Mindshare is the mirror root
- `G:\My Drive\Mindshare\role\who-am-i-cards\<proper-name>.md`
- role-slug room-card aliases when present

The local role-root `WhoAmI.md` is the primary source. G Drive role mirrors and room cards must stay current enough to carry the same Autonomy Context, even when their surrounding compiled text differs.

When the role owns a workflow:

- `workflow.md`

When the role has a proposed loop, hook, script, skill, FileWatch, or Automation:

- `loop.md`
- `hook-spec.md`
- `script-spec.md`
- `SKILL.draft.md`
- `automation.md`

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
- Unapproved authority implied by file text.
- New structure not rolled into templates or backup expectations.

## Correction Routing

- Cole may create missing stage-required structural files and mirrors when the requirement is clear, file content is template-derived, and the action does not change role authority, lifecycle, autonomy, Git/release, production, external communication, spending, secrets, or another owner's substantive content.
- Cole may send an internal role-home context-repair prompt when an active office lacks current WhoAmI/Autonomy Context evidence. The prompt may only ask the role to load its WhoAmI card and confirm identity, autonomy level, active boundaries, and canonical autonomy source in first person; it must not grant authority, activate runtime, approve promotion, or change role status.
- Role lifecycle, roster, or `/role` output: Ana.
- Organization notice or channel guidance: Mae.
- Autonomy, gate, FileWatch, Automation, hook, loop, runtime, or authority implication: Tess and Vik.
- Git, release, branch, PR, or promotion file: Reid.
- Backup expectation: Bea.
- Public/training website status mirror: Liz when in scope.
- Final approval or authority expansion: Scott.

## Boundary

This standard describes expected structure and Scott-approved HR gap filling for required structural files. It does not approve role activation, authority changes, autonomous runtime, Git/release actions, production actions, spending, external communication, secrets access, or broad access to every role's private context.
