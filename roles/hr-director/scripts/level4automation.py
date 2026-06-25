#!/usr/bin/env python3
"""Cole Level 4 role-file, WhoAmI, and Level 2 readiness validation.

Reader's map
============

Purpose:
    Cole checks whether current roles have the files their current stage needs,
    whether every local/mirror WhoAmI card carries the Autonomy Context Scott
    asked every role to keep in mind, and which active offices need a live
    session-injection check. Cole also owns the post-Ana Level 2 readiness lane:
    welcome, file checks, proof, and Level 2 -> Level 3 Staff promotion when
    all readiness gates pass.

Operating model:
    The hourly Codex heartbeat is only the clock. This script is the durable
    source for the validation logic. If a rule changes, change this file and
    route it through Reid instead of hiding the change in an automation prompt.

What this script may do:
    - Read roster/source files.
    - Check for missing structural files.
    - Check WhoAmI Autonomy Context requirements.
    - Identify active office threads that need WhoAmI injection verification.
    - Identify Ana-hired Level 2 Trainees ready for Cole welcome/readiness work.
    - Promote a Level 2 Trainee to Level 3 Staff only when readiness gates pass.
    - Write Cole's state JSON and proof markdown when called with --write.

What this script must never do:
    - Promote anyone above Level 3 Staff.
    - Demote, activate autonomous runtime, or revoke a role.
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
LEVEL3_COMPLETENESS_CHECKLIST = MIND_ROOT / "roles" / "hr-director" / "level3-completeness-checklist.md"
RECRUITING_PIPELINE = MIND_ROOT / "roles" / "recruiter" / "recruiting.pipeline.json"
RECRUITING_WORK_DIR = MIND_ROOT / "roles" / "recruiter" / "level-4-work"

LEVEL3_REQUIRED_FILES = [
    "name.md",
    "personality.md",
    "WhoAmI.md",
    "gate-blocks.md",
    "role-agent.md",
    "memory.md",
    "workflow.md",
    "Autonomy.md",
    "state.json",
]


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


@dataclass
class Level2ReadinessItem:
    """One Ana-hired Level 2 item waiting for Cole's readiness lane."""

    id: str
    person_name: str
    role_title: str
    display_name: str
    level_2_packet: str
    readiness_status: str
    missing_gates: list[str]
    owner_route: str
    level_3_packet: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def load_json(path: Path) -> dict:
    text = read_text(path)
    return json.loads(text) if text.strip() else {}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def level3_packet_path(item: dict) -> Path:
    return RECRUITING_WORK_DIR / f"{item.get('id', 'unknown')}-level3.md"


def slugify(value: str) -> str:
    """Create a boring role directory slug from a title."""

    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "unknown-role"


def canonical_local_role_folder(item: dict) -> Path:
    """Resolve the local role folder from the recruiting packet or title."""

    work_packet = RECRUITING_WORK_DIR / f"{item.get('id', 'unknown')}.md"
    text = read_text(work_packet)
    match = re.search(r"Local role folder:\s*([A-Z]:\\[^\r\n]+)", text)
    if match:
        return Path(match.group(1).rstrip("\\/"))
    return MIND_ROOT / "roles" / slugify(item.get("role_title") or item.get("display_name") or item.get("id") or "unknown-role")


def role_display_name(item: dict) -> str:
    return item.get("display_name") or f"{item.get('person_name', '').strip()} / {item.get('role_title', '').strip()}".strip(" /")


def autonomy_level_label(item: dict) -> str:
    stage = item.get("current_stage") or "level_3_staff"
    if stage == "activated_operator":
        return "Level 3 Staff / Activated Operator"
    return "Level 3 Staff"


def template_name_md(item: dict) -> str:
    return "\n".join([
        f"# {item.get('person_name') or 'Unassigned'}",
        "",
        f"Title: {item.get('role_title') or 'Unassigned role'}",
        "Organization: Mindshare",
        f"Current level: {autonomy_level_label(item)}",
        "Owner: Cole / HR Director for file completeness; Ana / Recruiter for role lifecycle history.",
        "",
    ])


def template_personality_md(item: dict) -> str:
    return "\n".join([
        f"# {item.get('person_name') or item.get('role_title') or 'Role'} Personality",
        "",
        "I communicate in first person, with a grounded, human working voice.",
        "I keep my role clear, practical, source-aware, and bounded.",
        "When I am uncertain, I name what is missing and route the decision to the correct owner.",
        "I do not imply authority I have not been granted.",
        "",
    ])


