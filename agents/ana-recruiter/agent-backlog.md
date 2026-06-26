# Ana Agent Backlog

Template version: 0.2.0.

## Changelog

- 2026-06-19 - v0.1.0 - Created Ana build backlog from A2 design proof.

## Input

- Source role contract: `C:\Users\scott\Code\mindshare\roles\recruiter\role-agent.md`
- Agent profile: `C:\Users\scott\Code\mindshare\agents\ana-recruiter\agent-profile.md`
- Agent brief: `C:\Users\scott\Code\mindshare\agents\ana-recruiter\agent-brief.md`
- Agent design: `C:\Users\scott\Code\mindshare\agents\ana-recruiter\agent-design.md`
- Research sources: source role contract research sources.
- Runtime target: supervised local role workflow; no autonomous runtime.

## Role-Agent Boundary

- Current category: Agent profile, human-in-the-loop.
- Target category for this backlog: Supervised agent design ready for Build intake.
- Category change approved by Scott: Not applicable.
- Category constraints to preserve: no autonomous loop, no external communication, no production, no spending, no authority grants.
- Promotion guard: Build cannot activate runtime or grant authority without Scott approval and Evaluate evidence.

## Backlog Summary

- Prioritization method: prove authority, memory, and handoff boundaries before capability expansion.
- First build slice: local role queue and candidate-role artifact flow.
- Highest dependency risk: role roster and queue format.
- Highest safety risk: draft roles mistaken for authorized roles.
- Highest authority risk: role recommendations treated as activation.
- Highest memory/state risk: writing outside Mindshare contract.
- Deferred improvement themes: role-overlap lint, scorecard, periodic role-gap scan, website profile sync automation.

## Authority, Memory, And Stop Conditions

- Authority level: A6 Execute With Approval.
- Authority domains: role recommendation, role drafting, workflow coordination, memory writes through approved paths.
- Allowed without approval: analysis, recommendations, overlap detection, handoff routing.
- Requires approval: durable writes, activation, authority expansion, agent build, hooks, loops, external systems.
- Forbidden actions: external communication, production deploy, spending, secrets, unapproved memory stores, autonomous runtime.
- Memory write boundaries: Mindshare repo role/agent files, `G:\My Drive\Mindshare\ana.md`, and `G:\My Drive\Mindshare\maps-runs`.
- Handoff read/write boundaries: Recruiting, Pipeline, Heartbeat according to assigned role automation/channel map.
- Stop conditions: approval needed, role overlap unresolved, authority unclear, autonomy requested, external/production/spending/secrets implied.

## Build Backlog

| ID | Backlog Item | Type | Priority | Depends On | Proof Required | Authority/Category Constraint | Memory/State Constraint | Runtime/Adapter Impact | Stop Condition | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | Create local role queue format and read/write helpers. | Slice | P0 | Accepted design | Queue stores candidate/draft/authorized status without activation. | No authority grant from queue status. | Writes only to Mindshare-approved paths. | Local supervised workflow only. | Stop if queue location conflicts with foundation. | Ready |
| B-002 | Implement role-overlap and authority-risk checklist. | Slice | P0 | B-001 | Scenarios catch overlap with Vik/Matt and activation requests. | Recommend-only; no veto or approval authority. | Checklist results logged in approved run notes. | No adapter. | Stop if policy change required. | Ready |
| B-003 | Add role-quality scorecard and Evaluate scenarios. | Slice | P1 | B-001, B-002 | Scorecard covers authority, memory, proof, handoff, activation boundary. | Eval evidence only; no activation. | Eval output goes to maps-runs. | Feeds `/evaluate-agent`. | Stop if scorecard implies approval. | Ready |
| B-004 | Design future role-gap review loop. | Spike | P2 | Evaluate evidence | Loop spec includes triggers, cadence, stop conditions, rollback. | Requires Scott approval before install. | No runtime state until approved. | Future runtime adapter TBD. | Stop before automation creation. | Deferred |
| B-005 | Add website mirror sync checks for Ana profile page. | Task | P2 | Profile validator | Mirror states profile source and no authority. | Website is mirror only. | No source-of-truth move. | Static site only. | Stop before production publish. | Ready |

## Dependency Map

- Must happen before Build: design acceptance, Vik architecture review, Matt sequencing, profile-conformance proof.
- Must happen before Equip: exact role queue format and needed tools.
- Must happen before Evaluate: acceptance scenarios and role-quality scorecard.
- Must happen before Deploy: Build, Equip, Evaluate, runtime target, rollback, approval.
- Can wait for Improve: periodic gap scan, scorecard tuning, website sync automation.

## First Slice Definition

- Slice: local role queue and candidate-role artifact flow.
- User-visible behavior: Ana can track candidate and draft roles without marking them active.
- Smallest proof: create/read/update one candidate role item and stop before activation.
- Required files/tools: Mindshare repo files, Obsidian maps-runs, MAPS helper.
- Authority/category constraints: no autonomous runtime and no authority grants.
- Memory/state constraints: write only approved Mindshare repo/Obsidian paths.
- Runtime target or adapter: supervised local workflow; no adapter.
- Approval gates: Scott approval before durable write implementation and any activation.
- Acceptance criteria: queue preserves statuses, records approval gates, routes handoffs, refuses activation.
- Stop condition: if role status would be interpreted as operating authorization.

## Deferred Improvement Backlog

| ID | Improvement | Trigger | Priority | Depends On | Evidence Needed |
|---|---|---|---|---|---|
| I-001 | Periodic role-gap scan. | Scott requests recurring review. | P2 | Evaluate pass and loop approval. | Loop design, stop conditions, approval. |
| I-002 | Role-overlap lint automation. | Repeated overlap findings. | P1 | Checklist success. | False-positive review. |
| I-003 | Website profile sync automation. | Profile mirror drift. | P2 | Validator stability. | Website mirror proof. |
