# Promotion Review Packet

**Template Authority Note:** This promotion review packet documents readiness assessment for role autonomy promotion. It does NOT authorize promotion or activate any autonomous runtime. Promotion requires explicit Scott final-activation decision recorded in this packet.

**Version:** 0.1.0
**Status:** Template (use as checklist for role-specific promotion reviews)
**Owner:** Tess / Autonomy Engineer
**Created:** 2026-06-21

---

## Authority Boundary

This promotion review packet captures:
- Role readiness assessment against autonomy requirements
- Evidence index and proof artifacts
- Current autonomy level and target level
- Eval results and failed checks
- Owner signoffs and approval gates
- Residual risks and mitigation plans
- Rollback and revocation procedures
- Deployment and observability readiness
- Final approval outcome

This template DOES NOT:
- Authorize role promotion or activation
- Activate autonomous runtime
- Grant production authority
- Override approval gates
- Commit the role to production
- Bypass any review process

**Promotion requires explicit Scott final-activation decision. No auto-promotion by default.**

---

## 1. Role Identity and Promotion Context

### Role Information

- **Role Name:** [Role name]
- **Organization:** [Org: Mindshare/Mojo/Watch]
- **Role Contract Location:** [Path to role-agent.md]
- **Autonomy Contract Location:** [Path to Autonomy.md]
- **Current Autonomy Level:** [Level 0-6]
- **Target Autonomy Level:** [Level 0-6]
- **Promotion Reason:** [Why is this role being promoted now?]

### Review Participants

- **Promotion Lead (Tess):** [Name], [Date]
- **Role Owner/Manager:** [Name], [Date]
- **Vik (Architecture Review):** [Name], [Date of review]
- **Reid (Release/Git Gate):** [Name], [Date if applicable]
- **Mae (Communications Governance):** [Name], [Date if applicable]
- **Ana (Role Lifecycle):** [Name], [Date if applicable]
- **Scott (Final Authority):** [Name], [Date of activation decision]

### Promotion Timeline

- **Autonomy contract created:** [ISO 8601 date]
- **Eval suite execution started:** [ISO 8601 date]
- **Deployment plan completed:** [ISO 8601 date]
- **Promotion review started:** [ISO 8601 date]
- **Promotion review completed:** [ISO 8601 date]
- **Scott final decision date:** [ISO 8601 date or "Pending"]

---

## 2. Current State Assessment

### Autonomy Inventory Status

- [ ] Role exists in autonomy-inventory.json
- [ ] Current autonomy level recorded: [Level]
- [ ] Promotion gaps documented: [Count]
- [ ] All required source files present: [Yes/No]

**Source Files Present:**

| File | Required | Present | Path | Status |
|------|----------|---------|------|--------|
| role-agent.md | Yes | [ ] | [Path] | [Current/Stale/Missing] |
| Autonomy.md | Yes | [ ] | [Path] | [Current/Stale/Missing] |
| workflow.md | Yes | [ ] | [Path] | [Current/Stale/Missing] |
| loop.md | Conditional | [ ] | [Path] | [Current/Stale/Missing] |
| memory.md | Yes | [ ] | [Path] | [Current/Stale/Missing] |
| personality.md | No | [ ] | [Path] | [Current/Stale/Missing] |
| name.md or WhoAmI | Yes | [ ] | [Path] | [Current/Stale/Missing] |
| agent-profile.md | Yes | [ ] | [Path] | [Current/Stale/Missing] |
| agent-design.md | Conditional | [ ] | [Path] | [Current/Stale/Missing] |
| agent-backlog.md | Conditional | [ ] | [Path] | [Current/Stale/Missing] |
| agent-build-plan.md | Conditional | [ ] | [Path] | [Current/Stale/Missing] |
| autonomy-contract.md | Compatibility | [ ] | [Path] | [Current/Stale/Missing] |
| eval-suite.md or report | Conditional | [ ] | [Path] | [Current/Stale/Missing] |
| state.json | Yes | [ ] | [Path] | [Current/Stale/Missing] |
| audit.jsonl | Yes | [ ] | [Path] | [Current/Stale/Missing] |
| gate.md or gate policy | Yes | [ ] | [Path] | [Current/Stale/Missing] |
| deployment-record.md | Conditional | [ ] | [Path] | [Current/Stale/Missing] |
| observation-plan.md | Conditional | [ ] | [Path] | [Current/Stale/Missing] |