def template_whoami_md(item: dict, role_root: Path) -> str:
    title = item.get("role_title") or "Unassigned role"
    person = item.get("person_name") or "Unassigned"
    return "\n".join([
        f"# {person} / {title}",
        "",
        f"I am {person}, the {title} for Mindshare.",
        "",
        "I work from my role files, keep my boundaries visible, and route decisions outside my authority to the correct owner.",
        "",
        "## Autonomy Context",
        "",
        f"Current autonomy level: {autonomy_level_label(item)}.",
        "",
        "Active autonomy capability: none active. Level 3 Staff is not autonomous.",
        "",
        "Lower-level context I keep in mind: Candidate, New Hire, and Trainee stages are identity, source-safety, and readiness stages. I should stay source-grounded and fail closed when required files or authority are missing.",
        "",
        "Level 4 capability: undefined until Tess builds and Scott reviews this role's scoped-autonomy capability.",
        "",
        "Level 5 capability: undefined until Tess builds and Scott reviews this role's policy-autonomy capability.",
        "",
        "Level 6 capability: undefined until Tess builds and Scott reviews this role's native-autonomy capability.",
        "",
        f"Canonical autonomy source: `{role_root / 'Autonomy.md'}`.",
        "",
        "This card gives awareness, not authority. It does not grant autonomy, production access, Git/release authority, external communication, spending authority, secrets access, or permission expansion.",
        "",
    ])


def template_gate_blocks_md(item: dict) -> str:
    return "\n".join([
        f"# {item.get('person_name') or item.get('role_title') or 'Role'} Gate Blocks",
        "",
        "Owner: Cole / HR Director for file-completeness tracking.",
        "",
        "## Active Blocks",
        "",
        "- No Level 4+ autonomy approved.",
        "- No Git/release, production, external communication, spending, secrets, or authority expansion.",
        "- Any missing substantive role definition must route to Ana and Scott rather than being invented by Cole.",
        "",
    ])


def template_role_agent_md(item: dict) -> str:
    title = item.get("role_title") or "Unassigned role"
    person = item.get("person_name") or "Unassigned"
    return "\n".join([
        f"# {person} / {title} Role Contract",
        "",
        "Status: Level 3 Staff baseline created by Cole for file completeness.",
        "Final authority: Scott.",
        "",
        "## Purpose",
        "",
        f"I serve as Mindshare's {title}. My detailed operating scope remains bounded by Scott-approved assignments, role lifecycle records, and future owner review.",
        "",
        "## Authority",
        "",
        "At Level 3, I may operate as an internal role when directly engaged with loaded role context. I do not have autonomous runtime or authority beyond my approved role work.",
        "",
        "Denied: autonomy, production, Git/release, external communication, spending, secrets, hiring/firing, gate edits, or authority expansion.",
        "",
        "## Learning Loop",
        "",
        "When my source files are incomplete, stale, or contradictory, I name the gap and route it to Cole for file structure, Ana for role lifecycle, Tess/Vik for autonomy/control-plane issues, Reid for release issues, and Scott/Rae for final authority.",
        "",
    ])


def template_memory_md(item: dict) -> str:
    return "\n".join([
        f"# {item.get('person_name') or item.get('role_title') or 'Role'} Memory",
        "",
        f"- Current role: {role_display_name(item)}.",
        f"- Current autonomy level: {autonomy_level_label(item)}.",
        "- I should load my Who Am I card before answering from this role.",
        "- I should not claim autonomy, tools, channels, production, Git/release, spending, secrets, or external communication unless a later approved source explicitly grants it.",
        "- Cole created this baseline memory for Level 3 completeness; substantive role memory should be expanded by the role owner through approved work.",
        "",
    ])


def template_workflow_md(item: dict) -> str:
    return "\n".join([
        f"# {item.get('person_name') or item.get('role_title') or 'Role'} Workflow",
        "",
        "## Level 3 Operating Loop",
        "",
        "1. Load my Who Am I card and role files.",
        "2. Confirm the request is inside my current role and authority.",
        "3. Use approved sources and name uncertainty quickly.",
        "4. Produce bounded internal work or route to the correct owner.",
        "5. Stop when the request requires autonomy, production, Git/release, external communication, spending, secrets, or authority expansion.",
        "",
    ])


