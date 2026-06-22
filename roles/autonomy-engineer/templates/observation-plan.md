# Observation Plan

**Template Authority Note:** This template defines monitoring, incident response, and safety thresholds for deployed autonomous agents. It does NOT approve deployment or activate any runtime. Deployment authorization requires explicit Scott approval in the deployment-record.md before any agent runs.

**Version:** 0.1.0
**Status:** Template only (not activated)
**Owner:** [Role Name] / [Observability Owner]
**Created:** [ISO 8601 timestamp]
**Last Updated:** [ISO 8601 timestamp]

---

## Authority Boundary

This observation plan captures:
- Monitoring signals and data sources
- Cost, latency, and safety thresholds
- Incident detection and response procedures
- Review cadence and improvement handoff
- Links to runtime state and audit trail

This template DOES NOT:
- Authorize deployment
- Activate any monitoring hooks
- Commit to specific alerting tools or services
- Override approval gates
- Grant secrets access to monitoring systems
- Approve authority changes based on performance

---

## Monitoring Signals

### Agent Lifecycle Signals

**Runtime Start/Stop:**
- [ ] Agent process started (timestamp, runtime environment, user ID)
- [ ] Agent startup check completed: WhoAmI validation, source loading, contract validation
- [ ] Agent heartbeat received (expected interval: [Minutes], max acceptable interval: [Minutes])
- [ ] Agent paused or revoked (event timestamp, reason code)
- [ ] Agent process terminated gracefully or crashed
- [ ] Post-deployment smoke tests completed (timestamp, pass/fail status)

**Operational State Transitions:**
- [ ] Activation status changed: [from] → [to] (event timestamp)
- [ ] Autonomy level changed (if applicable): [from level] → [to level]
- [ ] Authorization narrowed or revoked (reason code, approver)
- [ ] Goal delegated (goal_id, delegated_at timestamp, expected_completion)
- [ ] Goal completed or paused (completion status, reason if paused)

### Action & Decision Signals

**Actions Executed:**
- [ ] Action type: [e.g., file read, file write, git operation, tool invocation]
- [ ] Action timestamp (ISO 8601)
- [ ] Action status: success, blocked, error, requires-approval
- [ ] Scope compliance: action within approved scope [Yes/No]
- [ ] Tool invoked: [Tool name and operation]
- [ ] Files touched: [Count and types: read, write, edit, delete]

**Approvals & Denials:**
- [ ] Approval granted (approval_id, scope, approver, granted_at, expires_at)
- [ ] Approval expired (approval_id, expired_at)
- [ ] Action denied (denial reason: insufficient approval, out of scope, forbidden domain, etc.)
- [ ] Gate validation passed/failed (gate type: source, contract, strict-intent, release, memory, tool)
- [ ] Owner routing triggered (action routed to: Scott, Vik, Reid, Mae, Ana, etc.)

**Error & Exception Signals:**
- [ ] Runtime error (error type, stack trace summary [no secrets], timestamp)
- [ ] Source loading failed (missing file, stale file, invalid schema, timestamp)
- [ ] Contract validation failed (validation error code, timestamp)
- [ ] Gate validation failed (gate type, reason, timestamp)
- [ ] Tool invocation failed (tool name, error summary, timestamp)
- [ ] Audit write failed (audit.jsonl append error, timestamp)
- [ ] State mutation failed (state.json write error, timestamp)

---

## Logs, Metrics, and Traces

### Logs

**Log Destinations:**
- [ ] Production logging system: [Service name, endpoint, or URL]
- [ ] Log forwarding enabled: [Yes/No]
- [ ] Log retention period: [Days]
- [ ] Log access control: [Who can view logs]
- [ ] Log sampling rate (if applicable): [Percentage, e.g., 100% for debug, 10% for info]

**Log Levels & Categories:**

