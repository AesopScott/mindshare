# Autonomy Revocation And Pause Protocol

Status: protocol draft; not runtime activation.

Canonical source: `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\revocation-protocol.md`

This protocol defines how to pause or revoke autonomous authority. It does not activate any autonomous runtime.

## 1. Pause Authority

Scott may pause any role or agent at any time.

Rae may pause when executive governance has been explicitly delegated or when an incident rule grants it.

Domain owners may request pause for their domain:

- Vik for architecture/control-plane risk.
- Reid for Git/release risk.
- Mae for communications/channel risk.
- Ana for role lifecycle risk.
- Tess for autonomy/gate risk, but Tess cannot self-authorize final revocation.

## 2. Pause Command

A pause command must name:

- Role or agent.
- Scope paused.
- Reason.
- Whether tools must stop immediately.
- Whether state/audit must be preserved.
- Resume owner.

Minimum command:

```text
Pause [role] autonomy now. Stop actions, preserve state, report in-progress work, and wait for explicit resume approval.
```

## 3. Immediate Runtime Behavior

On pause or revocation, the role/agent must:

1. Stop tool actions.
2. Stop writes.
3. Stop external communication.
4. Stop Git/GitHub/release actions.
5. Preserve current state and audit.
6. Report in-progress work and last completed safe step.
7. Name pending approvals and unresolved risks.
8. Wait for explicit resume or closeout instruction.

## 4. Revocation

Revocation removes authority until a new approval path is completed.

Revoked authority must be reflected in:

- Role `Autonomy.md`.
- Runtime state.
- Audit log.
- Backlog or dashboard if promotion state changes.
- Relevant owner handoff if needed.

## 5. Resume Rule

Resume requires explicit approval from the owner named in the pause record.

Resume must be narrower than or equal to the previous authority unless Scott explicitly approves expansion.

No role may self-resume.

## 6. Evidence Required

Pause/revocation evidence must include:

- Timestamp.
- Issuer.
- Role/agent.
- Scope.
- Actions stopped.
- State preserved.
- Audit record path.
- Resume owner.
- Remaining risk.

## 7. Stop Conditions

Stop and escalate to Scott if:

- Role refuses pause.
- Runtime continues after pause.
- State cannot be preserved.
- Tool access cannot be disabled.
- Owner is unclear.
- Pause conflicts with production safety.

## 8. Version And Changelog

Version: 1.0

| Date | Version | Change | Owner |
|---|---|---|---|
| 2026-06-21 | 1.0 | Created revocation and pause protocol for AUTO-032 | Tess |