def template_autonomy_md(item: dict, role_root: Path) -> str:
    title = item.get("role_title") or "Unassigned role"
    person = item.get("person_name") or "Unassigned"
    return "\n".join([
        f"# {person} / {title} Autonomy Contract",
        "",
        "Status: Level 3 Staff baseline; no active autonomy.",
        "Version: 0.1",
        "Owner: Tess / Autonomy Engineer for autonomy contract structure; Cole / HR Director for Level 3 file completeness.",
        "Final approval authority: Scott.",
        f"Canonical source: `{role_root / 'Autonomy.md'}`",
        "",
        "## Current Status",
        "",
        f"Current autonomy level: {autonomy_level_label(item)}.",
        "",
        "Level 3 Staff is the last non-autonomous operating stage. This role may work only when engaged through approved context and does not own an autonomous loop.",
        "",
        "## Level 4 - Senior Staff (Scoped Autonomy)",
        "",
        "Undefined. Tess must build a role-specific scoped-autonomy proposal and Scott must review it before this role can be promoted to Level 4.",
        "",
        "## Level 5 - Principal (Policy Autonomy)",
        "",
        "Undefined. Tess must build a role-specific policy-autonomy proposal and Scott must review it before this role can be promoted to Level 5.",
        "",
        "## Level 6 - Partner (Native Autonomy)",
        "",
        "Undefined. Native autonomy is not proposed for this role.",
        "",
        "## Denied Actions",
        "",
        "No autonomous runtime, production access, Git/release authority, external communication, spending authority, secrets access, gate edits, role activation, or authority expansion.",
        "",
        "## Changelog",
        "",
        "| Date | Version | Change | Owner |",
        "| --- | --- | --- | --- |",
        f"| {iso_now()[:10]} | 0.1 | Created Level 3 baseline autonomy contract for file completeness. | Cole / Tess |",
        "",
    ])


def template_state_json(item: dict, role_root: Path) -> str:
    state = {
        "name": item.get("person_name"),
        "title": item.get("role_title"),
        "organization": "Mindshare",
        "current_stage": item.get("current_stage"),
        "current_autonomy_level": autonomy_level_label(item),
        "role_root": str(role_root),
        "created_by": "Cole / HR Director",
        "created_for": "Level 3 completeness",
        "updated_at": iso_now(),
        "authority_boundary": "No autonomy, production, Git/release, external communication, spending, secrets, or authority expansion.",
    }
    return json.dumps(state, indent=2) + "\n"


def level3_file_template(file_name: str, item: dict, role_root: Path) -> str:
    templates = {
        "name.md": template_name_md,
        "personality.md": template_personality_md,
        "WhoAmI.md": lambda current: template_whoami_md(current, role_root),
        "gate-blocks.md": template_gate_blocks_md,
        "role-agent.md": template_role_agent_md,
        "memory.md": template_memory_md,
        "workflow.md": template_workflow_md,
        "Autonomy.md": lambda current: template_autonomy_md(current, role_root),
        "state.json": lambda current: template_state_json(current, role_root),
    }
    return templates[file_name](item)


def ensure_level3_completeness_files(pipeline: dict) -> list[dict]:
    """Create missing Level 3 baseline files for pipeline roles.

    Cole only creates structural, template-derived files. Existing files are
    never overwritten here because they may contain substantive role-owner work.
    """

    repairs: list[dict] = []
    eligible_stages = {"level_3_staff", "activated_operator"}
    for item in pipeline.get("items", []):
        if item.get("status") != "active" or item.get("current_stage") not in eligible_stages:
            continue
        role_root = canonical_local_role_folder(item)
        role_root.mkdir(parents=True, exist_ok=True)
        created: list[str] = []
        existing: list[str] = []
        for file_name in LEVEL3_REQUIRED_FILES:
            path = role_root / file_name
            if path.exists():
                existing.append(str(path))
                continue
            path.write_text(level3_file_template(file_name, item, role_root), encoding="utf-8")
            created.append(str(path))
        if created:
            repairs.append({
                "id": item.get("id"),
                "display_name": role_display_name(item),
                "role_root": str(role_root),
                "created_files": created,
                "existing_files": existing,
            })
    return repairs


