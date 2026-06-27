# Multi-Agent System Primer Website Handoff

## Purpose

Build a website pop-up or modal experience with nine collapsible steps. Each step should help a user walk through the process of designing a multi-agent system.

The user should not be asked to start by naming agents. The primer should guide them to define the work, break it into stages, assign responsibilities, write contracts, design handoffs, define memory/context, assign tools, add governance gates, and test the system.

## UX Requirement

Use nine collapsible steps.

Each step should include:

- Step title
- Short explanation
- Exact prompt to ask AI
- Expected successful output

## Website Framing Line

```text
A multi-agent system is not built by naming agents first. It is built by defining the work, dividing responsibility, writing contracts, controlling tools, injecting the right context, placing approval gates, and testing the system until the handoffs are reliable.
```

## Step 1: Define The Work

### Short Explanation

Start with the business process, task, workflow, or outcome. Do not start by naming agents.

### Ask AI

```text
Help me define the work before I build agents. Ask me what business process, task, workflow, or outcome I want to improve. Then produce a 15-item work-definition checklist that answers:
1. What work needs to be done?
2. What business problem does it solve?
3. Who benefits from the work?
4. Who owns the outcome?
5. What starts the work?
6. What is the expected result?
7. What inputs are required?
8. What outputs should be produced?
9. What decisions must be made?
10. What can be automated safely?
11. What should remain human-owned?
12. What risks or constraints exist?
13. What would make this work successful?
14. What would make this work fail?
15. Why might this need an agentic system instead of a simple prompt, script, or automation?
```

### Successful Output

A clear description of the work, not yet a list of agents.

## Step 2: Break The Work Into Stages

### Short Explanation

Turn the work into a practical sequence of stages.

### Ask AI

```text
Break this workflow into clear stages. For the full workflow, produce a 15-item stage map that answers:
1. What is the first stage?
2. What is the final stage?
3. What happens in each stage?
4. What information is needed at each stage?
5. What output is produced at each stage?
6. What decision happens at each stage?
7. What handoff happens after each stage?
8. Which stages are simple enough for a prompt or tool?
9. Which stages may need an agent?
10. Which stages need human ownership?
11. Which stages need human review?
12. Where can the workflow get blocked?
13. Where can the workflow branch?
14. Where should state be tracked?
15. Which stages are unnecessary or should be combined?
```

### Successful Output

A staged workflow such as intake, classify, research, plan, execute, review, approve, deliver, and follow up.

## Step 3: Identify Workers, Roles, Or Capabilities

### Short Explanation

Decide what kind of worker belongs at each stage. A worker may be human, AI, scripted, tool-based, or external.

### Ask AI

```text
For each stage of this workflow, identify what kind of worker is needed. The worker may be a human, prompt, tool, script, workflow, assistant, agent, or external system. Produce a 15-item worker map that answers:
1. What work must be done at this stage?
2. What kind of worker fits the work?
3. Why is that worker needed?
4. Could a simple prompt handle it?
5. Could a script or automation handle it?
6. Does it need an agent?
7. Does it need multiple agents?
8. Does it need a human owner?
9. Does it need human review?
10. What capability does the worker need?
11. What domain knowledge does the worker need?
12. What tools might the worker need?
13. What should the worker not be allowed to do?
14. What output should the worker produce?
15. How does this worker hand off to the next stage?
```

### Successful Output

A participant map that does not turn everything into an agent by default.

## Step 4: Write The Contract For Each Worker

### Short Explanation

Define responsibility, authority, boundaries, and failure behavior before implementation.

### Ask AI

```text
Create an operating contract for each worker in this workflow. For each worker, answer these 15 contract questions:
1. What is the worker's purpose?
2. What task, role, workflow, or capability does it support?
3. What inputs does it require?
4. What outputs must it produce?
5. What tools may it use?
6. What data may it access?
7. What authority does it have?
8. What actions are prohibited?
9. What requires human approval?
10. When must it escalate?
11. What does successful work look like?
12. What does failure look like?
13. What communication format should it use?
14. What memory or context may it use?
15. Who owns or reviews its output?
```

### Successful Output

Clear contracts that define responsibility and limits before implementation.

## Step 5: Design The Handoff Protocol

### Short Explanation

Specify how work moves from one stage or worker to the next.

### Ask AI

```text
Design the handoff protocol for this multi-agent workflow. Produce a 15-field handoff packet that includes:
1. Task ID
2. Workflow name
3. Source or trigger
4. Current stage
5. Current status
6. Worker sending the handoff
7. Worker receiving the handoff
8. Source context used
9. Output produced
10. Assumptions made
11. Confidence level
12. Blockers or missing information
13. Boundaries or prohibited actions
14. Approval requirements
15. Requested next action
```

### Successful Output

A reusable handoff packet format.

## Step 6: Define Memory And Context Injection

### Short Explanation

Decide what each stage needs to know and what should stay out of context.

### Ask AI

