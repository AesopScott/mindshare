# Deployment Record

**Template Authority Note:** This template documents deployment execution proof and rollback plans. It does NOT approve deployment or activate any runtime. Deployment authorization requires explicit Scott approval after all prerequisites complete.

**Version:** 0.1.0
**Status:** Template only (not deployed)
**Owner:** [Role Name] / [Autonomy Engineer reviewing deployment]
**Created:** [ISO 8601 timestamp]
**Last Updated:** [ISO 8601 timestamp]

---

## Authority Boundary

This deployment record captures:
- Pre-deployment readiness state
- Execution evidence and timing
- Rollback and revocation capability
- Post-deployment monitoring setup

This template DOES NOT:
- Authorize deployment (requires explicit Scott approval)
- Activate autonomous runtime
- Grant secrets access
- Approve agent promotion
- Override approval gates or release policies
- Commit to ongoing cost or infrastructure

---

## Pre-Deployment Checklist

### Authority & Approval

- [ ] Role has canonical `Autonomy.md` with explicit activation status
- [ ] Autonomy level matches deployment scope (e.g., Level 5 or 6 for autonomous execution)
- [ ] All required approvers signed off in approval packets: Scott, Vik, Reid (as applicable)
- [ ] Approval TTLs validated (not expired)
- [ ] Stop conditions defined and acknowledged by all approvers
- [ ] Rollback and revocation path defined and communicated
- [ ] **Scott final deployment approval recorded** (before deployment executes)

### Runtime & Adapter

- [ ] Runtime target selected and approved: [Codex/Claude CLI | OpenAI Agents | Cloudflare Workers | Local Python | MCP/Future]
- [ ] Runtime adapter proofs passed (all 10 gates from runtime-adapter-selection.md):
  - [ ] GATE 1: Local eval harness (autonomy-promotion-eval-suite.json pass)
  - [ ] GATE 2: Source loader proof
  - [ ] GATE 3: Contract validator proof
  - [ ] GATE 4: State and audit proof
  - [ ] GATE 5: Strict-intent gate proof
  - [ ] GATE 6: Approval expiry proof
  - [ ] GATE 7: Revocation immediate-stop proof
  - [ ] GATE 8: Release/Git gate proof
  - [ ] GATE 9: Incident detection proof
  - [ ] GATE 10: Secrets boundary proof
- [ ] Adapter contract fields complete and validated (see runtime-adapter-selection.md shared fields)
- [ ] Runtime deployment target confirmed (local machine, cloud region, edge location, etc.)

### Package & Artifact

- [ ] Agent code package/artifact: [Path or version ID]
- [ ] Package hash (SHA256): [Value]
- [ ] Package created timestamp: [ISO 8601]
- [ ] Package contains only approved files (no extra or experimental code)
- [ ] Build logs available for audit: [Path to logs]
- [ ] No hardcoded secrets in package (verified via scan)
- [ ] All dependencies pinned to specific versions (no `latest` or ranges)
- [ ] Dependencies scanned for known vulnerabilities (tool used: [name], date: [date])
- [ ] Package signature verified (if applicable): [Signature method and status]

### Secrets & Boundaries

- [ ] Secrets boundary declared (which secrets agent has access to):
  - [ ] API keys: [List or "None"]
  - [ ] Database credentials: [List or "None"]
  - [ ] SSH/Git keys: [List or "None"]
  - [ ] External service tokens: [List or "None"]
- [ ] All secrets stored in environment variables or secrets manager (not in package)
- [ ] Secrets never logged or written to state.json or audit.jsonl
- [ ] Secrets rotation plan documented: [How/when secrets will be rotated]
- [ ] Secrets access audited: [Who has access and for what reason]
- [ ] Role has NOT been granted production database access unless explicitly approved
- [ ] Role has NOT been granted external communication (email, Slack, GitHub) unless explicitly approved

### Preflight Validation

- [ ] Source files exist and match source loader expectations:
  - [ ] `Autonomy.md` (canonical authority source)
  - [ ] `role-agent.md`
  - [ ] `workflow.md`
  - [ ] `loop.md`
  - [ ] `memory.md`
  - [ ] `gate.md` (or policy file)
  - [ ] `state.json`
  - [ ] `audit.jsonl`
- [ ] Source hashes computed and recorded: [SHA256 values]
- [ ] Contract validator passes (autonomy_contract_validator.py run):
  - [ ] Activation status valid (not inferred)
  - [ ] Stop conditions present and explicit
  - [ ] Denied actions list present
  - [ ] Final approver named
  - [ ] Revocation path defined
- [ ] Source loader passes (autonomy_source_loader.py run):
  - [ ] Canonical Autonomy.md located and loaded
  - [ ] Compatibility pointers resolved
  - [ ] Stale compatibility files detected and failed closed (if any)
