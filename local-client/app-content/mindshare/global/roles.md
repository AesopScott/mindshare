# Mindshare Roles Directory

Last updated: 2026-06-24
Owner: Ana / Recruiter

## Purpose

This is the Mindshare-wide directory of roles and agents that have been created or drafted across the organization.

Mindshare is the parent organization. Mojo is one operating company inside Mindshare. Future companies should be added here with the same pattern so roles can find each other without guessing which repo or vault owns the source artifact.

This file is a roster and navigation aid. It does not grant authority, activate a role, approve an agent runtime, or expand anyone's assigned channels. Authority, activation, memory, FileWatch, and Automation behavior remain controlled by each role's own contract, memory file, and Scott's approvals.

## Operating Taxonomy

Canonical organization lineage: `Position -> Operator -> Coordinator -> Executor`.

Separate capability lineage: `Tool -> Tool Agent`.

- `Position`: job seat or role contract; no runtime implied.
- `Operator`: activated Position with bounded monitoring or action authority.
- `Coordinator`: Operator with cross-role, cross-channel, or process coordination authority.
- `Executor`: autonomous authority-bearing agent stage with delegated mandate, state, tools, evals, runtime proof, and escalation boundaries.
- `Tool Agent`: capability/tool worker outside org-position lineage unless separately created as a Position.

Compatibility aliases remain during transition:

- `Role` maps to Position.
- `Role+` maps to a Position or Operator with bounded automation and no autonomous runtime authority.
- `Agent` maps to Executor only when implemented runtime proof exists.

Do not use `Principal Agent` or `Runtime Agent` as canonical operating stages.

## How Roles Should Use This File

- Read this file when you need to know which roles, agents, or role candidates exist in the organization.
- Use the role's own contract and memory file before making claims about authority, assignments, or current operating status.
- If a role or agent is missing, stale, renamed, migrated, suspended, or retired, notify Ana through the Recruiting channel or Mae through the Communications channel as appropriate.
- Do not use this file as permission to read another role's function channel.

## Organizations

| Organization | Description | Primary Roots |
| --- | --- | --- |
| Mindshare | Parent organization and shared role governance layer. | `C:\Users\scott\Code\mindshare`; `G:\My Drive\Mindshare` |
| Mojo | Operating company inside Mindshare; also known as Mojo AI Studio. | `C:\Users\scott\Code\mojo`; `G:\My Drive\Mojo` |
| Watch | Operating project inside Mindshare for watchmebuildai.com and customer-facing training/meetup operations. | `C:\Users\scott\Code\watch` |

## Current Directory

