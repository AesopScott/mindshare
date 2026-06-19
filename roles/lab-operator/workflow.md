# Lab Operator Workflow

## Purpose

The Lab Operator workflow is currently a draft. If Scott grants operating authorization, the Lab Operator keeps `G:\My Drive\Mindshare\lab.md` actionable for MAPS skill-development work, role-development work, memory-loading decisions, and future monitor-session handoffs.

## Work Item Shape

Each lab item should include:

- Status
- Owner
- Surface
- Priority
- Approval state
- Request
- Context
- Acceptance criteria
- Notes

## Stages

### 1. Intake

Read the new request, identify the affected surface, and create or update a lab item.

### 2. Normalize

Make the item actionable:

- reduce broad requests into one reviewable change
- name the likely owner
- state whether Scott approval is needed
- add acceptance criteria
- add relevant file paths or memory locations

### 3. Classify

Classify the work as one of:

- skill instruction change
- template or output-contract change
- helper/script change
- role artifact
- memory-loading or RAG routing decision
- eval or proof requirement
- monitor or automation proposal
- documentation or runbook update

### 4. Gate

Block or escalate items that involve:

- global defaults
- automatic memory loading
- recurring automation or monitors
- external communication
- spending or commitments
- production, infrastructure, security, or secrets
- authority expansion

### 5. Handoff

Route ready work to:

- Scott for approval or final decision
- Matt for MAPS program review
- a monitor session for bounded action
- a MAPS skill for phase-specific work
- another role once that role exists

### 6. Verify

Before marking done, confirm:

- requested artifact exists
- acceptance criteria were satisfied
- approval state was respected
- memory updates were made or explicitly unnecessary
- run helper was used when a MAPS skill or role output completed

### 7. Record

Update:

- lab item status
- lab history
- `lab-operator.md` when a durable learning or decision appears
- project run log through the appropriate helper when a MAPS skill or role completes

## Monitor Session Rules

A monitor session may act on `lab.md` only when Scott creates an explicit goal for that session.

The monitor session should:

- read the selected lab item
- verify status is `ready` or explicitly assigned
- check approval state
- obey acceptance criteria
- stop on ambiguity or broad policy impact
- report changes back to `lab.md`

The monitor session should not:

- infer approval from a proposed item
- create recurring automation unless Scott approved it
- change role authority
- change memory-loading rules
- execute external communication, spending, deployment, or security-impacting work

## Done Criteria

A lab item is done when:

- the requested change or decision exists
- verification has been performed
- memory impact is recorded
- any required approval is documented
- next action is clear or unnecessary

## Review Checklist

- Is the item small enough?
- Is the affected surface clear?
- Is ownership clear?
- Is approval status clear?
- Are acceptance criteria testable?
- Are memory and RAG implications named?
- Is Matt needed for MAPS program judgment?
- Is Scott needed for authority, automation, or global defaults?

## Changelog

- 2026-06-19 - v0.1.0 - Created Lab Operator workflow for `lab.md` queue management and monitor-session handoffs.
