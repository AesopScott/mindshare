#!/usr/bin/env python3
"""Lane Level 4 token-reporting automation checks.

Purpose:
    Keep deterministic token-reporting checks in a readable role-local script.
    The hourly Codex heartbeat remains the live context worker for app-visible
    reporting and any missing usage-row collection that requires current thread
    context.

The script owns:
    - Token log schema validation.
    - Previous-complete-hour coverage detection.
    - HTML report rebuild through the existing PowerShell builder.
    - State/proof writes and boundary bookkeeping.

The script never commits, releases, contacts external services, reads secrets,
activates runtime, promotes Lane, or expands authority.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


ROLE_ROOT = Path(r"C:\Users\scott\Code\mojo\roles\lab-operator")
AUTONOMY_PATH = ROLE_ROOT / "Autonomy.md"
TOKEN_LOG_PATH = ROLE_ROOT / "token usage.md"
HTML_PATH = ROLE_ROOT / "token-usage.html"
BUILDER_PATH = ROLE_ROOT / "build-token-usage.ps1"
STATE_PATH = ROLE_ROOT / "level4-token-usage-state.json"
PROOF_PATH = ROLE_ROOT / "level4-token-usage-proof.md"
LOCAL_TZ = ZoneInfo("America/Denver")
EXPECTED_COLUMNS = [
    "logged_at_mdt", "window_start_mdt", "window_end_mdt", "interface",
    "room_or_session", "room_title_or_cwd", "input_tokens", "output_tokens",
    "cache_create_tokens", "cache_read_tokens", "total_tokens", "confidence", "notes",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def iso_now() -> str:
    return datetime.now(LOCAL_TZ).isoformat(timespec="seconds")


def parse_dt(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(tzinfo=LOCAL_TZ)


def previous_complete_hour(now: datetime) -> tuple[datetime, datetime]:
    end = now.replace(minute=0, second=0, microsecond=0)
    start = end - timedelta(hours=1)
    return start, end


def parse_token_log() -> tuple[list[dict], list[str]]:
    errors: list[str] = []
    rows: list[dict] = []
    text = read_text(TOKEN_LOG_PATH)
    if not text:
        return rows, [f"Missing or empty token log: {TOKEN_LOG_PATH}"]

    header_seen = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells:
            continue
        if cells[0] == "logged_at_mdt":
            header_seen = True
            if cells[: len(EXPECTED_COLUMNS)] != EXPECTED_COLUMNS:
                errors.append(f"Header columns do not match expected schema at line {line_number}.")
            continue
        if cells[0].startswith("---"):
            continue
        if len(cells) < len(EXPECTED_COLUMNS):
            errors.append(f"Line {line_number} has {len(cells)} cells; expected {len(EXPECTED_COLUMNS)}.")
            continue
        try:
            row = dict(zip(EXPECTED_COLUMNS, cells[: len(EXPECTED_COLUMNS)]))
            row["line"] = line_number
            row["logged_at"] = parse_dt(row["logged_at_mdt"])
            row["window_start"] = parse_dt(row["window_start_mdt"])
            row["window_end"] = parse_dt(row["window_end_mdt"])
            for key in ["input_tokens", "output_tokens", "cache_create_tokens", "cache_read_tokens", "total_tokens"]:
                row[key] = int(row[key])
            rows.append(row)
        except Exception as exc:  # noqa: BLE001 - proof should record exact parse failure.
            errors.append(f"Line {line_number} failed to parse: {exc}")
    if not header_seen:
        errors.append("Token log header row was not found.")
    return rows, errors


def rebuild_html() -> dict:
    if not BUILDER_PATH.exists():
        return {"status": "failed", "reason": f"Missing builder: {BUILDER_PATH}"}
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(BUILDER_PATH)],
        cwd=str(ROLE_ROOT),
        text=True,
        capture_output=True,
        timeout=120,
    )
    return {
        "status": "pass" if completed.returncode == 0 else "failed",
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-1000:],
        "stderr_tail": completed.stderr[-1000:],
    }


def build_state(mode: str, do_rebuild: bool) -> dict:
    now = datetime.now(LOCAL_TZ)
    window_start, window_end = previous_complete_hour(now)
    rows, errors = parse_token_log()
    matching_rows = [row for row in rows if row["window_start"] == window_start and row["window_end"] == window_end]
    confidence_counts = Counter(str(row["confidence"]) for row in rows)
    latest_row = max(rows, key=lambda row: row["logged_at"], default=None)
    html_before = HTML_PATH.stat().st_mtime if HTML_PATH.exists() else None
    rebuild_result = rebuild_html() if do_rebuild else {"status": "skipped"}
    html_after = HTML_PATH.stat().st_mtime if HTML_PATH.exists() else None
    html_changed = html_before != html_after

    if errors:
        result = "error_token_log_invalid"
    elif not matching_rows:
        result = "eligible_work_missing_previous_hour_rows"
    else:
        result = "no_eligible_work_previous_hour_logged"

    return {
        "schema_version": 1,
        "role": "Lane / Mojo Lab Operator",
        "automation_id": "lane-hourly-token-usage-update",
        "logic_owner": str(Path(__file__).resolve()),
        "mode": mode,
        "checked_at": iso_now(),
        "current_policy": "Level 3 token-usage reporting with proposed Level 4 script/timer separation",
        "result": result,
        "window": {
            "start_mdt": window_start.strftime("%Y-%m-%d %H:%M:%S"),
            "end_mdt": window_end.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "counts": {
            "token_rows": len(rows),
            "previous_hour_rows": len(matching_rows),
            "parse_errors": len(errors),
            "confidence_kinds": len(confidence_counts),
        },
        "latest_row": {
            "logged_at_mdt": latest_row["logged_at_mdt"],
            "window_start_mdt": latest_row["window_start_mdt"],
            "window_end_mdt": latest_row["window_end_mdt"],
            "interface": latest_row["interface"],
            "confidence": latest_row["confidence"],
        } if latest_row else None,
        "confidence_counts": dict(sorted(confidence_counts.items())),
        "errors": errors,
        "html_rebuild": rebuild_result,
        "html_changed": html_changed,
        "sources": {
            "autonomy": str(AUTONOMY_PATH),
            "token_log": str(TOKEN_LOG_PATH),
            "html": str(HTML_PATH),
            "builder": str(BUILDER_PATH),
        },
        "gate_status": {
            "contract": "pass" if AUTONOMY_PATH.exists() else "fail",
            "token_log": "pass" if TOKEN_LOG_PATH.exists() and not errors else "fail",
            "html_builder": rebuild_result["status"] if do_rebuild else "skipped",
            "state": "pass_after_write" if mode in {"manual", "scheduled"} else "pending",
            "boundary": "pass_denied_actions_held",
        },
        "denied_actions_held": [
            "no Git/GitHub/release action",
            "no production",
            "no external service contact",
            "no spending",
            "no secrets",
            "no deletes or moves",
            "no authority expansion",
            "no runtime activation",
            "no Level 4 promotion",
        ],
    }


def proof_entry(state: dict) -> str:
    return "\n".join([
        f"## {state['checked_at']} - Lane Token Usage Script Run ({state['mode']})",
        "",
        f"Result: {state['result']}",
        f"Logic owner: `{state['logic_owner']}`",
        f"Window: `{state['window']['start_mdt']} - {state['window']['end_mdt']}`",
        f"Counts: `{json.dumps(state['counts'], sort_keys=True)}`",
        f"HTML rebuild: `{state['html_rebuild']['status']}`",
        f"HTML changed: `{state['html_changed']}`",
        "",
        "Denied actions held: no Git/GitHub/release, production, external service contact, spending, secrets, deletes/moves, authority expansion, runtime activation, or Level 4 promotion.",
        "",
    ])


def write_outputs(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    existing = read_text(PROOF_PATH)
    PROOF_PATH.write_text(existing.rstrip() + "\n\n" + proof_entry(state), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Lane Level 4 token-reporting checks.")
    parser.add_argument("--write", action="store_true", help="Write state/proof files.")
    parser.add_argument("--mode", choices=["manual", "scheduled"], default="manual")
    parser.add_argument("--rebuild-html", action="store_true", help="Run the existing HTML builder script.")
    args = parser.parse_args()
    state = build_state(args.mode, args.rebuild_html)
    if args.write:
        write_outputs(state)
    print(json.dumps(state, indent=2))
    return 0 if state["result"] in {"no_eligible_work_previous_hour_logged", "eligible_work_missing_previous_hour_rows"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
