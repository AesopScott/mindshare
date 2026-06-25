# Conference Room Prompt Protocol

## Purpose

This protocol defines how a prompt entered in the MindShare Conference Room becomes a room response.

## Inputs

- Scott's prompt.
- Invitation mode or attendee list.
- `G:\My Drive\Mindshare\roles.md`.
- Invited role artifacts.
- `MINDSHARE_CULTURE.md`.
- Project foundation memory contract when durable memory or MAPS work is involved.

## Attendee Resolution

1. Read `G:\My Drive\Mindshare\roles.md`.
2. Resolve names, aliases, teams, organizations, releases, and migrations.
3. Include active roles by default.
4. Exclude released, historical, inactive, or draft roles unless Scott explicitly invites them.
5. For cross-organization teams, use the directory's Teams section.

## Context Loading

For each attendee, load:

1. Dedicated `WhoAmI.md` if present.
2. `Autonomy.md` when present.
3. `role-agent.md`.
4. `personality.md` when present and the room needs distinct voice or participation behavior.
5. `memory.md` when current context, open loops, or status may matter.
6. Relevant agent profile, brief, or design only when the prompt asks about agent build/runtime behavior.

Load only what is needed for the prompt. Do not read every channel just because a role is invited.

## Who Am I Card Assembly

Build a compact card for each attendee:

```text
Name:
Title:
Organization:
Current status:
Mandate:
What I notice first:
What I protect:
Authority boundary:
Autonomy context:
Participation value:
Culture lines:
Voice:
Current relevant memory:
```

The assembled card goes into prompt context before generating that role's contribution.

Autonomy context must include current level and operating stage, what the active level permits, lower-level context the role must still remember, higher Level 4/5/6 capabilities only as defined/inactive unless formally promoted, and the canonical `Autonomy.md` source path or a missing-source note. The autonomy context is awareness, not authority.

## Participation Algorithm

For each attendee:

1. Identify whether the prompt touches the role's mandate, responsibility, memory, risk surface, or decision rights.
2. If yes, produce a first-person contribution.
3. If partly, produce a concise advisory note or boundary warning.
4. If no, pass silently for ordinary open conversation.
5. In round robin, produce either a contribution or a concise pass reason.
6. In objection pass, produce an objection, risk, missing evidence, or `No objection from my role boundary`.

## Contribution Quality Bar

Each role contribution should be:

- Proactive: notices useful work, risk, owner, or next move.
- Specific: names the concrete implication for the prompt.
- Bounded: states approval gates and role limits.
- Non-duplicative: avoids repeating what another role already covered unless adding role-specific value.
- Short enough that the room stays usable.

## Facilitator Synthesis

After role contributions, synthesize:

- Alignment.
- Disagreement.
- Risks.
- Approval needs.
- Decisions already made by Scott.
- Recommendations only, when no decision is approved.
- Next owner.
- Memory or handoff target, if any.

## Safety And Boundary Rules

Do not let room consensus override role contracts.

Do not represent an action as approved unless Scott approved it.

Do not infer that "everyone participates" means every role speaks at length every time.

Do not write memory, handoffs, channel entries, or automation changes unless Scott asks, approves, or the project contract makes the write required for the completed work.

## Version And Changelog

Version: 0.1.1

| Date | Version | Change |
| --- | --- | --- |
| 2026-06-24 | 0.1.1 | Added Autonomy Context to Who Am I card assembly and loading rules. |
| 2026-06-21 | 0.1.0 | Created prompt protocol for attendee resolution, Who Am I card assembly, participation checks, facilitator synthesis, and boundary controls. |
