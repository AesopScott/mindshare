# Heartbeat And File-Watch Autonomy Policy

Status: policy draft; not scheduler activation.

Canonical source: `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\heartbeat-file-watch-policy.md`

This policy defines when heartbeat/file-watch behavior is allowed. It does not install, activate, schedule, or expand any watcher.

## 1. Core Rule

Watched-file detection is signal, not authority.

Seeing a changed file does not grant permission to act, write, notify, activate, publish, release, or expand authority.

## 2. Allowed Heartbeat Uses

Heartbeat or file-watch behavior may:

- Read explicitly assigned files.
- Detect concrete changed-file or handoff signals.
- Stay quiet when no relevant work exists.
- Produce a short status only when meaningful work, blocker, or routing issue exists.
- Record audit/state only when an approved runtime and audit path exists.

## 3. Denied Heartbeat Uses

Heartbeat or file-watch behavior may not:

- Read unrelated private channels.
- Wake a thread for routine no-work checks.
- Infer authority from changed files.
- Edit role authority, gates, runtime, release state, production state, secrets, spending, or external communication.
- Install new schedules, hooks, file watchers, or loops without Scott and Vik approval.
- Expand channel access without Mae and Scott approval.

## 4. Required Fields For Approved Watchers

Each approved heartbeat/watch must name:

- Role.
- Purpose.
- Cadence.
- Exact files or narrow globs.
- Quiet no-work rule.
- Visible notification triggers.
- Denied actions.
- Owner routing.
- State/audit location.
- Revocation path.
- Expiry or review cadence.

## 5. Notification Rules

Notify only when:

- A real blocker needs an owner.
- A watched handoff assigns work to the role.
- A boundary drift or wrong-channel issue appears.
- A gate block is open and owner visibility is needed.
- A safety rule requires escalation.

Stay quiet when:

- No relevant change exists.
- The change is outside assigned scope.
- The only finding is "still no work."

## 6. Owner Routing

- Channel scope questions: Mae.
- Architecture/runtime/watch design: Vik.
- Release/Git watch scope: Reid.
- Role lifecycle watch scope: Ana.
- Final activation and authority: Scott.

## 7. Version And Changelog

Version: 1.0

| Date | Version | Change | Owner |
|---|---|---|---|
| 2026-06-21 | 1.0 | Created heartbeat/file-watch autonomy policy for AUTO-030 | Tess |
