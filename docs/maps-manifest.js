window.MAPS_MANIFEST = {
  pages: [
    {
      file: "phase0.html",
      label: "Phase 0",
      title: "Phase Alignment"
    },
    {
      file: "phase1.html",
      label: "Phase 1",
      title: "Define"
    }
  ],
  phases: [
    "00-phase-alignment.md",
    "01-define.md",
    "02-design.md",
    "03-build.md",
    "04-equip.md",
    "05-evaluate.md",
    "06-deploy.md",
    "07-observe.md",
    "08-improve.md"
  ],
  skills: [
    {
      name: "scaffold",
      files: ["SKILL.md", "scripts/create_maps_scaffold.py"]
    },
    {
      name: "phase-alignment",
      files: ["SKILL.md"]
    },
    {
      name: "define-agent",
      displayName: "/define-agent",
      files: ["SKILL.md"]
    },
    {
      name: "design-agent",
      files: ["SKILL.md"]
    },
    {
      name: "build-agent",
      files: ["SKILL.md"]
    },
    {
      name: "equip-agent",
      files: ["SKILL.md"]
    },
    {
      name: "evaluate-agent",
      files: ["SKILL.md"]
    },
    {
      name: "deploy-agent",
      files: ["SKILL.md"]
    },
    {
      name: "observe-agent",
      files: ["SKILL.md"]
    },
    {
      name: "improve-agent",
      files: ["SKILL.md"]
    }
  ],
  templates: [
    "phase-alignment-brief.md",
    "agent-definition-template.md",
    "workflow-spec.md",
    "tool-map.md",
    "eval-scorecard.md",
    "deployment-plan.md",
    "observation-report.md",
    "improvement-backlog.md"
  ],
  catalogs: [
    "repos.md",
    "skills.md",
    "tools.md"
  ],
  repos: [
    {
      label: "AesopScott/maps",
      url: "https://github.com/AesopScott/maps"
    },
    {
      label: "VoltAgent/awesome-agent-skills",
      url: "https://github.com/VoltAgent/awesome-agent-skills"
    },
    {
      label: "hqhq1025/skill-optimizer",
      url: "https://github.com/hqhq1025/skill-optimizer"
    }
  ],
  tools: [
    "Python",
    "GitHub CLI",
    "Git"
  ],
  phaseResources: {
    "0": {
      skills: ["scaffold", "phase-alignment"],
      repos: ["AesopScott/maps", "VoltAgent/awesome-agent-skills", "hqhq1025/skill-optimizer"],
      tools: ["Python", "GitHub CLI", "Git"],
      templates: ["phase-alignment-brief.md"],
      catalogs: ["skills.md", "repos.md", "tools.md"]
    },
    "1": {
      skills: ["define-agent"],
      repos: ["AesopScott/maps"],
      tools: ["Git", "Agent Skills"],
      templates: ["agent-definition-template.md"],
      catalogs: ["skills.md", "repos.md", "tools.md"]
    }
  }
};
