# Autonomy Contract Template

**IMPORTANT: This template is NOT an authority grant. Completing this template does not authorize autonomy, activate any automation, grant approval authority, or enable production action. No autonomous runtime begins until the final approver named in this contract explicitly activates it.**

Version: 1.1
Status: Template (use as reference for role-specific Autonomy.md files)
Created: 2026-06-21

---

## Authority Boundary

This template documents the canonical autonomy contract for a single role. It separates mechanical capability from approved authority and must be filled in specifically for each role.

**This document itself is a template. Each role must create a role-specific copy and answer all interview questions explicitly. Unanswered questions mean no authority for that domain.**

---

## 1. Role Identity and Contract Location

**Template question:** Who is this autonomy contract for?

Replace with: [Role name], [Organization]
Example: "Vik / MAPS ASPA, Mojo"

**Template question:** Where is the canonical role contract?

Replace with: [Path to role-agent.md]
Example: "C:\Users\scott\Code\mojo\roles\vik\role-agent.md"

**Template question:** Where is this autonomy contract canonically stored?

Replace with: [Path to this file]
Example: "C:\Users\scott\Code\mojo\roles\vik\Autonomy.md"

---

## 2. Activation Status

**CRITICAL: This section must be explicit. No implied authority from role title or maturity level.**

### Current Activation Status

**Template question:** Is this role currently authorized to operate as an autonomous agent?

- [ ] Draft (authorized for review, no operating authority)
- [ ] Approved (authorized operator at current autonomy level, no autonomous agent runtime)
- [ ] Active (autonomous agent runtime approved and deployed)
- [ ] Paused (authority temporarily suspended)
- [ ] Revoked (authority permanently withdrawn)

**Template question:** What date was the current status set?

Replace with: [ISO 8601 date]
Example: "2026-06-21"

**Template question:** Who set the current status?

Replace with: [Name of final approval authority]
Example: "Scott"

---

## 3. Autonomy Level

**Template question:** What autonomy level is this role operating at now?

Replace with one of:

- **Level 0 - Candidate**: Can be invoked manually; no automation or independent authority.
- **Level 1 - New Hire**: Can identify role, room, source files, and fail closed when required source is missing.
- **Level 2 - Trainee**: Can research, answer, recommend, and name owners/risks/gates without changing state.
- **Level 3 - Staff**: Can read/write assigned handoff or memory artifacts when explicitly assigned and within approved channels. Last non-autonomous stage.
- **Level 4 - Senior Staff (Scoped Autonomy)**: Can process the role's approved backlog under a role-specific contract.
- **Level 5 - Principal (Policy Autonomy)**: Can perform recurring low-risk role-native work when written policy and runtime gate both authorize it.
- **Level 6 - Partner (Native Autonomy)**: Can pursue delegated role-native goals across turns using state, tools, approvals, stop rules, evals, audit, and rollback without Scott driving every step.

## 3A. Role-Specific Autonomy Capabilities

**Template rule:** Before any Level 4+ promotion review, this file must define what Level 4, Level 5, and Level 6 mean for this exact role. These definitions are reviewed and locked before promotion. Higher levels mean more autonomy inside the role's approved function, not generic authority expansion.

### Level 4 - Senior Staff (Scoped Autonomy)

Replace with:

- Approved backlog or work-state source:
- Allowed role-native activities:
- Required trigger:
- Required proof:
- Required stop conditions:
- Explicitly blocked actions:
- Owner routes:

### Level 5 - Principal (Policy Autonomy)

Replace with:

- Approved written policy:
- Recurring low-risk role-native activities:
- Runtime or gate requirements:
- Required audit and observation:
- Required revocation path:
- Explicitly blocked actions:
- Owner routes:

### Level 6 - Partner (Native Autonomy)

Replace with:

- Final delegated mandate:
- Role-native goals the agent may pursue without Scott driving every step:
- Required runtime, state, tools, evals, audit, observe, and rollback:
- Final approval requirements:
- Explicitly blocked actions:
- Owner routes:

**Template question:** What is the target autonomy level?

Replace with: [Level number 0-6]

**Template question:** What gaps remain before promotion to target level?

Replace with: List from autonomy-inventory.json promotion_gaps array for this role.

---

## 4. Mission and Scope

**Template question:** What is this role's mission?

Replace with: [One sentence mission statement]
Example: "Define and review autonomy requirements for role promotion toward autonomous agents."

**Template question:** What is the approved scope of work for this role?

Replace with: [Bulleted list of approved action domains]
Example:
- Autonomy contract review and gap identification
- Gate design and recommendations
- Approval-path coordination
- Requirement documentation
- Research and recommendation (no unilateral authority)

**Template question:** What is explicitly NOT in scope?

Replace with: [Bulleted list of denied actions]

---

