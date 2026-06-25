"""
Strict-intent gate for exact-operation approval of sensitive file edits.

Validates approval packets for control-plane, gate-policy, release-git,
state-audit, workflow-loop, and memory files. Blocks unrelated changes,
stale approvals, missing approvers, and unauthorized paths.

Does not edit files or run git. Returns approval/denial decision with audit entry.
Uses stdlib only.
"""

import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Set, Any, Tuple

from agents.shared.autonomy_source_loader import load_autonomy_sources
from agents.shared.autonomy_contract_validator import ContractValidator


class GateError(Exception):
    """Raised when gate validation fails."""
    pass


class SensitivePathError(Exception):
    """Raised when sensitive path classification fails."""
    pass


@dataclass
class DiffHunk:
    """Single hunk in a diff."""
    hunk_id: str
    original_lines: str
    new_lines: str
    rationale: str


@dataclass
class ApprovalRequest:
    """Approval request for exact-operation edit."""
    id: str
    timestamp: str
    requester: str
    target_file: str
    target_class: str
    intent: str
    reason: str
    diff_hunks: List[DiffHunk]
    scope_boundary: Dict[str, Any]
    approval_routing: Dict[str, Any]
    proof: Dict[str, Any]
    expiry: Dict[str, Any]


@dataclass
class ApprovalDecision:
    """Result of approval gate."""
    approved: bool
    reason: str
    audit_entry: Dict[str, Any] = field(default_factory=dict)


