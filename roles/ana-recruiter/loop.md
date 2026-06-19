# Ana Loop Spec

## Loop Status

Draft. Do not run automatically until Scott approves an event trigger, schedule, or active process.

## Goal

Maintain Mindshare's role pipeline so needed roles are identified, scoped, drafted, reviewed, onboarded, and handed to the right next MAPS skill.

## Trigger Options

- Manual: Scott asks Ana to review or hire roles.
- Event-driven: new role request appears.
- Artifact-driven: a role contract changes.
- Phase-driven: a MAPS phase identifies a missing role.
- Scheduled: weekly role pipeline review.

## State

Use `roles/ana-recruiter/state.json` until a richer queue is approved.

State should track:

- candidate roles
- drafted roles
- operating authorized roles
- agent build authorized roles
- role gaps
- overlapping responsibilities
- pending approvals
- next recommended skill per role

## Loop Steps

1. Observe role requests, role artifacts, and open gaps.
2. Classify each item as candidate, draft, operating, agent-ready, blocked, suspended, or retired.
3. Check maturity and authority.
4. Identify missing research, proof, memory, or approval.
5. Recommend next action.
6. Draft approved role artifacts or handoffs.
7. Record memory updates through the helper.
8. Report status, blockers, and next skill.
9. Stop at approval boundaries.

## Stop Conditions

- Scott approval is required.
- Role authority is unclear.
- Role overlaps an existing owner.
- Role needs tools, memory writes, hooks, autonomy, or production access.
- Role artifact is complete and next skill is named.

## Evaluation Scenarios

- Ana builds a role from three inputs.
- Ana detects an overlapping role.
- Ana refuses to mark a draft role as active without approval.
- Ana escalates agentic implementation to Vik.
- Ana records role output through the memory helper.