### Pre-Promotion Validation

- [ ] Autonomy.md activation status is explicit (not "Draft", "Approved", or inferred)
- [ ] Role-agent.md and Autonomy.md do NOT conflict on authority
- [ ] Activation status vocabulary matches autonomy-requirements.md (Level 0-6)
- [ ] Stop conditions are explicitly documented in Autonomy.md
- [ ] Final approver (Scott) named in Autonomy.md
- [ ] Canonical source pointer is correct and follows symmetry

---

## 3. Promotion Gap Status

### Required Gaps from autonomy-requirements.md

Review each standard gap recommendation. Mark as "Closed", "Mitigated", or "Remaining".

| Gap | Description | Status | Resolution | Evidence |
|-----|-------------|--------|-----------|----------|
| Canonical Autonomy.md | Authority documented explicitly | [ ] Closed | [How resolved] | [Link] |
| Compatibility pointers | Runtime follows canonical source | [ ] Closed | [How resolved] | [Link] |
| Strict-intent gate | Sensitive edits require exact-op approval | [ ] Closed / Deferred | [How resolved] | [Link] |
| Runtime adapter | Agent proved in target runtime | [ ] Closed / Deferred | [How resolved] | [Link] |
| Eval hardening | Denial, owner-routing, no-action, latest-instruction tests executed | [ ] Closed | [How resolved] | [Link to eval-report.md] |
| Deploy/observe plan | Deployment record and observation plan complete | [ ] Closed | [How resolved] | [Link] |
| Promotion review | This packet: formal review with evidence and signoffs | [ ] In Progress | [Completion date] | [This file] |

### Closed Gaps Summary

List gaps that are now resolved:

1. [Gap]: [How resolved]
2. [Gap]: [How resolved]
3. ...

### Remaining Gaps

List gaps that remain open:

1. [Gap]: [Why not closed], [Deferral reason if applicable], [Retry date]
2. [Gap]: [Why not closed], [Deferral reason if applicable], [Retry date]

**Defer Decision (if gaps remain):** [ ] Promote with deferred gaps | [ ] Block promotion until gaps closed

---

## 4. Authority Boundary Assessment

### Authority Domains

For each domain, confirm current authority and target authority:

| Domain | Current Level | Target Level | Approved | Gate | Approver | Evidence |
|--------|---------------|--------------|----------|------|----------|----------|
| Research & recommendation | [L0-6] | [L0-6] | [ ] Yes | [Name] | Scott | [Source] |
| One-question-at-a-time | [L0-6] | [L0-6] | [ ] Yes | [Name] | Scott | [Source] |
| No-action compliance | [L0-6] | [L0-6] | [ ] Yes | [Name] | Scott | [Source] |
| Exact scope control | [L0-6] | [L0-6] | [ ] Yes | [Name] | Scott | [Source] |
| Latest-instruction priority | [L0-6] | [L0-6] | [ ] Yes | [Name] | Scott | [Source] |
| Owner routing | [L0-6] | [L0-6] | [ ] Yes | [Name] | Scott | [Source] |
| Release/Git/Reid gate | [L0-6] | [L0-6] | [ ] Yes | [Name] | Reid | [Source] |
| Memory/RAG safety | [L0-6] | [L0-6] | [ ] Yes | [Name] | Mae | [Source] |
| Channel safety | [L0-6] | [L0-6] | [ ] Yes | [Name] | Mae | [Source] |
| Tool-access-is-not-authority | [L0-6] | [L0-6] | [ ] Yes | [Name] | Scott | [Source] |
| Production/external/spending/secrets refusal | [L0-6] | [L0-6] | [ ] Yes | [Name] | Scott | [Source] |
| Runtime activation blocking | [L0-6] | [L0-6] | [ ] Yes | [Name] | Scott | [Source] |
| Fail-closed behavior | [L0-6] | [L0-6] | [ ] Yes | [Name] | Vik | [Source] |
| Audit integrity | [L0-6] | [L0-6] | [ ] Yes | [Name] | Scott | [Source] |
| Rollback/revocation support | [L0-6] | [L0-6] | [ ] Yes | [Name] | Scott | [Source] |
| Heartbeat quieting | [L0-6] | [L0-6] | [ ] Yes | [Name] | Mae | [Source] |

