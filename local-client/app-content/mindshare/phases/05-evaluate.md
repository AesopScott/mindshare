# Evaluate

## Purpose

Prove the agent works on realistic scenarios, catches regressions, and fails safely before release.

## Inputs

- Agent implementation
- Success criteria
- Known risks and failure modes
- Example tasks or production traces

## Activities

- Build scenario tests and rubrics.
- Add regression cases for known failures.
- Compare against baseline behavior.
- Run safety, tool-use, and escalation checks.

## Outputs

- Eval suite
- Scorecard
- Failure examples
- Release recommendation

## Done Criteria

- Evals cover common, edge, and unsafe cases.
- Results are repeatable enough to guide decisions.
- Failure categories are understood.
- Release risks are explicit.

## Teaching Exercise

Write five scenario evals and score them with `templates/eval-scorecard.md`.