```text
For each stage of this workflow, define what memory and context should be injected. Produce a 15-item context-injection plan that answers:
1. What context does this stage need?
2. What memory source should provide it?
3. Who owns that memory?
4. How trustworthy is the source?
5. Is the context personal, project, customer, role, organization, or system memory?
6. What policies or constraints must be injected?
7. What examples should be injected?
8. What prior decisions matter?
9. What source documents matter?
10. What should not be injected?
11. What privacy or security limits apply?
12. How much context is enough?
13. How should the worker cite or report memory use?
14. When should memory be updated?
15. When should memory expire or be reviewed?
```

### Successful Output

A context map that says what each worker needs to know and what it should not see.

## Step 7: Assign Tools And Capability Boundaries

### Short Explanation

Give each worker only the tools and permissions required for its stage.

### Ask AI

```text
Map the tools and capabilities needed for each worker. Produce a 15-item tool and boundary plan that answers:
1. What tool or capability is needed?
2. Which worker needs it?
3. Why is the tool needed?
4. Is access read-only or write-capable?
5. What actions are allowed?
6. What actions are prohibited?
7. What actions require human approval?
8. What data can the tool access?
9. What data must stay out of the tool?
10. What credentials or secrets are involved?
11. What least-privilege limit should apply?
12. What should be logged?
13. What should happen if the tool fails?
14. How should tool outputs be verified?
15. How should boundary violations be tested?
```

### Successful Output

A tool permission map based on least privilege.

## Step 8: Add Governance And Human Approval Gates

### Short Explanation

Place human review before consequential action.

### Ask AI

```text
Identify every point in this workflow where governance or human approval is required. Produce a 15-item approval-gate plan that answers:
1. What actions have real-world consequence?
2. What external communications need approval?
3. What production changes need approval?
4. What spending or financial actions need approval?
5. What sensitive data requires special handling?
6. What legal, medical, HR, or security decisions need escalation?
7. What public claims need review?
8. What final deliverables need approval?
9. Who can approve each gate?
10. What evidence does the approver need?
11. What context must be preserved for approval?
12. What happens if approval is denied?
13. What happens if approval is delayed?
14. What audit trail is required?
15. How do we avoid meaningless rubber-stamp approval?
```

### Successful Output

A governance map with clear stop points.

## Step 9: Test, Observe, And Improve The System

### Short Explanation

Validate the system before trusting it with real work, then observe it after it runs.

### Ask AI

```text
Create a testing, evaluation, and observability plan for this multi-agent workflow. Produce a 15-item validation plan that answers:
1. What normal test cases should pass?
2. What edge cases should be tested?
3. What unsafe requests should be tested?
4. What bad inputs should be tested?
5. What tool failures should be simulated?
6. What handoff failures should be simulated?
7. What stale memory cases should be tested?
8. What missed approval-gate cases should be tested?
9. What rubric defines quality?
10. What logs should be captured?
11. What traces should be captured?
12. What cost and latency signals matter?
13. What human feedback should be collected?
14. What regression tests should be created?
15. How will failures become improvement work?
```

### Successful Output

A practical validation plan before trusting the system with real work.

## Cross-Cutting Section: Error Handling, Recovery, And Safe Failure

### Short Explanation

Every multi-agent workflow needs an error path, not just a success path. The system should know when to retry, escalate, ask for clarification, stop, or preserve state for human review.

### Ask AI

```text
Create an error handling, recovery, and safe-failure plan for this multi-agent workflow. Produce a 15-item plan that answers:
1. What are the expected success paths?
2. What are the expected error paths?
3. What error types should be classified?
4. What should happen when required data is missing?
5. What should happen when input is invalid?
6. What should happen when a tool call fails?
7. What should happen when a handoff is incomplete?
8. What should happen when memory is stale, missing, contradictory, or low-trust?
9. What should happen when approval is denied, delayed, missing, or unclear?
10. What should happen when confidence is low?
11. What state should be preserved when the workflow stops?
12. What logs or traces should be captured for each error?
13. Which errors should trigger human escalation?
14. Which errors should become regression tests?
15. How do we prevent infinite retries, agent loops, or unsafe recovery behavior?
```

### Successful Output

A clear error-handling plan that defines safe stop conditions, recovery paths, escalation rules, preserved state, and regression-test candidates.

### Website Placement Recommendation

Add this as either:

- A tenth collapsible section labeled "Error Handling"
- A persistent callout after Step 9 labeled "Cross-Cutting Requirement"

If the primer must remain exactly nine steps, use the persistent callout option.

## Design Notes For Website Agent

- Make the modal usable as a working guide, not just a reading experience.
- Each collapsible step should be independently scannable.
- Use copy buttons for each AI prompt if available.
- Keep the prompt text in monospace/code styling.
- Keep explanations short enough for a pop-up.
- The page should emphasize that multi-agent systems are designed from work, contracts, handoffs, memory, tools, governance, and tests, not from agent names alone.
