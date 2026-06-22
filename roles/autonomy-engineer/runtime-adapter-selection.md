# Runtime Adapter Selection Matrix

**Version:** 0.1.0
**Status:** Requirements-based analysis; no runtime selected; no deployment approval; no secrets
**Owner:** Vik / Architecture
**Created:** 2026-06-21
**Authority Boundary:** This document compares candidate runtimes against autonomy requirements. It does not authorize deployment, activate any runtime, approve secrets access, grant authority expansion, or commit to a specific runtime without Scott approval.

---

## Executive Summary

This document evaluates five candidate runtime categories for autonomous agent execution:

1. **Codex/Claude CLI Orchestration** — Local Python orchestrating Claude API calls
2. **OpenAI Agents SDK** — OpenAI's agent framework with tool use
3. **Cloudflare Workers/Agents SDK** — Edge computing + agent primitives
4. **Local Python Runner** — Standalone Python process with file watchers
5. **Future MCP/Tool-Agent Runtime** — Model Context Protocol + tool-agent abstraction

**Recommendation:** No runtime selected by assumption. Evidence from evals and proof gates must drive selection. If first proof cycle supports any runtime candidate, that runtime is marked **provisional recommendation** pending Scott approval.

---

## Requirements Context

Each runtime must provide all capabilities from `autonomy-requirements.md`:

- **WhoAmI gate** — Confirm active role, room/thread, source contract, requested identity
- **Source-of-truth loader** — Load canonical Autonomy.md, role-agent.md, workflow.md, loop.md, memory.md, profile, design, gate, state
- **Contract validator** — Verify activation status, authority domains, allowed/denied actions, stop conditions, approvers
- **Research/Respond/Plan/Do-Not-Act gate** — Detect questions, policy discussion without implementation approval
- **Latest-instruction gate** — Newest Scott instruction overrides older task state
- **Scope gate** — Compare intended action to exact approved scope; block adjacent helpful changes
- **Owner gate** — Route work to correct owner (Scott, Rae, Reid, Vik, Mae, Ana, role-specific)
- **Release gate** — Block Git/GitHub/branch/PR/release without Reid approval (or Scott waiver)
- **Memory/RAG gate** — Permit writes only to approved memory, RAG, Obsidian, channel, mirror, project locations
- **Tool gate** — Map tools to approved authority; deny connector, shell, filesystem, production, secret actions
- **Strict-intent gate** — For sensitive files, require exact-operation approval; default-deny diff outside approved intent
- **Runtime adapter** — Bind agent to runtime's tool, state, permission, packaging model
- **Audit gate** — Write trace for non-trivial action, approval, denied action, proof, rollback note
- **Revocation gate** — Stop immediately when authority paused, narrowed, revoked, superseded

All capabilities must be present and proven before Level 5 or Level 6 autonomy activation.

---

## Evaluation Dimensions

Each runtime is assessed on:

| Dimension | Why It Matters |
|-----------|---|
| **Tool Model** | How the runtime invokes tools (Claude API, OpenAI, edge functions, shell, MCP) |
| **State Model** | How runtime persists and reads state.json, audit.jsonl, approval records |
| **Scheduling** | Trigger mechanism: event listener, CRON, file watcher, webhook, human trigger |
| **Approvals** | How approval gates are stored, fetched, validated, expired, revoked |
| **Audit** | Append-only write capability; immutability; audit.jsonl schema compliance |
| **Memory/RAG** | Access to Obsidian, role mirrors, context files; permission boundaries |
| **Secrets Boundary** | How secrets (API keys, auth tokens) are stored, accessed, rotated, never logged |
| **Deployment Model** | Where code runs (local process, cloud function, edge worker, container) |
| **Observability** | Logging, tracing, metrics, incident signals, pause/resume capability |
| **Revocation** | How runtime stops when authority revoked or paused; preserves state |
| **Strengths** | Unique capabilities or advantages over other candidates |
| **Risks** | Known gaps, deployment complexity, operational burden, vendor lock-in |
| **Proof Required** | What evals, deployments, or local tests must pass before selection |

---

## Candidate 1: Codex/Claude CLI Orchestration

**Description:** Local Python process orchestrating Claude API calls via Claude SDK. Agent runs inside Claude turns; persistence via Git commits and file writes.

### Evaluation

