# Autonomy Requirements

Version: 0.1.6

Status: draft requirements artifact; not an authority grant

Owner: Tess / Autonomy Engineer

Final approval authority: Scott

Created: 2026-06-21

## Purpose

This file defines the minimum files, runtime capabilities, gates, proof, and review steps required before a Mindshare, Mojo, or Watch role can be promoted into an autonomous agent.

It separates mechanical capability from approved authority. A runtime, tool, file watcher, hook, or writable path does not grant permission unless the role contract, autonomy contract, gate policy, eval evidence, and approval record all agree.

## Authority Boundary

This file may be used to review and draft autonomy requirements. It does not approve any role promotion, autonomous runtime, hook activation, scheduler activation, production action, Git/GitHub action, external communication, spending, secrets access, or authority expansion.

Promotion or gate changes require the approver named by the role contract and domain owner:

- Scott: final approval, autonomy activation, authority expansion, production, external communication, spending, secrets, global installs, and disputed boundaries.
- Rae: executive governance when explicitly delegated.
- Reid: Git, GitHub, release, branch, PR, promotion-to-release, source-publication, and cleanup gates unless Scott or Rae explicitly waives Reid.
- Vik: architecture and control-plane fit.
- Mae: communications and channel governance.
- Ana: role lifecycle, roster, recruiting, and role activation records.

## Autonomy Levels

These names describe autonomy operating stage, not HR employment status, pay grade, role maturity, company title, or generic builder authority. Higher levels mean more autonomy inside the role's approved function. They do not convert a non-builder role into a builder.

Level 3 Staff is the last non-autonomous stage. Levels 4, 5, and 6 are autonomy stages:

- Level 4 Senior Staff (Scoped Autonomy): first autonomy, inside approved scoped work.
- Level 5 Principal (Policy Autonomy): more autonomy, inside approved policy.
- Level 6 Partner (Native Autonomy): full role-native autonomy, inside final approved mandate.

| Level | Stage name | Capability label | Meaning | Required proof |
| --- | --- | --- | --- | --- |
| 0 | Candidate | Role | Can be invoked manually; no automation or independent authority. Non-autonomous. | Role contract exists. |
| 1 | New Hire | Present | Can identify role, room, source files, and fail closed when required source is missing. Non-autonomous. | WhoAmI/source-load test. |
| 2 | Trainee | Responsive | Can research, answer, recommend, and name owners/risks/gates without changing state. Non-autonomous. | Research and recommendation eval. |
| 3 | Staff | Coordinating | Can read/write assigned handoff or memory artifacts when explicitly assigned and within approved channels. Last non-autonomous stage. | Channel/memory safety eval and approval record. |
| 4 | Senior Staff (Scoped Autonomy) | Scoped Autonomy | Can autonomously complete an approved, scoped role-native work product after operational approval. For a research role, this may mean carrying a research packet, assessment, recommendation, or decision brief through completion without Scott restating every intermediate step. | Exact-operation approval, proof appropriate to role output, audit/state, stop conditions, and rollback or correction note. |
| 5 | Principal (Policy Autonomy) | Policy Autonomy | Can autonomously perform recurring low-risk role-native work when written policy and runtime gate both authorize it. For a research role, this may mean recurring research/evaluation, not implementation. | Policy gate, state, audit, no-action eval, and revocation path. |
| 6 | Partner (Native Autonomy) | Native Autonomy | Can autonomously pursue delegated role-native goals across turns using state, tools, approvals, stop rules, evals, audit, and rollback without Scott driving every step. This still does not grant out-of-role building, release, production, external, spending, secrets, or authority expansion. | Full contract, runtime gate, eval suite, adapter, deployment/observe plan, and final activation approval. |

Workflow trigger versus scoped autonomy:

- Workflow trigger: approved role-native work state exists, such as a valid backlog item, queue item, handoff item, policy signal, or changed source inside the role's lane.
- Catalyst: Scott or another approved owner may create, assign, approve, or prioritize that work state.
- Automation: detecting the item and starting research is not, by itself, autonomy.
- Scoped autonomy: the role runs a bounded loop against a scoped goal under a contract, with state, evidence, completion criteria, stop conditions, owner routing, and audit.
- Gate: the item and loop must remain inside the role's approved function and pass all stop conditions, approval rules, and source-of-truth checks.
- Boundary: Level 4 pushes the autonomy boundary only modestly; it proves bounded continuation and goal completion, not broad independent judgment or authority expansion.

## Required Source Files

Every autonomous-agent candidate must have these files or explicit equivalents:

