---
name: design-agent
description: Create the MAPS Design phase artifact for an agent or multi-agent system. Use when defining roles, workflows, handoffs, memory, context, guardrails, approvals, escalation paths, and system boundaries from an agent brief.
---

# Design Agent

## Overview

Use this skill to turn an agent brief into a practical system design.

## Workflow

1. Restate the agent goal and success criteria.
2. Decide whether the system should be single-agent or multi-agent.
3. Define each role, responsibility, input, output, and handoff.
4. Map workflow states and stopping conditions.
5. Decide memory, context, and retrieval boundaries.
6. Add guardrails, human approval gates, and escalation paths.
7. List assumptions that must be tested in evaluation.

## Output

Return a design with:

- System goal
- Agent roles
- Workflow
- State and memory
- Guardrails
- Human approval gates
- Open questions

Use `templates/workflow-spec.md` from the MAPS repo when working inside this repository.

## Done Criteria

- Every role has a purpose.
- Handoffs and approvals are explicit.
- Risks have controls.
- The design can be built and evaluated.