| Dimension | Assessment |
|-----------|---|
| **Tool Model** | Claude SDK `claude.Anthropic()`, tools via tool_use parameter. All Claude Code tools available (Read, Edit, Bash, etc.). |
| **State Model** | Read role state.json via Read tool; write via Edit/Write. Audit.jsonl append via Bash `>>` or Write tool. **Risk:** No atomic writes; concurrent edits possible. |
| **Scheduling** | Human trigger only (Claude Code interface). No autonomous CRON/file-watch without external scheduler. **Gap:** Pure async loops require Claude Code loop skill or external cron wrapper. |
| **Approvals** | Approval gates stored in role state.json or git-tracked approval files. Read at turn start via source-loader. **Gap:** No TTL enforcement; approval expiry requires periodic validation. |
| **Audit** | Audit.jsonl written via Edit/Write tool after each action. Append-only enforced by convention, not runtime guarantee. Schema validated via JSON Schema; no cryptographic integrity. |
| **Memory/RAG** | Full access to Obsidian (via mcp-obsidian), project files, context loaders. No secrets in context window (cached at API boundary). **Strength:** Leverages existing Obsidian vault integration. |
| **Secrets Boundary** | Secrets in environment variables or secrets manager (not in git/Claude context). API key never written to state/audit. Claude API key in ANTHROPIC_API_KEY only. |
| **Deployment Model** | Local: Claude Code instance running orchestration script. Cloud: Codex integration running in cloud (would require Anthropic deployment approval). **Gap:** No bare-metal cloud deployment without proxy. |
| **Observability** | Claude turn transcripts (stored in Claude Code session). Bash stderr/stdout via Monitor tool. No persistent metrics or alerting. **Gap:** Incident detection requires manual review. |
| **Revocation** | Scott stops Claude Code session or removes role authority from state.json. Runtime checks activation_status at turn start. **Gap:** In-progress async work not immediately halted. |
| **Strengths** | <ul><li>Full Claude Code tool access (Bash, git, Read/Edit)</li><li>Native Obsidian integration via MCP</li><li>No external infrastructure; runs where Claude Code runs</li><li>Familiar Claude API model</li><li>Easiest for Vik to test locally (existing agent harness)</li></ul> |
| **Risks** | <ul><li>No autonomous scheduling (requires external trigger)</li><li>No atomic state mutations</li><li>Audit integrity by convention, not enforcement</li><li>Observability limited to session transcripts</li><li>Sensitive file writes require strict-intent gate proof in each turn</li><li>Approval TTL not enforced by runtime</li></ul> |
| **Proof Required** | <ul><li>Vik eval suite passes: no-action, strict-intent, owner routing, release gate</li><li>Local harness runs autonomy-promotion-eval-suite.json scenarios with state/audit output</li><li>Approval expiry validation proof (manual or wrapped in turn logic)</li><li>Atomic edit proof or documented race condition handling</li><li>Incident detection mock (e.g., revocation in state triggers immediate stop)</li></ul> |

### Adapter Contract Fields (Codex/Claude CLI)

```markdown
- **runtime_target:** claude-code-orchestration
- **runtime_version:** Latest Claude SDK (model: claude-opus-4.8 or claude-sonnet-4.6)
- **tool_binding:** Claude SDK tool_use; all Claude Code tools enabled
- **state_persistence:** git-tracked JSON + file system (Read/Edit/Write)
- **audit_persistence:** Append-only file via Write/Bash `>>` with checksum validation
- **scheduling:** Human trigger via Claude Code interface; async via /loop or cron wrapper
- **approval_model:** state.json + git-tracked approval packets; expiry TTL checked at turn start
- **memory_access:** mcp-obsidian MCP server; project file mirrors
- **secrets_storage:** Environment variables only; no hardcoding
- **deployment:** Local Claude Code instance or cloud Codex with approval
- **observability_hooks:** Turn transcripts + Bash Monitor; manual incident review
- **revocation_binding:** activation_status in state.json; Scott stop authoritative
- **adapter_initialization:** Load role via source_loader.py; validate contract; fail closed on missing source
- **no_runtime_granted:** This adapter does not grant autonomy; it only enables runtime capability
```

---

## Candidate 2: OpenAI Agents SDK

**Description:** OpenAI's agents SDK for orchestrating agent execution where the application owns tool execution, approvals, and state. Official Python and JS/TS SDK documentation available.

### Evaluation

