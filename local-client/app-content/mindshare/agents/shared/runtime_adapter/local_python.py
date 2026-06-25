"""
Local Python runtime adapter proof harness.

Loads canonical autonomy sources, validates the autonomy contract, classifies a
requested action, blocks denied domains, and writes state/audit proof. It does
not execute shell commands, mutate target files, activate runtime, or grant
authority.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from agents.shared.autonomy_contract_validator import validate_contract
from agents.shared.autonomy_source_loader import load_autonomy_sources


DENIED_DOMAIN_PATTERNS = {
    "git_or_release": (
        "git ",
        "commit",
        "push",
        "branch",
        "pull request",
        " pr ",
        "merge",
        "release",
        "promote",
        "tag",
    ),
    "production": ("production", "deploy", "publish live"),
    "external_communication": ("external", "email", "send message", "contact customer"),
    "spending": ("spend", "buy", "purchase", "billing", "budget"),
    "secrets": ("secret", "credential", "api key", "token"),
    "authority_expansion": ("grant authority", "expand authority", "promote", "activate"),
    "runtime_activation": ("activate runtime", "autonomous runtime", "schedule yourself", "cron"),
}


@dataclass(frozen=True)
class RuntimeRequest:
    """Runtime-neutral request for an autonomy action decision."""

    role_root: str
    agent_root: Optional[str]
    intent: str
    actor: str
    state_dir: str
    require_canonical: bool = True


@dataclass
class AdapterDecision:
    """Decision and proof emitted by the local runtime adapter."""

    allowed: bool
    status: str
    reason: str
    denied_domains: List[str] = field(default_factory=list)
    source_summary: Dict[str, Any] = field(default_factory=dict)
    validation: Dict[str, Any] = field(default_factory=dict)
    state_path: Optional[str] = None
    audit_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LocalPythonRuntimeAdapter:
    """
    Proof adapter for local autonomy decisions.

    The adapter is intentionally conservative. Missing source, failing contract
    validation, denied action domains, or missing state target all fail closed.
    """

    def decide(self, request: RuntimeRequest) -> AdapterDecision:
        state_dir = Path(request.state_dir)
        if not request.state_dir:
            return AdapterDecision(
                allowed=False,
                status="blocked",
                reason="Missing state_dir; adapter requires explicit state/audit target.",
            )

        try:
            source = load_autonomy_sources(
                request.role_root,
                request.agent_root,
                require_canonical=request.require_canonical,
            )
        except Exception as exc:  # fail closed for all source-load failures
            decision = AdapterDecision(
                allowed=False,
                status="blocked",
                reason=f"Source load failed closed: {exc}",
            )
            self._write_proof(state_dir, request, decision)
            return decision

        source_dict = source.to_dict()
        autonomy_path = source.canonical_autonomy_path
        if not autonomy_path:
            decision = AdapterDecision(
                allowed=False,
                status="blocked",
                reason="Canonical Autonomy.md missing.",
                source_summary=source_dict,
            )
            self._write_proof(state_dir, request, decision)
            return decision

        autonomy_text = Path(autonomy_path).read_text(encoding="utf-8")
        validation = validate_contract(autonomy_text).to_dict()
        if not validation["ok"]:
            decision = AdapterDecision(
                allowed=False,
                status="blocked",
                reason="Autonomy contract validation failed.",
                source_summary=source_dict,
                validation=validation,
            )
            self._write_proof(state_dir, request, decision)
            return decision

        denied_domains = self._detect_denied_domains(request.intent)
        if denied_domains:
            decision = AdapterDecision(
                allowed=False,
                status="denied",
                reason="Intent touches denied or approval-gated domain.",
                denied_domains=denied_domains,
                source_summary=source_dict,
                validation=validation,
            )
            self._write_proof(state_dir, request, decision)
            return decision

        decision = AdapterDecision(
            allowed=True,
            status="allowed_for_planning_only",
            reason="No denied domain detected; adapter allows planning proof only, not execution.",
            source_summary=source_dict,
            validation=validation,
        )
        self._write_proof(state_dir, request, decision)
        return decision

    def _detect_denied_domains(self, intent: str) -> List[str]:
        text = f" {self._normalize(intent)} "
        denied: List[str] = []
        for domain, patterns in DENIED_DOMAIN_PATTERNS.items():
            if self._has_any(text, patterns):
                denied.append(domain)
        return denied

    def _write_proof(
        self,
        state_dir: Path,
        request: RuntimeRequest,
        decision: AdapterDecision,
    ) -> None:
        state_dir.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc).isoformat()

        state_path = state_dir / "state.json"
        audit_path = state_dir / "audit.jsonl"

        state = {
            "schema": "local-python-runtime-adapter-proof",
            "updated_at": now,
            "actor": request.actor,
            "role_root": request.role_root,
            "agent_root": request.agent_root,
            "intent": request.intent,
            "decision": {
                "allowed": decision.allowed,
                "status": decision.status,
                "reason": decision.reason,
                "denied_domains": decision.denied_domains,
            },
            "authority_boundary": "Runtime state is evidence only; it does not grant authority or activate runtime.",
        }
        state_path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")

        audit_entry = {
            "timestamp": now,
            "actor": request.actor,
            "intent": request.intent,
            "decision": decision.to_dict(),
            "authority_boundary": "Audit is proof only; no action executed.",
        }
        with audit_path.open("a", encoding="utf-8") as audit:
            audit.write(json.dumps(audit_entry, sort_keys=True) + "\n")

        decision.state_path = str(state_path)
        decision.audit_path = str(audit_path)

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"\s+", " ", (text or "").lower()).strip()

    @staticmethod
    def _has_any(text: str, needles: Iterable[str]) -> bool:
        return any(needle in text for needle in needles)