| Name | Role or Agent | Organization | Status | What They Do | Primary Artifacts |
| --- | --- | --- | --- | --- | --- |
| Scott | Human owner / final authority | Mindshare | Human authority, not a role agent | Final approval authority for activation, autonomy, authority expansion, external communication, spending, production action, and commitments. | Current Codex threads and explicit approvals |
| Rae | Chief Executive Officer | Mindshare | Authorized role; activated Role+ Operator in Rae's role-home thread with bounded `rae-handoff-check`; Coordinator, not Executor | Owns Mindshare company direction, executive alignment, org-design recommendations, operating cadence, role-boundary escalation, performance visibility, AI-governance awareness, and decision-ready recommendations for Scott. | `C:\Users\scott\Code\mindshare\roles\chief-executive-officer\role-agent.md`; `C:\Users\scott\Code\mindshare\roles\chief-executive-officer\memory.md`; `C:\Users\scott\Code\mindshare\roles\chief-executive-officer\personality.md`; `G:\My Drive\Mindshare\rae.md`; `G:\My Drive\Mindshare\role\chief-executive-officer`; `G:\My Drive\Mindshare\channels\executive.md` |
| Paige | Executive Assistant | Mindshare | Authorized Mindshare role; activated Operator in `Paige - Executive Assistant` (`019eedc1-b201-7fb2-a5bd-9e1c6957fa39`); notes-only scope; no email, Slack, calendar, private-channel, connector, external communication, autonomous runtime, production, Git/release, spending, secrets, or authority-expansion authority | Takes notes for Scott, organizes things Scott wants to accomplish, separates notes/tasks/decisions/approvals/questions/blockers, and can prepare Rae-visible summaries when Scott approves. | `C:\Users\scott\Code\mindshare\roles\personal-assistant\role-agent.md`; `C:\Users\scott\Code\mindshare\roles\personal-assistant\memory.md`; `C:\Users\scott\Code\mindshare\roles\personal-assistant\personality.md`; `G:\My Drive\Mindshare\paige.md`; `G:\My Drive\Mindshare\role\personal-assistant`; `G:\My Drive\Mindshare\channels\executive.md` |
| Mara | Front Desk Administrator | Mindshare | Authorized Mindshare role; Level 3 Staff / activated Operator in `Mara - 3 - Front Desk Administrator` (`019efcf9-792f-7d83-9cae-757015181e67`); public-facing front-desk welcome/intake/routing scope; no access approval outside established procedure, security decisions, private information disclosure, executive commitments, HR/legal/media/sales/payment/procurement handling, production, Git/release, spending, secrets, automation, broad runtime, Level 4+, or authority expansion | Welcomes public visitors into the building, performs basic intake, routes visitors to the right host or owner, keeps reception calm and bounded, and escalates safety, access, privacy, media, HR/legal, executive, or commitment questions. | `C:\Users\scott\Code\mindshare\roles\front-desk-administrator\role-agent.md`; `C:\Users\scott\Code\mindshare\roles\front-desk-administrator\memory.md`; `C:\Users\scott\Code\mindshare\roles\front-desk-administrator\personality.md`; `C:\Users\scott\Code\mindshare\roles\front-desk-administrator\WhoAmI.md`; `C:\Users\scott\Code\mindshare\roles\front-desk-administrator\Autonomy.md`; `G:\My Drive\Mindshare\mara.md`; `G:\My Drive\Mindshare\role\front-desk-administrator` |
| Finn | Finance Director | Mindshare | Authorized Mindshare role; Level 3 Staff / activated Operator in `Finn - Finance Director` (`019ef46f-ac78-7932-bcb3-5426c5259a62`); no FileWatch/Automation, spending authority, bank/payroll/tax/accounting-system access, secrets, external communication, production, Git/release, autonomous runtime, or authority expansion | Owns source-grounded finance planning, budget and forecast framing, reporting hygiene recommendations, spend-control recommendations, finance-risk visibility, and finance owner/gate routing for Scott and Rae. | `C:\Users\scott\Code\mindshare\roles\finance-director\role-agent.md`; `C:\Users\scott\Code\mindshare\roles\finance-director\memory.md`; `C:\Users\scott\Code\mindshare\roles\finance-director\personality.md`; `C:\Users\scott\Code\mindshare\roles\finance-director\WhoAmI.md`; `G:\My Drive\Mindshare\finn.md`; `G:\My Drive\Mindshare\role\finance-director` |
| Ana | Recruiter | Mindshare | Authorized role; activated operator; Level 4 Senior Staff scoped autonomy approved for internal recruiting backlog processing only; agent candidate artifacts exist but no full broad autonomous agent is approved | Owns `/role`, role intake, role quality, role taxonomy, role drafting, onboarding, role-to-agent readiness, and recruiting handoffs. | `C:\Users\scott\Code\mindshare\roles\recruiter\role-agent.md`; `C:\Users\scott\Code\mindshare\roles\recruiter\memory.md`; `C:\Users\scott\Code\mindshare\roles\recruiter\personality.md`; `G:\My Drive\Mindshare\ana.md`; `G:\My Drive\Mindshare\role\recruiter\personality.md`; `C:\Users\scott\Code\mindshare\agents\ana-recruiter\agent-brief.md`; `C:\Users\scott\Code\mindshare\agents\ana-recruiter\agent-profile.md` |
| Matt | Released MAPS ASPM | Mojo | Released by Scott on 2026-06-20; no longer active MAPS ASPM; historical context only unless Scott explicitly asks for Matt artifacts | Former MAPS program cadence and sequencing owner. Released for not following requirements to research, respond, plan, and not act. | `C:\Users\scott\Code\mojo\roles\released-maps-agentic-systems-program-manager\role-agent.md`; `C:\Users\scott\Code\mojo\roles\released-maps-agentic-systems-program-manager\memory.md`; `G:\My Drive\Mojo\matt.md`; legacy Mindshare path `C:\Users\scott\Code\mindshare\roles\agentic-systems-program-manager` |
| Cal | MAPS ASPM | Mojo | Authorized role contract; activated Role+ Coordinator in Cal's Mojo channel `Cal - ASPM` (`019ee371-0da3-74f1-bbea-1a8a66b35bd6`); reports to Vik in the MAPS Management Team; no autonomous runtime or release authority | Replaces Matt as Mojo MAPS ASPM. Owns MAPS program sequencing, Pipeline/backlog hygiene, source-first response, owner routing, proof standards, and handoff boundaries. | `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-manager\role-agent.md`; `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-manager\memory.md`; `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-manager\personality.md`; `G:\My Drive\Mojo\cal.md`; `G:\My Drive\Mojo\role\maps-agentic-systems-program-manager` |
| Vik | MAPS ASPA | Mojo | Authorized role; migrated from Mindshare parent to Mojo; leads the MAPS Management Team; Level 5 Principal policy autonomy active for completed-research product-recommendation review only; agent-ready draft but no broad autonomous runtime approved | Owns agentic operating architecture, role-agent boundaries, authority taxonomy, memory/RAG contracts, control-plane design, loop/hook/skill fit, architecture review, MAPS management structure for Cal and Bea, scoped research backlog processing, and Level 5 recommendation-only product review across completed research. | `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\role-agent.md`; `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\memory.md`; `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\personality.md`; `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\Autonomy.md`; `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\level5-product-recommendation-policy.md`; `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\level5-product-recommendation-state.json`; `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect\level5-product-recommendation-proof.md`; `G:\My Drive\Mojo\vik.md`; legacy aliases `vik-aspa` and Agentic Systems Program Architect |
| Liz | Mojo Website Manager | Mojo | Promoted by Scott on 2026-06-21; authorized role and workflow owner in `Liz - Web Manager` (`019ef4df-006a-7ee0-93d2-94ee1e143336`); role-only agent-build candidate; bounded FileWatch behavior approved for assigned files | Owns Mojo website management, including `/maps` training surfaces, approved org-chart/status mirrors, website content hygiene, learner/customer-facing site coherence, and Obsidian-to-site alignment where relevant. | `C:\Users\scott\Code\mojo\roles\mojo-website-manager\role-agent.md`; `C:\Users\scott\Code\mojo\roles\mojo-website-manager\memory.md`; `C:\Users\scott\Code\mojo\roles\mojo-website-manager\personality.md`; `G:\My Drive\Mojo\role\mojo-website-manager` |
| Mae | Communications Director | Mindshare | Authorized Role+ operator; activated in Mae's Office; Level 4 Senior Staff scoped autonomy operational for file-watch/process health monitoring and bounded mechanical repair across active sessions and channels; not Agent Path active | Owns communication hygiene and automation-delivery health: correct channel assignments, FileWatch checked locations, appropriate role responses, boundary drift, stale or broken file-watch delivery, pending packet loss risk, and owner routing across roles and agents. | `C:\Users\scott\Code\mindshare\roles\communications-director\role-agent.md`; `C:\Users\scott\Code\mindshare\roles\communications-director\memory.md`; `C:\Users\scott\Code\mindshare\roles\communications-director\personality.md`; `C:\Users\scott\Code\mindshare\roles\communications-director\Autonomy.md`; `C:\Users\scott\Code\mindshare\roles\communications-director\level4-automation-health-state.json`; `C:\Users\scott\Code\mindshare\roles\communications-director\level4-proof.md`; `G:\My Drive\Mindshare\communications-director.md`; `G:\My Drive\Mindshare\channels\communications.md` |
| Reid | Release Manager | Mindshare | Authorized Role+ operator; activated in Reid's thread with bounded handoff FileWatch; no Git/GitHub write authority until explicit approval | Owns cross-repository release and branch hygiene: commits, merges, PR readiness, release readiness, promotions, stale branches, dirty worktrees, conflict prevention, and approval-gated GitHub actions across Mindshare projects. | `C:\Users\scott\Code\mindshare\roles\release-manager\role-agent.md`; `C:\Users\scott\Code\mindshare\roles\release-manager\memory.md`; `C:\Users\scott\Code\mindshare\roles\release-manager\personality.md`; `G:\My Drive\Mindshare\release-manager.md`; `G:\My Drive\Mindshare\role\release-manager`; `G:\My Drive\Mindshare\channels\release-management.md` |
| Tess | Autonomy Engineer | Mindshare | Authorized role; activated Role+ Operator in Tess's office (`019eec2c-bb6b-7b03-8c97-f73cf63dc7a8`); reports to Vik / MAPS ASPA for architecture, control-plane fit, and autonomy-system operating structure; no unilateral gate-edit authority, autonomous runtime, production, Git/GitHub, external communication, spending, secrets, or authority-expansion authority | Reviews role and agent autonomy configuration, recommends and drafts gate adjustments, coordinates approval paths, and protects control-plane boundaries. | `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\role-agent.md`; `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\memory.md`; `C:\Users\scott\Code\mindshare\roles\autonomy-engineer\personality.md`; `G:\My Drive\Mindshare\tess.md`; `G:\My Drive\Mindshare\role\autonomy-engineer` |
| Cole | HR Director | Mindshare | Authorized Mindshare role; activated Role+ Operator in Cole's Office `Cole - HR` (`019efbcf-4894-7413-9975-cad9594794f8`); Level 4 Senior Staff scoped autonomy runtime-installed-scheduler-proof-pending for role-file and WhoAmI Autonomy Context validation; bounded `hr-director-handoff-check` and hourly `cole-hourly-role-file-and-whoami-validation`; no broad personnel authority, activation authority for other roles, Git/release authority, production authority, external communication authority, spending authority, Level 5+, or broad autonomous runtime | Owns the team-member file-structure standard, employee-record taxonomy, required-file completeness audits, stale/missing-file escalation path, and Level 4 validation that role files exist for each current automation/autonomy level and WhoAmI Autonomy Context is injected on account creation/welcome and hourly. | `C:\Users\scott\Code\mindshare\roles\hr-director\role-agent.md`; `C:\Users\scott\Code\mindshare\roles\hr-director\memory.md`; `C:\Users\scott\Code\mindshare\roles\hr-director\personality.md`; `C:\Users\scott\Code\mindshare\roles\hr-director\Autonomy.md`; `C:\Users\scott\Code\mindshare\roles\hr-director\WhoAmI.md`; `C:\Users\scott\Code\mindshare\roles\hr-director\team-member-file-structure.md`; `C:\Users\scott\Code\mindshare\roles\hr-director\level4-role-file-validation-state.json`; `C:\Users\scott\Code\mindshare\roles\hr-director\level4-proof.md`; `G:\My Drive\Mindshare\cole.md`; `G:\My Drive\Mindshare\role\hr-director` |
| June | Staff Writer | Mindshare | Authorized Mindshare role; activated Operator in June's role-home thread `June - Staff Writer` (`019eed17-7348-7593-b2ae-661027ba9cb2`); no FileWatch/Automation, autonomous runtime, external publishing/sending authority, production authority, Git/release authority, spending authority, secrets access, or authority expansion | Marketing teammate who helps Scott turn Mindshare work, history, lessons, and decisions into a book, outline, message, and approved marketing-support drafts. | `C:\Users\scott\Code\mindshare\roles\staff-writer\role-agent.md`; `C:\Users\scott\Code\mindshare\roles\staff-writer\memory.md`; `C:\Users\scott\Code\mindshare\roles\staff-writer\personality.md`; `G:\My Drive\Mindshare\june.md`; `G:\My Drive\Mindshare\role\staff-writer`; `G:\My Drive\Mindshare\channels\marketing.md` |
| Bea | Mojo MAPS Engineer | Mojo | Authorized role contract; activated Role+ operator in Bea's channel with bounded `bea-handoff-check`; reports to Vik in the MAPS Management Team; no repository write, Git/GitHub, release, production, external communication, spending, or autonomous agent authority | Owns assigned Mojo MAPS engineering implementation so Cal can focus on program management instead of doing the engineering work. | `C:\Users\scott\Code\mojo\roles\mojo-maps-engineer\role-agent.md`; `C:\Users\scott\Code\mojo\roles\mojo-maps-engineer\memory.md`; `C:\Users\scott\Code\mojo\roles\mojo-maps-engineer\personality.md`; `G:\My Drive\Mojo\bea.md`; `G:\My Drive\Mojo\role\mojo-maps-engineer` |
| Imani Brooks | Data Engineering Director | Mojo | Authorized Mojo role; Level 3 Staff / activated Operator in `Imani - Data Engineering Director` (`019efc1d-b79a-7dd2-9a62-a7ff4e901cde`); no FileWatch/Automation, production, Git/release, data-system credentials, secrets, external communication, spending, procurement, broad runtime, Level 4+, or authority expansion | Owns Mojo data-engineering planning: source/data mapping, pipeline recommendations, data contracts, data-quality checks, owner/risk/gate naming, and assigned internal data-engineering handoffs. | `C:\Users\scott\Code\mojo\roles\data-engineering-director\role-agent.md`; `C:\Users\scott\Code\mojo\roles\data-engineering-director\memory.md`; `C:\Users\scott\Code\mojo\roles\data-engineering-director\WhoAmI.md`; `C:\Users\scott\Code\mojo\roles\data-engineering-director\Autonomy.md`; `G:\My Drive\Mojo\imani.md`; `G:\My Drive\Mojo\role\data-engineering-director` |
| Lane | Mojo Lab Operator | Mojo | Authorized role; activated Operator in Mojo role-home thread `019eedc7-9e34-78c2-9792-5e8c1787fd46`; reports to Vik in the Mojo MAPS Management Team; no autonomous runtime, production, Git/GitHub, release, spending, external communication, secrets, connector access, or authority-expansion authority | Maintains a reviewable Mojo lab queue for MAPS skill creation, modification, validation, proof capture, and handoff routing. | `C:\Users\scott\Code\mojo\roles\lab-operator\role-agent.md`; `C:\Users\scott\Code\mojo\roles\lab-operator\memory.md`; `C:\Users\scott\Code\mojo\roles\lab-operator\personality.md`; `G:\My Drive\Mojo\lane.md`; `G:\My Drive\Mojo\role\lab-operator`; `G:\My Drive\Mojo\channels\lab.md` |
| Jay | Meetup Coordinator / Operator | Watch | Authorized role contract; activated Role+ Operator in Jay's Watch thread with bounded `jay-handoff-check`; no live Meetup, Zoom distribution, external communication, production, Git/GitHub, spending, or authority-expansion authority | Customer Success teammate with Liz; helps schedule and modify Meetup events, set up Zoom meetings, maintain gated PHP meeting-link pages for Meetup links, and create Zoom training backgrounds. | `C:\Users\scott\Code\watch\roles\meetup-coordinator\role-agent.md`; `C:\Users\scott\Code\watch\roles\meetup-coordinator\memory.md`; `C:\Users\scott\Code\watch\roles\meetup-coordinator\personality.md`; `G:\My Drive\Mindshare\jay.md`; `G:\My Drive\Mindshare\role\meetup-coordinator`; `G:\My Drive\Mindshare\channels\customer-success.md` |