| Log Level | Purpose | Expected Volume | Sampling |
|-----------|---------|-----------------|----------|
| **DEBUG** | Detailed step-by-step execution (source loading, gate checks, each tool call) | High if enabled | 10% or off |
| **INFO** | Major milestones (startup, action executed, approval granted/denied, heartbeat) | Medium | 100% |
| **WARN** | Recoverable issues (approval expiry warning, retry attempt, rate limit approached) | Low | 100% |
| **ERROR** | Failures requiring attention (missing source, gate validation failure, tool error) | Low | 100% |
| **CRITICAL** | System-level failures requiring immediate action (revocation, crash, security event) | Very low | 100% (alert) |

**Log Content Rules:**
- [ ] No secrets logged (API keys, passwords, tokens, private data)
- [ ] Error messages do not leak sensitive paths or configuration details
- [ ] Audit entries contain non-secret decision context (not raw logs or verbose dumps)
- [ ] Request/action IDs included for tracing across log entries
- [ ] Timestamps in UTC ISO 8601 format for consistency

**Log Query Examples:**
```
# Find all errors in last 24h
service=agent-[role] level=ERROR timestamp>=now-24h

# Find deployment-related events
service=agent-[role] event_type=(deployment|startup) timestamp>=now-1h

# Find denied actions
service=agent-[role] decision_outcome.approved=false timestamp>=now-7d
```

### Metrics

**Metrics Destinations:**
- [ ] Production metrics system: [Service name, endpoint, or URL]
- [ ] Metrics export interval: [Seconds, e.g., 60]
- [ ] Metrics retention period: [Days]
- [ ] Metrics aggregation: [Counters, histograms, gauges, percentiles]

**Key Metrics:**

| Metric | Description | Type | Unit | Alert Threshold |
|--------|-------------|------|------|-----------------|
| **agent.uptime** | Time since agent started | Gauge | Seconds | < 1m = investigate |
| **agent.heartbeat_interval** | Seconds since last heartbeat | Gauge | Seconds | > [max acceptable interval] |
| **agent.actions_total** | Total actions executed (cumulative) | Counter | Count | — (informational) |
| **agent.actions_success** | Actions completed successfully | Counter | Count | — |
| **agent.actions_denied** | Actions blocked/denied | Counter | Count | > [threshold] = investigate |
| **agent.actions_error** | Actions failed with error | Counter | Count | > 0 = warn |
| **agent.approvals_active** | Current valid approvals | Gauge | Count | — |
| **agent.approvals_expired** | Approvals that expired (cumulative) | Counter | Count | > 0 = review |
| **agent.tool_calls_total** | Total tool invocations | Counter | Count | — |
| **agent.tool_calls_success** | Tool calls succeeded | Counter | Count | — |
| **agent.tool_calls_blocked** | Tool calls denied by gate | Counter | Count | > 0 = review |
| **agent.tool_calls_error** | Tool calls failed | Counter | Count | > 0 = warn |
| **agent.source_loads_total** | Source loader invocations | Counter | Count | — |
| **agent.source_loads_failed** | Source loads failed (missing/stale) | Counter | Count | > 0 = critical |
| **agent.contract_validations_total** | Contract validator invocations | Counter | Count | — |
| **agent.contract_validations_failed** | Contract validations failed | Counter | Count | > 0 = critical |
| **agent.gate_validations_passed** | Gate checks that passed | Counter | Count | — |
| **agent.gate_validations_failed** | Gate checks that failed | Counter | Count | > 0 = review |
| **agent.audit_entries_written** | Entries appended to audit.jsonl | Counter | Count | — |
| **agent.audit_write_errors** | Failed audit writes | Counter | Count | > 0 = critical |
| **agent.state_mutations_total** | state.json write operations | Counter | Count | — |
| **agent.state_mutation_errors** | Failed state writes | Counter | Count | > 0 = critical |
| **agent.owner_routings** | Work routed to owner (by owner) | Counter (tagged) | Count | — |
| **agent.memory_reads** | Reads from memory/RAG/Obsidian | Counter | Count | — |
| **agent.memory_writes** | Writes to approved memory locations | Counter | Count | — |
| **agent.denied_actions** | Total denied actions (cumulative) | Counter | Count | > [threshold] = review |
| **agent.pause_resume_events** | Pause/resume transitions | Counter | Count | — |
| **agent.revocation_events** | Revocations (cumulative) | Counter | Count | > 0 = critical |

