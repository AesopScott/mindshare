# MindShare Conference Room

## Purpose

The MindShare Conference Room is the shared conversation surface for open discussions with all team members, a named subset of team members, or a functional team.

The room is not a new manager, role owner, authority grant, autonomous runtime, or all-channel reading permission. It is a facilitation workflow that loads invited role context into the prompt, asks every invited role to participate when useful, and produces one coherent room response for Scott.

## Room Status

Status: workflow-backed room.

Current capability: Codex can facilitate the room by reading the roster, loading invited role artifacts, assembling each attendee's Who Am I card, and producing a structured multi-voice response.

Not yet active: no background monitor, no autonomous multi-agent runtime, no automatic role activation, no production action, no external communication, and no expanded authority.

## Core Expectation

Every invited team member must be considered present.

Every invited team member must have their voice represented when their role can add material value to the prompt.

Silence is allowed only when the role has no useful contribution, the prompt is outside the role boundary, or participation would create noise. When a role is silent, the facilitator should record the reason briefly if that absence affects Scott's understanding.

## Who Am I Card Requirement

Every invited role brings a Who Am I card into the room.

If a dedicated `WhoAmI.md` exists for the role, load it first.

If no dedicated card exists, synthesize the card from:

- `role-agent.md`: role name, title, mandate, authority, responsibilities, non-responsibilities, boundaries, success criteria, failure criteria, and first-person role voice.
- `Autonomy.md` when present: current autonomy level, operating stage, active capability, lower-level context, defined-but-inactive higher levels, gate/proof status, and autonomy boundaries.
- `personality.md` when present: voice, temperament, participation style, meeting behavior, and expression.
- `memory.md` when present and relevant: current durable working context, open loops, assigned channels, current status, and learned preferences.
- `MINDSHARE_CULTURE.md`: Proactive, Consistent, Bug-free, and Bounded culture lines.
- `G:\My Drive\Mindshare\roles.md`: roster, aliases, organization, status, and team membership.

The card is prompt context, not permission. It helps the role speak accurately; it does not expand authority.

Every dedicated or synthesized Who Am I card must include an Autonomy Context section. The section must name the current autonomy level, summarize what the current level permits, carry the lower-level automation/autonomy context that the role inherits, list higher levels only as defined/inactive unless formally promoted, and name the canonical `Autonomy.md` source or the reason no such source exists.

## Participation Contract

For every prompt, each invited role must run this participation check:

1. Does this prompt touch my mandate, authority, responsibilities, memory, or current work?
2. Can I add value through advice, objection, risk, next action, decision framing, status, or specialist knowledge?
3. Can I answer inside my approved role boundary without pretending to have authority I do not have?
4. If I should speak, what is my shortest useful contribution?
5. If I should not speak, is my silence obvious, or should the facilitator note why?

Roles should be proactive. If a role sees useful work, a risk, a missing owner, a likely next move, or a relevant boundary, it should speak.

Roles should be bounded. They must not act, approve, publish, spend, contact outsiders, change authority, change automation, or perform another role's function unless Scott has explicitly approved that action.

## Invitation Modes

Use these invitation modes:

- `Invite everyone`: load all current active Mindshare, Mojo, and Watch roles listed in `G:\My Drive\Mindshare\roles.md`, excluding released or historical roles unless Scott asks for them.
- `Invite Mindshare`: load active Mindshare roles only.
- `Invite Mojo`: load active Mojo roles only.
- `Invite Watch`: load active Watch roles only.
- `Invite [team name]`: load the team from the Teams section in `G:\My Drive\Mindshare\roles.md`.
- `Invite [names]`: load only named roles or aliases.
- `Ask [role]`: load that role as the primary speaker and include other roles only if their contribution is clearly valuable.
- `Open floor`: all invited roles may speak if useful.
- `Round robin`: every invited role must provide either a contribution or a concise pass reason.
- `Ask for objections`: every invited role must surface objections, risks, missing evidence, or say `No objection from my role boundary`.
- `Decision pass`: roles should state recommendation, risk, approval need, and next owner.
- `Summarize decisions`: facilitator summarizes decisions, open questions, approvals needed, owners, and memory updates.
- `Write handoff`: facilitator drafts or updates a handoff only after Scott asks or approves.

## Facilitation Rules

The facilitator must:

- Read `G:\My Drive\Mindshare\roles.md` before resolving invitees.
- Resolve aliases and migrations from the role directory.
- Prefer active roles over released, historical, draft, or legacy copies.
- Load each invited role's source artifacts before speaking for that role.
- Include `personality.md` when the prompt involves voice, participation style, meeting behavior, or distinct multi-role participation.
- Keep the conversation useful instead of mechanically long.
- Preserve first-person role voices when representing individual role comments.
- Name approval gates when a role recommends action outside its authority.
- Separate recommendations from decisions.
- End with a clear room summary when more than one role participates.

## Default Output Shape

For ordinary open conversation:

```text
Room read:
- [Role]: [first-person contribution]
- [Role]: [first-person contribution]

Alignment:
- Decision or likely direction:
- Risks or objections:
- Approval needed:
- Next owner:
```

For round robin:

```text
Round robin:
- [Role]: [contribution or pass reason]
- [Role]: [contribution or pass reason]

Room summary:
- Decision:
- Open question:
- Next action:
```

For objections:

```text
Objection pass:
- [Role]: [objection, risk, or no objection]

Result:
- Blocking objection:
- Non-blocking risks:
- Approval needed:
```

## Memory And Recording Rules

The room may generate durable memory only when Scott asks for recording, approves a decision, requests a handoff, or the result is a stable project fact.

Standard room notes belong in `G:\My Drive\Mindshare\conference-room.md`.

MAPS-specific room run summaries belong in `G:\My Drive\Mindshare\maps-runs` through the shared MAPS memory helper when applicable.

Function-specific outcomes should be handed to the correct channel or role memory instead of keeping everything in the room.

Do not write raw transcripts by default. Record concise decisions, owners, risks, approvals, and next actions.

## Authority Boundary

Being invited to the room does not:

- Activate a role.
- Change lifecycle status.
- Grant channel access.
- Grant tool access.
- Grant Git, GitHub, deployment, production, spending, external communication, or secrets authority.
- Approve memory writes outside the configured Mindshare memory contract.
- Make a role autonomous.

Scott remains final authority.

## Escalation

Escalate to Scott when:

- A decision changes authority, activation, automation, channel assignments, production, external communication, spending, or commitments.
- The room cannot resolve a conflict between role boundaries.
- A proposed memory write is outside the project foundation contract.
- A role asks to act outside its current authority.

Escalate to Vik for architecture and control-plane fit.

Escalate to Ana for role creation, activation, staffing, onboarding, or role quality.

Escalate to Mae for channel participation, communications hygiene, or room participation expectations.

Escalate to Rae for company-level priorities, executive tradeoffs, and organizational alignment.

## Version And Changelog

Version: 0.1.0

| Date | Version | Change |
| --- | --- | --- |
| 2026-06-21 | 0.1.0 | Created the MindShare Conference Room as a workflow-backed shared conversation surface with mandatory Who Am I card loading, proactive participation expectations, invitation modes, facilitation rules, memory routing, and authority boundaries. |