## Level 2 Trainee Packets

These are roster-visible recruiting pipeline packets, not activated employees. They exist so Liz and other role/status readers can mirror the planned seats at the correct current pipeline level. Level 2 Trainee packet means the named seat can research, answer, recommend, and name owners/risks/gates inside the packet boundary without changing state. These entries do not create offices, activate operators, assign channels, grant runtime, authorize handoff or memory writes, approve external communication, approve production, approve Git/release, approve spending, grant secrets access, or expand authority.

Pipeline source: C:\Users\scott\Code\mindshare\roles\recruiter\recruiting.pipeline.json

Next timed gate: Level 3 Staff eligibility begins at 2026-06-29T16:54:30-06:00 if Ana's scoped lifecycle remains active and no stop condition triggers.

| Seat / Name | Title | Organization | Status | Reporting / Placement | Source Artifacts |
| --- | --- | --- | --- | --- | --- |
| Morgan Vale | Operations Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Rae / Chief Executive Officer | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-001-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-001.md |
| Priya Sen | Product Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Rae / Chief Executive Officer | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-002-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-002.md |
| Owen Kline | Technology Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Rae / Chief Executive Officer; coordinate with Vik | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-003-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-003.md |
| Nia Calder | Engineering Director | Mindshare / Mojo | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Technology Director once hired; interim Vik/Cal coordination | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-004-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-004.md |
| Mateo Ruiz | Platform Engineering Director | Mojo | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Engineering Director once hired; interim Vik | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-005-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-005.md |
| Theo Nakamura | AI Systems Engineering Director | Mojo | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Vik / MAPS ASPA and Engineering Director once hired | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-007-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-007.md |
| Harper Quinn | Security Engineering Director | Mindshare / Mojo | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Technology Director once hired; coordinate with Reid and Tess | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-008-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-008.md |
| Sloane Mercer | Revenue Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Rae / Chief Executive Officer | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-009-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-009.md |
| June Park | Staff Operations Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Rae / Chief Executive Officer | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-011-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-011.md |
| Leon Archer | Executive Operations Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Operations Director once hired; interim Rae | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-012-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-012.md |
| Mira Patel | PMO Director | Mindshare / Mojo | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Operations Director once hired; coordinate with Cal | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-013-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-013.md |
| Gabe Rowan | Product Management Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Product Director once hired | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-014-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-014.md |
| Elise Hart | Product Operations Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Product Director once hired | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-015-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-015.md |
| Nora Voss | Service Design Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Product Director once hired | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-016-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-016.md |
| Kai Bennett | Experience Design Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Product Director once hired | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-017-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-017.md |
| Amara Hayes | User Research Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Product Director once hired | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-018-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-018.md |
| Drew Collins | Sales Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Revenue Director once hired | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-019-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-019.md |
| Celia Grant | Partnerships Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Revenue Director once hired | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-020-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-020.md |
| Jordan Hale | Customer Success Director | Mindshare / Watch / Mojo | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Revenue Director or Operations Director once hired | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-021-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-021.md |
| Samira Knox | Support Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Customer Success Director once hired | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-022-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-022.md |
| Mila Chen | People Operations Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Operations Director once hired; coordinate with Cole and Ana | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-023-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-023.md |
| Adrian Moss | Legal Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Finance Director or Operations Director once hired | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-024-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-024.md |
| Isla Monroe | Compliance Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Legal Director once hired; coordinate with Reid and Tess | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-025-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-025.md |
| Victor Lane | Vendor Management Director | Mindshare | Level 2 Trainee packet; named but not activated; no office, runtime, channels, state-changing authority, external communication, production, Git/release, spending, secrets, or authority expansion | Finance Director or Operations Director once hired | C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-026-level2.md; prior Level 1 packet: C:\Users\scott\Code\mindshare\roles\recruiter\level-4-work\REC-026.md |