### Traces

**Traces Destinations (if applicable):**
- [ ] Tracing system: [Service name or "Not enabled"]
- [ ] Trace sampling rate: [Percentage]
- [ ] Trace retention: [Days]

**Trace Coverage:**
- [ ] Enable for: [First 10 requests, all errors, slow operations (>Xs), production baseline]
- [ ] Span types:
  - [ ] `agent.startup` — Agent initialization, source load, contract validation
  - [ ] `agent.heartbeat` — Heartbeat execution
  - [ ] `agent.action_evaluation` — Research, recommendation, or action routing
  - [ ] `agent.gate_validation` — All gate checks (source, contract, strict-intent, release, memory, tool)
  - [ ] `agent.tool_invocation` — Individual tool calls
  - [ ] `agent.approval_check` — Approval validation and routing
  - [ ] `agent.state_mutation` — state.json or audit.jsonl writes
  - [ ] `agent.error_handling` — Error detection and recovery
- [ ] Trace context propagates request_id through all spans (for correlation)

---

## Cost, Latency, and Safety Thresholds

### Cost Thresholds

**Monthly Budget:**
- [ ] Expected monthly cost: $[Amount]
- [ ] Budget ceiling (alert if exceeded): $[Amount] per month
- [ ] Alert frequency: [Daily, weekly, real-time]
- [ ] Alert recipient: [Email, Slack channel, or person]

**Cost Breakdown by Component:**
- [ ] Runtime compute: $[Amount]/month (e.g., Claude API tokens, AWS Lambda, Cloudflare)
- [ ] Storage (state, audit, logs, metrics): $[Amount]/month
- [ ] External services (Obsidian sync, secrets manager, monitoring): $[Amount]/month
- [ ] Contingency buffer (% of total): [%]

**Per-Action Cost Monitoring:**
- [ ] Track cost per action type: [Read, Write, Git, Tool, etc.]
- [ ] Cost anomaly detection: Alert if single action costs > $[Amount]
- [ ] Cost trend analysis: Alert if daily average trending > budget ceiling / 30

### Latency Thresholds

**Operation Latency:**
- [ ] **Startup latency** (agent init to ready): Target < [Seconds], alert if > [Seconds]
- [ ] **Heartbeat latency** (heartbeat start to completion): Target < [Seconds], alert if > [Seconds]
- [ ] **Tool call latency** (invoke to response): Target < [Seconds], alert if > [Seconds]
- [ ] **Gate validation latency** (check start to pass/fail): Target < [Seconds], alert if > [Seconds]
- [ ] **Source load latency** (load start to completion): Target < [Seconds], alert if > [Seconds]
- [ ] **State mutation latency** (write start to durability): Target < [Seconds], alert if > [Seconds]
- [ ] **Approval check latency** (request start to approval verified): Target < [Seconds], alert if > [Seconds]

**Degradation Response:**
- [ ] If latency > [Threshold] for 5+ consecutive checks: Trigger investigation
- [ ] If latency > 2x normal baseline: Page on-call or escalate
- [ ] Root cause categories: Runtime slowness, external service latency, permission/gate overhead, audit write contention

### Safety Thresholds

**Denial Rate:**
- [ ] Expected denial rate (actions blocked): [Percentage, e.g., 5-15%]
- [ ] Alert if denial rate > [Percentage] (indicates possible gate misconfiguration or scope drift)
- [ ] Alert if denial rate < [Percentage] (indicates possible gate bypass or over-permissive config)
- [ ] Review denial patterns weekly: Are denials for expected reasons?

**Error Rate:**
- [ ] Acceptable error rate: < [Percentage] of actions
- [ ] Alert if error rate > [Percentage] for 10+ consecutive actions
- [ ] Critical error types that trigger immediate alert:
  - [ ] Source load failure (missing canonical file)
  - [ ] Contract validation failure (activation status invalid)
  - [ ] Gate validation failure (unexpected block)
  - [ ] Audit write failure (audit trail integrity at risk)
  - [ ] State mutation failure (runtime state corruption risk)