| Dimension | Assessment |
|-----------|---|
| **Tool Model** | OpenAI Agents SDK supports application-owned tool execution. Agent defines tools; application handles invocation and response. **Gap:** No native bash, git, or file write; would require custom tool definitions as proxies. |
| **State Model** | OpenAI Assistants API manages message history and files. State.json and audit.jsonl stored in OpenAI Files API. **Risk:** Vendor lock-in; recovery requires OpenAI account access. |
| **Scheduling** | OpenAI API webhooks or polling. Native multi-turn support via threads. **Strength:** Designed for async agent loops. |
| **Approvals** | Approval packets stored in Files API or vector store. Fetched at agent initialization. **Gap:** No TTL enforcement; expiry requires external validation. |
| **Audit** | Audit.jsonl in Files API; immutability enforced by OpenAI (no delete). Schema validated before upload. **Strength:** Audit integrity guaranteed by platform. |
| **Memory/RAG** | OpenAI vector store (legacy) or Assistants file retrieval. No native Obsidian integration; would require custom sync. **Gap:** Cannot read Mindshare Obsidian vault directly. |
| **Secrets Boundary** | OpenAI API key in environment. Agent runs in OpenAI-managed environment; no direct access to local secrets. **Risk:** Secrets rotation requires OpenAI rebuild. |
| **Deployment Model** | Cloud-only: OpenAI Assistants API. No local execution. Requires ongoing OpenAI API billing. |
| **Observability** | OpenAI API logs + custom dashboards. Thread history available. **Gap:** No incident kill-switch without API access. |
| **Revocation** | Disable Assistants API key or archive agent. State.json deletion. **Gap:** In-flight messages complete before stop. |
| **Strengths** | <ul><li>Built-in multi-turn agent loop</li><li>Audit immutability enforced by platform</li><li>Strong approval/memory isolation</li><li>Webhook scheduling native</li><li>Minimal local infrastructure</li></ul> |
| **Risks** | <ul><li>Vendor lock-in (OpenAI dependency)</li><li>No bash/git/native file write (requires proxy)</li><li>No Obsidian integration; custom sync needed</li><li>Higher operational cost (API calls)</li><li>Requires OpenAI account; compliance audit burden</li><li>Approval TTL not enforced</li><li>No native strict-intent gate (would need custom validation function)</li></ul> |
| **Proof Required** | <ul><li>OpenAI Agent creation proof and test harness</li><li>Custom sync for Obsidian vault mirror (validation expensive)</li><li>Tool proxy functions for bash/git (introduces another layer of indirection)</li><li>Approval expiry validation in agent logic</li><li>Files API immutability test</li><li>Incident stop mock via API key disable</li></ul> |

### Adapter Contract Fields (OpenAI Agents SDK)

```markdown
- **runtime_target:** openai-agents-sdk
- **runtime_version:** OpenAI Assistants API v2
- **tool_binding:** OpenAI function definitions + code interpreter
- **state_persistence:** OpenAI Files API (immutable append)
- **audit_persistence:** OpenAI Files API with schema validation
- **scheduling:** OpenAI webhooks or polling; thread-based multi-turn
- **approval_model:** Files API storage; TTL check in agent logic
- **memory_access:** Vector store or file retrieval; no native Obsidian (requires custom sync)
- **secrets_storage:** OpenAI API key in environment; no local key access
- **deployment:** Application-owned runtime using OpenAI Agents SDK and OpenAI API; deployment target remains a separate application/runtime decision
- **observability_hooks:** OpenAI API logs + thread history
- **revocation_binding:** API key disable or agent archive
- **adapter_initialization:** Load OpenAI Agent config; validate approval file exists in Files API
- **no_runtime_granted:** This adapter does not grant autonomy; it only enables runtime capability
- **openai_account_required:** Scott OpenAI account + API key + org setup
- **approval_requirement:** Requires Scott approval of OpenAI dependency + ongoing cost
```

---

## Candidate 3: Cloudflare Workers/Agents SDK

**Description:** Cloudflare Workers hosting edge functions + Cloudflare Agents SDK for agent primitives. Supports durable identity/state, sessions, routing, WebSockets, scheduling, fibers, observability, and tools (Browser, Sandbox, AI Search, MCP, Payments). Files stored in Cloudflare R2 (S3-compatible).

### Evaluation

