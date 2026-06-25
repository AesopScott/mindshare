# MAPS Scaffold Template

This template defines the repeatable repository structure created by `/scaffold`.

## Purpose

Create a MAPS-ready repository with phase docs, phase skills, reusable templates, catalogs, and lightweight docs pages.

## Repository Structure

```text
maps/
  README.md
  LICENSE
  .gitignore
  docs/
    phase0.html
    phase1.html
    styles.css
    maps-manifest.js
    maps-render.js
    contributing.md
  phases/
    00-phase-alignment.md
    01-define.md
    02-design.md
    03-build.md
    04-equip.md
    05-evaluate.md
    06-deploy.md
    07-observe.md
    08-improve.md
  skills/
    phase-alignment/
      SKILL.md
      agents/openai.yaml
    define-agent/
      SKILL.md
      agents/openai.yaml
    design-agent/
      SKILL.md
      agents/openai.yaml
    build-agent/
      SKILL.md
      agents/openai.yaml
    equip-agent/
      SKILL.md
      agents/openai.yaml
    evaluate-agent/
      SKILL.md
      agents/openai.yaml
    deploy-agent/
      SKILL.md
      agents/openai.yaml
    observe-agent/
      SKILL.md
      agents/openai.yaml
    improve-agent/
      SKILL.md
      agents/openai.yaml
  templates/
    maps-scaffold-template.md
    phase-alignment-brief.md
    agent-definition-template.md
    workflow-spec.md
    tool-map.md
    eval-scorecard.md
    deployment-plan.md
    observation-report.md
    improvement-backlog.md
  catalogs/
    repos.md
    skills.md
    tools.md
```

## Required Guarantees

- Every APS phase has a phase doc.
- Every APS phase has a `SKILL.md`.
- Every generated skill has valid frontmatter.
- Templates are reusable input shells, not completed outputs.
- Catalogs are present before resources are curated.
- Docs pages expose the scaffold and current phase resources.

## Instantiation

Use `/scaffold` to instantiate this template into a target directory.