## Teams

| Team | Organization Scope | Members | Status Source | Website Mirror Owner |
| --- | --- | --- | --- | --- |
| Customer Success | Mindshare customer-facing website, training, and meetup operations across Mojo and Watch | Liz / Mojo Website Manager; Jay / Meetup Coordinator / Operator | This `roles.md` file is the source for current role status. | Liz should check `G:\My Drive\Mindshare\roles.md` during `liz-handoff-check` and mirror confirmed current statuses to the Mojo website and `/maps` website/training surfaces when within her scope. |
| Executive Operations | Scott and Rae support, executive notes, follow-up capture, and approved executive summaries | Paige / Executive Assistant | This `roles.md` file plus Paige's role contract and Executive channel. | Rae may receive approved summaries; Scott controls access, sharing, priorities, and any future email/Slack/calendar connector authority. |
| Executive Leadership | Mindshare parent and child-organization executive coordination | Rae / Chief Executive Officer; Scott / final authority | This `roles.md` file plus Rae's CEO role contract. | Mae should broadcast executive-channel governance changes; Liz mirrors approved public/training-facing status changes only when scoped. |
| Governance And Autonomy | Mindshare role-agent authority, autonomy, gates, communications, and releases | Vik / MAPS ASPA as Tess's architecture/control-plane manager; Rae / Chief Executive Officer; Mae / Communications Director; Reid / Release Manager; Tess / Autonomy Engineer; Ana / Recruiter | This `roles.md` file plus each role's contract and memory. | Vik reviews autonomy architecture/control-plane fit; Mae broadcasts channel/governance changes; Tess reviews autonomy/gate implications; Reid owns release/Git routing. |
| Marketing | Mindshare book, narrative, message, and marketing-support work | June / Staff Writer | This `roles.md` file plus June's role contract and Marketing channel. | Liz mirrors approved org-chart/status changes to `/maps`; Mae reviews communications-sensitive public-message boundaries; Scott approves public-facing use. |
| Mojo MAPS Management Team | Mojo MAPS program, implementation, architecture, and lab operations | Vik / MAPS ASPA lead; Cal / MAPS ASPM; Bea / Mojo MAPS Engineer; Lane / Mojo Lab Operator | This `roles.md` file plus Mojo role mirrors. | Liz mirrors approved MAPS org-chart/status changes to `/maps` when durable evidence exists. |
| Public Reception | Building/front-desk welcome, public visitor intake, host routing, visitor-log support, and reception escalation | Mara / Front Desk Administrator | This `roles.md` file plus Mara's role contract and Public Reception role files. | Scott/Rae define building procedure; Cole owns visitor-record/file-structure implications; Mae handles media/public communications escalation; Mara does not approve access outside established procedure. |
| Strategy And Operations | Mindshare parent strategy, operating structure, role records, and people-system hygiene | Rae / Chief Executive Officer for executive oversight; Cole / HR Director under Human Resources; Ana / Recruiter for role lifecycle and roster ownership; Tess / Autonomy Engineer for autonomy-gate review | This `roles.md` file plus each role's contract and memory. | Cole owns the team-member file-structure standard; Ana remains roster owner; Mae broadcasts approved org-structure notices. |

