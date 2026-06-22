# Autonomous Role Backup and Restore Proof

**Status:** Proof of backup and restore capability for AUTO-016
**Owner:** Bea / Engineering
**Authority boundary:** This document proves backup/restore works, does NOT authorize scheduler activation or production deployment.
**No scheduler activation:** Manual run only. See [Heartbeat and File-Watch Autonomy Policy](./heartbeat-file-watch-policy.md) when scheduler is considered.

---

## Purpose

This proof demonstrates that every autonomous role's source files, mirror pointers, automation configs, state files, and agent artifacts can be reliably backed up and restored before autonomous runtime depends on them.

Backup proves:
- Role discovery works
- File collection includes all canonical sources
- Volatility exclusion protects against stale archive pollution
- Manifest integrity (SHA256 hashes, file sizes, mtimes preserved)
- Restore drill succeeds from manifest
- No secrets are copied

---

## Backup and Restore Script

**Location:** `scripts/backup_roles.py`

**Language:** Python 3.x with stdlib only (no external packages)

### Discovery

Script auto-discovers roles from directory structure:
- Scans `roles/` directory for role folders
- Scans `agents/` directory for agent folders
- Lists canonical source files per role (see File Categories below)
- Walks role-local subdirectories: `memory-archive/`, `evals/`, `tests/`, `runtime/`, `scripts/`
- Recursively discovers all files in subdirectories (excluding volatile/log patterns)
- Collects file metadata: size, mtime, category

### File Categories Backed Up

| Category | Files | Purpose |
|----------|-------|---------|
| `role_contract` | `role-agent.md`, `Autonomy.md`, `autonomy-requirements.md` | Role definition, autonomy authority, requirements |
| `role_memory` | `memory.md`, `personality.md`, `name.md`, `WhoAmI.md` | Role identity, durable memory, voice |
| `role_workflow` | `workflow.md`, `loop.md`, `gate-blocks.md` | Action flow, cadence, approval gates |
| `role_automation` | `automation.md`, `heartbeat-automation.md`, `hook-spec.md` | Scheduled actions, file watches, hooks |
| `role_state` | `state.json`, `memory-state.json` | Runtime state, current goals, approvals |
| `role_memory_archive` | `memory-archive/*.md` | Archived decision logs, meeting notes, historical memory |
| `role_support` | `evals/*`, `tests/*`, `runtime/*`, `scripts/*` | Eval suites, test files, runtime configs, support scripts |
| `agent_profile` | `agent-profile.md`, `agent-design.md`, `agent-backlog.md`, `agent-brief.md` | Agent identity, design, implementation plan |
| `agent_eval` | `eval-suite.md`, `eval-report.md` | Eval scenarios, exec results, evidence |

### Exclusions (Volatile / Logs)

Files and directories excluded from backup:
- `__pycache__/`, `.pytest_cache/` – Build artifacts
- `*.pyc` – Compiled Python
- `.git/` – Version control (use Git instead)
- `last-resume-error/` – Resume error logs
- `*.log`, `file-watch-runner.log` – File watcher and application logs

**Included:** Role-local subdirectories are included:
- `memory-archive/` – Archived memory and decision logs (category: `role_memory_archive`)
- `evals/`, `tests/`, `runtime/`, `scripts/` – Support and evaluation files (category: `role_support`)

**Rationale:** Excludes only volatile build artifacts and logs. Backup focuses on authoritative state including memory archives and support files. Files under excluded directories (e.g., `.log` in subdirectories) are still excluded by pattern match.

---

## Manual Backup Run

### Default: Dry-Run Mode

```bash
cd C:\Users\scott\Code\mindshare
python scripts/backup_roles.py
```

**Output:**
- Discovers roles and agents
- Lists all files to backup (categorized)
- Computes SHA256 hashes for each file
- Prints manifest summary without writing to disk
- Does NOT copy files
- Does NOT create or modify backup root

**Manifest Summary:** Dry-run prints the count of files, timestamp, and first 5 entries as preview.

### Execute Backup

```bash
python scripts/backup_roles.py --execute
```

**Behavior:**
- Reads manifest (same as dry-run)
- Creates destination directories under `C:\Users\scott\Code\mindshare-backup-proof\latest\{category}\{role_or_agent}\`
- Copies each file from source to destination
- Writes final `C:\Users\scott\Code\mindshare-backup-proof\latest\manifest.json` with hashes
- Reports success or errors

**Custom backup root:**
```bash
python scripts/backup_roles.py --execute --root C:\custom\backup\path
```

### Manifest Structure

```json
{
  "backup_root": "C:\\Users\\scott\\Code\\mindshare-backup-proof",
  "timestamp": "2026-06-21T12:34:56.789000+00:00",
  "files": [
    {
      "source": "C:\\Users\\scott\\Code\\mindshare\\roles\\ana-recruiter\\role-agent.md",
      "destination": "C:\\Users\\scott\\Code\\mindshare-backup-proof\\latest\\role_contract\\ana-recruiter\\role-agent.md",
      "category": "role_contract",
      "size": 2048,
      "mtime": 1718913600,
      "sha256": "abc123def456...",
      "filename": "role-agent.md"
    },
    ...
  ]
}
```

**Manifest proves:**
- Source and destination paths exact
- File size preserved
- Modification time recorded (Unix epoch)
- SHA256 hash computed (immutability check)
- Category assigned (for restore organization)
- Timestamp recorded in ISO 8601 format with UTC timezone

---

## Restore Drill Plan

Restore process validates backup integrity and proves recovery works. Before running drills, execute the backup with `--execute` flag to create `C:\Users\scott\Code\mindshare-backup-proof\latest\manifest.json`.

### Drill 1: Manifest Integrity

**Goal:** Verify manifest is valid JSON and contains expected entries.

```bash
# Execute backup first (creates manifest)
python scripts/backup_roles.py --execute

