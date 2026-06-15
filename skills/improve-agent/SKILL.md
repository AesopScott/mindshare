---
name: improve-agent
description: Create the MAPS Improve phase artifact for an agent or multi-agent system. Use when turning eval results, traces, failures, incidents, user feedback, and observations into prioritized prompt, tool, memory, policy, design, and eval improvements.
---

# Improve Agent

## Overview

Use this skill to turn evidence into the next iteration of an agent system.

## Workflow

1. Gather eval failures, traces, incidents, and user feedback.
2. Cluster problems by root cause.
3. Decide whether each fix belongs in prompts, tools, memory, policy, design, or evals.
4. Prioritize by impact, effort, and risk.
5. Add or update regression coverage.
6. Record the next experiment.
7. Feed lessons back into earlier MAPS phases.

## Output

Return:

- Improvement backlog
- Root-cause notes
- Proposed changes
- Eval coverage updates
- Next experiment

Use `templates/improvement-backlog.md` from the MAPS repo when working inside this repository.

## Done Criteria

- Improvements are evidence-backed.
- Regression coverage is considered.
- Priorities are clear.
- Earlier phase docs are updated when needed.