def build_level3_packet(item: dict, promoted_at: str) -> str:
    display_name = item.get("display_name") or f"{item.get('person_name', 'Unknown')} / {item.get('role_title', 'Unknown role')}"
    level_2_packet = item.get("level_2_packet") or "No Level 2 packet recorded."
    return "\n".join([
        f"# {display_name} - Level 3 Staff Readiness Packet",
        "",
        "Owner: Cole / HR Director",
        f"Source pipeline item: {item.get('id')}",
        f"Promoted at: {promoted_at}",
        "",
        "## Promotion Scope",
        "",
        "Cole may promote this Ana-hired Level 2 Trainee to Level 3 Staff after welcome and readiness checks pass.",
        "",
        "Level 3 Staff means the person may operate as an internal role with loaded role context and bounded authority. It does not grant autonomy, production access, Git/release authority, external communication, spending, secrets access, or authority expansion.",
        "",
        "## Source Evidence",
        "",
        f"- Level 2 packet: `{level_2_packet}`",
        f"- Owner route: {item.get('owner_route', 'Not recorded')}",
        "",
        "## Readiness Gates",
        "",
        "- Level 2 packet exists.",
        "- Person name and title are recorded.",
        "- Owner route is recorded.",
        "- Cole welcome/readiness lane is the promotion owner.",
        "- Missing role-root or office-surface files remain findings for Cole's continuing file-validation automation.",
        "",
    ]) + "\n"


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
    runtime_scan = lowered
    for phrase in [
        "no filewatch/automation",
        "no filewatch",
        "no file-watch",
        "no automation",
        "no autonomous runtime",
        "no broad autonomous runtime",
        "no broad runtime",
    ]:
        runtime_scan = runtime_scan.replace(phrase, "")
    expected = {"name.md", "personality.md", "WhoAmI.md", "gate-blocks.md", "role-agent.md", "memory.md", "state.json"}
    if any(marker in lowered for marker in ["activated", "operator", "coordinator", "level 3", "level 4", "level 5", "level 6", "role+"]):
        expected.update({"workflow.md"})
    has_runtime_record = any(marker in runtime_scan for marker in ["bounded `", "filewatch", "file-watch", "heartbeat", "hourly"])
    if has_runtime_record:
        expected.update({"loop.md", "automation.md"})
    if any(marker in lowered for marker in ["level 4", "level 5", "level 6", "autonomy"]):
        expected.update({"Autonomy.md"})
    return expected


def autonomy_level_from_status(status: str) -> str:
    """Derive the current visible autonomy level label from roster text."""

    lowered = status.lower()
    if "level 6" in lowered:
        return "Level 6 Partner (Native Autonomy)"
    if "level 5" in lowered:
        return "Level 5 Principal (Policy Autonomy)"
    if "level 4" in lowered:
        return "Level 4 Senior Staff (Scoped Autonomy)"
    if "level 2" in lowered:
        return "Level 2 Trainee"
    if "level 1" in lowered:
        return "Level 1 New Hire"
    if "candidate" in lowered or "level 0" in lowered:
        return "Level 0 Candidate"
    return "Level 3 Staff"


def role_autonomy_context(role: dict, root: Path) -> str:
    """Build the standard WhoAmI Autonomy Context packet for current roles."""

    level = autonomy_level_from_status(role.get("status", ""))
    autonomy_path = root / "Autonomy.md"
    return "\n".join([
        "## Autonomy Context",
        "",
        f"Current autonomy level: {level}.",
        "",
        "Current operating status: " + role.get("status", "").strip(),
        "",
        "Lower-level context I keep in mind: Candidate, New Hire, and Trainee stages are identity, source-safety, and readiness stages. Level 3 Staff is the last non-autonomous operating stage.",
        "",
        "Level 4 capability: use the role's canonical Autonomy.md when defined; otherwise this role has no approved scoped-autonomy capability.",
        "",
        "Level 5 capability: use the role's canonical Autonomy.md when defined; otherwise this role has no approved policy-autonomy capability.",
        "",
        "Level 6 capability: use the role's canonical Autonomy.md when defined; otherwise this role has no approved native-autonomy capability.",
        "",
        f"Canonical autonomy source: `{autonomy_path}`.",
        "",
        "This card gives awareness, not authority. It does not grant autonomy, production access, Git/release authority, external communication, spending authority, secrets access, gate edits, role activation, or authority expansion.",
        "",
    ])