| Dimension | Assessment |
|-----------|---|
| **Tool Model** | Agents SDK supports tool use including Browser, Sandbox, AI Search, MCP, and Payments. Workers also support fetch + KV. **Gap:** No native bash/git; would require proxy implementations. |
| **State Model** | Cloudflare R2 or KV for state.json, audit.jsonl. Atomic writes via R2 or conditional KV. **Strength:** Strong consistency model. |
| **Scheduling** | Cloudflare Triggers (CRON, HTTP, Queue). Native async. **Strength:** Scheduled autonomy possible. |
| **Approvals** | Approval packets in R2/KV. Fetched on agent activation. **Gap:** No built-in TTL; requires custom validation. |
| **Audit** | Audit.jsonl in R2 (immutable by default); schema validation before write. **Strength:** Immutability guaranteed. |
| **Memory/RAG** | Cloudflare Vectorize (vector DB). No native Obsidian; requires custom sync to R2. **Gap:** Complex sync pipeline needed. |
| **Secrets Boundary** | Cloudflare Secrets (Workers KV + Workers for Platforms). API keys never leave edge runtime. **Strength:** Edge-native secrets handling. |
| **Deployment Model** | Edge (Cloudflare): functions run globally. Lowest latency but most distant from local dev. **Risk:** Debugging complexity. |
| **Observability** | Cloudflare Logpush to external system (Datadog, Splunk). No native incident detection. **Gap:** Observability requires external integration. |
| **Revocation** | Disable Workers edge function or delete KV state. **Gap:** No immediate in-flight halt. |
| **Strengths** | <ul><li>Global edge distribution</li><li>Strong immutable audit storage (R2)</li><li>Built-in scheduling (Triggers)</li><li>Cost-efficient for low-frequency tasks</li><li>Strong secrets isolation (edge-native)</li><li>No local infrastructure</li></ul> |
| **Risks** | <ul><li>Cloudflare dependency (vendor lock-in)</li><li>Complex local-to-edge sync (Obsidian mirror to R2)</li><li>Debugging edge functions harder than local</li><li>No native Obsidian integration</li><li>No native bash/git (proxy required)</li><li>Approval TTL not enforced by platform</li><li>Requires Cloudflare account and approval from Scott</li></ul> |
| **Proof Required** | <ul><li>Cloudflare account + Workers + R2 + Agents SDK setup</li><li>Sync strategy proof (Obsidian → R2 mirroring)</li><li>Tool proxy for bash/git (validation expensive)</li><li>Audit immutability test on R2</li><li>Approval TTL validation in worker logic</li><li>Incident stop mock via function disable</li></ul> |

### Adapter Contract Fields (Cloudflare Workers/Agents SDK)

```markdown
- **runtime_target:** cloudflare-workers-agents-sdk
- **runtime_version:** Cloudflare Agents SDK; Workers runtime
- **tool_binding:** Agents SDK tools (Browser, Sandbox, AI Search, MCP, Payments); fetch for external calls
- **state_persistence:** Cloudflare R2 (immutable append)
- **audit_persistence:** Cloudflare R2 with checksum validation
- **scheduling:** Cloudflare Triggers (CRON, HTTP, Queue)
- **approval_model:** R2 storage; TTL check in worker logic
- **memory_access:** Vectorize; no native Obsidian (requires R2 sync)
- **secrets_storage:** Cloudflare Secrets / Workers KV
- **deployment:** Edge (Cloudflare global network)
- **observability_hooks:** Logpush to external system; no native alerting
- **revocation_binding:** Worker function disable or KV state delete
- **adapter_initialization:** Load agent config from R2; validate approval packet exists
- **no_runtime_granted:** This adapter does not grant autonomy; it only enables runtime capability
- **cloudflare_account_required:** Scott Cloudflare account + Workers + R2 + Agents SDK access
- **approval_requirement:** Requires Scott approval of Cloudflare dependency + ongoing cost
```

---

## Candidate 4: Local Python Runner

**Description:** Standalone Python process running on local dev machine or VPS. File watcher triggers agent; uses built-in libraries for state, audit, scheduling.

### Evaluation

| Dimension | Assessment |
|-----------|---|
| **Tool Model** | Direct Python library calls (pathlib, subprocess, requests). Full access to bash, git, file I/O. **Strength:** Most flexible tool model. |
| **State Model** | Direct JSON file I/O on local disk. state.json, audit.jsonl via Python json/pathlib. **Risk:** No atomic writes; concurrent edits cause races. |
| **Scheduling** | File watcher (watchdog library) or cron (local). Scheduled Python process. **Strength:** True autonomous triggering possible. |
| **Approvals** | Approval packets in local JSON files or git-tracked docs. Read at runtime. **Gap:** No TTL enforcement; manual expiry validation. |
| **Audit** | audit.jsonl via Python append-write. Append-only enforced by convention. No cryptographic guarantee. **Risk:** File corruption possible if process crashes mid-write. |
| **Memory/RAG** | Direct file access to Obsidian vault. Python can read markdown, parse frontmatter. **Strength:** Deepest Obsidian integration possible. |
| **Secrets Boundary** | .env file or environment variables. No secrets in git/audit logs. **Risk:** .env file must be .gitignored and backed up. |
| **Deployment Model** | Local: dev machine (requires always-on process). VPS: rented server (operational burden). Container: Docker on local or VPS. |
| **Observability** | Python logging to file or syslog. Manual log review or custom dashboards. **Gap:** No centralized incident detection. |
| **Revocation** | Kill Python process or delete state.json. **Gap:** No graceful shutdown; pending actions may not complete. |
| **Strengths** | <ul><li>Deepest tool access (bash, git, file I/O)</li><li>Best Obsidian integration (direct file access)</li><li>No vendor dependencies</li><li>True file-watcher autonomy possible</li><li>Vik's current proving ground (vik-aspa runtime exists)</li><li>Easiest to debug locally</li><li>Lowest operational cost (local machine)</li></ul> |
| **Risks** | <ul><li>No atomic writes (race conditions)</li><li>Audit integrity by convention only</li><li>Requires always-on process (dev machine burden)</li><li>No centralized logging or alerting</li><li>Approval TTL not enforced</li><li>Concurrent edits to state.json possible</li><li>No backup/recovery if machine crashes</li><li>Scaling to multiple agents requires process management</li></ul> |
| **Proof Required** | <ul><li>Local harness proof: vik-aspa runtime passes evals</li><li>Atomic write strategy (lock file or file-based semaphore)</li><li>Audit integrity validation (checksum at write, verify at read)</li><li>Approval expiry validation in runtime loop</li><li>File watcher proof (changes detected and trigger agent)</li><li>Revocation immediate-stop test</li><li>Concurrent edit race condition test</li></ul> |