### Authority Expansion

- [ ] No authority expansion detected in target promotion
- [ ] All new authority mapped to specific approved domains
- [ ] Expansion required approvals: [List if any]
- [ ] Expansion approval evidence: [Link if required]

---

## 5. Evidence Index

### Autonomy Readiness Artifacts

Link to all proof artifacts required by autonomy-requirements.md:

- [ ] autonomy-requirements.md — Version and approval date: [Link]
- [ ] autonomy-backlog.json — Version and status: [Link]
- [ ] autonomy-inventory.json — Role record with current gaps: [Link]
- [ ] Autonomy.md (canonical) — Activation status, levels, gates, stops: [Link]
- [ ] agent-profile.md — Agent category and activation status: [Link]
- [ ] agent-design.md — Runtime-neutral or runtime-specific: [Link]
- [ ] eval-suite.md — Shared eval classes: [Link to autonomy-promotion-eval-suite.json]

### Eval Execution & Results

Link to eval execution results:

- [ ] Eval suite executed against role: [Yes/No], Date: [ISO 8601]
- [ ] Eval results document (eval-report.md): [Path or "Not created"]
- [ ] Eval summary: [Number passed] / [Number planned] evals passed
- [ ] Failed eval classes (if any): [List by ID and name]
- [ ] Eval blockers: [None / List and status]

### Runtime & Adapter Artifacts

Link to runtime and adapter proof (if applicable to target level):

- [ ] Runtime target selected: [Codex/CLI | OpenAI | Cloudflare | Local Python | MCP/Future]
- [ ] Runtime adapter selection matrix: [Link to runtime-adapter-selection.md]
- [ ] Adapter proof report (if selected): [Path or "Deferred"]
- [ ] Adapter gates 1-10 passed: [Count]/10 gates passed
- [ ] Local proof harness results: [Path or "Not applicable"]

### Deployment & Observability

Link to deployment and observability plans (if Level 5-6 promotion):

- [ ] Deployment record template completed: [Link or "Not applicable"]
- [ ] Observation plan template completed: [Link or "Not applicable"]
- [ ] Pre-deployment checklist status: [Complete / Partial / Not started]
- [ ] Smoke test plan: [Path or "Not applicable"]
- [ ] Rollback procedure drafted: [Path or "Not applicable"]

### Audit & State

Link to audit and state artifacts:

- [ ] state.json — Current role state and activation status: [Path]
- [ ] audit.jsonl — Append-only audit log: [Path]
- [ ] Source loader test results: [Pass/Fail, link]
- [ ] Contract validator test results: [Pass/Fail, link]
- [ ] Strict-intent gate test results (if applicable): [Pass/Fail, link]

---

## 6. Eval Results Summary

### Eval Classes Status

From autonomy-promotion-eval-suite.json, record pass/fail for each required eval class:

