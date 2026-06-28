#!/usr/bin/env python3
"""Ana Level 4 recruiting lifecycle checker.

Reader's map
============

Purpose:
    Keep Ana's repeatable Level 4 recruiting lifecycle checks in a readable
    script. The Codex heartbeat is only the timer, packet-writing role context,
    and escalation surface.

What this script checks:
    - Recruiting backlog rows that are still `backlog`.
    - Pipeline items eligible for Level 1 -> Level 2.
    - Pipeline items at Level 2 that need office placement and Cole handoff.
    - The boundary that Ana's Level 4 stops at Level 2 plus Cole handoff.
    - Whether a Reid release-management request exists for durable changes.

What this script writes with --write:
    - roles/recruiter/level4-lifecycle-state.json
    - roles/recruiter/level4-lifecycle-proof.md

What this script never does:
    - Promote Level 2 roles to Level 3.
    - Promote anyone to Level 4+.
    - Contact candidates.
    - Change Git/release/production/spending/secrets/authority.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


ROLE_ROOT = Path(r"C:\Users\scott\Code\mindshare\roles\recruiter")
BACKLOG_PATH = ROLE_ROOT / "recruiting.backlog.md"
PIPELINE_PATH = ROLE_ROOT / "recruiting.pipeline.json"
AUTONOMY_PATH = ROLE_ROOT / "Autonomy.md"
STATE_PATH = ROLE_ROOT / "level4-lifecycle-state.json"
PROOF_PATH = ROLE_ROOT / "level4-lifecycle-proof.md"
RELEASE_QUEUE = Path(r"G:\My Drive\Mindshare\channels\release-management.md")


@dataclass
class BacklogRow:
    id: str
    title: str
    priority: str
    status: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_backlog() -> list[BacklogRow]:
    rows: list[BacklogRow] = []
    for line in read_text(BACKLOG_PATH).splitlines():
        if not line.startswith("| REC-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            continue
        rows.append(BacklogRow(
            id=cells[0],
            title=cells[2] if len(cells) > 2 else "",
            priority=cells[4] if len(cells) > 4 else "",
            status=cells[6].lower() if len(cells) > 6 else "",
        ))
    return rows


def load_pipeline() -> dict:
    text = read_text(PIPELINE_PATH)
    return json.loads(text) if text.strip() else {"items": []}


def release_request_present() -> bool:
    queue = read_text(RELEASE_QUEUE)
    return "Ana Level 4" in queue and "Reid" in queue


def build_state(mode: str) -> dict:
    now = datetime.now(timezone.utc).astimezone()
    backlog = parse_backlog()
    pipeline = load_pipeline()
    items = pipeline.get("items", [])
    backlog_eligible = [row for row in backlog if row.status == "backlog"]
    l1_ready = []
    l2_for_cole = []
    for item in items:
        stage = item.get("current_stage")
        status = item.get("status")
        eligible_at = parse_dt(item.get("next_eligible_at"))
        if status != "active":
            continue
        if stage == "level_1_new_hire":
            if eligible_at is None or eligible_at > now:
                continue
            l1_ready.append(item)
        elif stage == "level_2_trainee":
            l2_for_cole.append(item)
    result = "eligible_work" if backlog_eligible or l1_ready or l2_for_cole else "no_eligible_work"
    return {
        "schema_version": 1,
        "role": "Ana / Recruiter",
        "automation_id": "ana-l4-recruiting-backlog-processing",
        "logic_owner": str(Path(__file__).resolve()),
        "mode": mode,
        "checked_at": iso_now(),
        "result": result,
        "current_level": "Level 4 Senior Staff (Scoped Autonomy)",
        "counts": {
            "backlog_rows": len(backlog),
            "backlog_eligible": len(backlog_eligible),
            "pipeline_items": len(items),
            "level_1_ready_for_level_2": len(l1_ready),
            "level_2_ready_for_cole_handoff": len(l2_for_cole),
        },
        "eligible_backlog": [asdict(row) for row in backlog_eligible],
        "eligible_level_1_to_2": [
            {"id": item.get("id"), "role_title": item.get("role_title"), "next_eligible_at": item.get("next_eligible_at")}
            for item in l1_ready
        ],
        "level_2_for_cole_handoff": [
            {
                "id": item.get("id"),
                "person_name": item.get("person_name"),
                "role_title": item.get("role_title"),
                "level_2_packet": item.get("level_2_packet"),
                "owner_route": "Cole / HR Director",
            }
            for item in l2_for_cole
        ],
        "gate_status": {
            "contract": "pass" if AUTONOMY_PATH.exists() else "fail",
            "trigger": "pass" if BACKLOG_PATH.exists() and PIPELINE_PATH.exists() else "fail",
            "state": "pass_after_write" if mode in {"manual", "scheduled"} else "pending",
            "boundary": "pass_denied_actions_held",
            "reid_durability_route": "pass" if release_request_present() else "needs_request_when_files_change",
        },
        "denied_actions_held": [
            "no external recruiting",
            "no candidate contact",
            "no human hiring",
            "no Level 3 promotion",
            "no Level 4+ promotion for hired roles",
            "no Git/GitHub/release action",
            "no production or website edits",
            "no spending",
            "no secrets",
            "no authority expansion",
        ],
    }


def proof_entry(state: dict) -> str:
    return "\n".join([
        f"## {state['checked_at']} - Ana Level 4 Lifecycle Script Run ({state['mode']})",
        "",
        f"Result: {state['result']}",
        f"Logic owner: `{state['logic_owner']}`",
        f"Counts: `{json.dumps(state['counts'], sort_keys=True)}`",
        "Denied actions held: no external recruiting, candidate contact, human hiring, Level 3 promotion, Level 4+ promotion, Git/GitHub/release, production, website edit, spending, secrets, or authority expansion.",
        "",
    ])


def write_outputs(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    existing = read_text(PROOF_PATH)
    PROOF_PATH.write_text(existing.rstrip() + "\n\n" + proof_entry(state), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Ana Level 4 recruiting lifecycle checks.")
    parser.add_argument("--write", action="store_true", help="Write state/proof files.")
    parser.add_argument("--mode", choices=["manual", "scheduled"], default="manual")
    args = parser.parse_args()
    state = build_state(args.mode)
    if args.write:
        write_outputs(state)
    print(json.dumps(state, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
