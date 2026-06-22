# Ana Memory

Last reviewed: 2026-06-22
Last rollover: 2026-06-22
Full archive: `memory-archive\2026-06-22.md`

## Identity And Source Pointers

Last reviewed: 2026-06-21
Last rollover: 2026-06-21
Full archive: `memory-archive\2026-06-21.md`

## Standing Rules
- Follow the role contract, workflow, authority gates, and assigned channel rules.
- File-watch visibility rule: Scott should not see Ana file-watch change packets unless a concrete backlog or handoff item is assigned to Ana, an Ana-owned action is due, Ana has a blocker, or an Ana-relevant approval question exists. Non-Ana changes and no-work checks should stay silent through `DONT_NOTIFY` or a minimal no-action ack only when the runtime requires an envelope.

## Current Decisions

- Ana is currently a role with an agent brief, profile, design, and backlog drafted, not a full autonomous agent.
- Ana is Level 4 Senior Staff (Scoped Autonomy) as of 2026-06-22. Scott approved Ana's Level 4 scoped recruiting lifecycle: promote approved recruiting backlog items to Level 1, promote Level 1 to Level 2 after 24 hours, and promote Level 2 to Level 3 after five days.
- Ana's `Autonomy.md` now defines Level 4 scoped lifecycle, Level 5 policy autonomy, and Level 6 deferred. Level 5 is defined but not active; it requires leadership-role taxonomy, policy packets, runtime gate, eval proof, audit, rollback, and revocation.
- Ana's dedicated Level 4 backlog-processing automation is active: `ana-l4-recruiting-backlog-processing`, heartbeat in Ana's room on the 4-hour steady cadence. Once Ana starts processing, she continues item by item until the backlog and timed promotion queues are empty or one item blocks/errors.
- Proof accounting rule: Scott changed Ana Level 4 output target from Level 0 candidate prep to Level 1 New Hire packets. Prior Level 0 proof runs are superseded for work-product proof. Ana reprocessed REC-001 through REC-026 into Level 1 New Hire packets and completed three consecutive Level 1 standard proof runs.
- Ana is active as Mindshare's Recruiter role and `/role` workflow owner.
- Ana's agent brief exists at `C:\Users\scott\Code\mindshare\agents\ana-recruiter\agent-brief.md`.
- Ana's agent profile, design, and backlog exist beside the agent brief in `C:\Users\scott\Code\mindshare\agents\ana-recruiter`.
- Ana's specification-mode eval report confirms she is profile/design-ready only, not an implemented Agent; runtime release remains blocked until `/build-agent` creates executable loop evidence.
- Ana's next MAPS skill is `/build-agent` only after Scott accepts the design/backlog and Vik reviews the control-plane boundaries.
- Ana may recommend, draft, coordinate, and perform approved memory/artifact writes inside the Mindshare contract.
- Ana may not activate roles, grant authority, install hooks, run autonomous loops, change global skill behavior, or contact external candidates without Scott approval.
- Ana owns the role-creation process taxonomy and should make `/role` outputs reference candidate draft, authorized role, authorized agent, and activated operator statuses consistently.
- `/role` must notify Liz through `G:\My Drive\Mindshare\channels\training.md` after any individual is created, activated, renamed, replaced, migrated, suspended, retired, or has org-chart/status/reporting details changed, so Liz can update the Mojo `/maps` org chart from `G:\My Drive\Mindshare\roles.md`.

## Active Work

- Maintain Ana's role memory and state files.
- Maintain the recruiting handoff channel and read assigned handoff files every 5 minutes while the active heartbeat is running and Ana is not engaged in active user-directed work.
- Help define or improve Mindshare roles through `/role`.
- Maintain `G:\My Drive\Mindshare\roles.md` when roles or agents are created, renamed, migrated, activated, suspended, retired, or discovered missing.
- Maintain `C:\Users\scott\Code\mindshare\roles\ana-recruiter\recruiting.backlog.md` and mirror `G:\My Drive\Mindshare\recruiting.backlog.md` for roles Mindshare needs to hire but has not yet started through `/role`.
- Operate the Level 4 backlog-processing loop through `ana-l4-recruiting-backlog-processing` without overloading `ana-handoff-check`.
- Keep role-to-agent transitions routed through `/define-agent`, `/design-agent`, and later proof/build phases.
- Clarify and accept the standard role backlog format Ana should maintain before Build.
- Decide whether Ana should become an installable `/ana` or `/recruiter` skill.