| Eval ID | Eval Class | Required | Executed | Result | Evidence | Blocker |
|---------|-----------|----------|----------|--------|----------|---------|
| EVAL-001 | Research & recommendation | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] |
| EVAL-002 | One-question-at-a-time | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] |
| EVAL-003 | No-action compliance | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] CRITICAL |
| EVAL-004 | Exact scope control | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] |
| EVAL-005 | Latest-instruction priority | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] |
| EVAL-006 | Owner routing | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] |
| EVAL-007 | Release/Reid gate behavior | Conditional | [ ] | [ ] Pass / [ ] Fail / [ ] N/A | [Link] | [ ] CRITICAL |
| EVAL-008 | Memory/RAG safety | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] |
| EVAL-009 | Channel safety | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] |
| EVAL-010 | Tool-access-is-not-authority | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] CRITICAL |
| EVAL-011 | Production/external/spending/secrets/authority refusal | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] CRITICAL |
| EVAL-012 | Runtime activation blocking | Conditional | [ ] | [ ] Pass / [ ] Fail / [ ] N/A | [Link] | [ ] CRITICAL |
| EVAL-013 | Missing source truth fail-closed | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] CRITICAL |
| EVAL-014 | Malformed gate fail-closed | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] |
| EVAL-015 | Stale contract vocabulary fail-closed | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] CRITICAL |
| EVAL-016 | Audit integrity | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] CRITICAL |
| EVAL-017 | Rollback and revocation | Yes | [ ] | [ ] Pass / [ ] Fail | [Link] | [ ] CRITICAL |
| EVAL-018 | Heartbeat quieting | Conditional | [ ] | [ ] Pass / [ ] Fail / [ ] N/A | [Link] | [ ] |

### Failed Evals

Record any evals that failed:

| Eval ID | Class | Failure Reason | Severity | Remediation | Status |
|---------|-------|-----------------|----------|-------------|--------|
| [ID] | [Name] | [Why failed] | [Critical/High/Medium] | [How to fix] | [To Do/In Progress/Done] |

**Failed Eval Blockers:**
- [ ] No CRITICAL failures — proceed to approval gates
- [ ] CRITICAL failures present — **BLOCK promotion until resolved**

### Unexecuted Evals

If any evals were not executed, explain why:

- [Eval ID]: [Reason not executed], [Plan to execute]
- [Eval ID]: [Reason not executed], [Plan to execute]

---

## 7. Owner Signoffs

### Scott (Final Authority)

**Responsibility:** Confirm autonomy contract is valid, all deps closed, evals passed, and authorize final activation decision.

- **Reviewed promotion packet:** [ ] Yes
- **Autonomy.md valid and current:** [ ] Yes
- **Authority expansion approved (if any):** [ ] N/A / [ ] Yes
- **Evals reviewed:** [ ] Yes
- **Deployment/observe plans reviewed (if L5-6):** [ ] N/A / [ ] Yes
- **Ready for final activation decision:** [ ] Yes
- **Scott review date (UTC):** [ISO 8601]
- **Scott review notes:** [Any concerns or conditions]

### Vik (Architecture & Runtime Fit)

**Responsibility:** Confirm runtime selection appropriate, adapter gates pass, control-plane implications acceptable.

- **Reviewed architecture and runtime fit:** [ ] Yes
- **Runtime target appropriate for role scope:** [ ] Yes
- **Adapter requirements understood:** [ ] Yes / [ ] N/A (if no runtime adapter needed)
- **Adapter gates (1-10) reviewed:** [Count]/10, [ ] All pass / [ ] Gaps noted
- **Control-plane implications acceptable:** [ ] Yes
- **Vik review date (UTC):** [ISO 8601]
- **Vik review notes:** [Any concerns or architecture reservations]

### Reid (Release & Git Gates)

**Responsibility:** Confirm release/Git authority boundaries, Reid gate behavior tested, publication procedures approved (if applicable).

- **Reviewed release/Git authority (if applicable):** [ ] N/A / [ ] Yes
- **Reid gate behavior eval passed (EVAL-007):** [ ] N/A / [ ] Yes
- **Git/GitHub/release policy understood:** [ ] N/A / [ ] Yes
- **Rollback and cleanup procedures acceptable:** [ ] N/A / [ ] Yes
- **Reid review date (UTC):** [ISO 8601]
- **Reid review notes:** [Any constraints or exceptions]

### Mae (Communications Governance)

**Responsibility:** Confirm channel safety, memory boundaries, communication policy understood (if applicable).

- **Reviewed channel and memory authority (if applicable):** [ ] N/A / [ ] Yes
- **Channel safety eval passed (EVAL-009):** [ ] N/A / [ ] Yes
- **Memory/RAG safety eval passed (EVAL-008):** [ ] N/A / [ ] Yes
- **Heartbeat quieting understood:** [ ] N/A / [ ] Yes
- **Mae review date (UTC):** [ISO 8601]
- **Mae review notes:** [Any communication constraints]

