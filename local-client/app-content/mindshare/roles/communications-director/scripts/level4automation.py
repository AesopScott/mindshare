#!/usr/bin/env python3
"""Mae Level 4 automation health check.

Purpose:
    Put Mae's deterministic automation-health checks in a durable script so the
    heartbeat is only the timer, live thread checker, and exception router.

This script checks local automation config, watched paths, state files, packet
evidence, resume errors, and Reid durability routing. It does not modify
automation configs, create/delete/pause automations, change target threads,
commit, push, release, deploy, spend, use secrets, or expand authority.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


AUTOMATIONS_ROOT = Path(r"C:\Users\scott\.codex\automations")
ROLE_ROOT = Path(r"C:\Users\scott\Code\mindshare\roles\communications-director")
STATE_PATH = ROLE_ROOT / "level4-automation-health-state.json"
PROOF_PATH = ROLE_ROOT / "level4-proof.md"
RELEASE_QUEUE = Path(r"G:\My Drive\Mindshare\channels\release-management.md")


@dataclass
class AutomationResult:
    automation_id: str
    config_path: str
    kind: str
    status: str
    target_thread_id: str
    watched_count: int
    missing_watched_paths: list[str]
    watch_state_exists: bool
    hard_error_marker: bool
    output_size: int | None
    pending_packet: bool
    reid_route_present: bool
    severity: str
    findings: list[str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def toml_value(text: str, key: str) -> str:
    match = re.search(rf'(?m)^{re.escape(key)}\s*=\s*"([^"]*)"', text)
    return match.group(1) if match else ""


def watched_paths(text: str) -> list[str]:
    match = re.search(r"watched_paths\s*=\s*\[(.*?)\]", text, re.S)
    if not match:
        return []
    return re.findall(r'"([^"]+)"', match.group(1))


def has_reid_route(text: str) -> bool:
    lowered = text.lower()
    return "reid" in lowered or "release-management.md" in lowered or "release management" in lowered


def has_hard_error(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in [
        "thread/resume failed",
        "failed to read thread",
        "is archived",
        "corrupted",
        "does not start with session metadata",
    ])


def check_config(path: Path) -> AutomationResult:
    text = read_text(path)
    aid = toml_value(text, "automation_id") or toml_value(text, "id") or path.parent.name
    status = toml_value(text, "status") or "UNKNOWN"
    kind = toml_value(text, "kind") or path.name
    target = toml_value(text, "target_thread_id")
    paths = watched_paths(text)
    missing = [p for p in paths if not Path(p).exists()]
    watch_state_name = toml_value(text, "watch_state_path") or "watch_state.json"
    watch_state = path.parent / watch_state_name
    last_error = path.parent / "last-resume-error.txt"
    last_output = path.parent / "last-resume-output.txt"
    pending = (path.parent / "pending-change-packet.json").exists() or (path.parent / "pending-change-packet.md").exists()
    findings: list[str] = []
    if status == "ACTIVE" and path.name == "file-watch.toml":
        if not target:
            findings.append("missing target_thread_id")
        if missing:
            findings.append(f"missing watched paths: {len(missing)}")
        if not watch_state.exists():
            findings.append("missing watch_state")
        if last_error.exists() and has_hard_error(read_text(last_error)):
            findings.append("hard resume error marker present")
    output_size = last_output.stat().st_size if last_output.exists() else None
    hard_error = last_error.exists() and has_hard_error(read_text(last_error))
    reid = has_reid_route(text)
    if status == "ACTIVE" and not reid and any(word in text.lower() for word in ["write", "update", "repair", "commit", "push", "release", "promot"]):
        findings.append("missing Reid durability route")
    severity = "pass"
    if any("hard resume" in f or "missing target" in f or "missing Reid" in f for f in findings):
        severity = "critical"
    elif findings:
        severity = "warning"
    return AutomationResult(
        automation_id=aid,
        config_path=str(path),
        kind=kind,
        status=status,
        target_thread_id=target,
        watched_count=len(paths),
        missing_watched_paths=missing,
        watch_state_exists=watch_state.exists(),
        hard_error_marker=hard_error,
        output_size=output_size,
        pending_packet=pending,
        reid_route_present=reid,
        severity=severity,
        findings=findings,
    )


def active_configs() -> list[Path]:
    configs = sorted(list(AUTOMATIONS_ROOT.glob("*/file-watch.toml")) + list(AUTOMATIONS_ROOT.glob("*/automation.toml")))
    return [p for p in configs if toml_value(read_text(p), "status") == "ACTIVE"]


def release_request_present() -> bool:
    queue = read_text(RELEASE_QUEUE)
    return "Automation Reid-Durability Routing" in queue and "Next owner: Reid" in queue


def build_state(mode: str) -> dict:
    results = [check_config(path) for path in active_configs()]
    critical = [r for r in results if r.severity == "critical"]
    warning = [r for r in results if r.severity == "warning"]
    result = "fail" if critical else ("warn" if warning else "pass")
    return {
        "schema_version": 2,
        "role": "Mae / Communications Director",
        "automation_id": "mae-automation-health-check",
        "logic_owner": str(Path(__file__).resolve()),
        "mode": mode,
        "checked_at": iso_now(),
        "autonomy_level": 4,
        "stage": "Senior Staff (Scoped Autonomy)",
        "status": "operational" if result == "pass" else "operational_with_findings",
        "result": result,
        "counts": {
            "active_configs_checked": len(results),
            "critical": len(critical),
            "warning": len(warning),
            "pass": sum(1 for r in results if r.severity == "pass"),
        },
        "release_management_request_present": release_request_present(),
        "results": [asdict(r) for r in results],
        "denied_actions_held": [
            "no role authority changes",
            "no lifecycle changes",
            "no autonomy promotion",
            "no cadence or target-thread change",
            "no new/deleted/paused automation",
            "no runner code changes",
            "no gate edits",
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
        f"## {state['checked_at']} - Mae Automation Health Script Run ({state['mode']})",
        "",
        f"Result: {state['result']}",
        f"Logic owner: `{state['logic_owner']}`",
        f"Counts: `{json.dumps(state['counts'], sort_keys=True)}`",
        f"Reid durability request present: `{state['release_management_request_present']}`",
        "",
    ]
    for item in state["results"]:
        if item["severity"] != "pass":
            lines.append(f"- {item['severity']} / {item['automation_id']}: {', '.join(item['findings'])}")
    lines.append("")
    lines.append("Denied actions held: no authority/lifecycle/autonomy/cadence/target-thread/new-runtime/gate/Git/release/production/external/spending/secrets expansion.")
    lines.append("")
    return "\n".join(lines)


def write_outputs(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    existing = read_text(PROOF_PATH)
    PROOF_PATH.write_text(existing.rstrip() + "\n\n" + proof_entry(state), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Mae automation health deterministic checks.")
    parser.add_argument("--write", action="store_true", help="Write state/proof files.")
    parser.add_argument("--mode", choices=["manual", "scheduled"], default="manual")
    args = parser.parse_args()
    state = build_state(args.mode)
    if args.write:
        write_outputs(state)
    print(json.dumps(state, indent=2))
    return 0 if state["result"] in {"pass", "warn"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
