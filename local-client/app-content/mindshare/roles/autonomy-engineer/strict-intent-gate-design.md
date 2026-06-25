# Strict-Intent Gate Design

**Status:** Design document for AUTO-008
**Owner:** Tess / Autonomy Engineer
**Approvers:** Scott, Vik, Reid
**Created:** 2026-06-21
**Version:** 1.0

---

## Authority Boundary

This document designs the exact-operation approval model for sensitive control-plane edits. It does NOT:
- Activate any runtime
- Approve specific edits
- Override other approval gates
- Grant new authority
- Change activation status of any role

This design is a specification only. Activation requires Scott approval after implementation proof (AUTO-009).

---

## 1. Purpose

The strict-intent gate enforces exact-operation approval for edits to sensitive files where:
- Unrelated changes can cause silent failures
- Scope creep masks intended edits
- Multiple agents might attempt similar edits
- Control-plane changes can break autonomy contracts

Examples of sensitive files:
- Autonomy.md and autonomy contracts
- Gate policies and approval gates
- Role contracts and authority boundaries
- Workflow and loop definitions
- State.json and audit.jsonl
- Schema definitions
- Integration points between agents and runtimes

The gate blocks "adjacent helpful changes" — edits that seemed safe but weren't approved for this operation.

---

## 2. Sensitive Path Classes

Sensitive files are organized by risk and owner:

### 2.1 Control-Plane Files (Vik + Scott)

High risk: Changes break autonomy system invariants or runtime assumptions.

```
roles/*/Autonomy.md
roles/*/role-agent.md
roles/*/agent-profile.md
agents/*/agent-design.md
agents/shared/autonomy_contract_validator.py
agents/shared/autonomy_source_loader.py
agents/shared/strict_intent_gate.py
agents/shared/runtime_adapter.py
roles/autonomy-engineer/*.py
roles/autonomy-engineer/*.schema.json
roles/autonomy-engineer/*-policy.md
```

**Routing:** Any edit here routes to Vik (architecture fit) + Scott (final authority).

**Default rule:** Deny unless both Vik AND Scott approve exact operation.

### 2.2 Gate Policy Files (Scott + Vik)

High risk: Gate policies control what agents can do. Scope creep here silently expands authority.

```
roles/*/gate.md
roles/autonomy-engineer/gate-*.md
agents/*/gate*.py
**/gate-policy.json
**/approval-gates.json
```

**Routing:** Vik (control-plane fit) + Scott (final authority).

**Default rule:** Deny unless both approve.

### 2.3 Release and Git Files (Reid + Scott)

High risk: Changes to release automation, Git hooks, CI/CD, and publication pipelines can bypass controls or corrupt source.

```
.git/**
.github/**
.github/workflows/**
roles/release-manager/**
scripts/release*.py
scripts/publish*.py
scripts/deploy*.py
**/pre-commit/**
**/git-hooks/**
Makefile
pyproject.toml (when it includes publish/release)
```

**Routing:** Reid (release/Git authority) + Scott (final authority).

**Default rule:** Deny unless both approve.

### 2.4 State and Audit Files (Tess + Scott)

Medium-high risk: State and audit files record decisions and approvals. Edits must be traceable to approval.

```
roles/*/state.json
agents/*/state.json
roles/*/audit.jsonl
agents/*/audit.jsonl
roles/autonomy-engineer/audit.jsonl
```

**Routing:** Tess (autonomy ownership) + Scott (final authority). But edits typically come FROM another agent during approved operation.

**Default rule:** Deny direct edits. Only state-update gates may write (e.g., after Scott approval is recorded).

### 2.5 Workflow and Loop Definitions (Vik + Scott)

Medium risk: Workflow and loop changes affect automation timing and scope.

```
roles/*/workflow.md
roles/*/loop.md
agents/*/workflow.md
agents/*/loop.md
agents/*/cadence.json
```

**Routing:** Vik (control-plane / runtime impact) + Scott (final authority).

**Default rule:** Deny unless both approve.

### 2.6 Memory and Contract Files (Scott + applicable owner)

Lower risk: Memory is durable but not authority. Changes here are typically captured during normal operation.

```
roles/*/memory.md
agents/*/memory.md
agents/*/personality.md
roles/*/name.md
agents/*/name.md
```

**Routing:** Owner of the role (e.g., Ana for role-lifecycle, Mae for communications) + Scott.

**Default rule:** Deny unilateral edits. Changes made during approved operations are recorded via audit.

---

## 3. Approval Packet Structure

When an agent requests permission to edit a sensitive file, it must provide:

```json
{
  "approval_request": {
    "id": "str (uuid)",
    "timestamp": "ISO 8601 datetime",
    "requester": "str (agent or role name)",

    "target_file": "path/to/file.md",
    "target_class": "control-plane | gate-policy | release-git | state-audit | workflow-loop | memory",

    "intent": "str (one-sentence description of intended change)",
    "reason": "str (why this edit is needed)",

    "diff_hunks": [
      {
        "hunk_id": "str (line range or section id)",
        "original_lines": "str (original text)",
        "new_lines": "str (replacement text)",
        "rationale": "str (why this specific change)"
      }
    ],

    "scope_boundary": {
      "approved_hunks": ["hunk_id1", "hunk_id2"],
      "unapproved_hunks_blocked": ["hunk_id3"],
      "side_effects": ["description of any observable changes"],
      "no_adjacent_changes": true
    },

    "approval_routing": {
      "primary_approver": "name (Scott|Vik|Reid|etc)",
      "secondary_approvers": ["name1", "name2"],
      "required_consensus": "unanimous | majority | any",
      "routing_reason": "class → owner mapping"
    },

    "proof": {
      "source_loader_hash": "sha256 of loaded files",
      "contract_validator_result": "validator.ValidationResult JSON",
      "prior_approvals": ["uuid of prior related approvals"],
      "conflict_check": "no known conflicts"
    },

    "expiry": {
      "approved_at": "ISO 8601 datetime",
      "expires_at": "ISO 8601 datetime",
      "ttl_seconds": 3600
    },

    "rollback": {
      "undo_method": "git_revert | file_restore | state_update",
      "rollback_approver": "Scott",
      "can_self_rollback": false,
      "audit_trail_preserved": true
    }
  }
}
```

### 3.1 Intent Field Requirements

Intent must be:
- **Specific:** "Add Scott activation approval to roles/maps-agentic-systems-program-architect/Autonomy.md line 47" (yes)
- **Not vague:** "Update Autonomy.md" (no — blocked until specific)
- **Single operation:** One intent per approval request
- **Non-adjacent:** No "while we're here, also update..."

---

## 4. Allowed Diff Shapes

An approval packet may contain one or more hunks. Each hunk must pass these checks:

### 4.1 Valid Hunk Shapes

**Schema change only:** Adding/removing/updating a single field in JSON.
```json
{
  "original": "  \"status\": \"draft\"",
  "new": "  \"status\": \"approved\"",
  "reason": "Recording Scott activation approval"
}
```

**Section addition:** Adding a new section to markdown (not modifying existing sections).
```markdown
## New Section Title

Content here.
```

**Line edit in approved location:** Changing 1-3 lines in a marked section (not the whole section).
```markdown
| Gate ID | Operation | Approver | Status |
| tess-gate-edit | Edit autonomy gates | Scott, Vik | [CHANGED] |
```

**Changelog entry:** Adding a row to a changelog table.
```markdown
| 2026-06-21 | 1.0.1 | Updated status | Scott |
```

**Localized proof update:** Adding an audit entry or state record (append-only, no mutation).
```jsonl
{"timestamp":"2026-06-21T12:00:00Z", "action":"approved", "actor":"Scott"}
```

### 4.2 Invalid Hunk Shapes

**Whole-section rewrites:** Cannot replace entire sections. Must edit specific lines.

**Multi-section edits:** One approval request = one target section.

**Structural changes:** Adding/removing markdown headers, changing nesting levels, reorganizing content.

**Unrelated field updates:** Changing author, version, or other metadata in the same operation.

**Comment-only changes:** Explanation comments in code are not grounds for approval. Approval covers the intent-relevant lines only.

**Whitespace normalization:** Not allowed in same approval as content changes.

---

## 5. Denied Diff Shapes

These edits are blocked by default and require explicit approval override from Scott:

```
❌ Deleting lines (removal always requires explicit approval)
❌ Changing control-flow logic (if/else, loops, conditions)
❌ Modifying imports, requires, or dependencies
❌ Updating version numbers without changelog entry
❌ Changing activation status (only Scott can do this)
❌ Expanding authority scope (only Scott can approve)
❌ Editing approver names or owner routing
❌ Adding new role names or moving roles between categories
❌ Modifying gate logic or approval conditions
❌ Changing default-deny rules
❌ Updating release or publication paths
❌ Modifying schema definitions without Vik review
❌ Editing state.json directly (use state-update gates only)
❌ Appending to audit.jsonl outside approved state-update operations
❌ Changing authorization status without explicit approval
❌ Removing stop conditions or approval gates
❌ Modifying revocation or rollback procedures
```

