# Multi-Agent Orchestration Class Lists

Tracking convention: every list built for this class should be added here with the relevant topic as the heading above the list.

## Core Class Topics

1. Roles vs. Agents
2. Agent Contracts
3. Orchestration Patterns
4. Communication Protocols
5. Shared Memory and Context Injection
6. Tool Use and Capability Boundaries
7. Governance and Human Approval Gates
8. Testing, Evaluation, and Observability
9. Building a Real Multi-Agent Workflow

## Roles vs. Agents

1. A role is the job definition; an agent is the running worker.
2. A role defines responsibility; an agent performs tasks.
3. A role says what should happen; an agent is one way to make it happen.
4. A role creates accountability; an agent creates execution.
5. A role can exist without an agent.
6. An agent should not exist without a role.
7. A role defines purpose, responsibilities, boundaries, authority, and success criteria.
8. An agent defines model, prompt, tools, memory, runtime, triggers, and permissions.
9. The role is the source of authority.
10. One role can be implemented by many agents.
11. One agent can support multiple roles, but that increases governance risk.
12. Roles are organizational artifacts; agents are technical artifacts.
13. Roles are reviewed like job descriptions and operating contracts; agents are tested like software systems.
14. A role answers "Should this work be done, by whom, and under what limits?"
15. An agent answers "How will this work be executed, with what tools, memory, and workflow?"

## Roles, Tasks, Workflows, and Agents

1. Do not start by asking, "What agent should I build?"
2. Start by asking, "What work needs to be done?"
3. That work may be described as a task, role, function, workflow, process, job, responsibility, or capability.
4. The label matters less than the boundary.
5. Before building an agent, define the unit of work.
6. A unit of work needs a purpose.
7. It needs inputs.
8. It needs outputs.
9. It needs success criteria.
10. It needs authority limits.
11. It needs escalation rules.
12. It needs a human owner.
13. Only then should you decide whether that work should be handled by a prompt, a tool, a workflow, an assistant, an agent, or a multi-agent system.
14. An agent is not the work itself. It is one possible execution mechanism for the work.
15. The mistake is turning every useful task into "an agent" before you understand the task.

## Agent Contracts

1. A contract defines the agreement between the work and the worker.
2. A contract can apply to a task, workflow, role, capability, assistant, agent, or service.
3. A contract starts with purpose.
4. A contract defines inputs.
5. A contract defines outputs.
6. A contract defines authority.
7. A contract defines boundaries.
8. A contract defines escalation rules.
9. A contract defines success criteria.
10. A contract defines failure conditions.
11. A contract defines tool permissions.
12. A contract defines data rules.
13. A contract defines communication rules.
14. A contract defines review and approval points.
15. A contract turns "the AI should help" into an operating agreement.

## Orchestration Patterns

1. Orchestration is how work moves through the system.
2. The simplest pattern is single-agent execution.
3. A supervisor pattern uses one coordinator to route work.
4. A planner-executor pattern separates strategy from action.
5. A router pattern classifies the request and sends it to the right worker.
6. A peer-to-peer handoff pattern lets agents pass work directly.
7. A queue-based pattern turns work into durable tasks.
8. A critic/reviewer pattern separates creation from evaluation.
9. A debate pattern uses multiple agents to test competing interpretations.
10. A consensus pattern requires agreement before action.
11. A human-in-the-loop pattern places approval gates at key points.
12. A tool-calling pattern lets agents use external systems.
13. A memory-augmented pattern injects context before action.
14. A fallback pattern defines what happens when confidence is low or a tool fails.
15. A good orchestration pattern is chosen by risk, complexity, and handoff needs.

## Communication Protocols

1. A communication protocol defines how work is passed between agents, tools, systems, and humans.
2. A good protocol makes every message actionable.
3. Every handoff should include task identity.
4. Every handoff should include source context.
5. Every handoff should include current state.
6. Every handoff should include the requested next action.
7. Every handoff should include assumptions.
8. Every handoff should include confidence.
9. Every handoff should include blockers.
10. Every handoff should include boundaries.
11. Communication should be structured when reliability matters.
12. Communication can be conversational when exploration matters.
13. Protocols should separate facts from recommendations.
14. Protocols should preserve traceability.
15. The goal is not more messages. The goal is cleaner handoffs.

## Shared Memory and Context Injection

1. Shared memory is what the system can remember across tasks.
2. Memory and context are not the same thing.
3. Good systems do not inject everything.
4. Shared memory should have ownership.
5. Memory should be source-aware.
6. Memory should have trust levels.
7. Memory should be scoped.
8. Context injection should match the task.
9. Context injection should include constraints, not just facts.
10. Memory can improve continuity, but it can also preserve mistakes.
11. Agents should say what memory they used.
12. Memory needs update rules.
13. Retrieval quality matters more than storage volume.
14. Shared memory requires privacy and access control.
15. The goal is not to make agents remember everything.

## Tool Use and Capability Boundaries

1. Tool use is what lets an agent affect the world outside the chat.
2. A capability is broader than a tool.
3. Tool access should follow the work, not curiosity.
4. Every tool should have a reason.
5. Every tool should have a boundary.
6. Read access and write access are different risks.
7. External actions need stronger controls.
8. Production tools should be gated.
9. Secrets should not be casually exposed to agents.
10. Agents should use least privilege.
11. Tool calls should be observable.
12. Tool failures need defined behavior.
13. Tool outputs are not automatically truth.
14. Capability boundaries should be tested, not assumed.
15. The goal is useful power under control.

## Governance and Human Approval Gates

1. Governance defines what the system is allowed to do.
2. Human approval gates define where automation must stop.
3. Approval gates should match consequence, not complexity.
4. External communication usually needs a gate.
5. Production changes need explicit approval.
6. Spending and financial actions need approval.
7. Sensitive data requires special handling.
8. Agents should know when to stop.
9. Governance should define who can approve what.
10. Approval gates should be visible in the workflow.
11. Approvals should preserve context.
12. Governance should be testable.
13. Governance should include audit trails.
14. Human approval should not become meaningless rubber-stamping.
15. The goal is not to slow the system down.

## Testing, Evaluation, and Observability

1. Testing asks whether the system works.
2. Evaluation asks whether the system is good enough.
3. Observability asks what actually happened.
4. Test scenarios should reflect real work.
5. Each agent needs unit-style tests.
6. The full workflow needs end-to-end tests.
7. Evaluation needs a rubric.
8. Outputs should be evaluated separately from actions.
9. Trace every important step.
10. Measure failure modes directly.
11. Watch cost and latency.
12. Use regression tests.
13. Human feedback should become evaluation data.
14. Observability should support accountability.
15. The goal is not to prove the system is perfect.

## Error Handling, Recovery, and Safe Failure

1. Every workflow needs a success path and an error path.
2. Errors should be classified.
3. Agents should not improvise around critical failures.
4. Tool failures need explicit behavior.
5. Handoff failures need explicit behavior.
6. Memory failures need explicit behavior.
7. Approval failures need explicit behavior.
8. Low-confidence outputs should be marked, not hidden.
9. Errors should preserve state.
10. Errors should be observable.
11. Some errors should create regression tests.
12. Some errors should trigger human escalation.
13. Safe failure is better than confident wrong action.
14. Recovery should be bounded.
15. A mature agent system is judged by how it fails, not only by how it succeeds.
