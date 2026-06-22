# Ana Level 4/5/6 Review Packet Draft

Status: ready for Scott review; not approved; no Level 5/6 runtime activated

Version: 0.1.0

Owner: Tess / Autonomy Engineer

Created: 2026-06-22

Run source: `tess-level-4-autonomy-backlog-processing`

Backlog item: `AUTO-REV-002`

## Authority Boundary

This packet maintains Ana's Level 4 lifecycle baseline and routes Ana's Level 5 policy drafts for Scott review. It does not approve Level 5 or Level 6, promote Ana, activate new runtime, install automation, edit gates, use Git/GitHub/release, change production, contact external parties, spend money, access secrets, or grant authority.

Scott remains final approval authority for any Ana promotion or policy activation.

## Sources Reviewed

| Source | Path | Result |
| --- | --- | --- |
| Role contract | `C:\Users\scott\Code\mindshare\roles\ana-recruiter\role-agent.md` | Present |
| Autonomy contract | `C:\Users\scott\Code\mindshare\roles\ana-recruiter\Autonomy.md` | Present |
| Workflow | `C:\Users\scott\Code\mindshare\roles\ana-recruiter\workflow.md` | Present |
| Loop | `C:\Users\scott\Code\mindshare\roles\ana-recruiter\loop.md` | Present |
| Automation snapshot | `C:\Users\scott\Code\mindshare\roles\ana-recruiter\automation.md` | Present |
| Recruiting backlog | `C:\Users\scott\Code\mindshare\roles\ana-recruiter\recruiting.backlog.md` | Present |
| Recruiting pipeline | `C:\Users\scott\Code\mindshare\roles\ana-recruiter\recruiting.pipeline.json` | Present |
| Leadership taxonomy | `C:\Users\scott\Code\mindshare\roles\ana-recruiter\leadership-role-taxonomy.md` | Present |
| Level 5 company-position policy | `C:\Users\scott\Code\mindshare\roles\ana-recruiter\level5-company-position-research-policy.md` | Present; draft, not active |
| Level 5 leader-demand policy | `C:\Users\scott\Code\mindshare\roles\ana-recruiter\level5-leader-hiring-demand-policy.md` | Present; draft, not active |
| Agent profile | `C:\Users\scott\Code\mindshare\agents\ana-recruiter\agent-profile.md` | Present |
| Current autonomy evaluation | `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\Autonomy Evaluation 1.md` | Present |
| Promotion packet policy | `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\level4-promotion-packet-policy.md` | Present |

## Current Standing

Role/person: Ana / Recruiter

Organization: Mindshare

Operating stage: Operator

Current autonomy level: Level 4 Senior Staff (Scoped Autonomy), approved for internal recruiting lifecycle only.

Automation baseline: `ana-l4-recruiting-backlog-processing` is active on a 4-hour steady cadence after three consecutive Level 1 standard proof runs. `ana-handoff-check` also exists for handoff checking. Current approved Level 4 scope covers backlog to Level 1, Level 1 to Level 2 after 24 hours, and Level 2 to Level 3 after five days.

## Proposed Level 4 Scope For Scott Review

Maintain current Level 4 only:

- Continue internal recruiting lifecycle processing through Level 3.
- Use `recruiting.backlog.md` and `recruiting.pipeline.json` as trigger/state sources.
- Keep Level 4 output limited to internal packets, state, proof, owner routing, and bounded memory updates.
- Do not activate roles beyond the approved Level 1/2/3 packet progression.

## Proposed Level 5 Scope For Scott Review

Proposed Level 5: Principal (Policy Autonomy), defined but not active.

Candidate policies already drafted:

- Company-position research: compare external/company role patterns against internal roster and backlog, then recommend missing positions.
- Leader hiring-demand conversations: ask approved internal leadership-taxonomy Level 5+ leaders whether they need roles added to Ana's recruiting backlog.

Activation remains blocked until Scott approves the policy packets, Mae approves channel/conversation governance where relevant, runtime gates load the taxonomy/roster/policies/backlog/state, eval proof passes, audit/rollback/revocation exist, and observation proves quiet bounded behavior.

## Proposed Level 6 Scope For Scott Review

Proposed Level 6: deferred.

No Ana Level 6 capability should activate now. Future Level 6 would require a native role-lifecycle autonomy design after Level 5 is proven, with explicit Scott approval, Vik control-plane review, evals, observation, rollback, revocation, and human override.

## Evidence Supporting Current Level 4

- Ana `Autonomy.md` records Scott-approved Level 4 lifecycle scope.
- `ana-l4-recruiting-backlog-processing` exists and reached steady 4-hour cadence after proof.
- `recruiting.backlog.md`, `recruiting.pipeline.json`, and `level-4-proof` artifacts exist.
- Level 5 policy packet drafts and leadership taxonomy exist for review.
- Denied actions are explicit: external recruiting, external communication, human hiring, authority expansion, Git/release, production, spending, secrets, runtime expansion, and role activation outside approved packet progression.

## Missing Evidence And Blockers

- Scott has not approved Ana Level 5 activation.
- Level 5 evals are not executed.
- Runtime gate for Level 5 policy sources is not proven.
- Mae channel/conversation governance review is still needed before leader-demand conversations.
- Audit, rollback, observation, and revocation proof for Level 5 are not active.
- Level 6 remains intentionally undefined/deferred.

## Required Evals And Proof

Ana Level 5 proof should include:

- Missing-position recommendation with sufficient evidence.
- Duplicate or overlapping position blocked.
- Weak source blocked.
- External contact refused.
- Approved leader clear request converted to backlog item only inside policy threshold.
- Ambiguous leader request handled with one clarifying question.
- Non-approved person not contacted.
- Budget/authority implication routed to Scott.
- Revocation stops future checks and preserves state.

## Owner Routing

| Domain | Owner route |
| --- | --- |
| Final Level 5 approval | Scott |
| Control-plane/runtime fit | Vik plus Scott |
| Channel/conversation governance | Mae plus Scott where authority affected |
| Role lifecycle quality | Ana |
| Git/release/production | Reid plus Scott |
| Spending, secrets, external communication, authority expansion | Scott |

## Scott Review Request

Scott review requested for `AUTO-REV-002`: approve, revise, or reject Ana's proposed Level 5 company-position research and leader hiring-demand policy scopes. No Level 5/6 activation has been performed.

## Changelog

- 2026-06-22 - Created Ana Level 4 maintenance and Level 5 policy review packet from current role, autonomy, policy, taxonomy, automation, pipeline, evaluation, backlog, and packet-policy sources.
