---
name: build-agent
description: Implement the MAPS Build phase for an agent or multi-agent system. Use when turning a design into a runnable agent loop, prompts, state, routing, orchestration, project files, local run commands, and basic tests.
---

# Build Agent

## Overview

Use this skill to implement the smallest useful agent that matches the design.

## Workflow

1. Read the project structure and existing conventions first.
2. Identify the minimal runnable agent path.
3. Implement prompts, state, routing, and orchestration.
4. Add tool stubs or interfaces needed by the design.
5. Add basic verification for the happy path.
6. Document the local run command.
7. Record deferred risks for Equip or Evaluate.

## Output

Return:

- Files changed
- How to run locally
- What was verified
- What remains for Equip, Evaluate, or Deploy

## Done Criteria

- The agent runs.
- The implementation matches the design.
- Basic behavior is verified.
- Known gaps are explicit.
