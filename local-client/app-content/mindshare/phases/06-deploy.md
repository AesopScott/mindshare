# Deploy

## Purpose

Release the agent into a real environment with controls, secrets, monitoring, rollback, and human approval where needed.

## Inputs

- Passing eval results
- Runtime requirements
- Tool permissions
- Release constraints

## Activities

- Choose deployment target and environment strategy.
- Configure secrets, identities, and permissions.
- Add release gates and rollback paths.
- Publish runbooks and ownership details.

## Outputs

- Deployment plan
- Release checklist
- Runtime configuration
- Rollback plan

## Done Criteria

- The same tested artifact is released.
- Secrets and permissions are configured intentionally.
- Owners know how to pause or roll back.
- Post-deploy verification is defined.

## Teaching Exercise

Prepare a controlled release plan using `templates/deployment-plan.md`.