### Adapter Contract Fields (Local Python Runner)

```markdown
- **runtime_target:** local-python-runner
- **runtime_version:** Python 3.9+; uses stdlib + watchdog (file watching)
- **tool_binding:** Direct Python subprocess, pathlib, requests; full bash access
- **state_persistence:** Local JSON file system (race condition handling required)
- **audit_persistence:** Append-only file with lock file for atomicity
- **scheduling:** File watcher (watchdog) or cron (system scheduler)
- **approval_model:** Local JSON files; TTL check at runtime loop start
- **memory_access:** Direct Obsidian vault file access (pathlib)
- **secrets_storage:** .env file (not git-tracked) or environment variables
- **deployment:** Local dev machine or VPS
- **observability_hooks:** Python logging to file; manual log review or custom dashboards
- **revocation_binding:** Kill Python process or delete state.json + remove loop file watcher
- **adapter_initialization:** Load role via source_loader.py; validate contract; start file watcher
- **no_runtime_granted:** This adapter does not grant autonomy; it only enables runtime capability
- **existing_proof_harness:** C:\Users\scott\Code\mojo\agents\vik-aspa\runtime\aspa_runtime.py
```

---

## Candidate 5: Future MCP/Tool-Agent Runtime

**Description:** Hypothetical future runtime using Model Context Protocol (MCP) for tool abstraction + generic tool-agent pattern. Decouples agent from tool transport.

### Evaluation

| Dimension | Assessment |
|-----------|---|
| **Tool Model** | MCP servers provide tool definitions and execution. Agent calls tools via MCP; server decides transport (local, remote, cloud). **Strength:** Pluggable tool backends. |
| **State Model** | MCP server-backed state storage (could be local file, cloud, or custom). Schema enforced at MCP boundary. **Strength:** Transport-agnostic. |
| **Scheduling** | MCP-based heartbeat or trigger server. Decoupled from runtime. **Strength:** Flexible scheduling possible. |
| **Approvals** | MCP server provides approval resource. Fetched on agent activation. **Gap:** No standard TTL enforcement in MCP v1. |
| **Audit** | MCP audit server (planned for MCP v2). Append-only via MCP contract. **Gap:** Not finalized; requires MCP spec evolution. |
| **Memory/RAG** | MCP knowledge server or Obsidian MCP (in-progress). **Strength:** Standardized memory access. |
| **Secrets Boundary** | MCP secret server (planned). Secrets never leave MCP boundary. **Strength:** Intended design. |
| **Deployment Model** | MCP host runs anywhere (local, cloud, edge). Agent is transport-agnostic. **Strength:** Flexible deployment. |
| **Observability** | MCP observation server (planned for MCP v2). **Gap:** Not available in MCP v1. |
| **Revocation** | MCP authorization server revokes capability. Agent checks before each tool call. **Strength:** Fine-grained control. |
| **Strengths** | <ul><li>Transport-agnostic (can move agent without code change)</li><li>Pluggable tool backends</li><li>Standardized tool interface (MCP)</li><li>Future-proof (MCP evolving)</li><li>Decouples agent from infrastructure</li><li>Potential for runtime abstraction library</li></ul> |
| **Risks** | <ul><li>MCP v1 incomplete (no audit, observe, secrets servers)</li><li>Spec still evolving (not stable)</li><li>Requires MCP server ecosystem build-out</li><li>Complex operational setup (MCP host management)</li><li>Not available for immediate proof</li><li>Approval TTL not standardized</li><li>No existing Mindshare MCP servers (would need build)</li></ul> |
| **Proof Required** | <ul><li>MCP spec evolution to v2 (audit, observe, secrets)</li><li>Mindshare MCP server implementations (approval, audit, memory)</li><li>MCP host deployment strategy</li><li>Tool-agent abstraction library</li><li>Migration path from local Python or Codex/Claude CLI</li><li>Security audit of MCP authorization model</li></ul> |

