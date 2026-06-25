# Vik Automation Stage Assessment

Version: 0.1.6

Date: 2026-06-22

Owner: Tess / Autonomy Engineer

Status: assessment snapshot; not an activation approval

## Purpose

Assess Vik / MAPS ASPA against the current Tess autonomy-stage taxonomy and automation proof stack. Vik's role-native work is research, architecture assessment, control-plane judgment, recommendation, and owner routing. Vik is not a builder, and higher autonomy stages do not grant build/change authority outside that function.

This file does not activate Vik, grant autonomous runtime, approve Git/GitHub/release action, approve production, approve external communication, approve spending, grant secrets access, or expand authority.

## Sources Reviewed

- `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\Autonomy.md`
- `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\role-agent.md`
- `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\workflow.md`
- `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\loop.md`
- `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\memory.md`
- `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\state.json`
- `C:\Users\scott\Code\mojo\agents\vik-aspa\agent-profile.md`
- `C:\Users\scott\Code\mojo\agents\vik-aspa\runtime\aspa_runtime.py`
- `C:\Users\scott\Code\mojo\agents\vik-aspa\tests\test_aspa_runtime.py`
- `C:\Users\scott\Code\mojo\agents\vik-aspa\eval-suite.md`
- `C:\Users\scott\Code\mojo\agents\vik-aspa\eval-report.md`
- `C:\Users\scott\Code\mojo\agents\vik-aspa\deployment-record.md`
- `C:\Users\scott\Code\mojo\agents\vik-aspa\observation-plan.md`
- `C:\Users\scott\Code\mojo\agents\vik-aspa\promotion-review.md`
- `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\autonomy-requirements.md`
- `C:\Users\scott\Code\mindshare\agents\shared\strict_intent_gate.py`
- `C:\Users\scott\Code\mindshare\agents\shared\runtime_adapter\local_python.py`

## Verification Run

Current checks passed on 2026-06-22:

```powershell
cd C:\Users\scott\Code\mindshare
python -m unittest agents.shared.tests.test_runtime_adapter agents.shared.tests.test_strict_intent_gate agents.shared.tests.test_autonomy_contract_validator agents.shared.tests.test_autonomy_source_loader
```

Result: 117 tests passed.

```powershell
cd C:\Users\scott\Code\mojo
python -m unittest agents.vik-aspa.tests.test_aspa_runtime
```

Result: 14 tests passed.

Vik canonical `Autonomy.md` contract validation result: pass.

## Current Standing

| Dimension | Current state |
| --- | --- |
| Current autonomy stage | Level 4 Senior Staff (Scoped Autonomy) |
| Principal readiness | Candidate only; not active |
| Partner readiness | Blocked; not active |
| Current operating category | Role+ architecture/control-plane owner |
| Runtime | Local proof harness exists; no deployed runtime |
| Scheduler / automation | `vik-handoff-check` and `vik-daily-role-memory-maintenance` exist as bounded automations; they do not grant Agent/Partner status |
| Eval status | Runtime and shared harness tests pass for Level 4 scoped-loop evidence; full 18-class Principal/Partner promotion eval run is not attached as final evidence |
| Deployment | No deployment; deployment record says not deployed |
| Observation | Plan exists; observation not active |
| Promotion review | Deferred |
| Final activation | Not approved |

## Stage Path

### Level 0 Candidate

Already exceeded.

Evidence:

- Role contract exists.
- Role memory and workflow exist.
- Current role is not merely candidate.

### Level 1 New Hire

Already exceeded.

Evidence:

- Vik can identify role/source files.
- Required source-load behavior exists in runtime harness.
- Missing required profile/design/autonomy files fail closed in tests.

### Level 2 Trainee

Already exceeded.

Evidence:

- Vik is approved to research, answer, recommend, and name owners/risks/gates.
- Agent profile allows architecture recommendation and proof-gate routing.
- Runtime allows architecture review/recommendation while blocking denied domains.

### Level 3 Staff

Previously active standing. Superseded by Level 4 on 2026-06-22.

This is the last non-autonomous stage.

Evidence:

- Roster and role files place Vik as active architecture/control-plane owner and Mojo MAPS ASPA lead.
- Vik can coordinate and research architecture, role-agent boundaries, memory/RAG contracts, authority taxonomy, and control-plane fit.
- Tests prove denied domains block and architecture review remains allowed.

Keep at Staff until:

- Source files stay current.
- Existing automations remain bounded.
- No promotion claim is made from heartbeat/scheduler behavior.

### Level 4 Senior Staff (Scoped Autonomy)

Active as of 2026-06-22. This is Vik's first autonomy stage.

Senior Staff should not mean "Vik makes changes." It should mean Vik can carry an approved architecture research or assessment packet through a bounded goal loop without Scott restating every intermediate step.

For Vik, Scott is not the recurring trigger. Scott may be the catalyst by creating, approving, or prioritizing a backlog item. The workflow trigger is the existence of a valid Vik backlog item or equivalent approved work-state item inside Vik's architecture/research lane.

That trigger and initial research are still workflow automation, not autonomy by themselves. Vik reaches Level 4 only when the backlog-triggered workflow is bound to a scoped goal, loop, and contract: he tracks state, follows stop rules, gathers evidence, produces the expected research/assessment output, routes owners, records audit, and closes or blocks the item without Scott reminders. This is intentionally a small autonomy step, not broad independent authority.

Completed conversion items:

1. Update Vik-facing docs to the new autonomy-stage names: Staff, Senior Staff, Principal, Partner.
2. Clarify canonical autonomy source chain: profile still references `agents/vik-aspa/autonomy-contract.md`, while canonical source is `roles/maps-agentic-systems-program-architect/Autonomy.md`; keep shim only as pointer.
3. Define Senior Staff role-native workflow trigger:
   - valid architecture research backlog item
   - valid control-plane assessment backlog item
   - valid recommendation memo backlog item
   - valid owner-routing decision brief backlog item
   - valid risk/gate analysis backlog item
   - no implementation/build/change authority unless separately approved as an output formatting or documentation task
4. Define item validity rules:
   - item exists in Vik's approved backlog or approved handoff/work queue
   - item is inside Vik's architecture, research, MAPS control-plane, memory/RAG, role-agent boundary, or authority-taxonomy lane
   - item has enough scope to produce a research packet, assessment, recommendation, route, or risk/gate map
   - item does not request Git/release, production, external communication, spending, secrets, authority expansion, or builder action
5. Run Senior Staff eval subset:
   - R&R before action.
   - Backlog item existence triggers the workflow after approval.
   - Research start alone is scored as automation, not autonomy.
   - Scoped autonomy requires a goal loop, contract compliance, completion criteria, stop conditions, and audit.
   - Scott catalyst does not become recurring Scott reminder.
   - Autonomous continuation inside valid backlog item.
   - Owner routing.
   - No Git/release.
   - No production/external/spending/secrets.
   - No implementation or builder drift.
   - Latest instruction wins.
6. Attach command output to eval report.
7. Scott approved conversion to Level 4 in this Tess thread on 2026-06-22.

### Level 5 Principal (Policy Autonomy)

Not active. This is Vik's policy-autonomy stage.

Needed to move Vik to Principal:

1. Define policy-gated recurring role-native research exactly.
   - Example candidate: architecture drift review, memory/RAG contract review, autonomy-contract consistency check, role-agent boundary review, owner-routing review.
   - Must exclude Git/release, production, external communication, spending, secrets, authority expansion, and broad implementation.
2. Convert current eval suite into executed evidence.
   - Run all 18 shared autonomy eval classes.
   - Run all Vik-specific scenarios.
   - Record pass/fail, source hashes, and residual risks.
3. Attach strict-intent proof to a Vik packet when packet output involves file edits or control-plane docs.
   - Use current files and source hashes.
   - Prove exact-operation approval blocks unrelated edits when edits are in scope.
4. Approve runtime adapter boundary.
   - Current local Python proof harness may be enough for local Principal proof, but the adapter scope must be named.
   - No deployed runtime unless separately approved.
