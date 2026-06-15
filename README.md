# MAPS: Multi-Agent Pipeline Skills

MAPS is a skill-based framework for building multi-agent systems.

It turns the agent development lifecycle into reusable phase skills:

```text
phase alignment -> define -> design -> build -> equip -> evaluate -> deploy -> observe -> improve
```

Each phase has two artifacts:

- A phase guide in `phases/` for teaching, documentation, and curriculum.
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
  phases/       Teaching guides for each MAPS phase
  skills/       One Agent Skill per phase
  templates/    Reusable phase deliverable templates
  catalogs/     Curated repos, skills, tools, and references
  docs/         Framework notes and contribution guidance
```

## Using The Skills

Install or copy the folders under `skills/` into an Agent Skills-compatible directory, such as `~/.codex/skills/`, `.agents/skills/`, or another client-specific skills path.

Each skill is intentionally small. The full teaching detail lives in `phases/` and the reusable deliverable shells live in `templates/`.

## Teaching Site

Open `docs/index.html` to view the first static teaching page for MAPS scaffolding and Phase 00 structure.

## Curation Model

MAPS catalogs repos and skills by phase. A good catalog entry should explain:

- Why it belongs in the phase.
- Whether it is recommended, useful reference, experimental, or avoid.
- Fit, maintenance, adoption, license, security, docs, and teaching value.

Start with `catalogs/repos.md` and `catalogs/skills.md`.