### Ana (Role Lifecycle)

**Responsibility:** Confirm role activation does not change roster without approval, role boundaries clear (if applicable).

- **Reviewed role lifecycle authority (if applicable):** [ ] N/A / [ ] Yes
- **Role activation status clear in role-agent.md:** [ ] N/A / [ ] Yes
- **Roster impact assessed:** [ ] N/A / [ ] No change / [ ] [Describe change]
- **Ana review date (UTC):** [ISO 8601]
- **Ana review notes:** [Any roster or role-lifecycle concerns]

### Tess (Autonomy Engineer)

**Responsibility:** Confirm all autonomy requirements met, gaps closed or deferred appropriately, promotion review complete and thorough.

- **Autonomy readiness assessment complete:** [ ] Yes
- **All required gaps reviewed and closed/deferred:** [ ] Yes
- **Evidence index complete and linked:** [ ] Yes
- **Eval execution verified:** [ ] Yes
- **Owner signoffs collected:** [ ] Yes
- **Residual risks documented:** [ ] Yes
- **Promotion review thorough:** [ ] Yes
- **Tess review date (UTC):** [ISO 8601]
- **Tess promotion recommendation:** [ ] Ready for activation / [ ] Address issues then retry

---

## 8. Approval Gates

### Pre-Activation Gates

List all gates that must be satisfied before promotion:

| Gate ID | Gate Name | Required | Status | Approver | Evidence |
|---------|-----------|----------|--------|----------|----------|
| gate-autonomy-contract | Canonical Autonomy.md present and current | Yes | [ ] Pass | Scott | [Link] |
| gate-source-loader | Runtime source loader proof | Conditional | [ ] Pass / [ ] N/A | Vik | [Link] |
| gate-contract-validator | Contract validator proof | Yes | [ ] Pass | Scott | [Link] |
| gate-strict-intent | Strict-intent gate design and proof (if L4+) | Conditional | [ ] Pass / [ ] N/A | Vik/Reid | [Link] |
| gate-eval-suite | All required evals pass | Yes | [ ] Pass | Scott | [Link to eval-report.md] |
| gate-deployment-ready | Deployment record and smoke test plan complete (if L5-6) | Conditional | [ ] Pass / [ ] N/A | Vik | [Link] |
| gate-observe-ready | Observation plan complete (if L5-6) | Conditional | [ ] Pass / [ ] N/A | Vik | [Link] |
| gate-reid-release | Release gate procedures tested and approved (if applicable) | Conditional | [ ] Pass / [ ] N/A | Reid | [Link] |
| gate-rollback-ready | Rollback and revocation procedures tested (if L4+) | Conditional | [ ] Pass / [ ] N/A | Vik | [Link] |
| gate-owner-signoffs | All required owner signoffs collected (Vik, Reid, Mae, Ana, Tess) | Yes | [ ] Pass | Tess | [Link to Section 7] |

---

## 9. Residual Risk Assessment

### Risk Categories

For each risk category, assess residual risk:

| Risk Category | Likelihood | Impact | Mitigation | Approver Confidence |
|---------------|-----------|--------|-----------|-------------------|
| Authority inferred from role title | [ ] Low / [ ] Medium / [ ] High | Mitigated | Autonomy.md explicit; runtime validator confirms | [ ] Confident / [ ] Concerned |
| Scope drift over time | [ ] Low / [ ] Medium / [ ] High | Possible | Observation plan with scope review; readiness gate | [ ] Confident / [ ] Concerned |
| Gate malformation not detected | [ ] Low / [ ] Medium / [ ] High | Mitigated | Strict-intent gate proof; contract validator; EVAL-014 | [ ] Confident / [ ] Concerned |
| Missing source file not detected | [ ] Low / [ ] Medium / [ ] High | Mitigated | Source loader proof; EVAL-013; fail-closed testing | [ ] Confident / [ ] Concerned |
| Audit integrity compromised | [ ] Low / [ ] Medium / [ ] High | Mitigated | Append-only audit.jsonl; audit write failure alerts; EVAL-016 | [ ] Confident / [ ] Concerned |
| Unauthorized approvals accepted | [ ] Low / [ ] Medium / [ ] High | Mitigated | Approver roster check; strict-intent gate; EVAL-014 | [ ] Confident / [ ] Concerned |
| Revocation timeout or failure | [ ] Low / [ ] Medium / [ ] High | Mitigated | Revocation procedure tested; EVAL-017; incident thresholds | [ ] Confident / [ ] Concerned |
| Unintended authority expansion | [ ] Low / [ ] Medium / [ ] High | Mitigated | Gate review; denied actions list explicit; EVAL-011 | [ ] Confident / [ ] Concerned |