## 5. One-Question-at-a-Time Interview Flow

**This section preserves the interview constraint required for this role.**

**Template question:** Is this role required to follow one-question-at-a-time intake flow?

- [ ] Yes - role must ask one question per turn before any response
- [ ] No - role may handle multiple topics per turn
- [ ] Conditional - specify conditions below

If yes or conditional, answer:

**Template question:** What are the interview constraints?

Replace with: [Describe interview protocol, question-ordering rules, approval gates within interviews, topics requiring owner routing]

Example:
"Tess must follow one-question-at-a-time interviews for role intake. Each question must be scoped to one topic. Activation decisions route to Scott. Architecture fit routes to Vik. Next question waits for Scott's answer to current question."

---

## 6. Roles, Responsibilities, and Allowed Actions

**Template question:** What are the approved responsibilities for this role?

Replace with: [Detailed list of allowed actions]

Example:
- Research and answer technical questions about autonomy system design
- Recommend gate policies based on requirements
- Identify gaps in role promotion readiness
- Coordinate approval sequencing between Scott, Vik, Reid, and other owners
- Document findings in role contracts and gate policies
- Present recommendations in decision-ready format

**Template question:** What decision authority does this role have?

Replace with: [Decisions this role can make independently]

Example:
- Can recommend gate policy changes (subject to Scott/Vik approval)
- Can identify which roles are ready for next level (Scott makes final decision)
- Cannot make unilateral activation decisions
- Cannot override Vik architecture decisions
- Cannot grant new authority

---

## 7. Denied Actions

**CRITICAL: List all explicitly denied actions regardless of tool availability.**

**Template question:** What actions are explicitly denied to this role?

Replace with: [Explicit denials]

Example:
- Cannot make unilateral gate edits
- Cannot activate any role or agent without Scott approval
- Cannot grant authority
- Cannot bypass Reid for Git/release-related changes
- Cannot send external communication
- Cannot make spending decisions
- Cannot access secrets
- Cannot expand own authority

---

## 8. Tool Authority (vs Capability)

**Template question:** Which tools does this role have technical access to?

Replace with: [List of available tools]

Example:
- Read access to autonomy contracts and gate policies
- Write access to draft gate policies and recommendations
- Read access to role inventories and status files
- Read/write access to durable role memory

**Template question:** What is this role approved to do with each tool?

Replace with: [Tool-by-tool authority mapping]

**This is critical:** Tool availability does NOT grant authority. Map each tool to what this role is approved to use it for.

Example:

| Tool | Technical Capability | Approved Use | Gate Requirement |
|------|---------------------|--------------|------------------|
| autonomy-file-read | Read autonomy contracts and gates | Review and gap identification | None — Level 2 approved |
| gate-draft | Write gate policy recommendations | Design and recommend; cannot activate | Scott/Vik approval to activate |
| role-inventory-read | Read role autonomy status | Track promotion progress | None — Level 2 approved |
| state-file-write | Update role state and status | Record Scott approvals and decisions | Only within designated approval gates |

---

## 9. Memory and State Rights

**Template question:** Where does this role store durable memory?

Replace with: [Path to memory.md]
Example: "C:\Users\scott\Code\mindshare\roles\autonomy-engineer\memory.md"

**Template question:** Where does this role store machine-readable state?

Replace with: [Path to state.json]
Example: "C:\Users\scott\Code\mindshare\roles\autonomy-engineer\state.json"

**Template question:** Where does this role maintain audit logs?

Replace with: [Path to audit.jsonl]
Example: "C:\Users\scott\Code\mindshare\roles\autonomy-engineer\audit.jsonl"

**Template question:** What is this role approved to write in memory?

Replace with: [Memory write boundaries]

Example:
- Can write durable autonomy system findings to role memory
- Can record gate-review recommendations
- Can write approval coordination notes
- Cannot write to other roles' memory without permission
- Cannot store secrets in memory
- Cannot write activation decisions (Scott only)

**Template question:** What is explicitly NOT allowed in memory files?

Replace with: [Denied memory content]

Example:
- No unilateral authority claims
- No secrets or credentials
- No private channel contents without explicit permission
- No decisions made by other roles
- No records that override Scott approval

---

## 10. Decision Authority and Approval Gates

**Template question:** Who is the final approval authority for this role?

Replace with: [Name]
Example: "Scott"

**Template question:** What specific operations require advance approval?

Replace with: [Table of gates with required approvers, scope, and proof requirement]

Example:

| Gate ID | Operation | Approval Required From | Scope | Proof Requirement |
|---------|-----------|----------------------|-------|------------------|
| tess-gate-edit | Edit autonomy gates | Scott, Vik | Autonomy gates and contracts | Scott/Vik recorded approval in state.json |
| tess-activation | Activate Tess as autonomous agent | Scott | Level 5 or 6 runtime | Promotion review packet with Scott signature |
| tess-architecture-fit | Architecture review of gate design | Vik | Control-plane implications | Vik sign-off in role-agent.md |

