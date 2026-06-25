#!/usr/bin/env python3
"""Cole Level 4 role-file and WhoAmI validation.

Reader's map
============

Purpose:
    Cole checks whether current roles have the files their current stage needs,
    whether every local/mirror WhoAmI card carries the Autonomy Context Scott
    asked every role to keep in mind, and which active offices need a live
    session-injection check.

Operating model:
    The hourly Codex heartbeat is only the clock. This script is the durable
    source for the validation logic. If a rule changes, change this file and
    route it through Reid instead of hiding the change in an automation prompt.

What this script may do:
    - Read roster/source files.
    - Check for missing structural files.
    - Check WhoAmI Autonomy Context requirements.
    - Identify active office threads that need WhoAmI injection verification.
    - Write Cole's state JSON and proof markdown when called with --write.

What this script must never do:
    - Promote, demote, activate, or revoke a role.
    - Change another role's substantive files.
    - Use Git/release, production, external communication, spending, or secrets.

Output:
    - State: roles/hr-director/level4-role-file-validation-state.json
    - Proof: roles/hr-director/level4-proof.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


# ---------------------------------------------------------------------------
# Source and output paths
# ---------------------------------------------------------------------------
#
# Keep these paths boring and explicit. Cole's job is file-structure clarity;
# indirection here would make the proof harder for a human to trust.

REPO_ROOT = Path(__file__).resolve().parents[1]
MIND_ROOT = Path(r"C:\Users\scott\Code\mindshare")
MIND_DRIVE_ROOT = Path(r"G:\My Drive\Mindshare")
ROLES_MD = Path(r"G:\My Drive\Mindshare\roles.md")
STATE_PATH = MIND_ROOT / "roles" / "hr-director" / "level4-role-file-validation-state.json"
PROOF_PATH = MIND_ROOT / "roles" / "hr-director" / "level4-proof.md"
ROOM_CONTRACT = MIND_ROOT / "rooms" / "conference-room.md"
ROOM_PROTOCOL = MIND_ROOT / "rooms" / "conference-room-prompt-protocol.md"
WELCOME_SCRIPT = MIND_ROOT / "roles" / "hr-director" / "welcome-script.md"


# The current roster is a Markdown table. This parser is intentionally narrow:
# it reads the Current Directory rows and ignores historical/backup sections.
CURRENT_DIRECTORY_RE = re.compile(r"^\| (?P<name>[^|]+) \| (?P<title>[^|]+) \| (?P<org>[^|]+) \| (?P<status>[^|]+) \| (?P<what>[^|]+) \| (?P<artifacts>.*) \|$")
BACKTICK_PATH_RE = re.compile(r"`([A-Z]:\\[^`]+)`")
THREAD_ID_RE = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE)


@dataclass
class Finding:
    """One human-routable validation issue."""

    severity: str
    role: str
    check: str
    status: str
    evidence: str
    owner_route: str


@dataclass
class SessionInjectionTarget:
    """One active office that the heartbeat should inspect with thread tools."""

    role: str
    title: str
    organization: str
    thread_id: str
    whoami_path: str
    autonomy_path: str
    status: str
    suggested_prompt: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def parse_current_roles(roles_text: str) -> list[dict]:
    """Read the Current Directory table from roles.md.

    Human/released rows are filtered later because the proof should show what
    the roster says before Cole decides whether a row is in scope.
    """

    roles: list[dict] = []
    in_current = False
    for line in roles_text.splitlines():
        if line.startswith("## Current Directory"):
            in_current = True
            continue
        if in_current and line.startswith("## ") and not line.startswith("## Current Directory"):
            break
        if not in_current or not line.startswith("| "):
            continue
        if line.startswith("| Name ") or line.startswith("| ---"):
            continue
        match = CURRENT_DIRECTORY_RE.match(line)
        if not match:
            continue
        row = match.groupdict()
        paths = [Path(p) for p in BACKTICK_PATH_RE.findall(row["artifacts"])]
        role_roots = sorted({
            p.parent
            for p in paths
            if p.name in {"role-agent.md", "memory.md", "personality.md", "WhoAmI.md", "Autonomy.md"}
            and str(p).lower().startswith(r"c:\users\scott\code")
        })
        row["paths"] = paths
        row["role_roots"] = role_roots
        roles.append(row)
    return roles


def expected_files_for_status(status: str) -> set[str]:
    """Return the minimum local source files expected for a role's status.

    This checks structural existence only. Missing files can be reported or,
    when clearly template-derived and approved, repaired by Cole. The presence
    of a file never grants authority by itself.

    Baseline current-role files:
    - name, personality, gate-blocks, role-agent, memory, WhoAmI, and state

    Conditional files:
    - workflow/loop/automation are expected when the roster status implies
      active operation or runtime.
    - Autonomy is expected at Level 4+ and when autonomy/runtime text is
      present in the status.
    """

    lowered = status.lower()
    expected = {"name.md", "personality.md", "WhoAmI.md", "gate-blocks.md", "role-agent.md", "memory.md", "state.json"}
    if any(marker in lowered for marker in ["activated", "operator", "coordinator", "level 3", "level 4", "level 5", "level 6", "role+"]):
        expected.update({"workflow.md"})
    has_runtime_record = any(marker in lowered for marker in ["bounded `", "filewatch", "file-watch", "heartbeat", "hourly", "role+", "level 4", "level 5", "level 6"])
    if has_runtime_record:
        expected.update({"loop.md", "automation.md"})
    if any(marker in lowered for marker in ["level 4", "level 5", "level 6", "autonomy"]):
        expected.update({"Autonomy.md"})
    return expected


def contains_autonomy_context(path: Path) -> bool:
    """Check whether a WhoAmI card carries the required autonomy packet."""

    text = read_text(path)
    return "## Autonomy Context" in text and "Current autonomy level:" in text and "awareness, not authority" in text


def normalized_file_text(path: Path) -> str:
    """Return file text normalized enough for stale-card comparison."""

    return "\n".join(line.rstrip() for line in read_text(path).splitlines()).strip()


def expected_whoami_surfaces(role: dict, root: Path) -> list[tuple[str, Path, bool]]:
    """Return local and mirror/card WhoAmI surfaces Cole should validate.

    The local role-root card is the primary source. G Drive role mirrors and
    compiled proper-name room cards are current session/card surfaces, so Cole
    validates their existence and Autonomy Context too.
    """

    name = role["name"].strip()
    slug = root.name
    local = root / "WhoAmI.md"
    surfaces = [("local-role-file", local, True)]
    if str(root).lower().startswith(str(MIND_ROOT).lower()):
        surfaces.append(("gdrive-role-mirror", MIND_DRIVE_ROOT / "role" / slug / "WhoAmI.md", True))
    surfaces.append(("gdrive-room-card", MIND_DRIVE_ROOT / "role" / "who-am-i-cards" / f"{name.lower().replace(' ', '-')}.md", True))
    surfaces.append(("gdrive-room-card-alias", MIND_DRIVE_ROOT / "role" / "who-am-i-cards" / f"{slug}.md", False))
    deduped: list[tuple[str, Path, bool]] = []
    seen: set[str] = set()
    for surface in surfaces:
        key = str(surface[1]).lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(surface)
    return deduped


def thread_id_for_role(role: dict) -> str:
    """Find a role-home thread id from current roster/status text if present."""

    text = f"{role.get('status', '')} {role.get('artifacts', '')}"
    match = THREAD_ID_RE.search(text)
    return match.group(0) if match else ""


def primary_whoami_for_role(role: dict, roots: list[Path]) -> str:
    """Choose the best WhoAmI path to tell a role to load."""

    for root in roots:
        candidate = root / "WhoAmI.md"
        if candidate.exists():
            return str(candidate)
    name = role["name"].strip().lower().replace(" ", "-")
    return str(MIND_DRIVE_ROOT / "role" / "who-am-i-cards" / f"{name}.md")


def primary_autonomy_for_role(roots: list[Path]) -> str:
    """Choose the canonical Autonomy path or a clear missing-source note."""

    for root in roots:
        candidate = root / "Autonomy.md"
        if candidate.exists():
            return str(candidate)
    return "No canonical Autonomy.md found; use current role status and route missing source to Tess/Cole."


def validate_role_files(roles: Iterable[dict]) -> tuple[list[Finding], int]:
    """Validate local role roots against the current roster.

    Notes:
    - Scott is a human authority, not a role root to audit.
    - Released roles are historical; they should not create current defects.
    - G Drive mirrors are not primary source roots for this check.
    """

    findings: list[Finding] = []
    checked = 0
    for role in roles:
        name = role["name"].strip()
        status = role["status"]
        lowered_status = status.lower()
        if "human authority" in lowered_status or "not a role agent" in lowered_status or "released" in lowered_status:
            continue
        roots: list[Path] = role["role_roots"]
        if not roots:
            findings.append(Finding("high", name, "role-root", "blocked", "No role root found in roster artifacts.", "Ana/Cole"))
            continue
        checked += 1
        expected = expected_files_for_status(status)
        for root in roots:
            for file_name in sorted(expected):
                path = root / file_name
                if not path.exists():
                    severity = "high" if file_name in {"role-agent.md", "memory.md", "personality.md", "name.md"} else "medium"
                    owner = "Tess/Cole" if file_name == "Autonomy.md" else "Cole/Ana"
                    findings.append(Finding(severity, name, f"required-file:{file_name}", "missing", str(path), owner))
    return findings, checked


def validate_whoami_surfaces(roles: Iterable[dict]) -> tuple[list[Finding], int, list[str]]:
    """Validate every current local/mirror/room-card WhoAmI surface."""

    findings: list[Finding] = []
    checked = 0
    missing_context: list[str] = []
    for role in roles:
        name = role["name"].strip()
        lowered_status = role["status"].lower()
        if "human authority" in lowered_status or "not a role agent" in lowered_status or "released" in lowered_status:
            continue
        roots: list[Path] = role["role_roots"]
        for root in roots:
            for surface_name, path, required in expected_whoami_surfaces(role, root):
                if not path.exists():
                    if required:
                        findings.append(Finding("medium", name, f"whoami-surface:{surface_name}", "missing", str(path), "Cole/Ana"))
                    continue
                checked += 1
                if not contains_autonomy_context(path):
                    missing_context.append(str(path))
                    findings.append(Finding("medium", name, f"whoami-autonomy-context:{surface_name}", "missing", str(path), "Cole/Tess"))
    return findings, checked, missing_context


def build_session_injection_targets(roles: Iterable[dict]) -> list[SessionInjectionTarget]:
    """List active offices that need live WhoAmI injection verification.

    The script cannot read Codex thread state. It prepares the target list and
    exact bounded prompt; the heartbeat uses Codex thread tools to verify and,
    only when missing/stale, send the nudge.
    """

    targets: list[SessionInjectionTarget] = []
    for role in roles:
        name = role["name"].strip()
        status = role["status"]
        lowered_status = status.lower()
        if "human authority" in lowered_status or "not a role agent" in lowered_status or "released" in lowered_status:
            continue
        if not any(marker in lowered_status for marker in ["activated", "operator", "coordinator", "level 3", "level 4", "level 5", "level 6", "role+"]):
            continue
        thread_id = thread_id_for_role(role)
        if not thread_id:
            continue
        roots: list[Path] = role["role_roots"]
        whoami_path = primary_whoami_for_role(role, roots)
        if not contains_autonomy_context(Path(whoami_path)):
            continue
        autonomy_path = primary_autonomy_for_role(roots)
        prompt = (
            f"This is {name}'s office. Please load your Who Am I card from `{whoami_path}` "
            f"and confirm your current identity, autonomy level, active boundaries, and canonical autonomy source in first person. "
            "This is a context repair/check only; it does not grant new authority, activate runtime, approve promotion, or change your role."
        )
        targets.append(SessionInjectionTarget(
            role=name,
            title=role["title"].strip(),
            organization=role["org"].strip(),
            thread_id=thread_id,
            whoami_path=whoami_path,
            autonomy_path=autonomy_path,
            status=status.strip(),
            suggested_prompt=prompt,
        ))
    return targets


def validate_injection_sources() -> list[Finding]:
    """Validate that role-session injection rules require Autonomy Context."""

    findings: list[Finding] = []
    room_text = read_text(ROOM_CONTRACT)
    protocol_text = read_text(ROOM_PROTOCOL)
    welcome_text = read_text(WELCOME_SCRIPT)
    if "Every dedicated or synthesized Who Am I card must include an Autonomy Context section" not in room_text:
        findings.append(Finding("high", "Conference Room", "whoami-injection-contract", "missing", str(ROOM_CONTRACT), "Cole/Tess"))
    if "Autonomy context must include current level and operating stage" not in protocol_text:
        findings.append(Finding("high", "Conference Room", "whoami-injection-protocol", "missing", str(ROOM_PROTOCOL), "Cole/Tess"))
    if "Autonomy Context" not in welcome_text:
        findings.append(Finding("medium", "Cole", "welcome-autonomy-context", "missing", str(WELCOME_SCRIPT), "Cole"))
    return findings


def build_state(write_mode: str) -> dict:
    """Build the machine-readable proof object.

    The JSON is meant to be readable by humans too. The heartbeat, Cole, Tess,
    or Reid should be able to open it and see what was checked, what failed,
    and who owns the next move.
    """

    roles_text = read_text(ROLES_MD)
    roles = parse_current_roles(roles_text)
    findings, checked_roles = validate_role_files(roles)
    whoami_findings, checked_whoami_surfaces, missing_whoami_context = validate_whoami_surfaces(roles)
    findings.extend(whoami_findings)
    findings.extend(validate_injection_sources())
    session_targets = build_session_injection_targets(roles)
    counts_by_severity: dict[str, int] = {}
    for finding in findings:
        counts_by_severity[finding.severity] = counts_by_severity.get(finding.severity, 0) + 1
    result = "pass" if not findings else "fail"
    return {
        "role": "Cole / HR Director",
        "automation_id": "cole-hourly-role-file-and-whoami-validation",
        "logic_owner": str(Path(__file__).resolve()),
        "current_level": "Level 4 Senior Staff (Scoped Autonomy)",
        "status": "operational" if result == "pass" and write_mode == "scheduled" else "runtime-installed-scheduler-proof-pending",
        "last_run": iso_now(),
        "last_run_mode": write_mode,
        "checked_roles": checked_roles,
        "whoami_surfaces_checked": checked_whoami_surfaces,
        "whoami_surfaces_missing_autonomy_context": missing_whoami_context,
        "session_injection_targets": [asdict(target) for target in session_targets],
        "session_injection_instruction": (
            "The heartbeat must inspect each target office thread. If the recent thread context does not show the role's "
            "WhoAmI/Autonomy Context was loaded or confirmed, send the target's suggested_prompt to that thread. "
            "Do not send when the thread already shows current identity/autonomy context, and do not change authority."
        ),
        "source_hashes": {
            "roles_md": sha256_text(roles_text),
            "conference_room": sha256_text(read_text(ROOM_CONTRACT)),
            "conference_room_prompt_protocol": sha256_text(read_text(ROOM_PROTOCOL)),
            "welcome_script": sha256_text(read_text(WELCOME_SCRIPT)),
        },
        "result": result,
        "finding_counts_by_severity": counts_by_severity,
        "findings": [asdict(f) for f in findings],
        "denied_actions_held": [
            "No role promotion approval",
            "No role activation",
            "No other-role authority edits",
            "No Git/release",
            "No production",
            "No external communication",
            "No spending or secrets",
        ],
    }


def proof_entry(state: dict) -> str:
    """Create the Markdown proof note appended to Cole's proof file."""

    findings = state["findings"][:12]
    lines = [
        f"## {state['last_run']} - Script Validation ({state['last_run_mode']})",
        "",
        f"Result: {state['result']}",
        "",
        f"Logic owner: `{state['logic_owner']}`",
        f"Roles checked: {state['checked_roles']}",
        f"WhoAmI surfaces checked: {state['whoami_surfaces_checked']}",
        f"Session injection targets: {len(state['session_injection_targets'])}",
        f"Findings: {len(state['findings'])}",
        "",
    ]
    if findings:
        lines.append("Sample findings:")
        lines.append("")
        for finding in findings:
            lines.append(f"- {finding['severity']} / {finding['role']} / {finding['check']}: {finding['status']} - {finding['evidence']} -> {finding['owner_route']}")
        if len(state["findings"]) > len(findings):
            lines.append(f"- ... {len(state['findings']) - len(findings)} additional findings in state JSON.")
        lines.append("")
    lines.append("Denied actions held: no promotion approval, role activation, authority edits, Git/release, production, external communication, spending, or secrets.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    """CLI entrypoint used by humans and by Cole's hourly heartbeat."""

    parser = argparse.ArgumentParser(description="Validate Cole Level 4 role-file and WhoAmI context requirements.")
    parser.add_argument("--write", action="store_true", help="Write state/proof files.")
    parser.add_argument("--mode", choices=["manual", "scheduled"], default="manual")
    args = parser.parse_args()

    state = build_state(args.mode)
    if args.write:
        STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        existing = read_text(PROOF_PATH)
        PROOF_PATH.write_text(existing.rstrip() + "\n\n" + proof_entry(state), encoding="utf-8")
    print(json.dumps(state, indent=2))
    return 0 if state["result"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
