# Autonomy Promotion Dashboard

Status: planning dashboard; not authority.

Canonical source: `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\autonomy-dashboard.md`

This dashboard summarizes autonomy readiness from source artifacts. It does not activate any role, grant authority, edit gates, deploy runtime, or approve promotion.

## 1. Source Inputs

- Backlog: `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\autonomy-backlog.json`
- Inventory: `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\autonomy-inventory.json`
- Requirements: `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\autonomy-requirements.md`
- Shared evals: `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\evals\autonomy-promotion-eval-suite.json`

## 2. Current State

| Area | Status | Notes |
|---|---|---|
| Requirements | Drafted | Needs Scott/Vik final approval before it becomes a closed contract |
| Inventory/schema | Complete | Inventory remains evidence, not authority |
| Contract template | Complete | Autonomy.md template exists |
| Source loader/validator | Complete | Shared loader and validator exist |
| Strict-intent gate | Complete | Design and proof harness exist |
| Shared evals | Complete | 18 eval classes defined |
| State/audit schema | Complete | Schemas exist |
| Runtime adapter | Blocked | No runtime target selected/approved |
| Role tracks | Mostly complete | Lab Operator remains blocked until operating role approval |
| Shared policies | In progress | Dashboard/policy/routing/revocation files complete this slice |

## 3. Role Track Status

| Role | Track | Status |
|---|---|---|
| Rae | Executive governance readiness | Complete |
| Ana | Role-lifecycle readiness | Complete |
| Cal | MAPS sequencing readiness | Complete |
| Vik | Architecture hardening | Complete; promotion deferred |
| Liz | Training coordination readiness | Complete |
| Mae | Communications governance readiness | Complete |
| Reid | Release management readiness | Complete |
| Tess | Autonomy governance readiness | Complete |
| Bea | MAPS engineering readiness | Complete |
| Lab Operator | Lab queue operations | Blocked until Scott approves operating role |
| Jay | Watch meetup/customer-success readiness | Complete |
| Matt | Released legacy | Complete; no-promotion block |

## 4. Promotion Blockers

- `AUTO-001`: requirements contract is drafted, not final approved.
- `AUTO-013`: runtime adapter build is blocked until runtime target is selected.
- `AUTO-026`: Lab Operator is blocked until Scott approves operating role.
- No role is activated as autonomous Executor by this dashboard.

## 5. Owner Routes

- Scott: final authority, activation, authority expansion, production, spending, secrets.
- Vik: architecture/control-plane fit.
- Reid: Git/GitHub/release/branch/PR/promotion.
- Mae: communications/channel governance.
- Ana: role lifecycle.
- Rae: executive governance when delegated.
- Tess: autonomy review, recommendations, gate drafts only.

## 6. Version And Changelog

Version: 1.0

| Date | Version | Change | Owner |
|---|---|---|---|
| 2026-06-21 | 1.0 | Created shared autonomy dashboard for AUTO-029 | Tess |