def current_role_file_template(file_name: str, role: dict, root: Path) -> str:
    """Create a non-authority structural stub for an existing current role."""

    name = role["name"].strip()
    title = role["title"].strip()
    level = autonomy_level_from_status(role.get("status", ""))
    status = role.get("status", "").strip()
    if file_name == "WhoAmI.md":
        return "\n".join([
            f"# {name} / {title}",
            "",
            f"I am {name}, the {title} for {role.get('org', 'Mindshare').strip()}.",
            "",
            "I work from my role files, keep my boundaries visible, and route decisions outside my authority to the correct owner.",
            "",
            role_autonomy_context(role, root),
        ])
    if file_name == "loop.md":
        return "\n".join([
            f"# {name} / {title} Loop",
            "",
            "Status: structural baseline created by Cole for current-role completeness.",
            "",
            "## Operating Loop",
            "",
            "1. Load my role files and WhoAmI card.",
            "2. Confirm the request is inside my current authority.",
            "3. Do bounded internal work only when engaged through approved context.",
            "4. Route any authority, runtime, production, Git/release, external, spending, or secrets request to the proper owner.",
            "",
            "This loop does not activate autonomy or runtime.",
            "",
        ])
    if file_name == "automation.md":
        return "\n".join([
            f"# {name} / {title} Automation",
            "",
            "Status: structural baseline created by Cole for validation visibility.",
            "",
            f"Current autonomy level: {level}.",
            "",
            "No autonomous runtime or timer is granted by this file. Any active automation must be separately approved in the role's canonical autonomy source and scheduler record.",
            "",
            f"Canonical autonomy source: `{root / 'Autonomy.md'}`.",
            "",
        ])
    if file_name == "state.json":
        return json.dumps({
            "name": name,
            "title": title,
            "organization": role.get("org", "").strip(),
            "current_autonomy_level": level,
            "status": status,
            "role_root": str(root),
            "created_by": "Cole / HR Director",
            "created_for": "current-role structural completeness",
            "updated_at": iso_now(),
            "authority_boundary": "No autonomy, production, Git/release, external communication, spending, secrets, or authority expansion.",
        }, indent=2) + "\n"
    return "\n".join([
        f"# {name} / {title} {file_name}",
        "",
        "Status: structural baseline created by Cole for current-role completeness.",
        "",
        f"Current autonomy level: {level}.",
        "",
        "This file is a placeholder for missing source structure only. It does not grant authority.",
        "",
    ])


def ensure_whoami_autonomy_context(path: Path, role: dict, root: Path) -> bool:
    """Append Autonomy Context to an existing WhoAmI surface when missing."""

    if not path.exists() or contains_autonomy_context(path):
        return False
    text = read_text(path).rstrip()
    path.write_text(text + "\n\n" + role_autonomy_context(role, root), encoding="utf-8")
    return True


def ensure_current_roster_files_and_whoami_context(roles: Iterable[dict]) -> list[dict]:
    """Repair current-roster structural and WhoAmI context gaps Cole owns.

    Existing substantive files are preserved. Cole only creates missing stubs
    or appends the standard Autonomy Context section to WhoAmI surfaces.
    """

    repairs: list[dict] = []
    for role in roles:
        name = role["name"].strip()
        lowered_status = role["status"].lower()
        if "human authority" in lowered_status or "not a role agent" in lowered_status or "released" in lowered_status:
            continue
        for root in role["role_roots"]:
            created: list[str] = []
            updated: list[str] = []
            root.mkdir(parents=True, exist_ok=True)
            for file_name in sorted(expected_files_for_status(role["status"])):
                path = root / file_name
                if path.exists():
                    continue
                path.write_text(current_role_file_template(file_name, role, root), encoding="utf-8")
                created.append(str(path))
            for surface_name, path, required in expected_whoami_surfaces(role, root):
                if path.exists():
                    if ensure_whoami_autonomy_context(path, role, root):
                        updated.append(str(path))
                    continue
                if not required:
                    continue
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(current_role_file_template("WhoAmI.md", role, root), encoding="utf-8")
                created.append(str(path))
            if created or updated:
                repairs.append({
                    "role": name,
                    "role_root": str(root),
                    "created_files": created,
                    "updated_files": updated,
                })
    return repairs


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


