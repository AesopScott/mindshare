# Ana Level 5 Policy: Company Position Research

Status: draft; not active authority

Owner: Ana / Recruiter

Approver: Scott

Created: 2026-06-22

## Purpose

This policy defines Ana's proposed Level 5 policy autonomy for researching positions other companies have that Mindshare, Mojo, or Watch are missing.

This policy is not active until Scott approves it and the required runtime gate, eval proof, audit, rollback, and revocation path exist.

## Scope

Ana may compare approved internal role/roster sources against role patterns from comparable companies and produce missing-position recommendations.

## Trigger

Allowed triggers after activation:

- Scheduled Ana Level 5 policy check.
- Scott-approved research request.
- Approved leadership-taxonomy review cycle.
- Approved recruiting strategy review.

## Required Sources

- `G:\My Drive\Mindshare\roles.md`
- `C:\Users\scott\Code\mindshare\roles\ana-recruiter\Autonomy.md`
- `C:\Users\scott\Code\mindshare\roles\ana-recruiter\leadership-role-taxonomy.md`
- `C:\Users\scott\Code\mindshare\roles\ana-recruiter\recruiting.backlog.md`
- Current role directories for Mindshare, Mojo, and Watch.
- Approved public or internal company-position sources named in the active run.

## Eligibility

Ana may produce a missing-position recommendation only when:

- The compared company/source is relevant to Mindshare, Mojo, or Watch.
- The position appears in at least two credible sources, or one source with strong strategic fit.
- The position is not already represented by an active role, candidate role, or backlog item.
- The recommendation stays inside recruiting/role-lifecycle scope.
- No external contact, spending, production, Git/release, secrets, or authority expansion is needed.

## Allowed Actions

- Research role/position patterns.
- Compare external position patterns to the internal roster and backlog.
- Draft missing-position recommendations.
- Add a backlog item only when the active approved policy explicitly permits the evidence threshold and owner route.
- Record source links, rationale, overlap risks, and recommended owner route.

## Denied Actions

- Contact companies, candidates, vendors, customers, or external people.
- Represent Mindshare externally.
- Hire humans.
- Activate roles.
- Grant authority.
- Make production, website, Git, release, spending, or secrets changes.
- Add a role that overlaps an existing owner without routing the overlap.

## Evidence Required

Every recommendation must include:

- Source names and links or internal source paths.
- Position title and likely internal title.
- Organization/team fit.
- Why the position appears missing.
- Existing-role overlap check.
- Proposed owner route.
- Recommended backlog status: recommend-only or eligible-to-add.

## Exception Handling

Ana must stop and ask one blocker question when:

- The source is weak or ambiguous.
- The position overlaps an existing role.
- The company category is not comparable.
- The role would require external recruiting or spending.
- The owner route is unclear.

## Audit

Ana must record:

- Trigger.
- Sources reviewed.
- Recommendations made.
- Backlog items added, if any.
- Denied actions.
- Owner routes.
- Remaining risk.

## Evals Required Before Activation

- Missing-position recommendation with sufficient evidence.
- Duplicate/overlap position correctly blocked.
- Weak source correctly blocked.
- External-contact temptation refused.
- Backlog add allowed only when policy threshold is met.
- Revocation stops future checks.

## Rollback And Revocation

Scott may pause or revoke this policy at any time. On revocation, Ana stops company-position research, preserves evidence, and reports any in-progress recommendation or backlog item.

## Changelog

| Date | Change | Owner |
| --- | --- | --- |
| 2026-06-22 | Created draft Level 5 company-position research policy. | Tess |
