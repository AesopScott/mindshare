# Equip

## Purpose

Give the agent the capabilities it needs: tools, data, retrieval, memory, permissions, and integration contracts.

## Inputs

- Working agent
- Workflow design
- Required external systems
- Security and compliance constraints

## Activities

- Map tools to tasks and permissions.
- Define context sources and retrieval behavior.
- Decide what memory is allowed and where it lives.
- Add tool schemas, error behavior, and audit expectations.

## Outputs

- Capability map
- Tool and permission inventory
- Context and memory plan
- Integration risk list

## Done Criteria

- Every tool has a reason to exist.
- Permissions are least-privilege by default.
- Tool failures and unsafe outputs have handling paths.
- Context sources are traceable.

## Teaching Exercise

Create a tool map for the agent using `templates/tool-map.md`.