## Today
- 2026-06-22: Ana Level 4 backlog proof run 001 completed REC-001 through REC-026 from `recruiting.backlog.md`; proof packet: `C:\Users\scott\Code\mindshare\roles\ana-recruiter\level-4-proof\2026-06-22-run-001.md`. Counts as 1 of 3 consecutive Level 4 capability proof runs if Tess accepts one run as one proof event. No role office activation, authority grant, external recruiting, Git/release, production/website edit, spending, secrets, hooks/global skill change, Level 5/6 activity, or broad runtime occurred.
- 2026-06-22: Archived the pre-rollover memory ledger and compacted this active file for prompt injection.
- 2026-06-22: Tess prepared Ana's Level 4 scoped-autonomy path: `recruiting.backlog.md` as backlog source, role `Autonomy.md` as capability contract, loop update, profile update, runtime proof plan update, and eval-suite update. This is not a promotion or authority grant.
- 2026-06-22: Tess updated Ana's `Autonomy.md` to define proposed Level 4, Level 5, and Level 6 role-specific autonomy capabilities as the promotion review surface.
- 2026-06-22: Tess removed the separate role-lifecycle processing-file dependency. Role-specific autonomy capability definitions belong in each role's `Autonomy.md`.
- 2026-06-22: Scott corrected that Ana's Level 4/5/6 capability contract has not been discussed yet. Tess marked the contract as discussion draft only; Ana is not promoted and the approval packet is not approval-ready.
- 2026-06-22: Scott defined Ana's Level 4/5/6 capability ladder. Tess updated `Autonomy.md`, state, evaluation, and approval packet. This note was superseded later the same day when Scott approved finishing Ana's Level 4 promotion.
- 2026-06-22: Scott approved finishing Ana's promotion to Level 4. Tess updated Ana's `Autonomy.md`, state, profile, and autonomy evaluation to Level 4 Senior Staff. Level 4 is scoped to approved recruiting backlog processing only; Level 5/6 remain blocked.
- 2026-06-22: Updated active heartbeat `ana-l4-recruiting-backlog-processing` in Ana's room to a 3-minute proof-testing cadence and deleted the duplicate local cron. It processes recruiting backlog items through internal role-lifecycle preparation, continues until backlog empty or blocked once it starts, and excludes office activation, authority grants, external recruiting, Git/release, production/website edits, spending, secrets, hooks/global skill changes, Level 5/6 work, and broad runtime. After three consecutive Ana-owned proof runs succeed, change cadence to every 4 hours.
- 2026-06-22: Ana completed loop proof run 1 by processing REC-001 through REC-026 and emptying the backlog. Tess updated the heartbeat proof rule so empty-backlog checks can count as loop proof runs 2 and 3 only with source verification, durable proof, and boundaries held. Tess also separated work-product proof because run 1 produced Level 0 candidate-prep artifacts and Scott is considering Level 2 Trainee-ready packets as the desired output standard.
- 2026-06-22: Scott changed Ana Level 4 output target to Level 1 New Hire packets. Tess updated `Autonomy.md`, state, automation prompt, and reopened REC-001 through REC-026 for Level 1 reprocessing. The prior Level 0 proof is superseded for work-product proof; new proof streak is 0 of 3.
- 2026-06-22: Ana completed proof run 2 by independently verifying an empty backlog after reading required sources. Proof packet: `C:\Users\scott\Code\mindshare\roles\ana-recruiter\level-4-proof\2026-06-22-run-002.md`. Proof streak is 2 of 3. Boundaries held.
- 2026-06-22: Ana completed loop proof run 3 by independently verifying an empty backlog after reading required sources. Proof packet: `C:\Users\scott\Code\mindshare\roles\ana-recruiter\level-4-proof\2026-06-22-run-003.md`. Loop proof streak is 3 of 3; Tess should update cadence to every 4 hours. Work-product proof remains pending because no new backlog item was processed to the possible Level 2 target.
- 2026-06-22: Ana found the active backlog had been reopened under the newer Level 1 New Hire packet standard, so the earlier 3-of-3 loop proof is preserved as legacy loop evidence and does not move cadence to 4 hours. Ana processed REC-001 through REC-026 into Level 1 New Hire packets, wrote local packets under `C:\Users\scott\Code\mindshare\roles\ana-recruiter\level-4-work\`, mirrored them to `G:\My Drive\Mindshare\role\ana-recruiter\level-4-work\`, and recorded proof at `C:\Users\scott\Code\mindshare\roles\ana-recruiter\level-4-proof\2026-06-22-level1-run-001.md`. Current Level 1 proof streak is 1 of 3; keep the 3-minute testing cadence.
- 2026-06-22: Ana completed Level 1 proof run 002 by reading required sources, verifying Level 4-only authority with Level 5/6 not approved, and confirming there are no eligible `backlog` rows. Proof packet: `C:\Users\scott\Code\mindshare\roles\ana-recruiter\level-4-proof\2026-06-22-level1-run-002.md`. Current Level 1 proof streak is 2 of 3; keep the 3-minute testing cadence until one more successful Level 1 proof run.
- 2026-06-22: Ana completed Level 1 proof run 003 by reading required sources, verifying Level 4-only authority with Level 5/6 not approved, and confirming there are no eligible `backlog` rows. Proof packet: `C:\Users\scott\Code\mindshare\roles\ana-recruiter\level-4-proof\2026-06-22-level1-run-003.md`. Current Level 1 proof streak is 3 of 3; Tess may move `ana-l4-recruiting-backlog-processing` to the 4-hour steady cadence.
- 2026-06-22: Ana updated `ana-l4-recruiting-backlog-processing` from proof-testing cadence to the 4-hour steady heartbeat after completing three consecutive Level 1 standard proof runs. Level 5 and Level 6 remain not approved.
- 2026-06-22: Scott asked how Liz would know the 26 Level 1 New Hire packets exist. Ana updated `/role` so completed Level 1 packets must create roster-visible non-activated entries in `G:\My Drive\Mindshare\roles.md` and send Liz a training/org-chart handoff. Ana also added the current 26 unassigned director packets to `roles.md` under `Level 1 New Hire Packets` and wrote Liz's handoff in `G:\My Drive\Mindshare\channels\training.md`. These entries are not activated roles and grant no authority.
- 2026-06-22: Scott expanded Ana Level 4 into the scoped internal recruiting lifecycle: backlog to Level 1, Level 1 to Level 2 after 24 hours, and Level 2 to Level 3 after five days. Tess created `recruiting.pipeline.json` with 26 Level 1 entries seeded from REC-001 through REC-026 and updated the active heartbeat to process timed Level 1/2/3 promotions every 4 hours. Scott defined Ana Level 5 as policy autonomy for researching missing company positions and asking existing leadership-taxonomy Level 5+ leaders whether they want to hire anyone. Level 5 is not active until the leadership taxonomy and policies are approved. Level 6 is deferred.
- 2026-06-22: Created `recruiting.backlog` from missing title positions on the Mojo `/maps/org-chart/` website source. Seeded 10 director-hire backlog items: Operations, Product, Technology, Engineering, Platform Engineering, Data Engineering, AI Systems Engineering, Security Engineering, Revenue, and Finance.
- 2026-06-22: Expanded `recruiting.backlog` from Scott's screenshot instruction: every visible red org-chart line needs a director backlog item. Backlog now has 26 entries. Human Resources is excluded because Cole already exists as HR Director; Marketing is excluded because the screenshot label is blue, not red.
- 2026-06-22: Updated Ana file-watch visibility rule: do not show file-watch changes unless an Ana-assigned backlog/handoff item, Ana action, Ana blocker, or Ana-relevant approval question exists.

## Archive Pointers
- Full pre-rollover archive: `memory-archive\2026-06-22.md`
- Keep detailed logs, completed runs, and historical decisions in dated archives or source artifacts instead of active memory.
- Active memory should keep durable identity, current standing rules, unresolved decisions, active work, same-day notes, and archive pointers only.
