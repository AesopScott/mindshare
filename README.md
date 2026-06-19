# MAPS: Multi-Agent Pipeline Skills

MAPS is a skill-based framework for building multi-agent systems.

It turns the agent development lifecycle into reusable phase skills:

```text
phase alignment -> define -> design -> build -> equip -> evaluate -> deploy -> observe -> improve
```

Each phase has two artifacts:

- A phase guide in `phases/` for planning, documentation, and shared vocabulary.
- A reusable Agent Skill in `skills/` for agent-compatible tools that support `SKILL.md`.

## Phase Map

| Phase | Core question | Primary output |
| --- | --- | --- |
| Align | What lifecycle, structure, naming, scope, and scaffolding are we agreeing to use? | Phase alignment brief |
| Define | What job should this agent or system do, for whom, and within what boundaries? | Agent brief |
| Design | How should the agent or agents reason, coordinate, escalate, and stay aligned? | System design |
| Build | How do we implement the agent loop, prompts, state, and orchestration? | Working agent |
| Equip | What tools, data, permissions, memory, and integrations does the agent need? | Capability map |
| Evaluate | How do we prove the agent works, fails safely, and improves over baselines? | Eval suite |
| Deploy | How do we release it into a real environment with appropriate controls? | Release plan |
| Observe | How do we monitor behavior, cost, quality, drift, failures, and outcomes? | Observation plan |
| Improve | How do we turn production evidence into better prompts, tools, evals, and workflows? | Improvement backlog |

## Repository Layout

```text
maps/
  phases/       Phase guides for each MAPS phase
  skills/       One Agent Skill per phase
  templates/    Reusable phase deliverable templates
  catalogs/     Curated repos, skills, tools, and references
  docs/         Framework notes and contribution guidance
```

## Using The Skills

Install or copy the folders under `skills/` into an Agent Skills-compatible directory, such as `~/.codex/skills/`, `.agents/skills/`, or another client-specific skills path.

Each skill is intentionally small. The phase detail lives in `phases/` and the reusable deliverable shells live in `templates/`.

## Skill Operating Contract

MAPS keeps skill behavior consistent across sessions with three layers:

- Always-on instructions in `AGENTS.md` and global Codex instructions for one-question interviews, memory helper usage, completion reports, skill versioning, and validation before publish.
- Per-skill contracts inside every `SKILL.md`, including `Versioning`, `Changelog`, `Output`, `Completion report`, project-foundation lookup, one-question interviews, and memory-helper instructions.
- A repo validator at `scripts/validate_maps_skills.py` that checks every MAPS skill for the required operating contract.

Run the validator before publishing skill changes:

```bash
python scripts/validate_maps_skills.py
```

### Non-Phase Builder Skills

MAPS can also include reusable builder skills that support the system but are not lifecycle phases.

- `/role` creates role-agent contracts for a root organization or multi-agent corporation. Use it to build advisory, workflow, skill-backed, loop-backed, or agentic organizational roles.

## Scaffold A New MAPS Repo

Use `skills/scaffold` when invoking `/scaffold` or creating a new MAPS-compatible repository structure.

```bash
python skills/scaffold/scripts/create_maps_scaffold.py /path/to/new-maps-repo
```

## Project Site

Open `docs/phase0.html` to view the static project page for MAPS scaffolding and Phase 00 structure.

## Curation Model

MAPS catalogs repos and skills by phase. A good catalog entry should explain:

- Why it belongs in the phase.
- Whether it is recommended, useful reference, experimental, or avoid.
- Fit, maintenance, adoption, license, security, docs, and builder value.

Start with `catalogs/repos.md` and `catalogs/skills.md`.