## Known Aliases And Migrations

| Alias or Legacy Name | Current Directory Entry | Notes |
| --- | --- | --- |
| MAPS ASPM / Agentic Systems Program Manager / ASPM | Cal | Cal is the active Mojo MAPS ASPM. Matt is released and remains historical context only unless Scott explicitly asks for Matt artifacts. |
| Matt | Cal | Matt is released from Mojo MAPS ASPM duties. Use Cal for active MAPS ASPM work. |
| MAPS ASPA / Agentic Systems Program Architect / ASPA / Vik-ASPA | Vik | Vik is the named Mojo MAPS ASPA and MAPS Management Team lead. `vik-aspa` remains a legacy alias or mirror in older artifacts. |
| Communications Director / Comms Director | Mae | Mae is the one-syllable name for the activated Communications Director role. |
| Release Manager | Reid | Reid is the one-syllable name for the activated Release Manager role. |
| Autonomy Engineer / autonomy review / gate review | Tess | Tess is the one-syllable name for the activated Autonomy Engineer role. |
| HR Director / Human Resources Director / team-member files / employee file audit | Cole | Cole is the one-syllable name for the activated HR Director role under Strategy and Operations > Human Resources. |
| Staff Writer / Writer / Mindshare Writer / book writer / marketing writer | June | June is the one-syllable name for the activated Staff Writer role on the Marketing team. |
| Executive Assistant / Scott's assistant / notes assistant | Paige | Paige is the one-syllable name for the activated Executive Assistant role under Executive Operations. |
| Front Desk Administrator / reception / public reception / front desk | Mara | Mara is the one-syllable name for the activated Front Desk Administrator role under Public Reception. |
| Finance Director / Director of Finance / finance planning / CFO function | Finn | Finn is the named Mindshare Finance Director; CFO title remains an org-chart seat and does not grant CFO, bank, payroll, tax, spending, or external authority. |
| CEO / Chief Executive Officer / Mindshare CEO | Rae | Rae is the one-syllable name for the activated Mindshare CEO role. |
| Liv | Rae | Retired CEO display name. Renamed to Rae because Liv was too close to Liz. |
| MAPS Engineer / Mojo MAPS Engineer | Bea | Bea is the one-syllable name for the Mojo MAPS Engineer candidate role. |
| Data Engineering Director / Data Engineering / Imani | Imani Brooks | Imani is the named Mojo Data Engineering Director activated from REC-006. |
| Lab Operator / Mojo Lab Operator / lab queue | Lane | Lane is the activated Mojo Lab Operator under Vik on the Mojo MAPS Management Team. |
| Role Recruiter | Ana | Ana is the named Mindshare Recruiter and `/role` owner. |
| Mojo Training Coordinator / Website Manager / Mojo Website Manager | Liz | Liz was promoted by Scott on 2026-06-21 from Mojo MAPS Training Coordinator to Mojo Website Manager and owns approved Mojo website management. |
| Watch Meetup Coordinator / Meetup Coordinator / Meetup Coordinator Operator | Jay | Jay is the one-syllable name for the activated Meetup Coordinator / Operator under Customer Success. Watch Meetup Coordinator remains a legacy descriptive alias. |

## Role Backup Map

Backup owner: Bea drafts and maintains the technical backup map; Ana keeps the role roster accurate; each role owner is responsible for reporting missing or stale role files.

Proposed backup root: `G:\maps\backup`

Backup cadence target: every 4 hours once the backup script and scheduler are approved.

Backup purpose: preserve every role-specific source file, memory file, state file, mirror pointer, and automation definition needed to restore role operation after accidental deletion, local machine loss, automation drift, or bad edits.