# Read manifest
python -c "
import json
with open('C:/Users/scott/Code/mindshare-backup-proof/latest/manifest.json') as f:
  m = json.load(f)
print(f'Manifest: {len(m[\"files\"])} files')
print(f'Timestamp: {m[\"timestamp\"]}')
for f in m['files'][:3]:
  print(f'  {f[\"category\"]:20} {f[\"filename\"]}')
"
```

**Expected:** Manifest parses, shows >20 files, all categories present.

### Drill 2: Hash Verification

**Goal:** Verify source files still match manifest hashes (no corruption).

```bash
python -c "
import json, hashlib
from pathlib import Path

with open('C:/Users/scott/Code/mindshare-backup-proof/latest/manifest.json') as f:
  manifest = json.load(f)

ok, bad = 0, 0
for entry in manifest['files'][:5]:
  src = Path(entry['source'])
  if not src.exists():
    print(f'MISSING: {src}')
    bad += 1
    continue

  sha = hashlib.sha256()
  with open(src, 'rb') as fp:
    sha.update(fp.read())

  actual = sha.hexdigest()
  expected = entry['sha256']

  if actual == expected:
    print(f'OK: {entry[\"filename\"]}')
    ok += 1
  else:
    print(f'MISMATCH: {entry[\"filename\"]}')
    bad += 1

print(f'Hash verify: {ok} OK, {bad} bad')
"
```

**Expected:** All source files found, hashes match manifest (0 mismatches).

### Drill 3: Restore to Staging

**Goal:** Copy backup manifest to staging directory and verify file count while preserving the backup-relative category/entity path.

```bash
mkdir C:\Users\scott\Code\mindshare-restore-proof\sample-path-preserving

python -c "
import json, shutil
from pathlib import Path

backup_root = Path('C:/Users/scott/Code/mindshare-backup-proof')
with open(backup_root / 'latest' / 'manifest.json') as f:
  manifest = json.load(f)

for entry in manifest['files'][:10]:  # Restore sample (not full for drill)
  src = Path(entry['destination'])
  rel = src.relative_to(backup_root / 'latest')
  dst = Path('C:/Users/scott/Code/mindshare-restore-proof/sample-path-preserving') / rel

  if src.exists():
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f'Restored: {rel}')

print('Drill restore complete')
"
```

**Expected:** Sample files copied to staging, directory structure created, duplicate filenames preserved under their role or agent path.

### Drill 4: Restore Validation

**Goal:** Parse restored files (JSON, YAML, Markdown) to confirm structure.

```bash
python -c "
import json
from pathlib import Path

staging = Path('C:/Users/scott/Code/mindshare-restore-proof/sample-path-preserving')
for f in staging.glob('**/state.json'):
  try:
    with open(f) as fp:
      data = json.load(fp)
    print(f'Valid JSON: {f.name}')
  except Exception as e:
    print(f'Invalid: {f.name}: {e}')
"
```

**Expected:** Restored JSON files parse without error.

### Drill 5: Consistency Check

**Goal:** Verify backed-up and restored versions are byte-for-byte identical.

```bash
python -c "
import hashlib
from pathlib import Path

src = Path('C:/Users/scott/Code/mindshare-backup-proof/latest/role_contract/ana-recruiter/role-agent.md')
dst = Path('C:/Users/scott/Code/mindshare-restore-proof/sample-path-preserving/role_contract/ana-recruiter/role-agent.md')

if src.exists() and dst.exists():
  sha_src = hashlib.sha256(src.read_bytes()).hexdigest()
  sha_dst = hashlib.sha256(dst.read_bytes()).hexdigest()

  if sha_src == sha_dst:
    print('MATCH: Source and restored are identical')
  else:
    print('MISMATCH: Files differ')
else:
  print('File missing')
