# Define

## Purpose

Clarify what the agent or multi-agent system is supposed to accomplish before designing behavior or choosing tools.

## Inputs

- Problem statement
- Target users or operators
- Business or learning goal
- Constraints, risks, and non-goals

## Activities

- Name the user, job, and desired outcome.
- Identify authorization level, approval gates, forbidden actions, scope, boundaries, and escalation points.
- Define success criteria and failure criteria.
- Capture assumptions that need validation.

## Outputs

- `agents/{agent-handle}/agent-brief.md`, created from `templates/agent-definition-template.md`
- Authorization boundary
- Success metrics
- Non-goals and boundaries
- Initial risk list

## Done Criteria

- The agent has a clear job.
- The agent's authorization level is explicit.
- A human can tell whether the agent succeeded.
- The team knows what the agent must not do.
- Unknowns are explicit.

## Phase Artifact

Use `/define-agent` to turn a vague agent idea into `agents/{agent-handle}/agent-brief.md`. Phase 2 Design uses that file to decide behavior, workflow, handoffs, controls, and tool needs.