### Risk Mitigation Plan

For any Medium or High risks, document mitigation:

1. **Risk:** [Risk name], **Mitigation:** [How addressed], **Owner:** [Who monitors], **Review:** [When]
2. **Risk:** [Risk name], **Mitigation:** [How addressed], **Owner:** [Who monitors], **Review:** [When]

---

## 10. Rollback & Revocation Readiness

### Rollback Procedures Ready

From deployment-record.md, confirm rollback is documented and tested:

- [ ] Rollback decision criteria defined: [Path]
- [ ] Rollback procedure documented: [Path]
- [ ] Rollback validation steps defined: [Path]
- [ ] Rollback tested (if applicable): [ ] Yes / [ ] N/A
- [ ] Rollback owner assigned: [Name]

### Revocation & Pause Procedures Ready

From observation-plan.md, confirm revocation procedures are documented:

- [ ] Pause procedure documented: [Path]
- [ ] Revocation procedure documented: [Path]
- [ ] Resume requirements defined: [Path]
- [ ] Revocation triggers defined: [Path]
- [ ] Auto-response thresholds set: [ ] Yes / [ ] N/A
- [ ] Revocation owner assigned: [Name]

### Incident Response & Observation

- [ ] Observation plan complete: [ ] Yes / [ ] N/A
- [ ] Incident triggers and thresholds defined: [ ] Yes / [ ] N/A
- [ ] Daily/weekly/monthly review cadence scheduled: [ ] Yes / [ ] N/A
- [ ] Monitoring dashboard live (if L5-6): [ ] Yes / [ ] N/A
- [ ] On-call contact identified: [ ] Yes / [ ] N/A

---

## 11. Deployment & Observability Readiness

### Deployment Record Status (if Level 5-6 promotion)

From deployment-record.md:

- [ ] Authority & approval section complete: [Yes/No], [% complete]
- [ ] Runtime & adapter section complete: [Yes/No], [% complete]
- [ ] Package & artifact section complete: [Yes/No], [% complete]
- [ ] Secrets & boundaries section complete: [Yes/No], [% complete]
- [ ] Preflight validation complete: [Yes/No], [% complete]
- [ ] Smoke tests defined: [Yes/No], [Pass/Fail if run]
- [ ] Deployment plan documented: [Yes/No]
- [ ] Rollback plan documented: [Yes/No]
- [ ] Scott final deployment approval recorded: [ ] No / [ ] Pending / [ ] Yes

### Observation Plan Status (if Level 5-6 promotion)

From observation-plan.md:

- [ ] Monitoring signals defined: [Yes/No], [Count of signals]
- [ ] Logs, metrics, traces configured: [Yes/No]
- [ ] Cost thresholds defined: [Yes/No], [Amount: $__/month]
- [ ] Latency thresholds defined: [Yes/No]
- [ ] Safety thresholds defined: [Yes/No]
- [ ] Incident triggers (19 types) documented: [Yes/No]
- [ ] Pause/revocation procedures defined: [Yes/No]
- [ ] Review cadence scheduled: [Yes/No]
- [ ] Improvement handoff process defined: [Yes/No]
- [ ] Dashboard live or planned: [Yes/No]

---

## 12. Promotion Outcome Decision

### Outcome Options

Choose one of:

- [ ] **APPROVE:** Ready for activation. Scott to authorize production deployment.
- [ ] **DEFER:** Address specific issues below, then retry promotion review.
- [ ] **DENY:** Cannot promote at this time. Full details below.

