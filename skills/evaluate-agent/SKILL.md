---
name: evaluate-agent
description: Create the MAPS Evaluate phase artifact for an agent or multi-agent system. Use when designing scenario tests, eval datasets, rubrics, scorecards, regression checks, red-team prompts, safety checks, and release evidence.
---

# Evaluate Agent

## Overview

Use this skill to prove agent behavior before release and create evidence for improvement.

## Workflow

1. Restate the agent's success and failure criteria.
2. Create common, edge, adversarial, and unsafe scenarios.
3. Define expected behavior and scoring rubrics.
4. Add regression cases for known failures.
5. Include tool-use and escalation checks.
6. Run or specify the evaluation process.
7. Produce a scorecard and release recommendation.

## Output

Return:

- Eval scenarios
- Rubric or scoring method
- Scorecard
- Failure categories
- Release recommendation

Use `templates/eval-scorecard.md` from the MAPS repo when working inside this repository.

## Done Criteria

- Evals reflect real tasks.
- Risky behavior is tested.
- Results can guide go/no-go decisions.
- Failures feed the Improve phase.