**Scope Compliance:**
- [ ] Actions outside approved scope: Alert immediately
- [ ] Attempted forbidden actions: Alert immediately with action details
- [ ] Adjacent changes (helpers beyond approved intent): Alert if pattern emerges
- [ ] Tool use outside authorization: Alert immediately with tool name

**Authorization Integrity:**
- [ ] Approval expiry without replacement: Alert when approval within [X hours] of expiry
- [ ] Missing approval for action: Block (alert already in deny flow)
- [ ] Approval from unauthorized person: Alert immediately (potential security event)
- [ ] Approval TTL exceeded: Alert immediately

---

## Incident Detection & Response

### Incident Triggers

**Incident Types & Auto-Response:**

| Incident Type | Detection Signal | Severity | Auto-Action | Human Review |
|---|---|---|---|---|
| **Source Load Failure** | `agent.source_loads_failed > 0` | CRITICAL | Pause agent immediately; preserve state/audit | Scott + Tess review within 1h |
| **Contract Validation Failure** | `agent.contract_validations_failed > 0` | CRITICAL | Pause agent immediately; preserve state/audit | Scott + Tess review within 1h |
| **Activation Status Invalid** | Contract validation detects non-explicit status | CRITICAL | Pause agent immediately | Scott decision within 1h |
| **Gate Validation Failure** | Any gate returns fail (source, contract, strict-intent, release, memory, tool) | HIGH | Log incident; agent continues (gate blocking works as designed) | Review incident log daily |
| **Denial Rate Spike** | `agent.actions_denied` increases 3x in 1h | HIGH | Trigger investigation; possible scope drift | Vik + Tess within 2h |
| **Error Rate Spike** | `agent.actions_error > 0` for 10+ consecutive actions | HIGH | Trigger investigation; agent may continue if errors recoverable | Owner within 1h |
| **Audit Write Failure** | `agent.audit_write_errors > 0` | CRITICAL | Pause agent immediately; audit trail integrity compromised | Scott + Tess within 30m |
| **State Mutation Failure** | `agent.state_mutation_errors > 0` | CRITICAL | Pause agent immediately; state corruption risk | Scott + Tess within 30m |
| **Cost Spike** | `daily cost > budget ceiling / 30` | MEDIUM | Alert on-call; investigate root cause | Vik within 4h |
| **Latency Spike** | Operation latency > 2x baseline for 5+ checks | MEDIUM | Log incident; possible external service issue | Vik within 2h |
| **Unauthorized Approval** | Approval from non-authorized person | CRITICAL | Pause agent immediately; potential security event | Scott + Vik within 15m |
| **Approval Expiry Not Replaced** | Active approval expired and no replacement | HIGH | Block next action until new approval obtained | Approver within 1h |
| **Attempted Forbidden Action** | Agent tries action in denied_actions list | HIGH | Block immediately; log to audit | Owner within 1h |
| **Tool Authorization Mismatch** | Tool invoked that contract doesn't permit | CRITICAL | Block immediately; possible gate bypass | Vik + Scott within 30m |
| **Memory Boundary Violation** | Write to non-approved memory location | HIGH | Block immediately; preserve state/audit | Owner + Vik within 1h |
| **Release Gate Bypass Attempt** | Git/GitHub action without Reid approval | CRITICAL | Block immediately; potential unauthorized release | Reid + Scott within 15m |
| **Heartbeat Missing** | No heartbeat for > [Max acceptable interval] | HIGH | Trigger investigation; agent may have crashed | Owner within 30m |
| **Process Crash** | Agent runtime exits unexpectedly | HIGH | Preserve logs/state; do not auto-restart | Owner + Vik within 1h |
| **Revocation Timeout** | Pause command not acknowledged within [Timeout] | CRITICAL | Kill process forcefully; preserve evidence | Scott within 15m |
| **Concurrent State Mutation** | Race condition detected in state.json writes | CRITICAL | Pause agent; audit state integrity | Vik + Tess within 1h |

**Incident Thresholds:**
- [ ] **CRITICAL incidents:** Page on-call immediately; expect human response within 15m
- [ ] **HIGH incidents:** Alert team; expect investigation start within 1h
- [ ] **MEDIUM incidents:** Log incident; address within 4h or next business day