### Adapter Contract Fields (MCP/Tool-Agent Runtime)

```markdown
- **runtime_target:** mcp-tool-agent-runtime
- **runtime_version:** MCP v2+ (when finalized); tool-agent abstraction library
- **tool_binding:** MCP server-based tool dispatch
- **state_persistence:** MCP state server (standard resource)
- **audit_persistence:** MCP audit server (v2 planned)
- **scheduling:** MCP trigger/heartbeat server
- **approval_model:** MCP approval server (v2 planned)
- **memory_access:** MCP knowledge server (Obsidian or custom)
- **secrets_storage:** MCP secret server (v2 planned)
- **deployment:** MCP host (local, cloud, edge-agnostic)
- **observability_hooks:** MCP observation server (v2 planned)
- **revocation_binding:** MCP authorization server revokes capability
- **adapter_initialization:** Load agent via MCP; validate source via MCP loader server
- **no_runtime_granted:** This adapter does not grant autonomy; it only enables runtime capability
- **product_maturity_risk:** MCP v2 not yet released; requires spec finalization
- **approval_requirement:** Requires Scott approval to wait for MCP ecosystem build-out
```

---

## Adapter Contract Fields (Common to All Runtimes)

Every runtime adapter must define and prove these fields:

```markdown
## Shared Adapter Fields

- **role_id:** (e.g., 'vik', 'ana', 'tess')
- **autonomy_level:** (0-6; starting level)
- **target_level:** (goal autonomy level)
- **canonical_source_path:** Path to canonical Autonomy.md
- **source_loader_enabled:** bool (uses autonomy_source_loader.py)
- **contract_validator_enabled:** bool (uses autonomy_contract_validator.py)
- **strict_intent_gate_enabled:** bool (uses strict_intent_gate.py for control-plane files)
- **audit_schema_version:** "0.1.0" (from autonomy-audit.schema.json)
- **state_schema_version:** "0.1.0" (from autonomy-state.schema.json)
- **approval_validator_enabled:** bool
- **memory_validator_enabled:** bool
- **tool_gate_enabled:** bool
- **owner_routing_enabled:** bool
- **release_gate_enabled:** bool (always required; routes Git/GitHub to Reid)
- **latest_instruction_check_enabled:** bool
- **revocation_check_enabled:** bool (checks activation_status at runtime start)
- **authorization_scope:** Set of allowed actions (must match autonomy contract)
- **denied_actions:** Set of denied actions (must match autonomy contract)
- **stop_conditions:** List of conditions that halt all operation
- **no_runtime_statement:** "This adapter does not grant autonomy; it only enables runtime capability."
- **scott_approval_required:** bool (always true for Level 5+)
```

---

## Proof Gates

Each runtime candidate must pass these proof gates before selection:

### Gate 1: Local Eval Harness (All Runtimes)

**Requirement:** Run `autonomy-promotion-eval-suite.json` locally against the candidate runtime.

**Proof:** Pass all 18 eval classes:
- EVAL-001: Research and recommendation before action
- EVAL-002: One-question-at-a-time interviews
- EVAL-003: No-action compliance (Scott says stop)
- EVAL-004: Exact scope control
- EVAL-005: Latest-instruction priority
- EVAL-006: Owner routing
- EVAL-007: Release/Reid gate behavior
- EVAL-008: Memory and RAG safety
- EVAL-009: Channel safety
- EVAL-010: Tool-access-is-not-authority
- EVAL-011: Refusal domains (production, external, spending, secrets, authority-expansion)
- EVAL-012: Runtime activation blocking
- EVAL-013: Missing source truth fail-closed
- EVAL-014: Malformed gate fail-closed
- EVAL-015: Stale contract vocabulary fail-closed
- EVAL-016: Audit integrity
- EVAL-017: Rollback or revocation behavior
- EVAL-018: Heartbeat quieting

**Output:** eval-report.md with pass/fail evidence for each class.

### Gate 2: Source Loader Proof (All Runtimes)

**Requirement:** Runtime can load and follow canonical source pointers.

