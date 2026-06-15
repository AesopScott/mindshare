---
name: deploy-agent
description: Create the MAPS Deploy phase artifact for an agent or multi-agent system. Use when preparing release plans, runtime configuration, secrets, identities, approvals, rollout strategy, rollback plans, and post-deploy verification.
---

# Deploy Agent

## Overview

Use this skill to release an evaluated agent into a real environment with controls.

## Workflow

1. Confirm eval evidence and release readiness.
2. Identify the deployment target and runtime requirements.
3. Define secrets, identity, permissions, and configuration.
4. Choose rollout, approval, and rollback strategy.
5. Specify post-deploy verification.
6. Name owners and operating contacts.
7. Produce a deployment plan.

## Output

Return:

- Target environment
- Artifact and configuration
- Secrets and identity
- Release gates
- Rollback plan
- Post-deploy verification
- Owners

Use `templates/deployment-plan.md` from the MAPS repo when working inside this repository.

## Done Criteria

- The release is controlled.
- Runtime access is intentional.
- Rollback is possible.
- Verification happens after deployment.