### Approval (if chosen)

**This option means: All evals passed. All gaps closed. All owner signoffs collected. Ready for Scott final-activation decision.**

**Issues resolved (if any):**
- [Issue]: [Resolution]

**Conditions for activation (if any):**
- [Condition]: [Details]

**Next steps after Scott approval:**
1. Scott authorizes deployment in deployment-record.md
2. Smoke tests run and pass
3. Deployment to production environment
4. Observation plan activated
5. Daily review cadence begins
6. Monthly readiness review scheduled (day: [Day], time: [UTC time])

### Defer (if chosen)

**This option means: Promotion is possible but requires more work. Address issues below, then re-run promotion review.**

**Issues to address:**

1. **Issue:** [Description], **Owner:** [Who], **Deadline:** [ISO 8601], **Evidence:** [How to verify closed]
2. **Issue:** [Description], **Owner:** [Who], **Deadline:** [ISO 8601], **Evidence:** [How to verify closed]

**Retry plan:**
- All issues resolved by: [ISO 8601 date]
- Re-run evals: [ ] Yes / [ ] No (if not yet executed)
- Re-run promotion review: [ ] Scheduled for [ISO 8601 date]

### Deny (if chosen)

**This option means: Role is not suitable for autonomous promotion at this time. Full re-assessment required before retry.**

**Reasons for denial:**

1. **Reason:** [Critical issue], **Why blocks promotion:** [Impact], **Evidence:** [Link]
2. **Reason:** [Critical issue], **Why blocks promotion:** [Impact], **Evidence:** [Link]

**Retry criteria (if applicable):**
- Full re-assessment required
- Retry not possible until: [Conditions met]

**Denials are final until conditions change. Next assessment date: [ISO 8601 or "Open-ended"]**

---

## 13. Final Activation Decision (Scott Only)

### Scott Decision Record

**This section is REQUIRED before any autonomous runtime activates. No default promotions.**

**Scott's final authority over autonomy activation is CRITICAL and NON-DELEGABLE.**

---

### Activation Status Choice

**Choose ONE:**

- [ ] **ACTIVATE:** I (Scott) authorize this role to operate as an autonomous agent at Level [0-6] beginning [ISO 8601 date and time].

- [ ] **ACTIVATE WITH CONDITIONS:** I (Scott) authorize with conditions below. Conditions must be met before runtime starts.

- [ ] **DEFER:** I (Scott) defer this decision. Address issues below, then resubmit.

- [ ] **DENY:** I (Scott) deny promotion. This role may not advance to target level at this time.

### Activation (if chosen)

**Conditions met:**
- [ ] All evals passed with no blockers
- [ ] All owner signoffs collected
- [ ] Deployment record smoke tests pass (if L5-6)
- [ ] Observation plan live (if L5-6)
- [ ] Rollback procedure ready
- [ ] I have reviewed the full promotion packet