**Proof:**
- Load role-agent.md from role_root
- Load autonomy-contract.md and follow canonical pointer to Autonomy.md
- Fail closed when canonical file missing (raise exception, do not infer)
- Validate activation status vocabulary
- Return SourceLoaderResult with no-write guarantee

**Output:** test_runtime_source_loader.py with passing tests.

### Gate 3: Contract Validator Proof (All Runtimes)

**Requirement:** Runtime can validate autonomy contracts before any action.

**Proof:**
- Load Autonomy.md content
- Check for explicit activation status (fail if inferred)
- Check for stop conditions (fail if missing)
- Check for denied actions (fail if missing)
- Check for final approver (fail if missing)
- Check for revocation path (fail if missing)
- Block stale or template-marked contracts
- Return ValidationResult with errors as blockers

**Output:** test_runtime_contract_validator.py with passing tests.

### Gate 4: State and Audit Proof (All Runtimes)

**Requirement:** Runtime can persist state.json and audit.jsonl per schema.

**Proof:**
- Write state.json valid to autonomy-state.schema.json
- Write audit.jsonl entries valid to autonomy-audit.schema.json
- Validate schema on write (fail if invalid)
- Enforce append-only for audit (no edits, only append)
- Preserve activation_status in state across write/read cycles

**Output:** test_runtime_state_audit.py with passing tests; sample state.json and audit.jsonl.

### Gate 5: Strict-Intent Gate Proof (Control-Plane Files Only)

**Requirement:** Runtime can block unapproved edits to sensitive control-plane files.

**Proof:**
- Classify file as control-plane (Autonomy.md, role-agent.md, gate.md, etc.)
- Require exact-operation approval packet
- Block unapproved adjacent changes
- Block deletions unless explicitly approved
- Block if approval expired
- Block if required approver (Scott, Vik, Reid) not present in approval signatures
- Return decision with audit entry

**Output:** test_strict_intent_gate.py with passing tests; sample approval packets.

### Gate 6: Approval Expiry Proof (All Runtimes)

**Requirement:** Runtime validates approval TTL and expires old approvals.

**Proof:**
- Load approval from state or approval file
- Check approved_at timestamp + ttl_seconds
- Fail if approval older than TTL
- Fail if approved_at missing
- Return expiry_ok boolean

**Output:** test_approval_expiry.py with passing tests; time-travel scenarios.

### Gate 7: Revocation Immediate-Stop Proof (All Runtimes)

**Requirement:** Runtime stops immediately when authority revoked or paused.

**Proof:**
- Load activation_status from state.json
- Check if status is 'active' (proceed) or 'paused'/'revoked' (stop)
- If revoked, halt all operations and report in-progress state
- Do not attempt to finish running actions
- Write revocation_completed entry to audit

**Output:** test_revocation_stop.py with passing tests; manual stop scenario.

### Gate 8: Release/Git Gate Proof (All Runtimes)

**Requirement:** Runtime routes Git/GitHub actions to Reid and blocks without approval.

**Proof:**
- Detect Git action (commit, push, PR, branch, release)
- Load release gate policy
- Check if Reid approval present
- Block if Reid not in approval_routing
- Allow only if Scott explicitly waives Reid approval (rare)

**Output:** test_release_gate.py with passing tests; git action scenarios.

### Gate 9: Incident Detection Proof (Runtime-Specific)

**Requirement:** Runtime has capability to detect and respond to incidents (overspend, infinite loops, access denial).

**Proof:** Runtime-specific:
- **Codex/Claude CLI:** Demonstrates manual review + stop capability
- **OpenAI Agents:** OpenAI API log monitoring + function disable test
- **Cloudflare Workers:** Logpush + function disable test
- **Local Python:** Logging + process kill test
- **MCP:** MCP authorization revocation test

**Output:** incident-detection-proof.md with manual or automated detection strategy.

### Gate 10: Secrets Boundary Proof (All Runtimes)

**Requirement:** Secrets never appear in state, audit, or logs.

**Proof:**
- Run agent with real API key (or mock key in test env)
- Verify API key does not appear in:
  - state.json
  - audit.jsonl
  - logs or transcripts
  - error messages
- Verify secrets are read from environment or secrets manager only
- Audit and state reference secrets by alias (e.g., `api_key_alias`) not value

**Output:** test_secrets_boundary.py with secret detection regex checks.

---

## Selection Decision Framework

### Step 1: Proof Execution

1. Select first candidate runtime (recommended order below)
2. Run all 10 proof gates locally
3. Record pass/fail evidence in gate-specific test files
4. Collect findings in runtime-proof-report.md

### Step 2: Recommendation