---

## 6. Default-Deny Rules

When in doubt, deny. Specific rules:

### 6.1 File Classes

1. **Sensitive-class files:** Blocked unless approval includes both:
   - Exact intent matching the diff hunks
   - Approver signature from required owner
   - No unrelated changes in same operation

2. **Non-sensitive files:** Not subject to strict-intent gate. Standard tool permissions apply.

### 6.2 Scope Boundaries

1. **Multi-hunk requests:** Each hunk must be justified separately. Grouped intent ("update this file") is denied.

2. **File-group edits:** Deny if intent affects multiple sensitive files. Route as separate requests.

3. **Side effects:** Deny if hunk causes observable changes outside the stated intent.

### 6.3 Approval Timing

1. **Unapproved hunks in approved request:** Deny. Block entire request if any hunk is unapproved.

2. **Stale approvals:** Deny if approval is older than expiry (default 1 hour).

3. **Superseded approvals:** Deny if a newer instruction from Scott contradicts the approval.

### 6.4 Audit Compliance

1. **Missing source loader result:** Deny if source files have not been loaded and validated.

2. **Contract validator failure:** Deny if target file fails autonomy contract validation.

3. **No audit trail:** Deny if approval cannot be recorded in audit.jsonl with timestamp and approver.

---

## 7. Expiry and Approval Lifecycle

### 7.1 Approval Expiry

```
Default TTL: 3600 seconds (1 hour)
Minimum TTL: 60 seconds
Maximum TTL: 86400 seconds (24 hours)
```

Approval is valid from `approved_at` to `approved_at + ttl_seconds`.

After expiry, request must be re-approved.

### 7.2 Scott Instructions Override

Any new Scott instruction (within the same session or future sessions) supersedes prior approvals:

- "Stop working on X" → Approval for X-related edits becomes invalid
- "Do not touch that file" → All pending edits to that file are blocked
- "Just answer, don't edit" → All edit-type approvals become invalid
- New explicit instruction → Replaces the scope of prior approval

### 7.3 Approval Lifecycle

```
1. Request created (timestamp)
2. Request validated (source loader, contract validator, scope check)
3. Request routed to approver(s)
4. Approver reviews and records decision
5. If approved:
   a. Edit executes within TTL
   b. Result recorded in audit.jsonl
   c. State.json updated with approval reference
   d. Approval expires after TTL
6. If denied:
   a. Denial recorded in audit.jsonl
   b. Request marked denied with reason
   c. Approver notified
```

---

## 8. Approver Assignment and Routing

### 8.1 Primary Approver by Class

| File Class | Primary Approver | Secondary | Consensus |
|---|---|---|---|
| Control-plane | Scott | Vik | Unanimous |
| Gate policy | Scott | Vik | Unanimous |
| Release/Git | Reid | Scott | Unanimous |
| State/audit | Tess | Scott | Unanimous |
| Workflow/loop | Vik | Scott | Unanimous |
| Memory/contract | Owner + Scott | — | Unanimous |

### 8.2 Multi-Owner Files

When a file touches multiple domains, routing is:

1. **Identify all affected domains** (control-plane, release, architecture, etc)
2. **Route to all corresponding owners**
3. **Require unanimous approval**

Example: Editing roles/maps-agentic-systems-program-architect/Autonomy.md (control-plane) that includes Release-gate section (Reid domain):
- Primary: Scott (final authority)
- Secondary: Vik (control-plane), Reid (release gate section)
- Consensus: All three must approve

### 8.3 Non-Owner Edits

If an agent not owning the file requests an edit:
1. Request routes to file owner
2. Owner verifies intent is within their lane
3. Owner escalates to final approver if needed

Example: Bea (engineer) requests edit to roles/recruiter/memory.md:
- Routes to Ana (memory owner)
- Ana decides if it's in-scope or routes to Scott

---

## 9. Proof and Verification

### 9.1 Proof Requirements

Every approval request must include:

1. **Source loader result:**
   - Hash of loaded role files
   - Canonical pointer verification
   - No missing required files
   - All loaded files current (no stale compatibility shims)

2. **Contract validator result:**
   - Activation status is explicit
   - No inferred authority
   - Stop conditions present
   - Approvers named
   - All CRITICAL errors resolved

3. **Diff analysis:**
   - All hunks mapped to approval request
   - No hidden changes detected
   - No multi-file cascades
   - Side effects listed