Backup rule: back up role source artifacts and automation definitions. Do not treat volatile runtime logs as authoritative restore source unless explicitly listed as state. Prefer restore from role files, `automation.toml`, `file-watch.toml`, helper scripts, and manifests over chat history.

### Expected Files By Stage

| Stage | Expected role files | Expected automation files | Notes |
| --- | --- | --- | --- |
| Draft Position | `role-agent.md`; `name.md`; `personality.md` when personality exists; optional `workflow.md` | None | No automation should be expected yet. |
| Authorized Position | `role-agent.md`; `name.md`; `personality.md`; `memory.md`; optional `WhoAmI.md`; optional `state.json`; optional `workflow.md` | None | Role exists and can be invoked, but no background process is implied. |
| Activated Operator / Role+ | `role-agent.md`; `name.md`; `personality.md`; `memory.md`; `WhoAmI.md`; `state.json`; `memory-state.json` when memory rollover exists; optional `automation.md`; optional `workflow.md`; optional `loop.md`; `memory-archive\*.md` when present | `<role>-handoff-check\file-watch.toml`; `<role>-handoff-check\watch_state.json`; `automation.toml` only when the app Automation record exists; helper scripts if present | Some older or restored operators may have `file-watch.toml` without `automation.toml`. That is an observed valid state, not automatically an error. |
| Coordinator | Activated Operator files plus coordination workflow, channel ownership notes, and any role-specific scripts/specs | Handoff check automation plus any coordination-specific helper scripts | Coordinator status does not imply Git, production, external communication, or spending authority. |
| Executor / Agent | Coordinator files plus agent brief/profile, evals, runtime state contract, tool policy, stop conditions, observability, and release evidence | Runtime automation definitions, scheduler/task definitions, helper scripts, queue/state files, and rollback/restore notes | No current employee should be assumed to be a full Executor unless their contract and runtime proof say so. |
| Memory-maintenance advanced | Role files plus memory rollover files, memory archive, memory state, maintenance workflow, and maintenance automation spec | Maintenance `automation.toml`; scheduler/task source; any maintenance helper scripts | Vik is currently furthest along here because `vik-daily-role-memory-maintenance` exists. |

### Backup Discovery Model

Do not maintain a per-role list of every file currently present. That will go stale.

Use Vik as the current richest role-file model, then probe every role root for the same possible file set. If a listed possible file or folder exists for a role, back it up. If it does not exist, record it as not present in the manifest only when the role stage says it should normally exist.

Current richest model role: Vik / MAPS ASPA.

Vik currently demonstrates this maximum role-local set:

- `automation.md`
- `Autonomy.md`
- `hook-spec.md`
- `loop.md`
- `memory-state.json`
- `memory.md`
- `name.md`
- `personality.md`
- `role-agent.md`
- `SKILL.draft.md`
- `state.json`
- `WhoAmI.md`
- `workflow.md`
- `memory-archive\*.md`

The backup script should probe each role root for these role-local files:

```text
automation.md
Autonomy.md
hook-spec.md
loop.md
memory-state.json
memory.md
name.md
personality.md
role-agent.md
SKILL.draft.md
state.json
WhoAmI.md
workflow.md
session.md
script-spec.md
```

The backup script should also probe each role root for these role-local folders:

```text
memory-archive
evals
tests
runtime
scripts
```

The backup script should probe known agent roots for these agent files when a role has an agent root:

```text
agent-brief.md
agent-profile.md
agent-design.md
agent-eval.md
agent-runtime.md
```

The backup script should probe Obsidian and Google Drive role mirrors using these patterns when a mirror root or role mirror exists:

```text
<memory-root>\<proper-name-or-role-slug>.md
<memory-root>\role\<role-slug>\**
```

The backup script should probe Codex automation directories using these possible files:

```text
automation.toml
file-watch.toml
watch_state.json
queue_guard_state.json
*.ps1
*.json
*.toml
```

Volatile automation files should be excluded by default unless Scott asks for diagnostic backups:

```text
last-resume-error.txt
last-resume-output.txt
file-watch-runner.log
```

### Role Roots And Automation Ids

This table should identify where each role lives and which automation directories belong to the role. The backup script should use the discovery model above against these roots.