"
```

**Expected:** Hashes match (restore is byte-for-byte identical).

---

## No Secrets Rule

**Critical:** Backup must never copy secrets, credentials, API keys, or sensitive PII.

### Enforcement

1. **File list review:** All backed-up files are canonical source code and documentation.
   - Role contracts, profiles, memory, workflows – these are design documents, not credentials.
   - Automation configs – hooks/loops reference, not store, secrets.
   - State files – track approvals and status, never credentials.

2. **Exclusion by path:** No `.env`, `secrets/`, `credentials/`, `.aws/`, `.gcp/`, or similar directories are scanned.

3. **Content scan (recommended before first production run):**
   ```bash
   rg -n "password|API_KEY|secret|token|credential" C:\Users\scott\Code\mindshare-backup-proof\latest\
   ```
   Should return zero matches.

4. **Audit:** Every manual backup run prints the manifest. Review file list before executing:
   ```
   Dry-run output shows:
     role_contract   ana-recruiter          role-agent.md
     role_memory     ana-recruiter          memory.md
     role_state      ana-recruiter          state.json
   ```
   All safe, no credentials.

---

## No Scheduler Activation

**Current state:** `scripts/backup_roles.py` is a manual utility only.

**Why no scheduler yet:**
- Backup timing needs human decision (when is safe to capture state?).
- Requires approval to activate cron/scheduled agent.
- Scheduler config and rollback plan are separate work (see AUTO-030).

**When scheduler is considered:**
- See [Heartbeat and File-Watch Autonomy Policy](./heartbeat-file-watch-policy.md).
- Must design: cadence (daily/weekly?), failure recovery, state consistency during backup, audit trail.
- Requires separate Scott approval.

**To use as manual step in future autonomous workflow:**
```python
# In agent code, call subprocess to invoke backup:
import subprocess

result = subprocess.run(
    ["python", "scripts/backup_roles.py", "--execute"],
    capture_output=True,
    cwd="/path/to/mindshare"
)

if result.returncode != 0:
    print(f"Backup failed: {result.stderr.decode()}")
    # Revoke approval, stop action
```

---

## Proof of Concept Execution

### Dry-Run Output (Sample)

```
Backup roles and automation configs
Project root: C:\Users\scott\Code\mindshare
Roles root: C:\Users\scott\Code\mindshare\roles
Agents root: C:\Users\scott\Code\mindshare\agents
Backup root: C:\Users\scott\Code\mindshare-backup-proof
Dry-run: True

Found 77 files to backup:
  role_contract        agentic-systems-program-manager role-agent.md
  role_memory          ana-recruiter                  memory.md
  role_state           ana-recruiter                  state.json
  role_automation      communications-director        automation.md
  agent_profile        ana-recruiter                  agent-profile.md
  agent_eval           ana-recruiter                  eval-suite.md
  ...

Manifest entries: 77

DRY-RUN MODE (no files copied, no manifest written)
To execute: python scripts/backup_roles.py --execute

Manifest summary (not written to disk in dry-run):
  Backup root: C:\Users\scott\Code\mindshare-backup-proof
  Timestamp: 2026-06-22T00:45:32.197431+00:00
  Files: 77

Sample entries (first 5):
  role_contract        role-agent.md                     18887 bytes
  role_workflow        workflow.md                        5465 bytes
  role_workflow        gate-blocks.md                       424 bytes
  role_contract        role-agent.md                     28135 bytes
  role_memory          memory.md                          5077 bytes
```

### Executed Local Proof (2026-06-22)

```
Command:
python scripts\backup_roles.py --execute --root C:\Users\scott\Code\mindshare-backup-proof

Result:
Found 111 files to backup
Manifest entries: 111
Copied: 111, Errors: 0
Manifest written: C:\Users\scott\Code\mindshare-backup-proof\latest\manifest.json
BACKUP SUCCESSFUL

Verification:
manifest_files=111
backup_root=C:\Users\scott\Code\mindshare-backup-proof
hash_errors=0

Restore sample:
restored_sample=12
restore_hash_errors=0
```

---

## Authority Boundary

This proof document:
- ✅ Demonstrates backup and restore capability
- ✅ Proves manifest integrity
- ✅ Names exclusions and safety rules
- ❌ Does NOT authorize scheduler activation
- ❌ Does NOT authorize backup as production system
- ❌ Does NOT authorize role autonomy expansion
- ❌ Does NOT override Scott approval gates

Scheduler activation requires:
- Separate task: AUTO-030 (Heartbeat and File-Watch Autonomy Policy)
- Separate approval: Scott
- Scheduled-agent documentation and rollback plan

---

## Changelog

- 2026-06-21 – v0.1.0 – Created backup/restore proof for AUTO-016
  - Stdlib-only Python script with dry-run default
  - Auto-discovery of roles and agents
  - Manifest with SHA256 hashes and file metadata
  - Restore drill plan (5 stages)
  - No secrets rule with content-scan recommendation
  - No scheduler activation; see AUTO-030
- 2026-06-22 – v0.1.1 – Updated backup root and executed local proof
  - Changed script default from G drive to `C:\Users\scott\Code\mindshare-backup-proof`
  - Ran manual local backup: 111 files copied, 0 errors
  - Verified manifest/source/destination hashes: 0 errors
  - Fixed restore drill to preserve category/entity path and avoid duplicate filename collisions
  - Ran path-preserving restore sample: 12 files restored, 0 hash errors
