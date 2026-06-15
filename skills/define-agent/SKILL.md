---
name: define-agent
description: Create an agent brief for the MAPS Define phase. Use when turning an agent or multi-agent system idea into goals, users, scope, non-goals, success criteria, failure criteria, escalation points, risks, and assumptions.
---

# Define Agent

## Overview

Use this skill to turn a vague agent idea into an agent brief. Prefer clarity over implementation detail.

## Workflow

1. Identify the user or operator.
2. State the job to be done in one sentence.
3. Separate in-scope work from out-of-scope work.
4. Define observable success and failure criteria.
5. Name human escalation points.
6. Capture risks, assumptions, and unknowns.
7. Produce or update an agent brief.

## Output

Return a concise brief with:

- Name
- User or operator
- Job to be done
- Desired outcome
- In scope
- Out of scope
- Success criteria
- Failure criteria
- Escalation points
- Risks and assumptions

Use `templates/agent-brief.md` from the MAPS repo when working inside this repository.

## Done Criteria

- The agent has a clear job.
- Success can be judged.
- Boundaries are explicit.
- Open questions are visible.
