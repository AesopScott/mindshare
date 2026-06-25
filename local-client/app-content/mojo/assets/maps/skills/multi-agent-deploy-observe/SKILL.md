---
name: multi-agent-deploy-observe
description: Create MAPS M10 Runtime Readiness for a multi-agent system. Use after M9 System Evaluate to coordinate release authority, runtime configuration, child APS deployment evidence, smoke checks, hold conditions, rollback, and handoff into M11 live observation.
---

# Multi-Agent Runtime Readiness
## Versioning

Current version: 0.2.0.

Follow semantic versioning for this skill:

- Patch: wording, examples, references, or small workflow clarifications.
- Minor: new outputs, new required steps, new helper behavior, or expanded workflow capability.
- Major: renamed outputs, changed artifact contracts, removed behavior, or incompatible workflow changes.

When changing this skill, update `Current version` and add a `Changelog` entry with the date, version, and short summary of behavior changed.

## Changelog

- 2026-06-24 - v0.2.0 - Reframed M10 from Deploy/Observe to Runtime Readiness; deployment stays in child APS/agent buildout and live observation moves to M11.
- 2026-06-20 - v0.1.0 - Created M10 Deploy/Observe for multi-agent release and production evidence loops.

Use `/multi-agent-deploy-observe` at M10 after M9 System Evaluate. M10 confirms that the multi-agent system is ready to run: release authority is explicit, runtime configuration is complete, child APS deployment evidence exists, smoke checks and hold conditions are defined, rollback is owned, and M11 has a clear live-observation handoff.

## Project foundation updates

At the start of every project run, look for `project-foundation.md`. If it exists, read `Persistent Memory Contract` and use its configured notes, sources, memory, RAG, and sync rules as the project defaults. If `.maps/foundation-preferences.json` exists, use it as the structured preference source for automation.

When this skill creates durable knowledge, write it through the shared MAPS memory helper. The helper gives this skill its own named note under the configured notes root, mirrors that note into the configured RAG location when one exists, appends `MAPS Skill Run Log`, and records a RAG reindex manifest.

At the end of the run, call the helper after creating the primary output artifact:

```bash
python "$CODEX_HOME/skills/foundation/scripts/maps_memory.py" complete-run --project . --skill /multi-agent-deploy-observe --phase M10 --output "<primary artifact path>" --summary-file "<primary artifact path>" --memory-updates "<notes, sources, memory, or RAG updates>"
```

If the helper is unavailable, manually append the timestamp, skill, phase, output path, memory updates, and short note to `project-foundation.md`, then update this skill's named note in `<notesRoot>/maps-runs/`.

## Research and Recommend

Read `assets/maps/catalogs/multi-agent-research-sources.md` when available. Use OpenTelemetry GenAI conventions, OpenAI tracing guidance, runtime-specific deployment docs, A2A task-state ideas, and NIST govern/map/measure/manage controls to define readiness evidence and observation handoff.

Ask exactly one question at a time. Do not present the user with a multi-question form, checklist, or table to fill out.

Start with:

> What runtime or environment does this multi-agent system need to be ready for first?

Then ask only the next missing question needed to define release authority, configuration, secrets, child APS deployment evidence, smoke checks, hold conditions, rollback, and the M11 observation handoff.

## Workflow

1. Read M0-M9 artifacts, release gates, child APS deploy outputs, runtime notes, and approval requirements.
2. Identify runtime units: orchestrator, routers, workers, child agents, tool servers, queues, schedulers, stores, dashboards, and user surfaces.
3. Define runtime configuration, environment variables, secrets, credentials, permissions, network boundaries, storage, retention, and revocation paths.
4. Confirm deployment evidence from child APS or agent buildout artifacts; do not deploy from the multi-agent phase itself.
5. Define release approval: owner, approver, release route, production-change boundary, communication plan, and hold conditions.
6. Define smoke checks, acceptance proof, rollback, and post-readiness verification.
7. Define the M11 observation handoff: live signals, incident triggers, owner, review cadence, and improvement intake route.
8. Produce `m/<project-handle>/runtime-readiness.md` from `templates/multi-agent-deploy-observe.md`.

## Completion report

When the skill is complete, tell the user explicitly. Do not end with only files changed or raw output.

Report:

- Completion status: complete, blocked, or needs more answers.
- Outcome: the concrete runtime readiness artifact, runtime plan, or release decision produced.
- Key decisions or changes made.
- Memory update: whether the shared MAPS memory helper ran, what note/run log was updated, and what RAG or notes locations need syncing.
- Next skill: `/multi-agent-improve` for M11 Observe/Improve after readiness evidence exists, or M9 if release gates are not satisfied.

If the skill is blocked, say what answer, artifact, access, approval, or tool is needed before the next skill can run.
## Output

- `m/<project-handle>/runtime-readiness.md`
- Runtime unit map
- Configuration, secret, permission, and approval plan
- Smoke check, rollback, and readiness evidence
- Observation handoff with signals, incident triggers, and review cadence

## Guardrails

- Do not deploy, publish, push, or change production from the skill alone. Deployment belongs to approved child APS/agent buildout or release processes.
- Do not treat observation as optional for multi-agent systems; hand it to M11 explicitly.
- Do not store secrets in artifacts or notes.
- Do not let release approval imply expanded runtime autonomy.