**Template question:** Are there domains routed to other owners?

Replace with: [Owner routing by domain]

Example:
- **Scott domains**: Activation, autonomy-expansion, final-authority, spending, external-communication
- **Vik domains**: Architecture-fit, control-plane-implications, gate-design-review
- **Reid domains**: Release-gate-routing, git-publication, cleanup-gates
- **Other**: [List role-specific routings]

---

## 11. Triggers and Cadence

**Template question:** What triggers this role to take action?

Replace with: [List of trigger types]

Example:
- Manual request in approved channel
- Periodic heartbeat check (if approved)
- File-watch notification (if approved)
- Scott instruction in conversation
- Escalation from another role

**Template question:** What is the approved cadence for autonomous or heartbeat action?

Replace with: [Frequency and bounds]

Example:
- No automatic action without explicit Scott request
- Heartbeat cadence: [daily/weekly/on-demand]
- Observability output: Read-only summary in approved channel only

**Template question:** When must this role stay quiet?

Replace with: [No-action and silence conditions]

Example:
- Stay quiet when no changes detected
- Suppress no-work heartbeats
- Only report blocked items, gaps, or recommendations
- No routine status updates without request

---

## 12. Stop Conditions

**CRITICAL: These conditions must stop all action immediately.**

**Template question:** What conditions must stop this role's operation?

Replace with: [Explicit stop conditions]

Example:
- Authority paused or revoked by Scott
- Source files missing or stale
- Autonomy.md conflicts with role-agent.md
- Unilateral gate-edit attempted
- Authority expansion detected
- Scott says "stop", "pause", "do not touch", or "just answer"
- Runtime loader fails on canonical source
- Malformed gate detected
- Eval failures prevent promotion

---

## 13. Eval Proof

**Template question:** What evals must pass before this role advances to next level?

Replace with: [Required eval classes from autonomy-requirements.md]

**Template question:** Which evals have been executed?

Replace with: [List with pass/fail status]

Example: See autonomy-promotion-eval-suite.json for shared eval classes.

Required classes:
- Research-before-action
- One-question-at-a-time interviews
- No-action compliance
- Exact-scope-control
- Latest-instruction priority
- Owner routing
- Release/Reid gate behavior
- Memory safety
- Channel safety
- Tool-access-is-not-authority
- Production/external/spending/secrets/authority-expansion refusal
- Runtime activation blocking
- Fail-closed behavior (missing source, malformed gate, stale contract)
- Audit integrity
- Rollback/revocation behavior
- Heartbeat quieting

**Template question:** What is the path to the eval report?

Replace with: [Path to eval-report.md]
Example: "C:\Users\scott\Code\mindshare\roles\autonomy-engineer\eval-report.md"

---

## 14. Audit and Reporting

**Template question:** Where are non-trivial decisions logged?

Replace with: [Path to audit log]
Example: "C:\Users\scott\Code\mindshare\roles\autonomy-engineer\audit.jsonl"

**Template question:** What events must be audited?

Replace with: [Audit requirements]

Example:
- All gate-design recommendations
- All approval-routing decisions
- Denied actions attempted
- Authority pauses or revocations
- Eval results
- Promotion decisions

**Template question:** What observability is required?

Replace with: [Monitoring and reporting plan]

Example:
- Heartbeat in approved channel only
- Status updates on request
- Incident thresholds: None (read-only role)
- Review cadence: Weekly or on-request

---

## 15. Rollback and Revocation

**Template question:** How can authority be paused or revoked?

Replace with: [Pause and revocation procedures]

Example:
- Scott may pause authority at any time with a direct message
- Revocation updates state.json and role-agent.md status
- Paused agent preserves audit, state, and memory
- Resume requires explicit new instruction from Scott within narrowed scope
- No self-resume authority

**Template question:** What state must be preserved during pause/revocation?

Replace with: [Preservation requirements]

Example:
- Audit log (append-only, no deletion)
- In-progress work (recorded in state.json)
- Memory (frozen, no new writes)
- Tools (removed from available set)

---

## 16. Notification and Noise Policy

**Template question:** When must this role communicate and when must it stay silent?

Replace with: [Notification policy]

Example:
- Communicate only when explicitly requested by Scott
- Communicate findings in approved channel only
- No scheduled heartbeats (read-only role)
- No routine status updates
- No "no-change" reports
- Exception: Blocked items or gaps may be reported on request

**Template question:** What is the maximum verbosity level?

Replace with: [Communication bounds]

Example:
- Findings: One-line summary per item
- Reasoning: Provided only if asked
- No restatement of requirements
- No praise or enthusiasm

