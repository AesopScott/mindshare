# Autonomy Requirements

Version: 0.1.15

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

- Level 4 Senior Staff (Scoped Autonomy): first autonomy, inside approved scoped work. This is where role-specific backlog processing, adjacent follow-on steps, and narrowly bounded continuation belong unless a real written policy/gate system exists.
- Level 5 Principal (Policy Autonomy): policy-based autonomy. The role may act across a class of recurring role-native situations only when a written policy, runtime gate, eval proof, audit, and revocation path authorize that class of action.
- Level 6 Partner (Native Autonomy): full role-native autonomy inside a final approved mandate, with policy creation/evolution limits, observation, rollback, and human escalation built in.

| Level | Stage name | Capability label | Meaning | Required proof |
| --- | --- | --- | --- | --- |
| 0 | Candidate | Role | Can be invoked manually; no automation or independent authority. Non-autonomous. | Role contract exists. |
| 1 | New Hire | Present | Can identify role, room, source files, and fail closed when required source is missing. Non-autonomous. | WhoAmI/source-load test. |
| 2 | Trainee | Responsive | Can research, answer, recommend, and name owners/risks/gates without changing state. Non-autonomous. | Research and recommendation eval. |
| 3 | Staff | Coordinating | Can read/write assigned handoff or memory artifacts when explicitly assigned and within approved channels. Last non-autonomous stage. | Channel/memory safety eval and approval record. |
| 4 | Senior Staff (Scoped Autonomy) | Scoped Autonomy | Can process the role's approved backlog: autonomously complete an approved, scoped role-native backlog item after operational approval, without Scott restating every intermediate step. Narrow role-specific task expansions, such as a recruiting role preparing hire packets and a next bounded handoff, or a research role researching and drafting recommendations from approved backlog work, should usually be treated as Level 4 scope until they require policy interpretation across a class of situations. | Backlog contract, exact-operation approval, proof appropriate to role output, audit/state, stop conditions, and rollback or correction note. |
| 5 | Principal (Policy Autonomy) | Policy Autonomy | Can autonomously perform recurring role-native work across a class of situations only when an approved written policy defines eligibility, thresholds, allowed actions, denied actions, exception handling, evidence requirements, notification/noise rules, and runtime gate enforcement. Level 5 is not just "the next task after Level 4." | Approved policy, policy gate, state, audit, no-action eval, exception evals, and revocation path. |
| 6 | Partner (Native Autonomy) | Native Autonomy | Can autonomously pursue delegated role-native goals across turns using state, tools, approved policies, stop rules, evals, observation, audit, and rollback without Scott driving every step. Level 6 may recommend policy changes but still cannot self-expand authority or override out-of-role gates. This still does not grant out-of-role building, release, production, external, spending, secrets, or authority expansion. | Full contract, policy set, runtime gate, eval suite, adapter, deployment/observe plan, rollback/revocation proof, and final activation approval. |

Workflow trigger versus scoped autonomy:

- Standard backlog rule: every role may have a role-native backlog. Level 4 is the first stage where the role can process that backlog under contract.
- Workflow trigger: approved role-native work state exists, such as a valid backlog item, queue item, handoff item, policy signal, or changed source inside the role's lane.
- Catalyst: Scott or another approved owner may create, assign, approve, or prioritize that work state.
- Automation: detecting the item and starting research is not, by itself, autonomy.
- Scoped autonomy: the role runs a bounded loop against a scoped goal under a contract, with state, evidence, completion criteria, stop conditions, owner routing, and audit.
- Gate: the item and loop must remain inside the role's approved function and pass all stop conditions, approval rules, and source-of-truth checks.
- Boundary: Level 4 pushes the autonomy boundary only modestly; it proves bounded continuation and goal completion, not broad independent judgment or authority expansion.

## Level 4 Gate

Level 4 has four non-paused states:

- Level 4 approved-not-operational: Scott or the authorized owner approved the Level 4 scope, but the role has not proven an operating trigger, runtime, loop, state, evidence, and display gate.
- Level 4 runtime-installed-pending-proof: authority, contract, trigger, runtime, state, boundary, review, and display gates pass, but scheduled work-loop evidence or loop-specific revocation proof has not passed yet.
- Level 4 runtime-configured-scheduler-proof-pending: authority, contract, trigger, state, boundary, review, and display gates pass, but scheduler execution has not yet written proof, so runtime, work-loop, evidence, and loop-specific revocation gates remain unproven.
- Level 4 operational: all Level 4 gates pass with current evidence.