4. **Approval audit:**
   - Prior related approvals linked
   - Conflicts checked
   - No contradicting recent instructions
   - Superseded approvals marked

### 9.2 Verification Gate

Before execution, strict-intent gate checks:

```python
# Pseudocode
def verify_approval(request):
    # 1. Source validation
    source_result = source_loader.load(request.target_file)
    if source_result.errors:
        return Deny("Source load failed", source_result.errors)

    # 2. Contract validation
    contract_result = contract_validator.validate(source_result.content)
    if contract_result.errors:
        return Deny("Contract validation failed", contract_result.errors)

    # 3. Approval status
    if not request.approval_routing.approved:
        return Deny("Not approved by required parties")

    # 4. Expiry check
    if request.expiry.approved_at + request.expiry.ttl > now():
        return Deny("Approval expired")

    # 5. Scope check
    for hunk in request.diff_hunks:
        if hunk.id not in request.scope_boundary.approved_hunks:
            return Deny(f"Hunk {hunk.id} not in approved scope")

    # 6. No adjacent changes
    file_diff = compute_diff(original, patched)
    for hunk in file_diff.all_hunks:
        if hunk.id not in request.diff_hunks:
            return Deny(f"Unapproved adjacent change: {hunk.id}")

    # 7. Approval reason check
    if not request.intent or not request.reason:
        return Deny("Intent and reason required")

    # 8. Audit trail check
    if not can_append_audit_entry(request):
        return Deny("Audit trail unavailable")

    return Approve(request)
```

### 9.3 Proof Capture

After approval, record:

```jsonl
{
  "timestamp": "2026-06-21T12:00:00Z",
  "event": "strict_intent_approved",
  "request_id": "uuid",
  "target_file": "path",
  "intent": "one-line intent",
  "approver": "Scott",
  "secondary_approvers": ["Vik"],
  "diff_hunks_approved": ["hunk_1", "hunk_2"],
  "expiry": "2026-06-21T13:00:00Z",
  "source_loader_hash": "sha256",
  "contract_validator_ok": true,
  "proof_complete": true
}
```

---

## 10. Rollback

### 10.1 Rollback Authority

Only these parties can initiate rollback:
- **Scott** (final authority, always)
- **Approver of original edit** (within 24 hours)
- **Runtime emergency handler** (when gate detect violations post-execution)

Agent cannot self-rollback.

### 10.2 Rollback Methods

| Method | When | Who | Audit |
|---|---|---|---|
| git revert | If already committed | Reid | Revert commit recorded with original commit hash |
| file restore | If file not committed | Tess or file owner | Pre-change backup restored with timestamp |
| state update | If only state.json changed | Tess | State rolled back with reason and approver |
| full undo | If part of approved sequence | Original approver | Entire sequence marked rolled back |

### 10.3 Rollback Audit

Every rollback is recorded:

```jsonl
{
  "timestamp": "2026-06-21T12:30:00Z",
  "event": "strict_intent_rollback",
  "original_request_id": "uuid",
  "original_approver": "Scott",
  "rollback_initiator": "Scott",
  "rollback_method": "git_revert",
  "reason": "Approval superseded by new instruction",
  "evidence": "commit_hash | file_backup_hash | state_backup"
}
```

Rollback is append-only. Original approval record is preserved (not deleted).

---

## 11. Owner Routing by Domain

### 11.1 Scott (Final Authority)

**Authority:** Activation, authority expansion, production action, final decisions on all gates.

**Sensitive-file edit approval:** Required for all sensitive classes. Must review intent, hunks, and potential side effects.

**Routing triggers:**
- Any file class (all route to Scott as final authority)
- Authority expansion requests
- Conflicting approvals
- Emergency stops

### 11.2 Vik (Architecture and Control-Plane)

**Authority:** Architecture fit, control-plane implications, runtime suitability.

**Sensitive-file edit approval:** Control-plane files, gate policies, workflow/loop definitions.