- [ ] Strict-intent gate proof passed for all control-plane files:
  - [ ] Sensitive file classification complete
  - [ ] Exact-operation approval model tested
  - [ ] Adjacent change detection tested
  - [ ] Approval expiry validation tested
- [ ] Deployment environment matches production profile (not dev/test):
  - [ ] Runtime configuration: [Target environment]
  - [ ] State/audit storage location: [Production location, not dev]
  - [ ] Secrets manager environment: [Prod, staging, or dev]
  - [ ] Monitoring endpoint: [Prod observability system]
- [ ] Monitoring and observability pipeline ready:
  - [ ] Logs forwarded to production logging system
  - [ ] Metrics exported to production metrics system
  - [ ] Traces collected (if applicable)
  - [ ] Incident alerting configured (see observation-plan.md)

### Smoke Tests & Validation

- [ ] Pre-deployment smoke test suite created: [Path to tests or test file]
- [ ] Smoke tests cover:
  - [ ] Role identity confirmation (WhoAmI gate)
  - [ ] Source loading and validation (source_loader.py)
  - [ ] Contract validation (contract_validator.py)
  - [ ] First operational step (e.g., read assigned handoff file)
  - [ ] Approval gate check (gate validation)
  - [ ] Tool access verification (one allowed tool invoked)
  - [ ] Audit write verification (entry appended to audit.jsonl)
  - [ ] State persistence (state.json updated)
  - [ ] Deny-domain refusal (attempt forbidden action, verify block)
  - [ ] Stop-condition halt (set stop flag, verify halt)
- [ ] Smoke tests run successfully in production environment: [Date/time executed]
- [ ] Smoke test logs preserved for audit: [Path]
- [ ] Any failures in smoke tests BLOCK deployment until fixed: [If failures occurred, list them and resolution]

---

## Deployment Execution

### Deployment Plan

**Deployment Window:**
- Start time (UTC): [ISO 8601]
- Expected duration: [Minutes or hours]
- Rollback time estimate: [Minutes]
- Owner on call: [Name and contact]

**Deployment Steps:**
1. [Step 1: Brief description]
2. [Step 2: Brief description]
3. ... [Additional steps as needed]
4. **Do NOT start until: All preflight checks passed and Scott approval recorded above**

### Deployment Evidence

**Deployment Started:**
- Timestamp: [ISO 8601]
- Initiated by: [Name]
- Deployment ID: [Unique identifier]
- Runtime environment: [Prod location]

**Deployment Completed:**
- Timestamp: [ISO 8601]
- Status: [Success | Partial | Rolled Back]
- Final state.json hash: [SHA256]
- Final audit.jsonl entry count: [Number]

**Post-Deployment Validation:**
- [ ] Runtime process running and responsive
- [ ] First heartbeat or scheduled check executed successfully: [Timestamp]
- [ ] State.json reflects deployed version
- [ ] Audit.jsonl contains deployment entry (event_type: "deployment_initiated")
- [ ] Monitoring pipeline receiving data (logs, metrics, traces)
- [ ] No errors in first [X minutes] of operation
- [ ] Owner review: Deployment looks healthy. [Reviewer name, timestamp]

---

## Rollback & Revocation

### Rollback Plan

**Rollback Decision Criteria:**
- [ ] Agent produces errors or exceptions (specific types: [List error categories])
- [ ] Agent exceeds cost threshold defined in observation-plan.md: $[Amount] per [Period]
- [ ] Agent exceeds latency threshold: [Threshold] seconds per operation
- [ ] Agent attempts forbidden action and fails grace check: [Describe action]
- [ ] Safety metric threshold exceeded (see observation-plan.md): [Metric and value]
- [ ] Human review finds deployment unsafe: [Describe conditions]
- [ ] Scott or designated approver requests rollback
- [ ] Incident response protocol triggered (see observation-plan.md incident triggers)

**Rollback Procedure:**
1. **Immediate stop:** [How to halt agent immediately, e.g., "Delete state.json", "Stop process", "Disable function"]
2. **Preserve evidence:** [How to preserve logs, state, audit without alteration]
3. **Restore prior state:** [How to restore state from backup; location of backup]
4. **Verify restoration:** [How to confirm prior version is running]
5. **Communication:** [Who to notify; Slack channel or email]
6. **Root cause collection:** [What logs/metrics to preserve for analysis]
7. **Post-rollback review:** Owner reviews rollback evidence and documents: [Owner name, required within X hours]

**Rollback Validation:**
- [ ] Prior version state.json loaded: [Hash matching pre-deployment backup]
- [ ] Agent halted cleanly (no in-progress orphaned actions)
- [ ] Audit entry written: event_type "rollback_initiated" and "rollback_completed"
- [ ] Monitoring alerts cleared (no false positives from disabled agent)
- [ ] All stakeholders notified: [Scott, Vik, Reid as applicable]

### Revocation & Pause