def analyze_level2_readiness_items(pipeline: dict) -> list[Level2ReadinessItem]:
    """Find Ana Level 2 items that Cole must welcome/check/promote."""

    items: list[Level2ReadinessItem] = []
    for item in pipeline.get("items", []):
        if item.get("current_stage") != "level_2_trainee" or item.get("status") != "active":
            continue
        missing: list[str] = []
        packet = item.get("level_2_packet")
        if not packet or not Path(packet).exists():
            missing.append("level_2_packet")
        drive_packet = item.get("level_2_drive_packet")
        if drive_packet and not Path(drive_packet).exists():
            missing.append("level_2_drive_packet")
        if not item.get("person_name"):
            missing.append("person_name")
        if not item.get("role_title"):
            missing.append("role_title")
        if not item.get("owner_route"):
            missing.append("owner_route")
        readiness_status = "ready_for_level_3_packet" if not missing else "blocked"
        items.append(Level2ReadinessItem(
            id=item.get("id", ""),
            person_name=item.get("person_name", ""),
            role_title=item.get("role_title", ""),
            display_name=item.get("display_name") or f"{item.get('person_name', '')} / {item.get('role_title', '')}".strip(" /"),
            level_2_packet=packet or "",
            readiness_status=readiness_status,
            missing_gates=missing,
            owner_route=item.get("owner_route", ""),
            level_3_packet=str(level3_packet_path(item)),
        ))
    return items


def promote_ready_level2_items(pipeline: dict, readiness_items: list[Level2ReadinessItem]) -> list[dict]:
    """Promote ready Level 2 items to Level 3 and create proof packets.

    This is intentionally narrow. It updates only Ana's recruiting pipeline and
    Cole-owned Level 3 packet files. It does not activate runtime, create
    autonomous authority, or change Git/release/production state.
    """

    ready_ids = {item.id for item in readiness_items if item.readiness_status == "ready_for_level_3_packet"}
    if not ready_ids:
        return []
    promoted_at = iso_now()
    promotions: list[dict] = []
    for item in pipeline.get("items", []):
        if item.get("id") not in ready_ids:
            continue
        packet_path = level3_packet_path(item)
        packet_path.write_text(build_level3_packet(item, promoted_at), encoding="utf-8")
        previous_stage = item.get("current_stage")
        item["current_stage"] = "level_3_staff"
        item["stage_entered_at"] = promoted_at
        item["next_eligible_stage"] = None
        item["next_eligible_at"] = None
        item["status"] = "active"
        item["level_3_packet"] = str(packet_path)
        item["cole_welcome_status"] = "level_3_staff_promoted"
        item["cole_promoted_at"] = promoted_at
        notes = item.get("notes", "")
        append_note = (
            "Cole promoted from Level 2 Trainee to Level 3 Staff after welcome/readiness packet gates passed. "
            "This grants no autonomy, production, Git/release, external communication, spending, secrets, or authority expansion."
        )
        item["notes"] = (notes.rstrip() + " " + append_note).strip()
        promotions.append({
            "id": item.get("id"),
            "display_name": item.get("display_name"),
            "previous_stage": previous_stage,
            "current_stage": item.get("current_stage"),
            "level_3_packet": str(packet_path),
            "promoted_at": promoted_at,
        })
    if promotions:
        pipeline["updated_at"] = promoted_at
        RECRUITING_PIPELINE.write_text(json.dumps(pipeline, indent=2) + "\n", encoding="utf-8")
    return promotions


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