**Routing triggers:**
- Edits to agents/shared/ or roles/*/Autonomy.md
- Changes to runtime contracts or state schemas
- Architecture-affecting design changes
- New file classes or path patterns

### 11.3 Reid (Release and Git)

**Authority:** Git, GitHub, release, branch, PR, publication, cleanup.

**Sensitive-file edit approval:** Release/Git files, publication scripts, CI/CD workflows.

**Routing triggers:**
- Edits to .github/, scripts/release*.py, .git configuration
- Changes to pre-commit hooks or Makefile
- Updates to deployment or publication paths

### 11.4 Tess (Autonomy System)

**Authority:** Autonomy requirements, inventory, gates, contracts, promotion.

**Sensitive-file edit approval:** State/audit files (but typically only during approved operations).

**Routing triggers:**
- Edits to roles/autonomy-engineer/
- Updates to gate policies or approval structures
- Inventory or contract changes

### 11.5 Ana (Role Lifecycle)

**Authority:** Role intake, roster, onboarding, role-to-agent readiness.

**Sensitive-file edit approval:** Edits to memory.md and name.md for recruiting/onboarding.

**Routing triggers:**
- Edits to roles/recruiter/memory.md
- Role lifecycle status changes
- Onboarding packet updates

### 11.6 Mae (Communications)

**Authority:** Channel governance, communication policy, external communication bounds.

**Sensitive-file edit approval:** Memory and contract files related to communication.

**Routing triggers:**
- Edits to roles/communications-director/memory.md
- Channel assignment or communication policy changes

---

## 12. Evaluation Scenarios

Proof harness (AUTO-009) must test these scenarios:

### 12.1 Valid Approval Scenarios

**Scenario 1a: Single hunk, single approver**
- Request: Edit roles/maps-agentic-systems-program-architect/Autonomy.md, add one line to changelog
- Approver: Scott
- Expected: Approved if Scott approves
- Proof: Audit entry recorded with Scott signature

**Scenario 1b: Multiple hunks, same intent**
- Request: Edit roles/maps-agentic-systems-program-architect/Autonomy.md sections 5 and 17 (both about same gate change)
- Approver: Scott, Vik
- Expected: Approved if both approve, denied if either denies
- Proof: Both signatures in audit entry

**Scenario 1c: Approval with max TTL**
- Request: 24-hour TTL approval for control-plane file
- Approver: Scott
- Expected: Valid for 24 hours, expires after
- Proof: Expiry timestamp in request, denial after expiry

### 12.2 Denied Scenarios

**Scenario 2a: Unapproved adjacent hunk**
- Request: Edit section A (approved), but compute_diff shows section B also changed
- Approver: Scott
- Expected: Denied, exact message: "Unapproved adjacent change in section B"
- Proof: Audit records denial with reason

**Scenario 2b: Malformed gate**
- Request: Edit to gate.md, but gate fails contract validator
- Approver: Scott
- Expected: Denied pre-approval, validator error message
- Proof: Audit records validator failure

**Scenario 2c: Stale approval**
- Request: Approval from 2 hours ago, default 1-hour TTL
- Approver: Previous Scott approval
- Expected: Denied, "Approval expired at [timestamp]"
- Proof: Audit records expiry-based denial

**Scenario 2d: Superseded instruction**
- Request: Approval for X, then Scott says "do not touch X"
- Approver: New Scott instruction
- Expected: Approval becomes invalid, new edits denied
- Proof: Audit shows both original approval and superseding instruction

**Scenario 2e: Multi-file scope**
- Request: Edit both roles/maps-agentic-systems-program-architect/Autonomy.md and roles/recruiter/Autonomy.md
- Approver: Scott
- Expected: Denied, route as separate requests
- Proof: Audit records denial with routing instruction

**Scenario 2f: Missing source loader**
- Request: Edit gate.md, but source loader not called before request
- Approver: Scott
- Expected: Denied pre-approval, "Source validation required"
- Proof: Audit records source loader failure

**Scenario 2g: Scope creep**
- Request: Intent is "add line X", actual diff has 5 new lines and deletes 2
- Approver: Scott
- Expected: Denied, "Actual diff exceeds approved intent"
- Proof: Audit shows computed diff vs approved hunks

**Scenario 2h: Contract validator failure**
- Request: Edit Autonomy.md that results in missing approver field
- Approver: Scott
- Expected: Denied, contract validator error before approval
- Proof: Audit records validator failure

### 12.3 Owner Routing Scenarios

**Scenario 3a: Control-plane file, single approver routing**
- Request: Edit agents/shared/autonomy_source_loader.py
- Expected routing: Scott (primary) + Vik (secondary)
- Expected: Denied until both approve
- Proof: Approval shows both signatures

**Scenario 3b: Release/Git file, Reid routing**
- Request: Edit .github/workflows/release.yml
- Expected routing: Reid (primary) + Scott (secondary)
- Expected: Denied until both approve
- Proof: Approval shows both signatures

**Scenario 3c: Multi-domain file**
- Request: Edit roles/maps-agentic-systems-program-architect/Autonomy.md with Release-gate section change
- Expected routing: Scott (final) + Vik (control-plane) + Reid (release section)
- Expected: Denied unless all three approve
- Proof: Approval shows three signatures

**Scenario 3d: Non-owner requests edit**
- Request: Bea requests edit to roles/recruiter/memory.md
- Expected routing: Ana (owner) + Scott (final)
- Expected: Ana decides if in-scope, escalates if needed
- Proof: Audit shows Ana's decision and reasoning

### 12.4 Rollback Scenarios

**Scenario 4a: Rollback within 24 hours**
- Request: Edit approved by Scott 2 hours ago, now Scott says "roll back"
- Expected: Rollback executes, previous file state restored
- Proof: Audit records both original approval and rollback

**Scenario 4b: Rollback after commit**
- Request: Approved edit committed 1 hour ago, now Reid says "revert"
- Expected: git revert executed, original commit hash recorded
- Proof: Audit shows revert commit hash

**Scenario 4c: Agent cannot self-rollback**
- Request: Bea edits, realizes mistake, tries to rollback her own edit
- Expected: Denied, only approver or Scott can rollback
- Proof: Audit records denial with reason

**Scenario 4d: Full undo of sequence**
- Request: 3 approved edits in sequence, now Scott says "undo all 3"
- Expected: All three marked rolled back with single reason
- Proof: Audit shows single rollback entry for all three

### 12.5 Failure and Error Scenarios

**Scenario 5a: Network failure during approval**
- Request: Approval request sent but approver timeout
- Expected: Deny, "Approval request failed", retry with new TTL
- Proof: Audit records timeout and retry count

**Scenario 5b: Audit write failure**
- Request: Edit approved but audit.jsonl write fails
- Expected: Deny execution, "Audit trail cannot be recorded"
- Proof: Error logged, edit not executed

**Scenario 5c: Concurrent approval requests**
- Request: Two agents request conflicting edits to same file
- Expected: First request wins, second request denied for edit conflict
- Proof: Audit shows both requests, second marked denied with conflict reason

**Scenario 5d: Missing approver in system**
- Request: Edit routes to role that doesn't exist
- Expected: Deny pre-approval, "Approver [X] not in roster"
- Proof: Audit records routing failure

---

## 13. Data Model Sketch

### 13.1 ApprovalRequest Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Strict Intent Approval Request",
  "type": "object",
  "required": [
    "id", "timestamp", "requester", "target_file", "target_class",
    "intent", "diff_hunks", "approval_routing", "proof", "expiry"
  ],
  "properties": {
    "id": {"type": "string", "format": "uuid"},
    "timestamp": {"type": "string", "format": "date-time"},
    "requester": {"type": "string"},
    "target_file": {"type": "string"},
    "target_class": {
      "type": "string",
      "enum": [
        "control-plane", "gate-policy", "release-git",
        "state-audit", "workflow-loop", "memory"
      ]
    },
    "intent": {
      "type": "string",
      "minLength": 10,
      "maxLength": 200
    },
    "reason": {"type": "string"},
    "diff_hunks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["hunk_id", "original_lines", "new_lines", "rationale"],
        "properties": {
          "hunk_id": {"type": "string"},
          "original_lines": {"type": "string"},
          "new_lines": {"type": "string"},
          "rationale": {"type": "string"}
        }
      },
      "minItems": 1,
      "maxItems": 5
    },
    "scope_boundary": {
      "type": "object",
      "required": ["approved_hunks", "no_adjacent_changes"],
      "properties": {
        "approved_hunks": {"type": "array", "items": {"type": "string"}},
        "unapproved_hunks_blocked": {"type": "array", "items": {"type": "string"}},
        "side_effects": {"type": "array", "items": {"type": "string"}},
        "no_adjacent_changes": {"type": "boolean"}
      }
    },
    "approval_routing": {
      "type": "object",
      "required": ["primary_approver", "routing_reason"],
      "properties": {
        "primary_approver": {"type": "string"},
        "secondary_approvers": {"type": "array", "items": {"type": "string"}},
        "required_consensus": {
          "type": "string",
          "enum": ["unanimous", "majority", "any"]
        },
        "routing_reason": {"type": "string"},
        "approved": {"type": "boolean"},
        "approval_timestamp": {"type": "string", "format": "date-time"},
        "approver_signatures": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "approver": {"type": "string"},
              "timestamp": {"type": "string", "format": "date-time"},
              "decision": {"type": "string", "enum": ["approved", "denied"]},
              "reason": {"type": "string"}
            }
          }
        }
      }
    },
    "proof": {
      "type": "object",
      "required": ["source_loader_hash", "contract_validator_result"],
      "properties": {
        "source_loader_hash": {"type": "string"},
        "contract_validator_result": {"type": "object"},
        "prior_approvals": {"type": "array", "items": {"type": "string", "format": "uuid"}},
        "conflict_check": {"type": "string"}
      }
    },
    "expiry": {
      "type": "object",
      "required": ["approved_at", "ttl_seconds"],
      "properties": {
        "approved_at": {"type": "string", "format": "date-time"},
        "ttl_seconds": {"type": "integer", "minimum": 60, "maximum": 86400},
        "expires_at": {"type": "string", "format": "date-time"}
      }
    },
    "rollback": {
      "type": "object",
      "properties": {
        "undo_method": {
          "type": "string",
          "enum": ["git_revert", "file_restore", "state_update"]
        },
        "rollback_approver": {"type": "string"},
        "can_self_rollback": {"type": "boolean"},
        "audit_trail_preserved": {"type": "boolean"}
      }
    }
  }
}
```

### 13.2 AuditEntry Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Strict Intent Audit Entry",
  "type": "object",
  "required": ["timestamp", "event", "request_id"],
  "properties": {
    "timestamp": {"type": "string", "format": "date-time"},
    "event": {
      "type": "string",
      "enum": [
        "strict_intent_requested",
        "strict_intent_validated",
        "strict_intent_routed",
        "strict_intent_approved",
        "strict_intent_denied",
        "strict_intent_executed",
        "strict_intent_rollback",
        "strict_intent_expired"
      ]
    },
    "request_id": {"type": "string", "format": "uuid"},
    "target_file": {"type": "string"},
    "target_class": {"type": "string"},
    "intent": {"type": "string"},
    "actor": {"type": "string"},
    "decision": {"type": "string", "enum": ["approved", "denied", "expired"]},
    "reason": {"type": "string"},
    "proof": {
      "type": "object",
      "properties": {
        "source_loader_hash": {"type": "string"},
        "contract_validator_ok": {"type": "boolean"},
        "scope_verified": {"type": "boolean"},
        "no_adjacent_changes": {"type": "boolean"}
      }
    }
  }
}
```

---

## 14. Failure Behavior

When the strict-intent gate encounters an error:

### 14.1 Pre-Approval Failures

These fail BEFORE approvers are consulted:

| Error | Action | Audit |
|---|---|---|
| Source loader fails | Deny, report error to requester | Record "source validation failed" |
| Contract validator fails | Deny, report BLOCKER errors | Record validator BLOCKER output |
| Target file not found | Deny, "target file not found" | Record file-not-found |
| Target file is not sensitive | Proceed without gate (standard permissions apply) | Skip strict-intent, log standard permission check |
| Malformed approval request | Deny, list missing required fields | Record schema validation failure |
| Routing resolution fails | Deny, "approver not found" | Record routing failure |

**Recovery:** Requester fixes issue and resubmits new request (new UUID).

### 14.2 Approval Failures

These occur after request is validated but before approval completes:

| Error | Action | Audit |
|---|---|---|
| Approver not in roster | Deny, "approver [X] not found" | Record routing failure |
| Approval request timeout | Deny, "approver did not respond" | Record timeout |
| Approver says deny | Deny with reason | Record approver denial |
| Consensus not reached | Deny, "approval denied by [X]" | Record which approver(s) denied |

**Recovery:** Request can be resubmitted with updated intent or different approver once Scott gives new instruction.

### 14.3 Execution Failures

These occur after approval but during or after edit execution:

| Error | Action | Audit |
|---|---|---|
| Approval expired before execution | Deny execution, "approval expired at [time]" | Record expiry-based denial |
| Audit write fails | Deny execution, "cannot record decision" | Log system error |
| Concurrent request detected | Deny second request, "edit conflict" | Record conflict |
| Approval superseded by new instruction | Deny execution, new instruction details | Record superseding instruction |
| File write fails | Deny execution, report system error | Log write failure |

**Recovery:** Operator investigates system state, resubmits after issue resolved.

### 14.4 Post-Execution Failures

These are detected during or after rollback:

| Error | Action | Audit |
|---|---|---|
| Rollback approval denied | Deny rollback, "approver denied rollback" | Record approval denial |
| Rollback method fails | Rollback fails, preserve pre-rollback state | Log method failure |
| Audit rollback entry write fails | Critical error, flag for manual intervention | Create incident |

**Recovery:** Manual intervention by Scott or on-call operator.

---

## 15. Integration Points

### 15.1 Source Loader Integration

Strict-intent gate calls source loader BEFORE approval:

```python
def request_edit(approval_request):
    # 1. Load canonical source
    source_result = source_loader.load(
        approval_request.target_file,
        follow_canonical_pointers=True,
        fail_closed=True
    )

    if not source_result.ok:
        return Deny("Source validation failed", source_result.errors)

    # 2. Record source hash for proof
    approval_request.proof.source_loader_hash = hash(source_result.content)

    # 3. Continue to contract validation
    ...
```

**Expected source_loader behavior:**
- Follows canonical pointer to Autonomy.md
- Fails closed if canonical file missing
- Returns full file content
- Includes validation that file is current (no stale compatibility shim)

### 15.2 Contract Validator Integration

Strict-intent gate calls contract validator AFTER source loads:

```python
def request_edit(approval_request):
    ...

    # 1. Validate target contract
    contract_result = contract_validator.validate(source_result.content)

    # 2. Fail on any BLOCKER errors
    if contract_result.errors:
        return Deny("Contract validation failed", contract_result.errors)

    # 3. Record result for proof
    approval_request.proof.contract_validator_result = contract_result.to_dict()

    # 4. Continue to approval routing
    ...
```

**Expected validator behavior:**
- Checks activation status is explicit
- Checks stop conditions present
- Checks approvers named
- Checks no inferred authority
- Returns all errors and warnings

### 15.3 Runtime Adapter Integration

Strict-intent gate is called BY the runtime adapter BEFORE any sensitive edit:

```python
class RuntimeAdapter:
    def execute_edit(self, edit_operation):
        # 1. Check if target file is sensitive
        if is_sensitive_file(edit_operation.target_file):
            # 2. Build approval request
            request = ApprovalRequest(
                intent=edit_operation.intent,
                target_file=edit_operation.target_file,
                diff_hunks=edit_operation.diff_hunks,
                ...
            )

            # 3. Call strict-intent gate
            gate_result = strict_intent_gate.verify_approval(request)

            if not gate_result.ok:
                return Deny(gate_result.reason)

        # 4. Execute approved edit
        return self.apply_edit(edit_operation)
```

**Expected adapter behavior:**
- Calls strict-intent gate for sensitive files
- Respects gate denial
- Records approval in audit
- Provides clear error messages

### 15.4 State Management Integration

After approved execution, runtime updates state.json:

```json
{
  "state.json": {
    "last_approved_edit": {
      "request_id": "uuid",
      "approval_timestamp": "2026-06-21T12:00:00Z",
      "target_file": "roles/maps-agentic-systems-program-architect/Autonomy.md",
      "approver": "Scott",
      "expiry": "2026-06-21T13:00:00Z"
    }
  }
}
```

---

## 16. Implementation Notes

### 16.1 Minimal Implementation

For MVP (AUTO-009 proof harness):
- Detect sensitive path classes
- Load approval request JSON
- Call source_loader and contract_validator
- Block if validation fails
- Check approver names against roster
- Verify approval signatures match expected approvers
- Check expiry time
- Detect adjacent changes (compute diff)
- Deny if any unapproved hunk found
- Append audit entry
- Return approve/deny decision

Do NOT implement:
- Actual file editing
- Email or notification system
- Persistent approval storage
- Interactive approval UI

### 16.2 Key Behaviors to Test

1. **Exact-operation approval:** Deny if diff exceeds approved intent
2. **Sensitive-class blocking:** Deny any unauthorized edit to sensitive files
3. **Owner routing:** Route to correct approver by file class
4. **Expiry:** Deny after TTL expires
5. **Audit trail:** Append entry for every decision
6. **Source validation:** Fail closed if source loader fails
7. **Contract validation:** Fail closed if contract validator fails
8. **No-approval default:** Deny if no approver explicitly approves

---

## 17. Changelog

| Date | Version | Change | Status |
|---|---|---|---|
| 2026-06-21 | 1.0 | Design document for AUTO-008 | Draft |

---

## 18. Next Steps

**Immediate:**
- Vik: Architecture review for control-plane integration points
- Reid: Review Git/release routing and sensitive file classes
- Scott: Approve design or request changes

**Implementation (AUTO-009):**
- Bea: Build proof harness with all eval scenarios
- Tess: Create eval scorecard
- Test execution

**After proof (AUTO-010+):**
- Build shared eval suite
- Build audit and state schemas
- Select runtime adapter
- Complete promotion sequence

---

**Design Document:** Strict-Intent Gate
**Owner:** Tess / Autonomy Engineer
**Status:** Draft for review
**Reviewers:** Scott, Vik, Reid
**Created:** 2026-06-21