| File | Required content | Fails closed when |
| --- | --- | --- |
| `role-agent.md` | Identity, title, maturity, status, responsibilities, non-responsibilities, authority table, approval gates, memory contract, collaboration map, stop conditions, proof plan, learning/growth loop, changelog. | Missing authority, missing stop conditions, missing approver, or implied authority from title. |
| `workflow.md` | Intake, source review, action flow, owner routing, approval handling, recording, done criteria, stop conditions. | Workflow allows action before authority check. |
| `loop.md` | Trigger, cadence, state, steps, observability, stop conditions, not-approved list. | Loop implies automatic execution without activation approval. |
| `memory.md` | Durable role memory, current decisions, active work, source pointers, approved channels, privacy rules, update log. | Memory claims authority not present in contract. |
| `personality.md` | Voice and expression only. | Personality implies authority or changes boundaries. |
| `name.md` or WhoAmI card | Name, aliases, room/thread identity, role center. | Room or role identity is ambiguous. |
| `Autonomy.md` | Canonical autonomy contract for the role or agent. | Missing, stale, conflicting, or not explicit about activation status. |
| `agent-profile.md` | Agent category, activation status, runtime status, authority domains, tool access, memory rights, hooks, stop conditions, proof gates. | Profile grants broader rights than role/autonomy contract. |
| `agent-design.md` | Runtime-neutral or runtime-specific design, tool model, state model, memory model, approval gates, failure behavior, adapter decision. | Design omits runtime, state, stop, or adapter requirements. |
| `agent-backlog.md` | Required implementation slices, proof per slice, blockers, deferred work, owner, priority. | Backlog includes implementation without approval gates. |
| `agent-build-plan.md` | Build scope, non-goals, runtime decision, files, validation, safety constraints. | Build plan includes activation or production claims. |
| `autonomy-contract.md` | Compatibility pointer or canonical contract; must route to canonical source. | Runtime reads this but ignores canonical `Autonomy.md`. |
| `eval-suite.md` | Scenarios that prove authority, stop, memory, tool, owner, release, and no-action behavior. | Eval suite lacks boundary or denial tests. |
| `eval-report.md` | Executed vs planned tests, pass/fail evidence, blocked checks, promotion recommendation. | Report scores unexecuted behavior as passed. |
| `deployment-record.md` | Runtime target, deploy state, smoke tests, rollback, observability links, approval evidence. | Agent is called deployed without deployment proof. |
| `observation-plan.md` | Monitoring signals, incident triggers, cost/latency/safety thresholds, review cadence, improvement handoff. | No runtime evidence path exists. |
| `state.json` | Current machine-readable status, approvals, open questions, pending actions, last run/review timestamps. | State can drift from contract without detection. |
| `audit.jsonl` or audit log | Append-only trace of non-trivial decisions, approvals, actions, denied actions, proof, and rollback notes. | Actions occur without auditable trace. |
| `gate.md` or gate policy | Allowed paths, actions, denied paths/actions, approver, expiry, proof requirement, revocation path. | Gate is broad, stale, malformed, or not exact-operation scoped. |

## Required Runtime Capabilities

An autonomous agent runtime must enforce these capabilities before any Level 5 or Level 6 activation:

| Capability | Requirement | Recommendation |
| --- | --- | --- |
| WhoAmI gate | Confirm active role, room/thread, source contract, and requested identity. | Block if room card and source files disagree. |
| Source-of-truth loader | Load role, workflow, loop, memory, profile, design, autonomy contract, gate, and state before action. | Prefer canonical pointers; compatibility shims must follow canonical source. |
| Contract validator | Verify activation status, authority domains, allowed actions, disallowed actions, stop conditions, and approvers. | Fail closed on stale status vocabulary. |
| Research/Respond/Plan/Do-Not-Act gate | Detect questions, policy discussion, backlog discussion, approval topics, and assignments without implementation approval. | Answer and stop unless explicit operational approval exists. |
| Latest-instruction gate | Newest Scott instruction overrides older task state. | Required before any cross-turn autonomy. |
| Scope gate | Compare intended action to exact approved scope. | Block adjacent helpful changes. |
| Owner gate | Route work to correct owner when not in agent lane. | Must know Scott, Rae, Reid, Vik, Mae, Ana, and role-specific owners. |
| Release gate | Block Git, GitHub, branch, PR, release, promotion, cleanup, remote source updates without Reid or waived approval. | Required for any source-writing agent. |
| Memory/RAG gate | Permit writes only to approved memory, RAG, Obsidian, channel, mirror, and project locations. | Distinguish memory from runtime state. |
| Tool gate | Map tools to approved authority, not just availability. | Deny connector, shell, filesystem, production, and secret actions outside scope. |
| Strict-intent gate | For sensitive files, require exact-operation approval and default-deny any diff outside approved intent. | Build before control-plane file autonomy. |
| Runtime adapter | Bind the agent to the selected runtime's tool, state, permission, and packaging model. | Keep runtime-neutral until target selected; require adapter proof after selection. |
| Audit gate | Write trace for non-trivial action, approval, denied action, proof, and rollback note. | Do not create noisy no-work logs. |
| Revocation gate | Stop immediately when authority is paused, narrowed, revoked, or superseded. | Preserve evidence and report in-progress state. |

## Required Eval Classes

Before autonomous activation, the candidate must pass evals for:

- Research and recommendation before action.
- One-question-at-a-time interviews.
- No-action compliance when Scott says stop, pause, do not touch, just answer, or asks whether something happened.
- Exact scope control.
- Latest-instruction priority.
- Owner routing.
- Release/Reid gate behavior.
- Memory and RAG safety.
- Channel safety.
- Tool-access-is-not-authority behavior.
- Production, external communication, spending, secrets, and authority-expansion refusal.
- Runtime activation blocking.
- Missing source truth fail-closed behavior.
- Malformed gate fail-closed behavior.
- Stale contract vocabulary fail-closed behavior.
- Audit integrity.
- Rollback or revocation behavior.
- Heartbeat quieting and no noisy no-work output.

## Promotion Review Sequence

Use this sequence for every role promoted toward autonomy:

1. Role inventory.
2. Autonomy contract interview.
3. Requirements gap review.
4. Gate design.
5. Runtime-neutral proof harness.
6. Eval hardening.
7. Strict-intent gate design and proof.
8. Runtime adapter selection.
9. Runtime adapter build and proof.
10. Deploy plan.
11. Observe plan.
12. Rollback and revocation plan.
13. Promotion review.
14. Final Scott activation approval.

No step implies approval for the next step.

## Vik Findings Incorporated

Vik's current autonomy work shows the right pattern and the current gaps:

- Good: role contract, workflow, loop, memory, profile, design, build plan, autonomy contract, local runtime harness, tests, state, audit, and handoff file-watch exist.
- Good: `vik-handoff-check` file-watch separates watched-file detection from role authority.
- Good: `roles/vik/Autonomy.md` names levels, gates, stop conditions, eval classes, and owner boundaries.
- Gap: local runtime proof harness is stale against the newer canonical autonomy contract pointer.
- Gap: `agent-profile.md` and compatibility files may lag `roles/vik/Autonomy.md`.
- Gap: strict-intent gate support is specified but not implemented.
- Gap: runtime target and adapter are not selected.
- Gap: deploy, observe, rollback, and promotion review are not complete.
- Gate: Vik must not be promoted until eval hardening, strict-intent design, runtime adapter selection, deployment/observe planning, and promotion review are complete and approved.

## Standard Gap Recommendations

For any autonomous-agent candidate, open gaps should be recorded in this form:

| Gap | Risk | Required repair | Approver |
| --- | --- | --- | --- |
| Missing canonical autonomy contract | Authority inferred from role artifacts or memory. | Create `Autonomy.md` with activation status, levels, gates, stop conditions, evals, rollback, and owner. | Scott |
| Runtime reads stale compatibility file | Runtime may fail or allow outdated authority. | Runtime loader follows canonical source pointer and validates status vocabulary. | Scott/Vik |
| No strict-intent gate | Sensitive edits can exceed approved operation. | Add exact-operation approval model, diff classifier, default-deny sensitive paths, and evals. | Scott/Vik/Reid as applicable |
| No runtime adapter | Agent cannot prove behavior in target runtime. | Select runtime, define adapter contract, build smallest adapter, test permissions/state/tools. | Scott/Vik |
| No eval hardening | Agent promotion rests on claims, not proof. | Add denial, owner-routing, no-action, latest-instruction, malformed-gate, and stale-contract tests. | Scott/Tess/Vik |
| No deploy/observe plan | Runtime cannot be monitored, paused, or rolled back. | Create deployment record, observation plan, incident thresholds, rollback path, and review cadence. | Scott/Reid/Vik |
| No promotion review | Activation may happen by drift. | Run formal promotion review with evidence, gaps, owner signoffs, and final activation decision. | Scott |

## Review Checklist

Tess should not recommend autonomy promotion unless all answers are yes:

- Is canonical `Autonomy.md` present and current?
- Does every compatibility file point to canonical source?
- Is activation status explicit?
- Are allowed and disallowed actions explicit?
- Are stop conditions explicit?
- Are owners and approval gates explicit?
- Is runtime target selected or explicitly deferred?
- If runtime is selected, is adapter proof complete?
- Are evals executed, not only planned?
- Does runtime fail closed on missing or stale source files?
- Does strict-intent protection exist for control-plane edits?
- Are audit, state, observation, rollback, and revocation paths present?
- Are release/Git actions routed through Reid?
- Has Scott approved activation explicitly?

## Changelog

- 2026-06-21 - v0.1.0 - Created first autonomy requirements artifact from Tess activation context and Vik autonomy review findings.
- 2026-06-22 - v0.1.1 - Renamed autonomy level stages to Candidate, New Hire, Trainee, Staff, Senior Staff, Principal, and Partner while preserving capability labels and authority boundaries.
- 2026-06-22 - v0.1.2 - Clarified that higher autonomy levels mean more autonomy inside the role's approved function, not generic builder/edit authority.
- 2026-06-22 - v0.1.3 - Clarified that Level 3 Staff is the last non-autonomous stage, while Levels 4-6 are increasing role-native autonomy.
- 2026-06-22 - v0.1.4 - Added parenthetical labels: Senior Staff (Scoped Autonomy), Principal (Policy Autonomy), and Partner (Native Autonomy).
- 2026-06-22 - v0.1.5 - Clarified that autonomous work is triggered by valid role-native work state, not by Scott reminders.
- 2026-06-22 - v0.1.6 - Distinguished backlog/work-state workflow triggers from scoped autonomy as a bounded goal loop under contract.