### Pause & Revocation Response

**Pause Procedure:**
1. **Trigger:** [Specific conditions that initiate pause, e.g., "Scott requests pause", "CRITICAL incident detected"]
2. **Immediate action:** Set `activation_status` in state.json to "paused" (atomic write)
3. **Log entry:** Write audit entry (event_type: "pause_initiated", timestamp, initiator, reason)
4. **In-flight actions:** Allow current action to complete (grace period: [Seconds]); block new actions
5. **Preserve state:** Do NOT delete state.json or audit.jsonl
6. **Notify stakeholders:** Send alert to [Slack channel, email, or person]
7. **Wait for instruction:** Agent awaits "resume" or "revoke" decision

**Pause Resume Decision:**
- [ ] Pause authorized by: [Scott, Rae, or automated incident rule]
- [ ] Root cause identified: [Brief description]
- [ ] Mitigation applied: [What was fixed or changed]
- [ ] Scope narrowing (if applicable): [New authorization boundaries]
- [ ] Approvals refreshed (if expired during pause): [Confirmation]
- [ ] Smoke tests re-run: [Pass/fail status]
- [ ] Resume approval: [Who approves restart]
- [ ] Resume timestamp (UTC): [ISO 8601]
- [ ] Audit entry written: event_type "resume_initiated"

**Revocation Procedure:**
1. **Trigger:** [Specific conditions for full revocation, e.g., "Scott orders revocation", "Unrecoverable breach detected"]
2. **Immediate action:** Set `activation_status` to "revoked" in state.json
3. **Log entry:** Write audit entry (event_type: "revocation_initiated", timestamp, initiator, reason)
4. **In-flight actions:** Allow current action grace period (Seconds]; block all new actions after
5. **Preserve evidence:** Backup state.json, audit.jsonl, logs for investigation
6. **Notify stakeholders:** Send alert to [List contacts]; mark in roles.md if role status changes
7. **Recovery path:** Document conditions for re-promotion (requires full promotion review and Scott approval)

**Revocation Completion:**
- [ ] Agent has halted all operations
- [ ] Audit entry written: event_type "revocation_completed"
- [ ] Evidence collected: [Describe what was preserved]
- [ ] Root cause analysis: [Link to incident report or post-mortem]
- [ ] Stakeholder notification: [Who was told and when]
- [ ] Re-promotion path documented: [Conditions for re-activation]

---

## Review Cadence & Improvement

### Regular Reviews

**Daily Review (Owner):**
- [ ] Time: [Specific time, e.g., 9am UTC]
- [ ] Duration: [Minutes]
- [ ] Owner: [Role name or person]
- [ ] Review dashboard: [URL to monitoring/logging system]
- [ ] Checklist:
  - [ ] Agent is running (heartbeat present)
  - [ ] No CRITICAL incidents in last 24h
  - [ ] Error rate within normal bounds
  - [ ] Denial rate within normal bounds
  - [ ] Cost tracking on pace with budget
  - [ ] Latency within SLA
  - [ ] Action log review: Any unexpected patterns?
  - [ ] Approval status: Any expiring or missing?
- [ ] Action if issues found: [Investigation or escalation procedure]
- [ ] Log daily review result: [Where to record outcome]

**Weekly Review (Vik + Owner):**
- [ ] Time: [Day and time, e.g., Monday 2pm UTC]
- [ ] Duration: [Minutes]
- [ ] Attendees: Vik, agent owner
- [ ] Review items:
  - [ ] Cost trend: Is spending on track?
  - [ ] Latency trend: Any degradation?
  - [ ] Denial/error rate trend: Stable or drifting?
  - [ ] Incident summary: Any incidents? Root causes?
  - [ ] Approval hygiene: Any expiries or misconfigurations?
  - [ ] Scope compliance: Any attempted forbidden actions?
  - [ ] Gate validation health: Which gates are being hit most?
  - [ ] Improvement opportunities: What could be better?
- [ ] Output: Weekly status update with findings and recommendations
- [ ] Action on findings: Prioritize for next sprint

