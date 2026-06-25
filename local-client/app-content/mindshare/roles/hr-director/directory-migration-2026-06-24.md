# Role Directory Migration Notice - 2026-06-24

Owner: Cole / HR Director

Status: applied for active local role roots and canonical role mirrors.

## Decision

Canonical role directories use role/function slugs only. Proper names stay inside role files and room cards.

This is a file-structure cleanup only. It does not grant authority, activate runtime, approve promotion, change lifecycle status, change reporting lines, approve Git/release or production work, contact external parties, spend money, use secrets, or change anyone's role contract.

## Mindshare Changes

| Person | Role | Old local directory | New local directory |
| --- | --- | --- | --- |
| Ana | Recruiter | `C:\Users\scott\Code\mindshare\roles\ana-recruiter` | `C:\Users\scott\Code\mindshare\roles\recruiter` |
| Vik | Agentic Systems Program Architect | `C:\Users\scott\Code\mindshare\roles\vik-aspa` | `C:\Users\scott\Code\mindshare\roles\agentic-systems-program-architect` |

## Mojo Changes

| Person | Role | Old local directory | New local directory |
| --- | --- | --- | --- |
| Bea | Mojo MAPS Engineer | `C:\Users\scott\Code\mojo\roles\bea` | `C:\Users\scott\Code\mojo\roles\mojo-maps-engineer` |
| Cal | MAPS ASPM | `C:\Users\scott\Code\mojo\roles\cal` | `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-manager` |
| Liz | Mojo Website Manager | `C:\Users\scott\Code\mojo\roles\liz` | `C:\Users\scott\Code\mojo\roles\mojo-website-manager` |
| Matt | Released MAPS ASPM | `C:\Users\scott\Code\mojo\roles\matt` | `C:\Users\scott\Code\mojo\roles\released-maps-agentic-systems-program-manager` |
| Vik | MAPS ASPA | `C:\Users\scott\Code\mojo\roles\vik` | `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect` |

`C:\Users\scott\Code\mojo\roles\lab-operator` was already canonical and was not renamed.

## Mirror Changes

Canonical role mirrors under `G:\My Drive\Mindshare\role` and `G:\My Drive\Mojo\role` were updated for the same active role roots where matching mirrors existed.

## Notification Text

Use this wording when updating each person:

Your role directory is being standardized to the role/function slug naming rule. Your proper name remains your identity and invocation name inside your files, but the filesystem directory now uses the role name. This does not change your authority, autonomy, lifecycle status, runtime, reporting line, or permissions.

## Verification

- Active local role roots in Mindshare now use role/function slugs.
- Active local role roots in Mojo now use role/function slugs.
- Live FileWatch and heartbeat config references were updated where they pointed at renamed role roots.
- Current role mirrors and Who Am I cards were updated where they pointed at renamed role roots.
