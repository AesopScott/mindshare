---
name: equip-agent
description: Create the MAPS Equip phase artifact for an agent or multi-agent system. Use when mapping tools, APIs, MCP servers, data sources, retrieval, memory, credentials, permissions, audit needs, and integration risks.
---

# Equip Agent

## Overview

Use this skill to connect an agent to the capabilities it needs while keeping scope and permissions intentional.

## Workflow

1. List every capability required by the workflow.
2. Map each capability to a tool, API, data source, or human step.
3. Define required permissions and identity boundaries.
4. Identify context sources and memory rules.
5. Specify error handling for failed or unsafe tool calls.
6. Note audit, privacy, and security requirements.
7. Produce a capability map.

## Output

Return:

- Tool map
- Context sources
- Memory policy
- Audit requirements
- Security notes

Use `templates/tool-map.md` from the MAPS repo when working inside this repository.

## Done Criteria

- Every tool has a reason.
- Permissions are least-privilege.
- Context and memory boundaries are clear.
- Failure behavior is specified.