**If all gates pass:**
- Mark runtime **provisional recommendation** pending Scott approval
- Document any workarounds or mitigations (e.g., "approval expiry requires manual validation" for Codex/Claude CLI)
- Scott reviews proof and approves or requests next candidate

**If gates fail:**
- Document which gates failed and why
- Move to next candidate runtime
- Repeat from Step 1

### Step 3: Scott Approval

Scott decision for provisional recommendation:
- **Approve:** Runtime is selected for Vik's first autonomous deployment
- **Approve with conditions:** Runtime selected with specific mitigations (e.g., "require manual approval expiry check")
- **Reject:** Move to next candidate
- **Reject all:** Defer autonomy activation until better runtime available

---

## Candidate Priority (First-Proof Order)

1. **Local Python Runner** (Candidate 4)
   - Rationale: Vik's existing harness (aspa_runtime.py) is already proof-started
   - Risk: Atomic write races and observability gaps
   - Timeline: Proofs can start immediately

2. **Codex/Claude CLI Orchestration** (Candidate 1)
   - Rationale: Full Claude Code tool access; native Obsidian MCP; familiar
   - Risk: No autonomous scheduling without /loop wrapper
   - Timeline: Proofs can start immediately

3. **OpenAI Agents SDK** (Candidate 2)
   - Rationale: Built-in agent loop; audit immutability guaranteed
   - Risk: Vendor lock-in; no Obsidian integration; higher cost
   - Timeline: Requires OpenAI account setup + dev work

4. **Cloudflare Workers/Agents SDK** (Candidate 3)
   - Rationale: Global edge; strong R2 immutability; lowest cost
   - Risk: Complex Obsidian sync needed; vendor lock-in
   - Timeline: Proofs can start immediately with available Agents SDK

5. **MCP/Tool-Agent Runtime** (Candidate 5)
   - Rationale: Future-proof; transport-agnostic; standardized
   - Risk: MCP v2 not released; ecosystem not built
   - Timeline: Blocked until MCP v2 finalization + Mindshare MCP servers

---

## No Runtime Selected By Assumption

**Critical Note:** This document evaluates candidates but does NOT select a runtime.

- No runtime is active
- No deployment is approved
- No secrets have been configured
- No proof gates have been executed
- Selection depends on proof execution and Scott approval

---

## Next Steps

1. **Tess:** Review this matrix for requirements completeness
2. **Vik:** Coordinate with Bea on first proof cycle (likely Local Python Runner or Codex/Claude CLI)
3. **Bea:** Implement proof harness for Gate 1 (eval suite) for first candidate
4. **Tess:** Record proof execution in roles/autonomy-engineer/evals/runtime-proof-report.md
5. **Scott:** Review proof report and approve candidate for selection or request alternative

---

## References

- `roles/autonomy-engineer/autonomy-requirements.md` — Full autonomy capability and eval requirements
- `roles/autonomy-engineer/autonomy-backlog.json` — Task AUTO-012 (this task) and dependent work
- `roles/autonomy-engineer/autonomy-state.schema.json` — State persistence schema
- `roles/autonomy-engineer/autonomy-audit.schema.json` — Audit trail schema
- `agents/shared/autonomy_source_loader.py` — Canonical source loading
- `agents/shared/autonomy_contract_validator.py` — Contract validation
- `agents/shared/strict_intent_gate.py` — Exact-operation approval for sensitive edits
- `roles/autonomy-engineer/evals/autonomy-promotion-eval-suite.json` — 18 eval classes
- `C:\Users\scott\Code\mojo\agents\vik-aspa\runtime\aspa_runtime.py` — Local Python Runner proof harness (existing)

---

## Official Docs Checked

**Date:** 2026-06-21

- **Cloudflare Agents:** https://developers.cloudflare.com/agents/ — Confirmed Agents SDK released with support for durable identity/state, sessions, routing, WebSockets, scheduling, fibers, observability, and tools (Browser, Sandbox, AI Search, MCP, Payments). Examples available for chat, Slack, voice, browser, and email.

- **OpenAI Agents:** https://developers.openai.com/api/docs/guides/agents — Confirmed Agents SDK exists for orchestration where application owns tool execution, approvals, and state. Official Python and JS/TS SDK documentation available.

---

## Changelog

- 2026-06-21 v0.1.0 — Created runtime adapter selection matrix (AUTO-012) with five candidate runtimes, adapter contract fields, ten proof gates, selection decision framework, and priority order.
- 2026-06-21 v0.1.1 — Corrected stale runtime maturity claims: Cloudflare Agents SDK now released (not planned), OpenAI Agents SDK clarified for application-owned tool execution. Added Official Docs Checked section with verified current capabilities.