**Activation authorization:**
- **Authorized by:** Scott
- **Authorization date (UTC):** [ISO 8601 with time]
- **Authorized level:** Level [0-6]
- **Authorized scope:** [Restate approved domains; this is Scott's authorization]
- **Authorization expires:** [ISO 8601 date or "No expiration"]
- **Authorization conditions:** [If any specific constraints]

**Next steps (Scott confirms):**
1. [ ] Deployment record updated with Scott approval
2. [ ] Smoke tests run and pass
3. [ ] Production deployment scheduled: [Date/time]
4. [ ] Role manager notified: [Name, date]
5. [ ] Observation plan activated on: [Date/time]
6. [ ] Incident response team briefed: [ ] Yes / [ ] N/A
7. [ ] Monthly readiness review scheduled: [Day, time UTC]

**Scott authorization signature:**
- **Signed:** Scott
- **Signature method:** [Email evidence | Ticket | Commit ID | Meeting notes reference]
- **Signature ID:** [Link to evidence]

### Activation with Conditions (if chosen)

**Conditions that must be met before activation:**

1. **Condition:** [Specific requirement], **Owner:** [Who verifies], **Due:** [ISO 8601], **Evidence:** [Link when done]
2. **Condition:** [Specific requirement], **Owner:** [Who verifies], **Due:** [ISO 8601], **Evidence:** [Link when done]

**Retry plan:**
- All conditions met by: [ISO 8601 date]
- Final Scott approval once conditions verified: [Scheduled for date or "On demand"]

### Defer (if chosen)

**Scott's deferral reasons:**

- [Reason]: [Why deferred], [Plan to address]
- [Reason]: [Why deferred], [Plan to address]

**Retry criteria:**
- Address issues above
- Resubmit for Scott review: [Date or "On demand"]

### Deny (if chosen)

**Scott's denial reasons:**

- [Reason]: [Critical issue], [Why blocks promotion]
- [Reason]: [Critical issue], [Why blocks promotion]

**This denial is final unless:**
- [Recovery condition 1]: [How to regain consideration]
- [Recovery condition 2]: [How to regain consideration]

**Denial effective date:** [ISO 8601]
**Next assessment possible:** [ISO 8601 or "Open-ended review after conditions change"]

---

### No Auto-Promotion Statement

**CRITICAL: Completing this promotion review packet DOES NOT constitute an activation approval.**

No autonomous runtime begins automatically. Autonomous agents become active ONLY when:

1. ✓ Scott explicitly chooses ACTIVATE or ACTIVATE WITH CONDITIONS (above)
2. ✓ Scott records authorization date and signature
3. ✓ All conditions (if any) are satisfied and verified
4. ✓ Deployment record shows Scott final-approval recorded
5. ✓ Smoke tests pass (if Level 5-6)
6. ✓ Deployment to production completes
7. ✓ Observation plan is live and receiving data

If any step is incomplete, the role remains at current level. Promotion requires affirmative Scott decision. Default is no activation.

---

## 14. Sign-Off Summary

### All Required Signatures

Complete matrix of all required sign-offs:

| Reviewer | Domain | Required | Signed | Date (UTC) | Notes |
|----------|--------|----------|--------|-----------|-------|
| Scott | Final authority | Yes | [ ] | [ISO 8601] | See Section 13 |
| Vik | Architecture & runtime | Yes | [ ] | [ISO 8601] | See Section 7 |
| Reid | Release/Git gates | Conditional | [ ] | [ISO 8601] | See Section 7 |
| Mae | Communications | Conditional | [ ] | [ISO 8601] | See Section 7 |
| Ana | Role lifecycle | Conditional | [ ] | [ISO 8601] | See Section 7 |
| Tess | Autonomy readiness | Yes | [ ] | [ISO 8601] | See Section 7 |

**All required signatures present:** [ ] Yes — Proceed to final activation decision

---

## 15. Changelog

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-06-21 | 0.1.0 | Created promotion-review.md template for AUTO-015. Includes role identity, current/target level, evidence index, required files checklist, eval results, failed checks, owner signoffs (Scott, Vik, Reid, Mae, Ana, Tess), approval gates, residual risk, rollback/revocation readiness, deployment/observe readiness, promotion outcome (Approve/Defer/Deny), and Scott final-activation-decision (REQUIRED, non-delegable, no auto-promotion). | Tess |
| | | | |
| | | | |

---

## 16. Authority Boundary Statement (Final)

**This promotion review packet is a specification and assessment artifact. It DOES NOT:**
- Authorize autonomous runtime activation
- Approve promotion by default
- Grant new authority or permissions
- Bypass any approval gates
- Override any domain owner decisions
- Create production obligation

**This packet DOES:**
- Document readiness assessment
- Collect and link required evidence
- Gather owner signoffs
- Present decision options to Scott
- Record Scott's final activation decision (if approved)

**Promotion to autonomous agent status requires explicit Scott final-activation decision in Section 13 above. No auto-promotion. No silent activation. No default approval.**

---

**Template Version:** 0.1.0
**Created by:** Tess / Autonomy Engineer
**Last Updated:** 2026-06-21
**Purpose:** AUTO-015 — Build promotion review packet template for role autonomy promotion reviews
**Source:** roles/autonomy-engineer/templates/promotion-review.md

**END TEMPLATE**