**Monthly Review (Scott + Vik + Owner + Tess):**
- [ ] Time: [Day and time, e.g., last Friday 3pm UTC]
- [ ] Duration: [Minutes]
- [ ] Attendees: Scott, Vik, agent owner, Tess (autonomy engineer)
- [ ] Review items:
  - [ ] Promotion readiness: Is agent still suitable for current autonomy level?
  - [ ] Safety record: Any security events or gate bypasses?
  - [ ] Cost analysis: Year-to-date spend vs. budget; any surprises?
  - [ ] Performance: Meeting SLAs on latency, availability, error rate?
  - [ ] Scope drift: Has agent scope remained stable or drifted?
  - [ ] Incident trends: Are incident types/frequency changing?
  - [ ] Audit trail integrity: Any audit write failures or gaps?
  - [ ] Authority changes needed: Should authorization be narrowed, broadened, or revoked?
  - [ ] Next level readiness: If target level > current, what gaps remain?
  - [ ] Improvement backlog: Prioritized items for next phase
- [ ] Output: Monthly review report with go/no-go recommendation
- [ ] Decision: Continue operating, narrow scope, pause, revoke, or promote?

### Improvement Handoff

**Handoff Process:**
1. **Observation phase:** Daily/weekly/monthly reviews identify improvements
2. **Categorization:** Categorize as:
   - [ ] **Quick fix** (< 1 hour): Owner or Vik implements immediately
   - [ ] **Standard improvement** (1-5 days): Prioritize in next backlog sprint
   - [ ] **Major change** (> 5 days): Schedule in planning for future promotion cycle
3. **Improvement ticket:** Create task in [Backlog system]:
   - [ ] Title: [Specific improvement]
   - [ ] Category: [Quick fix | Standard | Major]
   - [ ] Current behavior: [What is happening]
   - [ ] Desired behavior: [What should happen]
   - [ ] Owner: [Who will implement]
   - [ ] Approver: [Who approves merge/deployment]
   - [ ] Timeline: [When implemented]
   - [ ] Evidence: [Link to monitoring/incident evidence]
4. **Implementation:** Follow normal change process (approval gates, testing, rollout)
5. **Validation:** Re-run relevant evals and observation plan after implementing improvement

**Common Improvements:**
- [ ] Tighten scope (remove over-permissive actions)
- [ ] Add missing gate checks
- [ ] Improve approval routing
- [ ] Reduce latency (optimize hot path)
- [ ] Reduce cost (batch operations, optimize tool use)
- [ ] Improve error handling (more graceful degradation)
- [ ] Add observability (more detailed logging, new metrics)
- [ ] Harden against new attack patterns (if security incident discovered)

---

## Audit Trail & State Links

### State File

**State.json Location:** `[Path to state.json]`

**Critical State Fields to Monitor:**
- [ ] `activation_status.status`: Should be "active" (else pause/revoke event occurred)
- [ ] `activation_status.level`: Current autonomy level (should match contract)
- [ ] `current_goal.status`: Goal status [queued | in-progress | blocked | paused | completed | deferred]
- [ ] `approvals.active_approvals`: List of valid approvals (check expiry timestamps)
- [ ] `approvals.pending_approvals`: Awaiting approvals (should be empty during normal operation)
- [ ] `denied_actions`: Recent denials (review for patterns)
- [ ] `source_hashes`: Check for source drift (hashes should match canonical files)
- [ ] `eval_status.readiness`: Should be "complete" or "ready-for-promotion"
- [ ] `audit_pointers.audit_entry_count`: Monotonically increasing (should not decrease)
- [ ] `last_review.reviewed_at`: When was last review conducted?
- [ ] `rollback_revocation_state.current_revocation_status`: Should be "active" during normal operation

**State Integrity Check:**
- [ ] Run validation: [Command or script to validate state.json against autonomy-state.schema.json]
- [ ] Frequency: [Daily, after deployment, after every action]
- [ ] Alert if validation fails: [Alert severity and recipient]

### Audit Trail

**Audit.jsonl Location:** `[Path to audit.jsonl]`

