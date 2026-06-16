---
name: design-agent
description: Create the MAPS Design phase artifact for an agent or multi-agent system. Use when defining roles, workflows, handoffs, memory, context, guardrails, approvals, escalation paths, and system boundaries from an agent brief.
---

# Design Agent

## Overview

Use this skill to turn an agent brief into a practical system design.

Default to Research and Recommend (R&R): research comparable agents or similar implementations first, recommend a design answer for every major design question, then ask the user to accept or override the recommendations. Do not begin by asking the user a long list of blank-slate questions.

## Research And Recommend

R&R means the agent does the first pass of design judgment.

1. Read `agents/{agent-handle}/agent-brief.md`.
2. Identify the agent type, such as search agent, build agent, calendar integration agent, support agent, research agent, workflow agent, or coding agent.
3. Research comparable agents, reference architectures, product patterns, open-source implementations, platform examples, and design guidance. Use current web or repository research when available.
4. Analyze what the comparable examples suggest about workflow, tools, memory, controls, approvals, failures, observability, and user experience.
5. Produce a recommendation for every design question in this skill.
6. Present the recommendations with the reasoning and any sources used.
7. Ask the user to override only the recommendations they disagree with or want to sharpen.

If research access is unavailable, state that limitation and use known patterns from the brief and MAPS catalogs as the basis for the recommendations.

## Workflow

1. Restate the agent goal and success criteria from the agent brief.
2. Run R&R research for comparable agents or similar implementations.
3. Summarize the patterns, tradeoffs, and risks found during research.
4. Recommend whether the design should be single-agent, tool-using agent, supervised agent, or part of a multi-agent system.
5. Recommend each role, responsibility, input, output, and handoff.
6. Recommend workflow states, decision points, stopping conditions, and failure paths.
7. Recommend memory, context, retrieval boundaries, and data retention.
8. Recommend tools, integrations, permissions, and constraints.
9. Recommend guardrails, human approval gates, escalation paths, and forbidden paths.
10. Recommend observability needs and evaluation implications.
11. Ask the user to accept or override the recommendations.
12. Produce or update `agents/{agent-handle}/agent-design.md`.

## Output

Create or update `agents/{agent-handle}/agent-design.md` using `templates/workflow-spec.md` as the starting structure.

The completed file contains:

- System goal
- Research summary
- Comparable agents or patterns reviewed
- Recommendation table
- Agent roles
- Workflow
- Decision points
- State and memory
- Tools and integrations
- Guardrails
- Human approval gates
- Handoffs
- Failure modes
- Observability needs
- Open questions

Use `templates/workflow-spec.md` from the MAPS repo when working inside this repository.

## Done Criteria

- Every role has a purpose.
- Handoffs and approvals are explicit.
- Risks have controls.
- Recommendations have reasoning.
- User overrides are captured.
- The design can be built and evaluated.
