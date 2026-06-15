---
name: define-agent
description: Create an agent brief for the MAPS Define phase. Use when turning an agent or multi-agent system idea into goals, users, authorization level, scope, non-goals, success criteria, failure criteria, escalation points, risks, and assumptions.
---

# Define Agent

## Overview

Use this skill to turn a vague agent idea into an agent brief. Prefer clarity over implementation detail.

## Workflow

1. Identify the user or operator.
2. State the job to be done in one sentence.
3. Define the authorization level: advise, draft, act with approval, or act autonomously within explicit limits.
4. Name actions that require approval and actions that are forbidden.
5. Separate in-scope work from out-of-scope work.
6. Define observable success and failure criteria.
7. Name human escalation points.
8. Capture risks, assumptions, and unknowns.
9. Produce or update an agent brief.

## Output

Return a concise brief with:

- Name
- User or operator
- Job to be done
- Desired outcome
- Authorization level
- Approval required for
- Forbidden actions
- In scope
- Out of scope
- Success criteria
- Failure criteria
- Escalation points
- Risks and assumptions

Use `templates/agent-brief.md` from the MAPS repo when working inside this repository.

## Done Criteria

- The agent has a clear job.
- The authorization boundary is explicit.
- Success can be judged.
- Boundaries are explicit.
- Open questions are visible.
