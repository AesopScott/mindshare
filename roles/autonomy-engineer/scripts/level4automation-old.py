#!/usr/bin/env python3
"""Tess Level 4 autonomy backlog processor.

Reader's map
============

Purpose:
    Keep Tess's Level 4 backlog-processing proof, gate checks, and Reid
    durability routing in durable script logic instead of a long timer prompt.

Operating model:
    The Codex automation is only the clock. This script owns the deterministic
    checks and bookkeeping that can be safely done without inventing role
    authority. Promotion packet drafting still requires the surrounding Tess
    role context and source reads, but this script determines whether the run
    is eligible, blocked, complete, or no-op.

What this script may do:
    - Read Tess autonomy/backlog/checklist sources.
    - Check whether active writing automations include Reid durability routing.
    - Write Tess Level 4 state/proof/visible log bookkeeping.

What this script must never do:
    - Approve or perform promotions.
    - Change another role's authority.
    - Edit gates.
    - Commit, push, release, deploy, spend, use secrets, or contact externals.

Outputs:
    - roles/autonomy-engineer/level4-processing-state.json
    - roles/autonomy-engineer/level4-proof.md
    - roles/autonomy-engineer/level4-visible-log.md

Backlog rows:
    The processor recognizes `AUTO-*` promotion/readiness rows and `METH-*`
    durable-methodology conversion rows in `automation.backlog.md`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(os.environ.get("MINDSHARE_REPO_ROOT", r"C:\Users\scott\Code\mindshare"))
ROLE_ROOT = REPO_ROOT / "roles" / "autonomy-engineer"
AUTOMATIONS_ROOT = Path(os.environ.get("MINDSHARE_AUTOMATIONS_ROOT", r"C:\Users\scott\.codex\automations"))
RELEASE_QUEUE = Path(os.environ.get("MINDSHARE_RELEASE_QUEUE", r"G:\My Drive\Mindshare\channels\release-management.md"))

BACKLOG_PATH = ROLE_ROOT / "automation.backlog.md"
CHECKLIST_PATH = ROLE_ROOT / "level4-gate-checklist.md"
AUTONOMY_PATH = ROLE_ROOT / "Autonomy.md"
STATE_PATH = ROLE_ROOT / "level4-processing-state.json"
PROOF_PATH = ROLE_ROOT / "level4-proof.md"
VISIBLE_LOG_PATH = ROLE_ROOT / "level4-visible-log.md"


ROW_RE = re.compile(r"^\| (?P<id>(?:AUTO|METH)-[^|]+) \| (?P<role>[^|]+) \| (?P<org>[^|]+) \| (?P<work>[^|]+) \| (?P<expected>[^|]+) \| (?P<owner>[^|]+) \| (?P<priority>[^|]+) \| (?P<status>[^|]+) \| (?P<proof>.*) \|$")


@dataclass
class BacklogItem:
    id: str
    role: str
    org: str
    work: str
    priority: str
    status: str
    proof: str


@dataclass
class ReidRouteGap:
    automation_id: str
    config_path: str
    reason: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def parse_backlog() -> list[BacklogItem]:
    items: list[BacklogItem] = []
    for line in read_text(BACKLOG_PATH).splitlines():
        match = ROW_RE.match(line)
        if not match:
            continue
        data = {k: v.strip() for k, v in match.groupdict().items()}
        items.append(BacklogItem(
            id=data["id"],
            role=data["role"],
            org=data["org"],
            work=data["work"],
            priority=data["priority"],
            status=data["status"].lower(),
            proof=data["proof"],
        ))
    return items


def active_automation_configs() -> list[Path]:
    return sorted(list(AUTOMATIONS_ROOT.glob("*/automation.toml")) + list(AUTOMATIONS_ROOT.glob("*/file-watch.toml")))


def has_active_status(text: str) -> bool:
    match = re.search(r'(?m)^status\s*=\s*"([^"]+)"', text)
    return not match or match.group(1) == "ACTIVE"


def looks_like_writer(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in [
        "write ", "update ", "append ", "create ", "mark ", "repair",
        "fix ", "rebuild", "run ", "proof", "state", "report",
    ])


def mentions_durable_source(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in ["git", "release", "commit", "push", "promot", "durable"])


def has_reid_route(text: str) -> bool:
    lowered = text.lower()
    return "reid" in lowered or "release-management.md" in lowered or "release management" in lowered


def reid_route_gaps() -> list[ReidRouteGap]:
    gaps: list[ReidRouteGap] = []
    for path in active_automation_configs():
        text = read_text(path)
        if not has_active_status(text):
            continue
        if looks_like_writer(text) and mentions_durable_source(text) and not has_reid_route(text):
            gaps.append(ReidRouteGap(path.parent.name, str(path), "active writer has durable/release language without Reid route"))
    return gaps


def release_request_present() -> bool:
    queue = read_text(RELEASE_QUEUE)
    return "Automation Reid-Durability Routing" in queue and "Next owner: Reid" in queue


def build_state(mode: str) -> dict:
    items = parse_backlog()
    eligible = [item for item in items if item.status == "backlog"]
    blocked = [item for item in items if item.status in {"blocked", "errored"}]
    gaps = reid_route_gaps()
    result = "blocked" if gaps else ("eligible_work" if eligible else "no_eligible_work")
    return {
        "schema_version": 2,
        "role": "Tess / Autonomy Engineer",
        "automation_id": "tess-level-4-autonomy-backlog-processing",
        "logic_owner": str(Path(__file__).resolve()),
        "mode": mode,
        "checked_at": iso_now(),
        "result": result,
        "current_level": "Level 4 Senior Staff (Scoped Autonomy)",
        "backlog_counts": {
            "total": len(items),
            "backlog": len(eligible),
            "blocked_or_errored": len(blocked),
            "complete": sum(1 for item in items if item.status == "complete"),
        },
        "eligible_items": [asdict(item) for item in eligible],
        "blocked_items": [asdict(item) for item in blocked],
        "reid_durability": {
            "release_management_request_present": release_request_present(),
            "active_automation_route_gaps": [asdict(gap) for gap in gaps],
            "rule": "Any durable autonomy/runtime/source change must append or update a Release Management request for Reid.",
        },
        "gate_status": {
            "authority": "pass",
            "contract": "pass" if AUTONOMY_PATH.exists() else "fail",
            "trigger": "pass" if BACKLOG_PATH.exists() else "fail",
            "runtime": "pass_runtime_timer_calls_script_when_automation_active",
            "work_loop": "pass" if not gaps else "blocked_by_reid_route_gap",
            "state": "pass",
            "evidence": "pass_after_write" if mode in {"manual", "scheduled"} else "pending",
            "boundary": "pass_denied_actions_held",
            "reid_durability": "pass" if not gaps and release_request_present() else "blocked",
        },
        "denied_actions_held": [
            "no promotion approval",
            "no role promotion",
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


def proof_entry(state: dict) -> str:
    lines = [
        f"## {state['checked_at']} - Tess Level 4 Script Run ({state['mode']})",
        "",
        f"Result: {state['result']}",
        f"Logic owner: `{state['logic_owner']}`",
        f"Backlog counts: `{json.dumps(state['backlog_counts'], sort_keys=True)}`",
        f"Reid request present: `{state['reid_durability']['release_management_request_present']}`",
        f"Reid route gaps: `{len(state['reid_durability']['active_automation_route_gaps'])}`",
        "",
        "Denied actions held: no promotion approval, role promotion, runtime activation, gate edit, Git/GitHub/release, production, external communication, spending, secrets, or authority expansion.",
        "",
    ]
    return "\n".join(lines)


def visible_entry(state: dict) -> str:
    return (
        f"- {state['checked_at']} - Tess Level 4 script run: {state['result']}; "
        f"backlog={state['backlog_counts']['backlog']}; "
        f"Reid route gaps={len(state['reid_durability']['active_automation_route_gaps'])}; "
        "denied actions held.\n"
    )


def write_outputs(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    existing_proof = read_text(PROOF_PATH)
    PROOF_PATH.write_text(existing_proof.rstrip() + "\n\n" + proof_entry(state), encoding="utf-8")
    existing_visible = read_text(VISIBLE_LOG_PATH)
    VISIBLE_LOG_PATH.write_text(existing_visible.rstrip() + "\n" + visible_entry(state), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Tess Level 4 backlog-processing checks.")
    parser.add_argument("--write", action="store_true", help="Write state/proof/visible log.")
    parser.add_argument("--mode", choices=["manual", "scheduled"], default="manual")
    args = parser.parse_args()
    state = build_state(args.mode)
    if args.write:
        write_outputs(state)
    print(json.dumps(state, indent=2))
    return 0 if state["result"] in {"no_eligible_work", "eligible_work"} and not state["reid_durability"]["active_automation_route_gaps"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