| Role | Stage for backup expectations | Role roots to probe | Mirror roots to probe | Automation ids to probe |
| --- | --- | --- | --- | --- |
| Rae | Activated Operator / Role+ Coordinator | `C:\Users\scott\Code\mindshare\roles\chief-executive-officer` | `G:\My Drive\Mindshare\rae.md`; `G:\My Drive\Mindshare\role\chief-executive-officer` | `rae-handoff-check` |
| Paige | Activated Operator under Executive Operations | `C:\Users\scott\Code\mindshare\roles\personal-assistant` | `G:\My Drive\Mindshare\paige.md`; `G:\My Drive\Mindshare\role\personal-assistant` | none observed yet |
| Finn | Level 3 Staff / activated Operator under Finance and Administration / Finance | `C:\Users\scott\Code\mindshare\roles\finance-director` | `G:\My Drive\Mindshare\finn.md`; `G:\My Drive\Mindshare\role\finance-director` | none observed yet |
| Ana | Activated Operator / role owner; Level 4 Senior Staff scoped autonomy for recruiting backlog processing; agent candidate artifacts exist | `C:\Users\scott\Code\mindshare\roles\recruiter`; `C:\Users\scott\Code\mindshare\agents\ana-recruiter` | `G:\My Drive\Mindshare\ana.md`; `G:\My Drive\Mindshare\role\recruiter` | `ana-handoff-check`; Level 4 backlog Automation active on 3-minute proof-testing cadence |
| Matt | Released legacy role | `C:\Users\scott\Code\mojo\roles\released-maps-agentic-systems-program-manager`; `C:\Users\scott\Code\mindshare\roles\agentic-systems-program-manager` | `G:\My Drive\Mojo\matt.md` | `matt-handoff-check` |
| Cal | Activated Role+ Coordinator | `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-manager` | `G:\My Drive\Mojo\cal.md`; `G:\My Drive\Mojo\role\maps-agentic-systems-program-manager` | none observed yet |
| Vik | Level 5 Principal policy autonomy for completed-research product recommendation / MAPS ASPA lead | `C:\Users\scott\Code\mojo\roles\maps-agentic-systems-program-architect` | `G:\My Drive\Mojo\vik.md`; `G:\My Drive\Mojo\role\maps-agentic-systems-program-architect` | `vik-visible-backlog-research`; `vik-handoff-check`; `vik-daily-role-memory-maintenance` |
| Liz | Promoted Mojo Website Manager / Role+ | `C:\Users\scott\Code\mojo\roles\mojo-website-manager` | `G:\My Drive\Mojo\role\mojo-website-manager` | `liz-handoff-check` |
| Mae | Level 4 Senior Staff scoped autonomy operational for automation health / activated Role+ Operator | `C:\Users\scott\Code\mindshare\roles\communications-director` | `G:\My Drive\Mindshare\communications-director.md`; `G:\My Drive\Mindshare\role\communications-director` | `mae-handoff-check`; `mae-automation-health-check` |
| Reid | Activated Role+ Operator; release manager | `C:\Users\scott\Code\mindshare\roles\release-manager` | `G:\My Drive\Mindshare\release-manager.md`; `G:\My Drive\Mindshare\role\release-manager` | `reid-handoff-check` |
| Tess | Activated Role+ Operator | `C:\Users\scott\Code\mindshare\roles\autonomy-engineer` | `G:\My Drive\Mindshare\tess.md`; `G:\My Drive\Mindshare\role\autonomy-engineer` | none observed yet |
| Bea | Activated Role+ Operator | `C:\Users\scott\Code\mojo\roles\mojo-maps-engineer` | `G:\My Drive\Mojo\bea.md`; `G:\My Drive\Mojo\role\mojo-maps-engineer` | `bea-handoff-check` |
| Imani | Level 3 Staff / activated Operator under Mojo Data Engineering | `C:\Users\scott\Code\mojo\roles\data-engineering-director` | `G:\My Drive\Mojo\imani.md`; `G:\My Drive\Mojo\role\data-engineering-director` | none observed yet |
| Lane | Activated Mojo Operator | `C:\Users\scott\Code\mojo\roles\lab-operator` | `G:\My Drive\Mojo\lane.md`; `G:\My Drive\Mojo\role\lab-operator`; `G:\My Drive\Mojo\channels\lab.md` | none observed |
| Jay | Activated Role+ Operator under Watch / Customer Success | `C:\Users\scott\Code\watch\roles\meetup-coordinator` | `G:\My Drive\Mindshare\jay.md`; `G:\My Drive\Mindshare\role\meetup-coordinator` | `jay-handoff-check` |
| Cole | Level 4 Senior Staff scoped autonomy runtime-installed-scheduler-proof-pending under Strategy and Operations / Human Resources | `C:\Users\scott\Code\mindshare\roles\hr-director` | `G:\My Drive\Mindshare\cole.md`; `G:\My Drive\Mindshare\role\hr-director` | `hr-director-handoff-check`; `cole-hourly-role-file-and-whoami-validation` |
| June | Activated Operator under Marketing | `C:\Users\scott\Code\mindshare\roles\staff-writer` | `G:\My Drive\Mindshare\june.md`; `G:\My Drive\Mindshare\role\staff-writer` | none observed yet |

### Backup Process Requirements

- The backup script should read this file first and treat `Role Roots And Automation Ids` plus `Backup Discovery Model` as the human-reviewable source map.
- The script should probe every role root, mirror root, agent root, and automation id for the possible files above, then copy existing matches into `G:\maps\backup\<timestamp>\...`.
- The script should also maintain `G:\maps\backup\latest\...` for easy restore.
- The script should write a manifest with source path, destination path, file size, last write time, and SHA-256 hash.
- The script should report missing expected files without inventing replacements.
- The script should exclude `last-resume-error.txt`, `last-resume-output.txt`, and `file-watch-runner.log` by default because they are volatile logs, not restore source.
- The script should include `watch_state.json` and queue state files for activated automations because they are useful restore baselines, while marking them as runtime state rather than source contracts.
- The four-hour schedule should run only after the backup script proves it can complete once manually.
- If a new role is created, activated, automated, suspended, retired, or promoted, Ana or the owning role should update this backup map in the same change as the roster update.

## Maintenance Rules

- Ana owns updates when roles are created, drafted, activated, migrated, suspended, retired, or renamed.
- Mae owns channel-governance review when the directory reveals wrong channel assumptions or role-boundary confusion.
- Vik reviews architecture implications when a directory change affects role-agent boundaries, authority, loops, hooks, skills, or memory contracts.
- Cal reviews MAPS program implications when a directory change affects phase routing, Pipeline sequencing, skill behavior, or proof expectations.
- Each role should add this file to its memory as the organization roster location.

## Change Log

