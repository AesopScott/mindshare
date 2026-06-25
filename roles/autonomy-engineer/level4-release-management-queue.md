# Tess Level 4 Release Management Queue

This file is the app-bundled release routing queue for Tess Level 4 autonomy work when MindShare runs as a local Electron application.

## Automation Reid-Durability Routing

Next owner: Reid

Purpose: preserve a durable local route for Tess automation changes that affect runtime-read source files, role Autonomy.md files, automation prompts/config, state/proof files, evaluation snapshots, website source mirrors, or other release-relevant autonomy artifacts.

Rule: Tess may write deterministic state/proof and local review requests inside the app bundle, but commit, push, release, deploy, and promotion remain outside Tess authority unless explicitly approved through the release path.
