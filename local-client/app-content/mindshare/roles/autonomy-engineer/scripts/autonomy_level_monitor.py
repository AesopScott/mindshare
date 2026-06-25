#!/usr/bin/env python3
"""Tess autonomy-level monitor.

Reader's map
============

Purpose:
    Watch every current role `Autonomy.md` file I can discover and compare it
    with the active autonomy evaluation. If a current evaluation row shows a
    lower level than a canonical role contract, repair the evaluation before
    reporting. This is an anti-regression monitor, not a promotion engine.

What this script may do with --write:
    - Write autonomy-level-monitor-state.json.
    - Append autonomy-level-monitor-proof.md when changes, repairs, or
      conflicts are found.
    - Narrowly repair `Autonomy Evaluation 1.md` when a row's current autonomy
      field is lower than a canonical role `Autonomy.md` current level.

What this script must never do:
    - Demote anyone.
    - Promote anyone beyond a current canonical source.
    - Activate runtime, change authority, edit gates, use Git/release,
      production, external communication, spending, or secrets.

Demotion rule:
    A lower canonical value is treated as a conflict unless a current explicit
    Scott or Rae revocation source is present. This script currently does not
    implement revocation acceptance, so it fails closed and preserves the higher
    standing.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOTS = [
    Path(r"C:\Users\scott\Code\mindshare\roles"),
    Path(r"C:\Users\scott\Code\mojo\roles"),
    Path(r"C:\Users\scott\Code\watch\roles"),
]
ROLE_NAME_HINTS = {
    "autonomy-engineer": "Tess",
    "communications-director": "Mae",
    "hr-director": "Cole",
    "recruiter": "Ana",
    "ana-recruiter": "Ana",
    "chief-executive-officer": "Rae",
    "release-manager": "Reid",
    "staff-writer": "June",
    "executive-assistant": "Paige",
    "executive-assistant": "Paige",
    "maps-agentic-systems-program-architect": "Vik",
    "maps-agentic-systems-program-manager": "Cal",
    "mojo-maps-engineer": "Bea",
    "mojo-website-manager": "Liz",
    "lab-operator": "Lane",
    "meetup-coordinator": "Jay",
}

ROLE_ROOT = Path(r"C:\Users\scott\Code\mindshare\roles\autonomy-engineer")
EVALUATION_PATH = ROLE_ROOT / "Autonomy Evaluation 1.md"
STATE_PATH = ROLE_ROOT / "autonomy-level-monitor-state.json"
PROOF_PATH = ROLE_ROOT / "autonomy-level-monitor-proof.md"

LEVEL_LABELS = {
    0: "Level 0 Candidate",
    1: "Level 1 New Hire",
    2: "Level 2 Trainee",
    3: "Level 3 Staff",
    4: "Level 4 Senior Staff (Scoped Autonomy)",
    5: "Level 5 Principal (Policy Autonomy)",
    6: "Level 6 Partner (Native Autonomy)",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def level_from_text(text: str) -> int | None:
    patterns = [
        r"(?im)^current level:\s*(\d)\b",
        r"(?im)^current autonomy level:\s*level\s*(\d)\b",
        r"(?im)^current autonomy:\s*level\s*(\d)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
    return None


def role_name_from_path(path: Path, text: str) -> str:
    role_line = re.search(r"(?im)^role:\s*([^/\n|]+)", text)
    if role_line:
        first = role_line.group(1).strip().split("/")[0].strip()
        if first:
            return first
    heading = re.search(r"(?m)^#\s+([^/\n|]+)", text)
    if heading:
        first = heading.group(1).strip().split("/")[0].strip()
        if first and first.lower() not in {"autonomy", "gate blocks"}:
            return first
    return ROLE_NAME_HINTS.get(path.parent.name, path.parent.name)


def discover_canonical_roles() -> dict[str, dict]:
    roles: dict[str, dict] = {}
    for root in ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.glob("*/Autonomy.md")):
            text = read_text(path)
            level = level_from_text(text)
            if level is None:
                continue
            role = role_name_from_path(path, text)
            existing = roles.get(role)
            if existing and existing["level"] >= level:
                continue
            roles[role] = {
                "role": role,
                "level": level,
                "label": LEVEL_LABELS.get(level, f"Level {level}"),
                "path": str(path),
            }
    return roles


def parse_evaluation_rows(text: str) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for index, line in enumerate(text.splitlines()):
        if not line.startswith("| ") or line.startswith("| ---") or line.startswith("| Role "):
            continue
        cols = [part.strip() for part in line.strip("|").split("|")]
        if len(cols) < 4:
            continue
        level = None
        match = re.search(r"\bLevel\s+(\d)\b", cols[3])
        if match:
            level = int(match.group(1))
        rows[cols[0]] = {
            "line_index": index,
            "line": line,
            "current_autonomy": cols[3],
            "level": level,
            "columns": cols,
        }
    return rows


def repaired_autonomy_field(role: str, canonical: dict, old_field: str) -> str:
    suffix = ""
    if role == "Vik" and canonical["level"] == 5:
        suffix = " active for completed-research product-recommendation review only; Level 6 native loop defined-not-active"
    elif "defined-not-active" in old_field:
        tail = re.sub(r"^.*?(?=;\s*Level\s+[5-6])", "", old_field)
        suffix = tail
    return canonical["label"] + suffix


def repair_evaluation(evaluation_text: str, canonical_roles: dict[str, dict]) -> tuple[str, list[dict], list[dict]]:
    lines = evaluation_text.splitlines()
    rows = parse_evaluation_rows(evaluation_text)
    repairs: list[dict] = []
    conflicts: list[dict] = []
    for role, canonical in sorted(canonical_roles.items()):
        row = rows.get(role)
        if not row:
            continue
        eval_level = row["level"]
        if eval_level is None:
            conflicts.append({
                "role": role,
                "reason": "evaluation row has no parseable level",
                "canonical": canonical,
                "evaluation_current_autonomy": row["current_autonomy"],
            })
            continue
        if eval_level < canonical["level"]:
            columns = row["columns"]
            old_field = columns[3]
            columns[3] = repaired_autonomy_field(role, canonical, old_field)
            lines[row["line_index"]] = "| " + " | ".join(columns) + " |"
            repairs.append({
                "role": role,
                "from": old_field,
                "to": columns[3],
                "canonical_path": canonical["path"],
            })
        elif eval_level > canonical["level"]:
            conflicts.append({
                "role": role,
                "reason": "evaluation is higher than canonical role file; preserving higher standing until explicit revocation review",
                "canonical": canonical,
                "evaluation_current_autonomy": row["current_autonomy"],
            })
    return "\n".join(lines) + ("\n" if evaluation_text.endswith("\n") else ""), repairs, conflicts


def proof_entry(state: dict) -> str:
    return "\n".join([
        f"## {state['checked_at']} - Autonomy Level Monitor ({state['mode']})",
        "",
        f"Result: {state['result']}",
        f"Canonical files checked: `{state['counts']['canonical_files']}`",
        f"Repairs applied: `{state['counts']['repairs']}`",
        f"Conflicts preserved: `{state['counts']['conflicts']}`",
        "",
        f"Repairs: `{json.dumps(state['repairs'], sort_keys=True)}`",
        f"Conflicts: `{json.dumps(state['conflicts'], sort_keys=True)}`",
        "",
        "Denied actions held: no demotion, promotion beyond canonical source, runtime activation, gate edit, Git/GitHub/release, production, external communication, spending, secrets, or authority expansion.",
        "",
    ])


def build_and_maybe_write(mode: str, write: bool) -> dict:
    canonical_roles = discover_canonical_roles()
    evaluation_text = read_text(EVALUATION_PATH)
    repaired_text, repairs, conflicts = repair_evaluation(evaluation_text, canonical_roles)
    result = "repaired" if repairs else ("conflict_preserved" if conflicts else "no_change")
    state = {
        "schema_version": 1,
        "role": "Tess / Autonomy Engineer",
        "automation_id": "tess-autonomy-evaluation",
        "logic_owner": str(Path(__file__).resolve()),
        "mode": mode,
        "checked_at": iso_now(),
        "result": result,
        "counts": {
            "canonical_files": len(canonical_roles),
            "repairs": len(repairs),
            "conflicts": len(conflicts),
        },
        "repairs": repairs,
        "conflicts": conflicts,
        "canonical_roles": canonical_roles,
        "denied_actions_held": [
            "no demotion",
            "no promotion beyond canonical source",
            "no runtime activation",
            "no gate edit",
            "no git/github/release action",
            "no production",
            "no external communication",
            "no spending",
            "no secrets",
            "no authority expansion",
        ],
    }
    if write:
        if repairs:
            write_text(EVALUATION_PATH, repaired_text)
        write_text(STATE_PATH, json.dumps(state, indent=2) + "\n")
        if repairs or conflicts:
            existing = read_text(PROOF_PATH)
            write_text(PROOF_PATH, existing.rstrip() + "\n\n" + proof_entry(state))
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description="Monitor autonomy-level standing drift.")
    parser.add_argument("--write", action="store_true", help="Write state/proof and repair lower evaluation drift.")
    parser.add_argument("--mode", choices=["manual", "scheduled"], default="manual")
    args = parser.parse_args()
    state = build_and_maybe_write(args.mode, args.write)
    print(json.dumps(state, indent=2))
    return 0 if state["result"] in {"no_change", "repaired", "conflict_preserved"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