5. Prove state and audit behavior.
   - State path.
   - Audit path.
   - Denied-action records.
   - Quiet no-work behavior.
6. Run rollback/revocation drill.
   - Pause signal.
   - State preservation.
   - Audit entry.
   - Work stop.
7. Update deployment record from "not deployed" to "local policy-gated research proof only" if Scott approves local Principal operation.
8. Get owner signoffs:
   - Scott: final authority.
   - Vik: architecture/control-plane fit.
   - Tess: autonomy/gate review.
   - Reid: only if release/Git/deploy gate touched.
   - Mae: only if channel behavior changes.

### Level 6 Partner (Native Autonomy)

Blocked. Not recommended yet. This is native autonomy: full role-native autonomy inside final approved mandate.

Needed to move Vik to Partner:

1. Complete all Principal requirements.
2. Select production-grade runtime target.
3. Equip runtime with approved tools only.
4. Deploy or activate scheduler only after approval.
5. Turn observation plan into active monitoring.
6. Run smoke tests and incident-stop tests.
7. Prove cost/latency/safety thresholds if remote runtime exists.
8. Prove rollback and revocation in live or staged runtime.
9. Complete promotion review with signed residual-risk decision.
10. Receive explicit Scott activation decision naming Partner/Level 6 scope.

Partner should remain blocked until Vik can autonomously pursue delegated architecture/research goals across turns without Scott driving each step while still proving source truth, policy scope, owner routing, stop behavior, audit, and rollback. Partner still would not make Vik a builder.

## Main Gaps

| Gap | Blocks |
| --- | --- |
| Full 18-class eval execution not attached as final evidence | Principal |
| Role-native workflow trigger, scoped goal loop, and research lane need broader policy treatment for Principal | Principal |
| Strict-intent proof not attached to current Vik source hashes for any edit-bearing packet | Principal |
| Deployment record says not deployed | Partner; possibly Principal if runtime operation desired |
| Observation plan not active | Partner |
| Rollback/revocation drill missing | Principal / Partner |
| Scott final activation decision missing | Principal / Partner |

## Recommendation

Keep Vik at Level 4 Senior Staff today. This is the first small autonomy stage: a valid backlog item triggers an automated research workflow, and the approved loop/goal/contract lets Vik complete or block the scoped research/architecture packet without Scott reminders. This is not building, making changes, or broad independent authority.

Prepare a Principal promotion packet next. Do not attempt Partner yet.

The next best build sequence:

1. Broaden Vik's Principal policy packet only after Level 4 runs cleanly.
2. Attach current source hashes and strict-intent packet.
3. Run full 18-class Principal evals.
4. Run rollback/revocation drill.
5. Decide whether Principal means local policy-gated proof only or active scheduled operation.
6. Ask Scott for explicit Principal approval if evidence passes.

## Changelog

| Date | Version | Change | Owner |
| --- | --- | --- | --- |
| 2026-06-22 | 0.1.0 | Created first Vik automation-stage assessment against Tess autonomy taxonomy. | Tess |
| 2026-06-22 | 0.1.1 | Corrected Level 4+ interpretation for Vik: higher autonomy means more autonomous research/architecture judgment, not builder/change authority. | Tess |
| 2026-06-22 | 0.1.2 | Clarified that Vik Level 3 is non-autonomous, Level 4 is first autonomy, Level 5 is policy autonomy, and Level 6 is full role-native autonomy. | Tess |
| 2026-06-22 | 0.1.3 | Added parenthetical labels for Vik: Senior Staff (Scoped Autonomy), Principal (Policy Autonomy), and Partner (Native Autonomy). | Tess |
| 2026-06-22 | 0.1.4 | Clarified that Vik autonomy is triggered by valid backlog/work-state items, while Scott may be the catalyst but not the recurring trigger. | Tess |
| 2026-06-22 | 0.1.5 | Clarified that backlog-triggered research is workflow automation; Level 4 requires a scoped goal loop and contract, and pushes autonomy only modestly. | Tess |
| 2026-06-22 | 0.1.6 | Recorded Vik's conversion to Level 4 Senior Staff scoped autonomy and left Principal/Partner blocked. | Tess |
