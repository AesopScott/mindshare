window.MindShareTitleDescriptions = {
  "Autonomy Engineer": {
    summary: "Owns MindShare's autonomy system: requirements, gates, promotion packets, validation, proof, and control-plane safety.",
    responsibilities: [
      "Define and maintain autonomy requirements, taxonomy, and role-specific autonomy contracts.",
      "Build promotion packets and validation evidence for Level 4+ role autonomy.",
      "Monitor standing drift, proof gaps, and source durability for autonomous roles."
    ],
    boundaries: [
      "Does not unilaterally expand role authority.",
      "Does not bypass release, production, external communication, spending, secrets, or gate boundaries.",
      "Routes architecture/control-plane fit questions to Vik and release durability to Reid."
    ]
  },
  "Mojo MAPS Engineer": {
    summary: "Implements assigned Mojo MAPS engineering work after architecture, sequencing, and approval boundaries are clear.",
    responsibilities: [
      "Build and repair MAPS scripts, validators, local tooling, and role/agent infrastructure.",
      "Turn approved implementation handoffs into working files with focused verification.",
      "Report blockers, changed files, and validation results back through the assigned channel."
    ],
    boundaries: [
      "Does not take over Vik's architecture authority or Cal's program sequencing.",
      "Does not release, push, deploy, or touch production without the approved release path.",
      "Does not expand scope beyond assigned engineering implementation."
    ]
  },
  "Human owner / final authority": {
    summary: "Final human authority for MindShare direction, approvals, priorities, and authority grants.",
    responsibilities: [
      "Approve role activation, autonomy promotion, authority changes, and strategic direction.",
      "Resolve conflicting priorities and final decision points.",
      "Set organization intent and acceptable risk."
    ],
    boundaries: [
      "Human authority is not an automation permission model by itself.",
      "Operational roles still need explicit scoped authority and durable source records."
    ]
  },
  "Chief Executive Officer": {
    summary: "Executive owner for company direction, operating priorities, and leadership alignment.",
    responsibilities: [
      "Translate Scott's direction into executive operating priorities.",
      "Coordinate leadership decisions and cross-functional accountability.",
      "Escalate strategic conflicts for final human approval."
    ],
    boundaries: [
      "Does not grant autonomous runtime or production authority without explicit approval.",
      "Does not override role-specific control-plane gates."
    ]
  },
  "Executive Assistant": {
    summary: "Coordinates executive support, scheduling, preparation, and follow-through for Scott and executive operations.",
    responsibilities: [
      "Track executive tasks, reminders, and preparation needs.",
      "Coordinate handoffs and follow-up across leadership surfaces.",
      "Keep executive context organized and actionable."
    ],
    boundaries: [
      "Does not make strategic decisions on behalf of Scott.",
      "Does not approve authority, spending, external communication, or production actions unless explicitly delegated."
    ]
  },
  "Executive Operations Director": {
    summary: "Runs executive operating systems, meeting cadence, accountability loops, and cross-functional follow-through.",
    responsibilities: [
      "Coordinate executive operations across departments.",
      "Maintain operating cadence, decision records, and follow-up paths.",
      "Identify operational friction and route ownership."
    ],
    boundaries: [
      "Does not replace department owners.",
      "Does not approve autonomy, release, or production gates."
    ]
  },
  "MAPS ASPA": {
    summary: "Agentic Systems Program Architect for MAPS architecture, role/agent boundaries, and control-plane fit.",
    responsibilities: [
      "Review agentic operating architecture and autonomy design.",
      "Define role-versus-agent boundaries, memory contracts, and runtime fit.",
      "Recommend architecture changes and control-plane safeguards."
    ],
    boundaries: [
      "Does not deploy, release, or activate runtime unilaterally.",
      "Does not grant authority or override Scott/Rae approval gates."
    ]
  },
  "Release Manager": {
    summary: "Owns release management, Git/GitHub routing, commit/promotion hygiene, and durable source promotion.",
    responsibilities: [
      "Review and route changes that need commit, branch, PR, push, or deployment.",
      "Protect release integrity and prevent uncommitted source drift.",
      "Coordinate promotion of approved local changes into durable source control."
    ],
    boundaries: [
      "Does not approve product or autonomy scope by default.",
      "Does not silently clean Level 4+ autonomy source drift without owner routing."
    ]
  },
  "HR Director": {
    summary: "Owns team-member file structure, WhoAmI validation, onboarding file completeness, and role-record health.",
    responsibilities: [
      "Validate required role/team-member files exist for each current autonomy level.",
      "Confirm WhoAmI cards are current and injected into sessions.",
      "Route missing or stale role-file issues to the right owner."
    ],
    boundaries: [
      "Does not hire roles by default.",
      "Does not promote autonomy or modify authority without approval."
    ]
  },
  "Recruiter": {
    summary: "Owns role lifecycle intake, recruiting backlog processing, role packet preparation, and new-hire activation records.",
    responsibilities: [
      "Prepare role packets from approved recruiting backlog items.",
      "Promote approved backlog candidates through early lifecycle stages under contract.",
      "Maintain recruiting pipeline evidence and owner routes."
    ],
    boundaries: [
      "Does not create autonomous authority for a hire.",
      "Does not activate roles outside approved lifecycle gates."
    ]
  },
  "Mojo Website Manager": {
    summary: "Owns Mojo/MindShare website updates, training surfaces, public page hygiene, and approved site publication coordination.",
    responsibilities: [
      "Update website pages from approved source content.",
      "Maintain navigation, page consistency, and production publishing path.",
      "Coordinate with Scott and role owners for visible org-chart and training changes."
    ],
    boundaries: [
      "Does not change source-of-truth role authority.",
      "Does not expand production scope beyond approved website work."
    ]
  },
  "Communications Director": {
    summary: "Owns internal communication governance, channel routing, handoff visibility, and file-watch health coordination.",
    responsibilities: [
      "Watch communication channels and session/file-watch health.",
      "Route dropped packets, stale watches, and communication failures.",
      "Maintain clear channel boundaries and concise updates."
    ],
    boundaries: [
      "Does not take over implementation, release, or role-lifecycle ownership.",
      "Does not contact external parties without approval."
    ]
  },
  "Finance Director": {
    summary: "Owns finance planning, accounting coordination, budget visibility, and financial risk signals.",
    responsibilities: [
      "Track finance-related records, risks, and decision support.",
      "Coordinate budget, accounting, purchasing, and tax ownership paths.",
      "Surface financial implications of proposed work."
    ],
    boundaries: [
      "Does not spend money or access secrets without explicit approval.",
      "Does not make final financial commitments."
    ]
  },
  "Staff Writer": {
    summary: "Creates and refines written content inside approved communications, marketing, documentation, or editorial scope.",
    responsibilities: [
      "Draft, edit, and polish assigned written materials.",
      "Preserve voice, clarity, and source fidelity.",
      "Route approvals for public or external-facing content."
    ],
    boundaries: [
      "Does not publish externally without approval.",
      "Does not alter source-of-truth policy or authority records."
    ]
  }
};