Do not describe a role as operational Level 4 unless every gate in `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\level4-gate-checklist.md` passes.

Promotion durability rule: a Level 4+ promotion or autonomy-source repair is not operationally durable while its canonical runtime-read files exist only as uncommitted local working-tree changes. The owning role must route the source change through Reid / Release Management for Git promotion, commit, PR, or an explicitly approved protected-source alternative. Reid should not clean or stash Level 4+ autonomy-source drift as routine main hygiene; he should require the owning role to create or complete a Release Management request. Until that route is complete, record the role as approved-not-operational, runtime-installed-pending-proof, blocked, or source-drift-blocked as appropriate.

Required Level 4 gates:

1. Authority gate.
2. Contract gate.
3. Trigger gate.
4. Runtime gate.
5. Work-loop gate.
6. State gate.
7. Evidence gate.
8. Boundary gate.
9. Review gate.
10. Revocation gate.
11. Display gate.
12. Git promotion/durability gate.

If any gate fails, record the role as Level 4 approved-not-operational, runtime-installed-pending-proof, runtime-configured-scheduler-proof-pending, candidate, or paused as appropriate.

Policy autonomy:

- Policy trigger: a recurring role-native condition matches an approved written policy, not a one-off backlog item alone.
- Policy content: the policy must define eligibility, thresholds, allowed actions, denied actions, required evidence, stop conditions, exception routing, notification/noise behavior, audit fields, rollback/revocation, and owner approvals.
- Runtime enforcement: the runtime must load the current policy, classify the situation against it, block if any required field is missing or stale, and record why the policy did or did not apply.
- Boundary: Level 5 is not a pile of larger role tasks. Work that is still "process this approved backlog item and its direct handoff" remains Level 4 unless the role is interpreting a reusable policy across a class of situations.
- Approval: a role cannot enter Level 5 until Scott approves both the role's Level 5 policy and the runtime/eval evidence that enforces that policy.

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
| WhoAmI Autonomy Context | Current autonomy level, operating stage, active capability, lower-level context, inactive higher-level definitions, canonical `Autonomy.md` path or missing-source note, and awareness-not-authority reminder. | Role can forget its current stage, overclaim higher autonomy, or lose context on lower-level responsibilities. |
| `Autonomy.md` | Canonical autonomy contract for the role or agent. Must define Level 4 scoped-autonomy capability and, before any Level 5+ review, must define the approved policy-autonomy model instead of a mere list of larger tasks. | Missing, stale, conflicting, not explicit about activation status, missing Level 4 scoped capability, or treating Level 5/6 as ordinary task expansion instead of policy/native autonomy. |
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
| Git promotion request / release note | Release Management request or closeout showing canonical autonomy-source files, runtime state/proof files, and website/source mirrors were routed through Reid for commit/promotion or explicitly protected by an approved alternative. | Canonical runtime-read source exists only as uncommitted local drift, was left without an owner-filed Release Management request, or was mirrored to website without the role source being committed/protected. |

## Required Runtime Capabilities

An autonomous agent runtime must enforce these capabilities before any Level 5 or Level 6 activation:

| Capability | Requirement | Recommendation |
| --- | --- | --- |
| WhoAmI gate | Confirm active role, room/thread, source contract, and requested identity. | Block if room card and source files disagree. |
| WhoAmI Autonomy Context gate | Confirm the injected WhoAmI card includes current autonomy level, lower-level context, inactive higher-level boundaries, and source path. | Block if the card omits autonomy context or implies authority beyond the canonical `Autonomy.md`. |
| Source-of-truth loader | Load role, workflow, loop, memory, profile, design, autonomy contract, gate, and state before action. | Prefer canonical pointers; compatibility shims must follow canonical source. |
| Contract validator | Verify activation status, authority domains, allowed actions, disallowed actions, stop conditions, and approvers. | Fail closed on stale status vocabulary. |
| Research/Respond/Plan/Do-Not-Act gate | Detect questions, policy discussion, backlog discussion, approval topics, and assignments without implementation approval. | Answer and stop unless explicit operational approval exists. |
| Latest-instruction gate | Newest Scott instruction overrides older task state. | Required before any cross-turn autonomy. |
| Scope gate | Compare intended action to exact approved scope. | Block adjacent helpful changes. |
| Owner gate | Route work to correct owner when not in agent lane. | Must know Scott, Rae, Reid, Vik, Mae, Ana, and role-specific owners. |
| Release gate | Block Git, GitHub, branch, PR, release, promotion, cleanup, remote source updates without Reid or waived approval. | Required for any source-writing agent. |
| Git promotion/durability gate | Confirm canonical source edits that change autonomy status, runtime gates, state/proof, or role authority have been routed through Reid and committed/promoted or placed in an approved protected source. | Promotion is not operational if source lives only in a dirty worktree. |
| Memory/RAG gate | Permit writes only to approved memory, RAG, Obsidian, channel, mirror, and project locations. | Distinguish memory from runtime state. |
| Tool gate | Map tools to approved authority, not just availability. | Deny connector, shell, filesystem, production, and secret actions outside scope. |
| Strict-intent gate | For sensitive files, require exact-operation approval and default-deny any diff outside approved intent. | Build before control-plane file autonomy. |
| Runtime adapter | Bind the agent to the selected runtime's tool, state, permission, and packaging model. | Keep runtime-neutral until target selected; require adapter proof after selection. |
| Durable logic gate | Keep deterministic automation logic in a durable script, module, or similarly reviewable source file; schedulers/heartbeats should trigger it rather than reimplement it in prompt text. | Start with script-owned logic for file checks, state/proof generation, and validation pages; use role reasoning only for interpretation, routing, and exceptions. |
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
3. Build or update the role's canonical `Autonomy.md`.
4. Define the role-specific Level 4 scoped-autonomy capability, blocked actions, triggers, proof, stop conditions, and owner routes.
5. For Level 5+, define the written policy-autonomy model: policy trigger, eligibility, thresholds, allowed/denied actions, evidence, exceptions, audit, notification, rollback, and revocation.
6. Review and lock the `Autonomy.md` contract for the requested promotion level.
7. Requirements gap review.
8. Gate design.
9. Runtime-neutral proof harness.
10. Eval hardening.
11. Strict-intent gate design and proof.
12. Runtime adapter selection.
13. Runtime adapter build and proof.
14. Deploy plan.
15. Observe plan.
16. Rollback and revocation plan.
17. Promotion review.
18. Final Scott activation approval.
19. Git promotion / durable source routing through Reid for any runtime-read source, state/proof, website source mirror, or release-relevant autonomy file changed by the promotion.

No step implies approval for the next step.

When Scott says "promote [role] to Level 4," Tess should treat that as an instruction to build or update the role's `Autonomy.md`, runtime state/proof paths, evaluation record, and display handoff for review. The promotion is not complete until Scott reviews and approves the locked contract and the canonical runtime-read source changes are routed through Reid for Git promotion or explicitly protected by an approved durable-source alternative. The locked and durable contract is the source of truth for what that role may do at Level 4.

When Scott says "promote [role] to Level 5," Tess should not reuse old task ladders as policy autonomy. Tess should first build the role's Level 5 policy packet for review, then require runtime/eval proof that the policy is enforceable before promotion. The Level 5 promotion is not operational until the Level 5 `Autonomy.md`, policy, runtime state/proof, automation prompt changes, evaluation, and display/source mirrors are committed/promoted through Reid or otherwise protected by an approved durable-source path.

## Vik Findings Incorporated

Vik's current autonomy work shows the right pattern and the current gaps:

- Good: role contract, workflow, loop, memory, profile, design, build plan, autonomy contract, local runtime harness, tests, state, audit, and handoff file-watch exist.
- Good: `vik-handoff-check` file-watch separates watched-file detection from role authority.
- Good: `roles/maps-agentic-systems-program-architect/Autonomy.md` names levels, gates, stop conditions, eval classes, and owner boundaries.
- Gap: local runtime proof harness is stale against the newer canonical autonomy contract pointer.
- Gap: `agent-profile.md` and compatibility files may lag `roles/maps-agentic-systems-program-architect/Autonomy.md`.
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
| No Git promotion/durable source route | Runtime reads old committed files because uncommitted autonomy edits were never routed for release and durability. | Route all autonomy-source changes through Reid for commit/promotion or approved protected-source handling before calling the promotion operational; Reid should request the owning role's Release Management packet instead of cleaning this drift. | Scott/Reid/Tess |

## Review Checklist

Tess should not recommend autonomy promotion unless all answers are yes:

- Is canonical `Autonomy.md` present and current?
- Does the injected WhoAmI card carry current autonomy level, lower-level context, inactive higher-level boundaries, and canonical source path?
- Does `Autonomy.md` define this role's Level 4 scoped-autonomy capability?
- For Level 5+, does `Autonomy.md` define an actual written policy-autonomy model rather than a list of larger role tasks?
- Has the requested promotion level been reviewed and locked in `Autonomy.md`?
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
- Does deterministic automation logic live in durable source rather than only in an automation prompt?
- Are audit, state, observation, rollback, and revocation paths present?
- Are release/Git actions routed through Reid?
- Are autonomy-source, runtime state/proof, website source mirror, and automation prompt changes committed/promoted through Reid or protected by an approved durable-source alternative?
- Has Scott approved activation explicitly?

## Changelog

- 2026-06-21 - v0.1.0 - Created first autonomy requirements artifact from Tess activation context and Vik autonomy review findings.
- 2026-06-22 - v0.1.1 - Renamed autonomy level stages to Candidate, New Hire, Trainee, Staff, Senior Staff, Principal, and Partner while preserving capability labels and authority boundaries.
- 2026-06-22 - v0.1.2 - Clarified that higher autonomy levels mean more autonomy inside the role's approved function, not generic builder/edit authority.
- 2026-06-22 - v0.1.3 - Clarified that Level 3 Staff is the last non-autonomous stage, while Levels 4-6 are increasing role-native autonomy.
- 2026-06-22 - v0.1.4 - Added parenthetical labels: Senior Staff (Scoped Autonomy), Principal (Policy Autonomy), and Partner (Native Autonomy).
- 2026-06-22 - v0.1.5 - Clarified that autonomous work is triggered by valid role-native work state, not by Scott reminders.
- 2026-06-22 - v0.1.6 - Distinguished backlog/work-state workflow triggers from scoped autonomy as a bounded goal loop under contract.
- 2026-06-22 - v0.1.7 - Clarified the general Level 4 rule: every role may have a backlog, and Senior Staff means processing approved role-native backlog items under contract.
- 2026-06-22 - v0.1.8 - Added the promotion-contract rule: each role's `Autonomy.md` must define Level 4, 5, and 6 capabilities before review, and promotion requests build/review/lock that file before activation.
- 2026-06-22 - v0.1.9 - Corrected Level 5 interpretation: task expansions belong in Level 4 unless they require an approved reusable policy; Level 5 now requires policy trigger, thresholds, runtime gate, audit, evals, exceptions, and revocation.
- 2026-06-22 - v0.1.10 - Added the mandatory Level 4 gate and status distinction between approved-not-operational and operational Level 4.
- 2026-06-22 - v0.1.11 - Added the runtime-installed-pending-proof intermediate state for Level 4 gates.
- 2026-06-22 - v0.1.12 - Added the runtime-configured-scheduler-proof-pending status for configured scheduler paths that have not yet written proof.
- 2026-06-24 - v0.1.13 - Added Git promotion/durability gate after Vik/Mae regressions showed uncommitted autonomy-source edits can lose operational effect when not routed through Reid; Scott clarified Reid should stop cleaning this class of drift and require owner-filed Release Management requests.
- 2026-06-24 - v0.1.14 - Added WhoAmI Autonomy Context requirement so each role carries current autonomy level, lower-level context, inactive higher-level boundaries, and canonical source path in injected role context.
- 2026-06-24 - v0.1.15 - Added durable logic gate: deterministic Level 4+ validation logic should move into scripts/modules one role at a time, with automations acting as timers/triggers and role reasoning handling exceptions.