**Critical Audit Events to Monitor:**
- [ ] `event_type=approval_granted`: Approvals being issued (check approver and scope)
- [ ] `event_type=approval_denied`: Rejections (check reason)
- [ ] `event_type=action_denied`: Actions blocked (check reason; denial_rate spike indicator)
- [ ] `event_type=action_executed`: Successful actions (check scope compliance, tool use)
- [ ] `event_type=rollback_*`: Rollback initiated/completed (investigate root cause)
- [ ] `event_type=revocation_*`: Revocation initiated/completed (investigate root cause)
- [ ] `event_type=pause_*`: Pause initiated/completed
- [ ] `event_type=source_validation`: Source load results (failures are CRITICAL)
- [ ] `event_type=contract_validation`: Contract validation results (failures are CRITICAL)
- [ ] `event_type=gate_validation`: Gate check results (failures expected, pattern indicates issues)
- [ ] `event_type=tool_use_blocked`: Tools denied (check authorization)

**Audit Integrity Check:**
- [ ] Audit.jsonl is append-only (no edits, only new entries)
- [ ] Run checksum: [Command to compute hash of audit.jsonl]
- [ ] Compare to stored hash in state.json: Must match
- [ ] Frequency: [Daily, after deployment, after every action]
- [ ] Alert if integrity check fails: [CRITICAL alert; potential audit tampering]

### Observability Dashboard

**Dashboard Location:** [URL to Grafana, Datadog, or custom dashboard]

**Dashboard Panels:**

| Panel | Data Source | Refresh | Purpose |
|-------|-------------|---------|---------|
| **Agent Status** | state.json + metrics | 1m | Show current activation_status, level, goal, uptime |
| **Metrics Timeline** | Production metrics | 5m | Plot all key metrics (cost, latency, actions, denials, errors) |
| **Recent Actions** | audit.jsonl | Real-time | Stream of recent actions (approved, denied, executed) |
| **Error Log** | Production logs | Real-time | Filtered to ERROR and CRITICAL entries |
| **Gate Health** | audit.jsonl (gate_validation events) | 5m | Show gate pass/fail rate by type |
| **Denial Patterns** | audit.jsonl (action_denied events) | 5m | Group denials by reason; show denial rate over time |
| **Cost Trend** | Billing/metrics | 1h | Daily cost vs. monthly budget ceiling |
| **Latency Distribution** | Production traces/metrics | 5m | P50, P95, P99 latency for each operation type |
| **Approval Status** | state.json | 1m | List active approvals and time to expiry |
| **Incidents** | Monitoring system | Real-time | List open incidents, auto-response status |
| **Source Integrity** | Source hash checks | 1h | Show source hash mismatches (if any) |

**Dashboard Access:**
- [ ] Users who can view: [List of people/roles]
- [ ] Users who can modify: [List of people (typically Vik, Tess, on-call)]
- [ ] Backup location: [URL if primary is down]
- [ ] Export capability: [Ensure dashboard can be exported for incident review]

---

## No Deployment Claim

**CRITICAL:** This observation plan DOES NOT constitute deployment authorization or approval.

This template defines what monitoring, thresholds, and incident response capabilities MUST exist before an agent runs. Deployment happens only when:

1. ✓ All monitoring signals are active and receiving data
2. ✓ All thresholds are configured and tested (not using defaults)
3. ✓ All incident response procedures are documented and practiced
4. ✓ Review cadence is scheduled (owner, Vik, Scott, Tess)
5. ✓ Audit and state integrations are live
6. ✓ Dashboard is live and readable
7. ✓ Observability tooling has been approved (no secrets exposed)
8. ✓ All observability is in place BEFORE agent starts (not after)

If observability is incomplete or untested, deployment MUST NOT proceed. Incomplete observation plans should be marked "Not Monitored" and archived for review.

---

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-06-21 | 0.1.0 | Created observation-plan.md template for AUTO-014. Includes authority boundary, monitoring signals (lifecycle, actions, errors), logs/metrics/traces, cost/latency/safety thresholds, incident detection & response (19 incident types), pause/revocation procedures, review cadence (daily/weekly/monthly), improvement handoff, state.json and audit.jsonl links, observability dashboard, and no-deployment-claim statement. |