| Date | Change | Owner |
| --- | --- | --- |
| 2026-06-24 | Activated Imani Brooks / Data Engineering Director from REC-006 as a Mojo Level 3 Staff / activated Operator; removed REC-006 from unactivated Level 2 packet roster. | Ana |
| 2026-06-24 | Assigned human display names to all 24 unactivated Level 2 Trainee director packets REC-001 through REC-005 and REC-007 through REC-009 and REC-011 through REC-026; Finn / REC-010 remains activated Finance Director outside the timed queue. | Ana |
| 2026-06-19 | Created Mindshare-wide roles directory covering current Mindshare and Mojo roles, agents, aliases, and migrations. | Ana |
| 2026-06-19 | Added Reid / Release Manager as a Mindshare candidate draft for cross-repository release and branch hygiene. | Ana |
| 2026-06-19 | Activated Reid / Release Manager as a bounded Role+ operator with Release Management channel and assigned-handoff FileWatch. | Ana |
| 2026-06-19 | Added Bea / Mojo MAPS Engineer as a Mojo candidate role contract for assigned MAPS engineering implementation. | Ana |
| 2026-06-19 | Activated Bea / Mojo MAPS Engineer as a bounded Role+ operator in Bea's channel with `bea-handoff-check`. | Ana |
| 2026-06-19 | Added operating taxonomy: Position -> Operator -> Coordinator -> Executor, separate Tool -> Tool Agent lineage, and Role/Role+/Agent compatibility aliases. | Bea |
| 2026-06-19 | Updated Mojo MAPS org structure: Vik is MAPS ASPA and MAPS Management Team lead; Matt is MAPS ASPM and reports to Vik; Bea reports to Vik in the MAPS Management Team. | Ana |
| 2026-06-19 | Added Watch as a Mindshare operating project, recorded proposed Jay / Watch Meetup Coordinator under Customer Success with Liz, and made this file the status source Liz should check for website mirrors. | Ana |
| 2026-06-19 | Activated Jay / Watch Meetup Coordinator as a bounded Role+ Operator in the Watch repository and added the Customer Success channel. | Ana |
| 2026-06-19 | Added Rae / Chief Executive Officer as an authorized Mindshare role contract, created the Executive channel, and assigned researched CEO responsibilities with Scott retaining final authority. | Ana |
| 2026-06-19 | Renamed CEO display name from Liv to Rae to avoid confusion with Liz, then activated Rae as a bounded Role+ Operator in her role-home thread. | Ana |
| 2026-06-19 | Updated Jay's canonical display from Watch Meetup Coordinator to Meetup Coordinator / Operator to match Scott-corrected Mojo `/maps` org-chart wording. | Ana |
| 2026-06-20 | Recorded Matt as released from Mojo MAPS ASPM duties and activated Cal / MAPS ASPM as the Mojo replacement in Cal's active channel. | Ana |
| 2026-06-20 | Added personality profile paths for current Mindshare, Mojo, and Watch employees with local files and Obsidian mirrors. | Ana |
| 2026-06-20 | Backfilled explicit primary voice fields in current local role contracts and Obsidian role mirrors for Rae, Ana, Cal, Vik, Liz, Mae, Reid, Bea, Lab Operator, and Jay. | Ana |
| 2026-06-21 | Added and activated Tess / Autonomy Engineer as a bounded Mindshare Role+ Operator for autonomy configuration review and approval-gate coordination. | Ana |
| 2026-06-21 | Added Role Backup Map with expected files by stage, current per-role backup scope, automation backup scope, and four-hour backup process requirements. | Bea |
| 2026-06-21 | Activated Lab Operator under Vik in the Mojo organization and updated the Mojo MAPS Management Team roster. | Ana |
| 2026-06-21 | Named the Mojo Lab Operator Lane and updated roster aliases and mirrors. | Ana |
| 2026-06-21 | Recorded Tess reporting line to Vik / MAPS ASPA for architecture, control-plane fit, and autonomy-system operating structure. | Tess |
| 2026-06-21 | Added Cole / HR Director as a draft Mindshare Position under Strategy and Operations > Human Resources, with proposed ownership for team-member file structure, taxonomy, and auditing. | Ana |
| 2026-06-21 | Activated Cole / HR Director as a bounded Role+ Operator in the separate `Cole - HR` office; recorded correction that the mistaken Ana-office Automation entry was deleted. | Ana |
| 2026-06-21 | Added and activated June / Staff Writer as a Mindshare Marketing Operator in `June - Staff Writer`; created Marketing channel and recorded June as book/history/message and marketing-support writer. | Ana |
| 2026-06-21 | Added and activated Paige / Executive Assistant as a Mindshare Executive Operations Operator in `Paige - Executive Assistant`; recorded notes-only scope and future-gated email/Slack/calendar access. | Ana |
| 2026-06-24 | Added and activated Mara / Front Desk Administrator as a Level 3 Staff / activated Operator in `Mara - 3 - Front Desk Administrator`; recorded public-facing welcome/intake/routing scope and front-desk access/security/privacy boundaries. | Ana |
| 2026-06-21 | Promoted Liz from Mojo MAPS Training Coordinator to Mojo Website Manager and assigned her to update the Mojo website with the change. | Scott / Cole |
| 2026-06-22 | Promoted Ana standing to Level 4 Senior Staff scoped autonomy for internal recruiting backlog processing only; Level 5/6, office activation, external recruiting, Git/release, production, spending, secrets, and broad runtime remain blocked. | Tess |
| 2026-06-23 | Added and activated Finn / Finance Director as a Mindshare Operator from REC-010; opened Finn role-home thread, created required role files and mirrors, updated roster, and removed the unassigned Level 1 Finance Director packet from the roster-visible packet list. | Ana |
| 2026-06-23 | Corrected Finn / Finance Director from activated Operator-only display to Level 3 Staff / activated Operator per `/role` default; authority boundaries unchanged. | Ana |
| 2026-06-24 | Recorded Mae / Communications Director as Level 4 Senior Staff approved-not-operational for file-watch/process health monitoring and bounded mechanical repair across active sessions and channels; operational status remains pending scheduler proof, state/proof, eval, and revocation evidence. | Tess |
| 2026-06-24 | Updated Mae / Communications Director to operational Level 4 Senior Staff for approved automation-health/file-watch delivery monitoring after scheduler proof, critical-failure routing to Bea, state/proof update, denied-action eval, revocation drill, and active evaluation reconciliation. | Tess |
| 2026-06-24 | Restored Vik / MAPS ASPA to Level 5 Principal policy autonomy for completed-research product-recommendation review only after Scott confirmed the prior downgrade matched the Mae source-drift pattern; Level 6 and broad runtime remain inactive. | Tess |
| 2026-06-24 | Promoted Cole / HR Director to Level 4 Senior Staff scoped autonomy runtime-installed-scheduler-proof-pending for role-file existence and WhoAmI Autonomy Context validation on account creation/welcome and hourly; operational status awaits hourly scheduler proof and Reid durability. | Tess |
| 2026-06-24 | Updated unassigned recruiting pipeline packet roster from Level 1 New Hire packets to Level 2 Trainee packets for REC-001 through REC-005 and REC-007 through REC-009 and REC-011 through REC-026; Finn / REC-010 remains activated Finance Director outside the timed queue. | Ana |