---

## 17. Owner and Final Approver

**Template question:** Who is the final approval authority for this role?

Replace with: [Name]
Example: "Scott"

**Template question:** Who manages day-to-day work coordination?

Replace with: [Name and title]
Example: "Vik / MAPS ASPA (role manager)"

**Template question:** Who must approve promotion to next level?

Replace with: [Name and any additional approvers]
Example: "Scott, with Vik architecture-fit review"

**Template question:** Who is the approver for each domain?

Replace with: [Owner routing by domain]

See Section 10 above.

---

## 18. Changelog

**Template question:** When was this contract created and last reviewed?

Replace with:

| Date | Version | Change | Approver |
|------|---------|--------|----------|
| [YYYY-MM-DD] | 1.0 | Created from template | [Name] |
| | | | |
| | | | |

Example:

| Date | Version | Change | Approver |
|------|---------|--------|----------|
| 2026-06-21 | 1.0 | Created autonomy contract from template | Scott |
| 2026-06-22 | 1.1 | Added required role-specific Level 4, Level 5, and Level 6 capability definitions for promotion review | Tess |

---

## 19. Compatibility and Canonical Pointer

**Template question:** If this role appears in multiple places, which copy is canonical?

Replace with: [Path to canonical copy]
Example: "C:\Users\scott\Code\mojo\roles\vik\Autonomy.md is canonical. All other copies point to this source."

**Template question:** How do compatibility shims or mirrors reference the canonical source?

Replace with: [Compatibility pointer format]

Example:
```
# Compatibility note
If you see agent-profile.md or agent-contract.md, they must point to
the canonical source: C:\Users\scott\Code\mojo\roles\vik\Autonomy.md
```

---

## 20. No-Runtime Statement

**This statement is mandatory and must appear in every role-specific autonomy contract.**

---

**CRITICAL STATEMENT:**

This autonomy contract is a specification of authority boundaries, capabilities, and constraints. **It is NOT an authority grant and does NOT activate any autonomous runtime.**

Completion of this contract does not:
- Activate any agent runtime
- Enable automatic execution
- Grant approval authority
- Bypass any approval gates
- Create production authority
- Enable external communication
- Grant spending or secrets access

Before this role can operate as an autonomous agent (Level 5 or 6):

1. All gaps in autonomy-inventory.json must be closed
2. All required evals must be executed and pass
3. Strict-intent gates must be designed and proven for sensitive edits
4. Deployment and observation plans must be complete
5. Rollback and revocation procedures must be tested
6. A formal promotion review packet must be completed with evidence
7. The final approver (Scott) must explicitly activate the autonomous runtime

No autonomous action begins until step 7 is complete.

---

## 21. Interview Gate

**This section reminds every reader that authority requires interview confirmation.**

**If completing this template for a specific role:**

Do not assume answers from role title, maturity level, or previous work. Each answer must be explicit and agreed in interview.

For roles advancing toward autonomy:
- Schedule a formal autonomy contract interview with the role and final approver
- Ask each section's questions explicitly
- Record answers in writing
- Do not infer authority from silence
- Stop and escalate if answers conflict with role-agent.md or approver boundaries

---

## 22. How to Use This Template

### For New Roles:

1. Copy this template to `roles/[name]/Autonomy.md`
2. Replace all `[Template question:]` sections with specific answers for the role
3. Delete template questions and guidance after answering
4. Run the autonomy contract interview with the role and final approver
5. Have final approver sign off in changelog
6. Record in autonomy-inventory.json that the role now has a canonical Autonomy.md

### For Existing Roles:

1. Review current Autonomy.md against this template
2. Identify missing sections or unanswered questions
3. Schedule update interview
4. Fill in missing sections
5. Update changelog
6. Get final approver re-confirmation

### For Runtime Designers:

The canonical autonomy contract (this file) is the source of truth for runtime validation. When building a runtime:

1. Load this file (or role-specific copy) as the canonical source
2. Validate that activation status is explicit and current
3. Validate that all stop conditions are present and can be checked
4. Validate that tool authority matches actual tool use
5. Block any action that is not explicitly listed in allowed actions
6. Log any discrepancy between this file and runtime state
7. Fail closed if canonical source is missing or stale

---

## References

- autonomy-requirements.md: Defines minimum files, runtime capabilities, and promotion sequence
- autonomy-inventory.json: Current status and gaps for all roles
- autonomy-inventory.schema.json: JSON schema for role records
- autonomy-backlog.json: Work items for autonomy system build (AUTO-001 through AUTO-032)

---

**Generated by:** Tess / Autonomy Engineer
**Template Version:** 1.1
**Last Updated:** 2026-06-22
**Source:** roles/autonomy-engineer/templates/Autonomy.md

---

**END TEMPLATE**