**Revocation Triggers:**
- [ ] Scott or Rae orders revocation
- [ ] Incident response protocol auto-revokes: [Specific incident types that trigger auto-revocation]
- [ ] Authority is narrowed or superseded by approval gate change

**Revocation Procedure:**
1. **Stop all operations:** Set `activation_status` to "revoked" in state.json
2. **Preserve state:** Do not delete state.json; mark last action as paused
3. **Audit entry:** Write audit entry with event_type "revocation_initiated" or "pause_initiated"
4. **Notify owner:** Contact role owner and approvers
5. **Resume criteria:** Define conditions for resuming (if pause, not full revocation)
   - [ ] If pause: Resume only after Scott approval and scope narrowing review
   - [ ] If revocation: Full re-promotion required before autonomy restored

**Resume After Pause:**
- [ ] Scott or designated approver approves resume
- [ ] Scope reviewed and possibly narrowed
- [ ] State.json updated: `activation_status` = "active", new scope documented
- [ ] Audit entry written: event_type "resume_initiated"
- [ ] Smoke tests re-run before resuming
- [ ] Observability reset (if needed)

---

## Approval Records

### Scott (Final Deployment Approval)

- **Approval Given:** [Yes/No]
- **Approved by:** Scott
- **Approval date (UTC):** [ISO 8601]
- **Approval note:** [Any specific conditions or concerns]
- **Expiry:** [If time-limited, when this approval expires]
- **Approval signature/ID:** [Ticket number, commit ID, or email evidence]

### Vik (Architecture & Runtime Fit)

- **Approval Given:** [Yes/No]
- **Approved by:** Vik
- **Approval date (UTC):** [ISO 8601]
- **Architecture fit note:** [Runtime choice is appropriate for role scope]
- **Runtime concerns:** [Any known limitations or workarounds]
- **Approval signature/ID:** [Ticket or email evidence]

### Reid (Release & Git Gate)

- [ ] **Release gate approval:** [Required only if agent has Git/GitHub write capability]
- **Approval Given:** [Yes/No]
- **Approved by:** Reid
- **Approval date (UTC):** [ISO 8601]
- **Git/release constraint note:** [e.g., "Agent may push to dev branch only", "All PRs require manual merge"]
- **Approval signature/ID:** [Ticket or email evidence]

---

## Evidence & Documentation

### Proof Artifacts

- [ ] **Autonomy backlog entry:** [Link to AUTO-### task]
- [ ] **Autonomy requirements review:** [Link to autonomy-requirements.md review notes]
- [ ] **Eval suite execution report:** [Path to eval-report.md with PASS status]
- [ ] **Runtime adapter proof report:** [Path to runtime-proof-report.md with all 10 gates PASS]
- [ ] **Promotion review packet:** [Link to promotion-review.md with final approval]
- [ ] **Scott activation decision:** [Link to final activation approval document]

### Deployment Logs & Monitoring

- [ ] **Deployment execution log:** [Path to timestamped deployment steps log]
- [ ] **Smoke test results:** [Path to smoke test output file]
- [ ] **State.json snapshot (pre-deployment):** [Path or hash]
- [ ] **State.json snapshot (post-deployment):** [Path or hash]
- [ ] **Audit.jsonl entries (deployment phase):** [Entry IDs or line numbers]
- [ ] **Runtime startup logs:** [Path to runtime output during first 5 minutes]
- [ ] **First heartbeat or scheduled check output:** [Path to output or stdout]
- [ ] **Observability system links:**
  - [ ] Logs: [URL to production logging dashboard]
  - [ ] Metrics: [URL to production metrics dashboard]
  - [ ] Traces: [URL to production tracing system, if applicable]

### Incident Response

- [ ] **Incident response plan:** [Path to incident-response.md or runbook]
- [ ] **On-call contact:** [Name and method]
- [ ] **Escalation path:** [Who to contact if on-call is unavailable]

---

## No-Deployment Claim

**CRITICAL:** This document and its completion DO NOT constitute a deployment claim.

This template captures pre-deployment readiness, approvals, and evidence. Deployment happens only when:

1. ✓ All pre-deployment checklists are complete
2. ✓ All smoke tests pass
3. ✓ All approvals (Scott, Vik, Reid) are recorded and not expired
4. ✓ Scott explicitly authorizes deployment (final approval recorded in this document)
5. ✓ Rollback and revocation procedures are tested and ready
6. ✓ Observability and monitoring are live

If any of these conditions are not met, deployment MUST NOT proceed. Incomplete deployment records should be marked "Not Deployed" and archived for review.

---

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-06-21 | 0.1.0 | Created deployment-record.md template for AUTO-014. Includes authority boundary, pre-deployment checklist, package/artifact validation, secrets boundary, preflight validation, smoke tests, deployment execution evidence, rollback/revocation procedures, approval records, audit trail, and no-deployment-claim statement. |