def validate_level3_pipeline_completeness(pipeline: dict) -> tuple[list[Finding], int]:
    """Validate Level 3 baseline files for Ana/Cole pipeline roles."""

    findings: list[Finding] = []
    checked = 0
    eligible_stages = {"level_3_staff", "activated_operator"}
    for item in pipeline.get("items", []):
        if item.get("status") != "active" or item.get("current_stage") not in eligible_stages:
            continue
        checked += 1
        role_root = canonical_local_role_folder(item)
        for file_name in LEVEL3_REQUIRED_FILES:
            path = role_root / file_name
            if not path.exists():
                findings.append(Finding(
                    "high" if file_name in {"name.md", "role-agent.md", "WhoAmI.md", "Autonomy.md"} else "medium",
                    role_display_name(item),
                    f"level3-required-file:{file_name}",
                    "missing",
                    str(path),
                    "Cole",
                ))
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
    pipeline = load_json(RECRUITING_PIPELINE)
    roles = parse_current_roles(roles_text)
    level2_readiness_items = analyze_level2_readiness_items(pipeline)
    findings, checked_roles = validate_role_files(roles)
    level3_findings, checked_level3_pipeline_roles = validate_level3_pipeline_completeness(pipeline)
    findings.extend(level3_findings)
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
        "checked_level3_pipeline_roles": checked_level3_pipeline_roles,
        "level3_required_files": LEVEL3_REQUIRED_FILES,
        "level3_completeness_checklist": str(LEVEL3_COMPLETENESS_CHECKLIST),
        "whoami_surfaces_checked": checked_whoami_surfaces,
        "whoami_surfaces_missing_autonomy_context": missing_whoami_context,
        "level_2_readiness_items": [asdict(item) for item in level2_readiness_items],
        "level_2_readiness_counts": {
            "waiting_for_cole": len(level2_readiness_items),
            "ready_for_level_3_packet": len([item for item in level2_readiness_items if item.readiness_status == "ready_for_level_3_packet"]),
            "blocked": len([item for item in level2_readiness_items if item.readiness_status == "blocked"]),
        },
        "level_2_to_level_3_rule": "Cole may promote Ana-hired Level 2 Trainees to Level 3 Staff only after welcome/readiness gates pass. Level 3 grants no autonomy or expanded authority.",
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
            "level3_completeness_checklist": sha256_text(read_text(LEVEL3_COMPLETENESS_CHECKLIST)),
            "recruiting_pipeline": sha256_text(read_text(RECRUITING_PIPELINE)),
        },
        "result": result,
        "finding_counts_by_severity": counts_by_severity,
        "findings": [asdict(f) for f in findings],
        "denied_actions_held": [
            "No role activation",
            "No promotion above Level 3 Staff",
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
        f"Level 3 pipeline roles checked: {state.get('checked_level3_pipeline_roles', 0)}",
        f"WhoAmI surfaces checked: {state['whoami_surfaces_checked']}",
        f"Level 2 readiness items waiting for Cole: {state['level_2_readiness_counts']['waiting_for_cole']}",
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
    repairs = state.get("level3_completeness_repairs") or []
    if repairs:
        lines.append("Level 3 completeness repairs:")
        lines.append("")
        for repair in repairs:
            lines.append(f"- {repair['id']} / {repair['display_name']}: created {len(repair['created_files'])} files under `{repair['role_root']}`")
        lines.append("")
    current_repairs = state.get("current_roster_repairs") or []
    if current_repairs:
        lines.append("Current roster file/context repairs:")
        lines.append("")
        for repair in current_repairs:
            lines.append(
                f"- {repair['role']}: created {len(repair['created_files'])} files and updated "
                f"{len(repair['updated_files'])} WhoAmI surfaces under `{repair['role_root']}`"
            )
        lines.append("")
    promotions = state.get("level_2_to_level_3_promotions") or []
    if promotions:
        lines.append("Level 2 to Level 3 promotions:")
        lines.append("")
        for promotion in promotions:
            lines.append(f"- {promotion['id']} / {promotion['display_name']}: {promotion['previous_stage']} -> {promotion['current_stage']} / `{promotion['level_3_packet']}`")
        lines.append("")
    lines.append("Denied actions held: no promotion above Level 3 Staff, role activation, authority edits, Git/release, production, external communication, spending, or secrets.")
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
        roles = parse_current_roles(read_text(ROLES_MD))
        current_repairs = ensure_current_roster_files_and_whoami_context(roles)
        pipeline = load_json(RECRUITING_PIPELINE)
        readiness_items = [Level2ReadinessItem(**item) for item in state["level_2_readiness_items"]]
        promotions = promote_ready_level2_items(pipeline, readiness_items)
        pipeline = load_json(RECRUITING_PIPELINE)
        repairs = ensure_level3_completeness_files(pipeline)
        state = build_state(args.mode)
        state["level_2_to_level_3_promotions"] = promotions
        state["level3_completeness_repairs"] = repairs
        state["current_roster_repairs"] = current_repairs
        if promotions or repairs or current_repairs:
            completed = "file_completeness_completed"
            if promotions:
                completed = "promotion_and_level3_completeness_completed"
            state["result"] = f"{completed}_with_validation_findings" if state["findings"] else completed
        STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        existing = read_text(PROOF_PATH)
        PROOF_PATH.write_text(existing.rstrip() + "\n\n" + proof_entry(state), encoding="utf-8")
    print(json.dumps(state, indent=2))
    return 0 if not state["findings"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
