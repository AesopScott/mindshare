# Design

## Purpose

Translate the agent brief into a system design that describes roles, workflow, decision points, state, controls, and handoffs.

## Inputs

- Agent brief
- Success criteria
- Known constraints
- Existing systems and users

## Activities

- Run Research and Recommend (R&R) before asking the user to make design decisions.
- Research comparable agents, similar implementations, reference architectures, and design guidance.
- Analyze patterns, tradeoffs, risks, and common failure modes.
- Recommend answers for every major design question.
- Ask the user to accept or override the recommendations.
- Choose single-agent, tool-using agent, supervised agent, or multi-agent structure.
- Define agent roles and responsibilities.
- Map workflow states, handoffs, approvals, and escalation.
- Decide memory, context, guardrails, and policy checks.
- Define the test-first proof plan before Build: test strategy, acceptance scenarios, eval shape, unit/integration/e2e balance, mock vs real tool policy, failure cases, regression gates, and what must be proven before Phase 3 starts.

## Outputs

- `agents/{agent-handle}/agent-design.md`
- Research summary
- Recommendation table
- Workflow diagram
- Role definitions
- Control and escalation plan
- Test-first proof plan

## Done Criteria

- Every agent role has a purpose and owner.
- Comparable agents or patterns were considered.
- Design choices are recommended before the user is asked to override.
- Handoffs and stopping conditions are explicit.
- Risk controls are designed before implementation.
- Test strategy, acceptance scenarios, eval shape, mock policy, failure cases, and regression gates are explicit.
- The design names what must be proven before Phase 3 Build starts.
- The design can be evaluated.

## Research And Recommend

R&R is the default Phase 2 method. The agent should inspect the Phase 1 brief, determine the type of agent being designed, research similar agents or implementations, and make a recommended design. The user should not have to answer a blank questionnaire first. The user reviews the recommendations and overrides anything that is wrong, risky, missing, or not aligned with the intended build.

## Useful References

- Addy Osmani, "How to write a good spec for AI agents": useful when turning the agent brief into design-ready objectives, context, constraints, acceptance criteria, and boundaries.
- Addy Osmani agent-skills: useful as a skill/workflow alternative for spec, plan, API/interface design, and test-driven development.
- GSA-TTS AI Agent Specification Template: useful as a deep design-template alternative for agent architecture, autonomy, tools, memory, and oversight.
- GitHub Spec Kit: useful as a spec-to-plan process alternative.
- Obra Superpowers test-driven-development skill: useful as a strict TDD workflow reference.
- Disciplined Agentic Engineering: useful as an ATDD and acceptance-proof reference for agentic work.