class StrictIntentGate:
    """Gate for exact-operation approval of sensitive edits."""

    SENSITIVE_PATH_CLASSES = {
        'control-plane': {
            'patterns': [
                r'roles/.*/Autonomy\.md',
                r'roles/.*/role-agent\.md',
                r'roles/.*/agent-profile\.md',
                r'agents/.*/agent-design\.md',
                r'agents/shared/autonomy_contract_validator\.py',
                r'agents/shared/autonomy_source_loader\.py',
                r'agents/shared/strict_intent_gate\.py',
                r'agents/shared/runtime_adapter\.py',
                r'roles/autonomy-engineer/.*\.py',
                r'roles/autonomy-engineer/.*\.schema\.json',
                r'roles/autonomy-engineer/.*-policy\.md',
            ],
            'primary_approver': 'Scott',
            'secondary_approvers': ['Vik'],
            'required_consensus': 'unanimous',
        },
        'gate-policy': {
            'patterns': [
                r'roles/.*/gate\.md',
                r'roles/autonomy-engineer/gate-.*\.md',
                r'agents/.*/gate.*\.py',
                r'.*/gate-policy\.json',
                r'.*/approval-gates\.json',
            ],
            'primary_approver': 'Scott',
            'secondary_approvers': ['Vik'],
            'required_consensus': 'unanimous',
        },
        'release-git': {
            'patterns': [
                r'\.git/.*',
                r'\.github/.*',
                r'\.github/workflows/.*',
                r'roles/release-manager/.*',
                r'scripts/release.*\.py',
                r'scripts/publish.*\.py',
                r'scripts/deploy.*\.py',
                r'.*/pre-commit/.*',
                r'.*/git-hooks/.*',
                r'Makefile',
                r'pyproject\.toml',
            ],
            'primary_approver': 'Reid',
            'secondary_approvers': ['Scott'],
            'required_consensus': 'unanimous',
        },
        'state-audit': {
            'patterns': [
                r'roles/.*/state\.json',
                r'agents/.*/state\.json',
                r'roles/.*/audit\.jsonl',
                r'agents/.*/audit\.jsonl',
                r'roles/autonomy-engineer/audit\.jsonl',
            ],
            'primary_approver': 'Tess',
            'secondary_approvers': ['Scott'],
            'required_consensus': 'unanimous',
        },
        'workflow-loop': {
            'patterns': [
                r'roles/.*/workflow\.md',
                r'roles/.*/loop\.md',
                r'agents/.*/workflow\.md',
                r'agents/.*/loop\.md',
                r'agents/.*/cadence\.json',
            ],
            'primary_approver': 'Vik',
            'secondary_approvers': ['Scott'],
            'required_consensus': 'unanimous',
        },
        'memory': {
            'patterns': [
                r'roles/.*/memory\.md',
                r'agents/.*/memory\.md',
                r'agents/.*/personality\.md',
                r'roles/.*/name\.md',
                r'agents/.*/name\.md',
            ],
            'primary_approver': None,
            'secondary_approvers': ['Scott'],
            'required_consensus': 'unanimous',
        },
    }

    DENIED_DIFF_PATTERNS = [
        r'^\s*-\s+\w',
        r'(?:can|may|will)\s+(?:automatically|autonomously)',
        r'(?:auto|self)\s*(?:act|execute|decide|approve)',
        r'control[_-]?flow',
        r'\bif\s+\w+.*:',
        r'\belse\s*:',
        r'(?:import|from).*(?:import)',
        r'(?:require)\s*\(',
    ]

    def __init__(self):
        self.compiled_denied_patterns = [
            re.compile(p, re.IGNORECASE | re.MULTILINE)
            for p in self.DENIED_DIFF_PATTERNS
        ]
        self.contract_validator = ContractValidator()

    def classify_sensitive_path(self, file_path: str) -> Optional[str]:
        """
        Classify file as sensitive and return class name.
        Returns None if not sensitive.
        """
        for class_name, config in self.SENSITIVE_PATH_CLASSES.items():
            for pattern in config['patterns']:
                pattern_re = re.compile(pattern, re.IGNORECASE)
                if pattern_re.search(file_path):
                    return class_name
        return None

    def verify_approval(
        self,
        request: ApprovalRequest,
        current_time: Optional[str] = None,
        source_content: Optional[str] = None,
    ) -> ApprovalDecision:
        """
        Verify approval request and return decision.

        Args:
            request: ApprovalRequest to verify
            current_time: Override current time for testing (ISO 8601 string)
            source_content: Pre-loaded source content (for testing)

        Returns:
            ApprovalDecision with approved flag and audit entry
        """
        if current_time is None:
            current_time = datetime.utcnow().isoformat() + 'Z'

        audit = {
            'timestamp': current_time,
            'event': 'strict_intent_verified',
            'request_id': request.id,
            'target_file': request.target_file,
            'target_class': request.target_class,
            'intent': request.intent,
            'actor': request.requester,
            'decision': None,
            'reason': '',
            'proof': {},
        }

        try:
            # 1. Validate request structure
            self._validate_request_structure(request)

            # 2. Classify sensitive path
            classified_class = self.classify_sensitive_path(request.target_file)
            if not classified_class:
                return ApprovalDecision(
                    approved=False,
                    reason=f"File {request.target_file} is not in a sensitive class",
                    audit_entry=audit,
                )

            if classified_class != request.target_class:
                return ApprovalDecision(
                    approved=False,
                    reason=f"Target class mismatch: request says {request.target_class}, "
                            f"but file maps to {classified_class}",
                    audit_entry=audit,
                )

            # 3. Validate intent field
            self._validate_intent(request.intent)

            # 4. Load and validate source
            source_result = source_content or self._load_source(request.target_file)
            audit['proof']['source_loader_ok'] = bool(source_result)
            if not source_result:
                audit['decision'] = 'denied'
                audit['reason'] = 'Source validation failed'
                return ApprovalDecision(
                    approved=False,
                    reason='Source validation failed',
                    audit_entry=audit,
                )

            # 5. Validate contract
            contract_result = self._validate_contract(source_result)
            audit['proof']['contract_validator_ok'] = contract_result.ok
            if not contract_result.ok:
                audit['decision'] = 'denied'
                audit['reason'] = f"Contract validation failed: {contract_result.errors}"
                return ApprovalDecision(
                    approved=False,
                    reason=f"Contract validation failed: {', '.join(contract_result.errors)}",
                    audit_entry=audit,
                )

            # 6. Check expiry
            expiry_ok = self._check_expiry(request.expiry, current_time)
            if not expiry_ok:
                audit['decision'] = 'denied'
                audit['reason'] = f"Approval expired at {request.expiry.get('expires_at')}"
                return ApprovalDecision(
                    approved=False,
                    reason=f"Approval expired at {request.expiry.get('expires_at')}",
                    audit_entry=audit,
                )

            # 7. Check routing and approvers
            routing_ok, routing_reason = self._check_routing(
                request.target_class,
                request.approval_routing,
            )
            if not routing_ok:
                audit['decision'] = 'denied'
                audit['reason'] = routing_reason
                return ApprovalDecision(
                    approved=False,
                    reason=routing_reason,
                    audit_entry=audit,
                )

            # 8. Validate diff hunks
            diff_ok, diff_reason = self._validate_diff_hunks(request.diff_hunks)
            if not diff_ok:
                audit['decision'] = 'denied'
                audit['reason'] = diff_reason
                return ApprovalDecision(
                    approved=False,
                    reason=diff_reason,
                    audit_entry=audit,
                )

            # 9. Check approved hunks in scope boundary
            hunks_ok, hunks_reason = self._validate_scope_boundary(
                request.diff_hunks,
                request.scope_boundary,
            )
            if not hunks_ok:
                audit['decision'] = 'denied'
                audit['reason'] = hunks_reason
                return ApprovalDecision(
                    approved=False,
                    reason=hunks_reason,
                    audit_entry=audit,
                )

            # All checks passed
            audit['decision'] = 'approved'
            audit['proof']['scope_verified'] = True
            audit['proof']['no_adjacent_changes'] = True
            audit['proof']['all_approvers_present'] = True

            return ApprovalDecision(
                approved=True,
                reason='Approval granted',
                audit_entry=audit,
            )

        except Exception as e:
            audit['decision'] = 'denied'
            audit['reason'] = str(e)
            return ApprovalDecision(
                approved=False,
                reason=str(e),
                audit_entry=audit,
            )

    def _validate_request_structure(self, request: ApprovalRequest) -> None:
        """Validate approval request has required fields."""
        required = ['id', 'timestamp', 'requester', 'target_file', 'target_class',
                    'intent', 'diff_hunks', 'scope_boundary', 'approval_routing',
                    'proof', 'expiry']
        for field in required:
            if not getattr(request, field, None):
                raise GateError(f"Missing required field: {field}")

        if not isinstance(request.diff_hunks, list) or len(request.diff_hunks) == 0:
            raise GateError("diff_hunks must be non-empty list")

    def _validate_intent(self, intent: str) -> None:
        """Validate intent field."""
        if not intent:
            raise GateError("Intent required")

        if len(intent) < 10:
            raise GateError("Intent too short (min 10 chars)")

        intent_lower = intent.lower()

        if intent_lower.startswith('update '):
            raise GateError("Intent too vague: must specify what is being updated (e.g., 'Add', 'Change', 'Record'), not just 'Update'")

        vague_words = ['also', 'while we', 'adjacent', 'similar', 'and then']
        if any(w in intent_lower for w in vague_words):
            raise GateError("Intent suggests adjacent changes (not allowed)")

    def _load_source(self, target_file: str) -> Optional[str]:
        """Load source file content, fail closed if missing."""
        try:
            path = Path(target_file)
            if path.is_file():
                with open(target_file, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception:
            pass
        return None

    def _validate_contract(self, content: str) -> Any:
        """Validate contract content."""
        return self.contract_validator.validate(content)

    def _check_expiry(self, expiry: Dict[str, Any], current_time: str) -> bool:
        """Check if approval has expired."""
        approved_at_str = expiry.get('approved_at')
        ttl_seconds = expiry.get('ttl_seconds', 3600)

        if not approved_at_str:
            return False

        try:
            approved_at = datetime.fromisoformat(approved_at_str.replace('Z', '+00:00'))
            current = datetime.fromisoformat(current_time.replace('Z', '+00:00'))
            expires_at = approved_at + timedelta(seconds=ttl_seconds)

            return current <= expires_at
        except Exception:
            return False

    def _check_routing(
        self,
        target_class: str,
        approval_routing: Dict[str, Any],
    ) -> Tuple[bool, str]:
        """Check that required approvers are present and approved."""
        config = self.SENSITIVE_PATH_CLASSES.get(target_class)
        if not config:
            return False, f"Unknown target class: {target_class}"

        required_approvers = set()
        if config['primary_approver']:
            required_approvers.add(config['primary_approver'])
        required_approvers.update(config['secondary_approvers'])

        if not approval_routing.get('approved'):
            return False, "Approval not marked as approved"

        approver_sigs = approval_routing.get('approver_signatures', [])
        approved_by = set()
        for sig in approver_sigs:
            if sig.get('decision') == 'approved':
                approved_by.add(sig['approver'])

        missing = required_approvers - approved_by
        if missing:
            return False, f"Missing approval from: {', '.join(sorted(missing))}"

        return True, ''

    def _validate_diff_hunks(self, hunks: List[DiffHunk]) -> Tuple[bool, str]:
        """Validate individual hunks against denied patterns."""
        for hunk in hunks:
            # Check for deletions (denied by default)
            if hunk.new_lines == '' and hunk.original_lines != '':
                return False, f"Hunk {hunk.hunk_id}: Deletions require explicit approval"

            # Check for denied patterns
            combined = hunk.new_lines
            for pattern in self.compiled_denied_patterns:
                if pattern.search(combined):
                    return False, f"Hunk {hunk.hunk_id}: Denied pattern detected"

        return True, ''

    def _validate_scope_boundary(
        self,
        hunks: List[DiffHunk],
        scope_boundary: Dict[str, Any],
    ) -> Tuple[bool, str]:
        """Validate that all hunks are in approved scope."""
        approved_hunk_ids = set(scope_boundary.get('approved_hunks', []))
        unapproved = scope_boundary.get('unapproved_hunks_blocked', [])

        for hunk in hunks:
            if hunk.hunk_id not in approved_hunk_ids:
                return False, f"Hunk {hunk.hunk_id} not in approved scope"

        # Check that no unapproved hunks are listed
        for unapproved_id in unapproved:
            for hunk in hunks:
                if hunk.hunk_id == unapproved_id:
                    return False, f"Hunk {unapproved_id} is marked unapproved"

        # Check no_adjacent_changes flag
        if not scope_boundary.get('no_adjacent_changes', False):
            return False, "Unapproved adjacent changes detected"

        return True, ''


def verify_approval(
    request_dict: Dict[str, Any],
    current_time: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Public interface for approval verification.

    Args:
        request_dict: Approval request as dict
        current_time: Override current time for testing

    Returns:
        Dict with 'approved' bool and 'audit' entry
    """
    gate = StrictIntentGate()

    try:
        hunks = [DiffHunk(**h) for h in request_dict.get('diff_hunks', [])]
        request = ApprovalRequest(
            id=request_dict['id'],
            timestamp=request_dict['timestamp'],
            requester=request_dict['requester'],
            target_file=request_dict['target_file'],
            target_class=request_dict['target_class'],
            intent=request_dict['intent'],
            reason=request_dict.get('reason', ''),
            diff_hunks=hunks,
            scope_boundary=request_dict.get('scope_boundary', {}),
            approval_routing=request_dict.get('approval_routing', {}),
            proof=request_dict.get('proof', {}),
            expiry=request_dict.get('expiry', {}),
        )

        decision = gate.verify_approval(request, current_time)
        return {
            'approved': decision.approved,
            'reason': decision.reason,
            'audit': decision.audit_entry,
        }
    except Exception as e:
        return {
            'approved': False,
            'reason': f"Request validation failed: {str(e)}",
            'audit': {'error': str(e)},
        }
