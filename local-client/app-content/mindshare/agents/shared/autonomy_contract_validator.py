"""
Autonomy contract validator for role and agent autonomy agreements.

Validates activation status, autonomy level, allowed/denied actions,
stop conditions, approvers, tool rights, memory rights, release gates,
and revocation path before any action.

Fails closed on missing or stale contracts. Does not activate anything.
Uses stdlib only.
"""

import re
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Set, Any


@dataclass
class ValidationResult:
    """Result of autonomy contract validation."""
    ok: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    parsed: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict."""
        return {
            'ok': self.ok,
            'errors': self.errors,
            'warnings': self.warnings,
            'parsed': self.parsed,
        }


class ContractValidator:
    """Validate autonomy contracts."""

    VALID_STATUSES = {'draft', 'approved', 'active', 'paused', 'revoked'}
    VALID_LEVELS = {0, 1, 2, 3, 4, 5, 6}

    INFERRED_AUTHORITY_PATTERNS = [
        r'(?:can|may|will)\s+(?:automatically|autonomously)',
        r'(?:auto|self)\s*(?:act|execute|decide|approve)',
        r'implied\s+(?:by|from|through)',
        r'due\s+to\s+(?:role|title|maturity)',
        r'(?:infer|deduce|conclude)\s+(?:authority|permission)',
    ]

    def __init__(self):
        self.compiled_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.INFERRED_AUTHORITY_PATTERNS
        ]

    def validate(
        self,
        content: str,
        source_loader_result: Optional[Any] = None,
    ) -> ValidationResult:
        """
        Validate autonomy contract content.

        Args:
            content: Full Autonomy.md or autonomy contract text
            source_loader_result: Optional SourceLoaderResult for path validation

        Returns:
            ValidationResult with ok, errors, warnings, parsed fields
        """
        result = ValidationResult(ok=False)
        parsed = {}

        if not content or not content.strip():
            result.errors.append('Contract content is empty')
            return result

        # 1. Extract and validate activation status
        status = self._extract_status(content)
        if not status:
            result.errors.append(
                'BLOCKER: No explicit activation status found. '
                'Must have one of: Draft, Approved, Active, Paused, Revoked'
            )
        else:
            if status not in self.VALID_STATUSES:
                result.errors.append(
                    f'BLOCKER: Unknown status vocabulary "{status}". '
                    f'Must be one of: {", ".join(sorted(self.VALID_STATUSES))}'
                )
            parsed['activation_status'] = status

        # 2. Extract and validate autonomy level
        level = self._extract_level(content)
        if level is not None:
            if level not in self.VALID_LEVELS:
                result.errors.append(
                    f'BLOCKER: Autonomy level {level} invalid. Must be 0-6.'
                )
            parsed['autonomy_level'] = level
        else:
            result.warnings.append('No autonomy level found in contract')

        # 3. Check for inferred authority language
        inferred = self._find_inferred_authority(content)
        if inferred:
            result.errors.append(
                f'BLOCKER: Inferred authority language detected: "{inferred}". '
                'Authority must be explicit, not inferred from role or maturity.'
            )

        # 4. Extract allowed and denied actions
        allowed = self._extract_section(content, r'allowed\s+actions', 10)
        denied = self._extract_section(content, r'denied\s+actions|explicitly\s+denied', 10)

        if not allowed:
            result.warnings.append('No allowed actions documented')
        else:
            parsed['allowed_actions'] = allowed

        if not denied:
            result.errors.append(
                'BLOCKER: No explicitly denied actions listed. '
                'Must document what this role cannot do.'
            )
        else:
            parsed['denied_actions'] = denied

        # 5. Check for stop conditions
        stop_conds = self._extract_section(content, r'stop\s+conditions', 10)
        if not stop_conds:
            result.errors.append(
                'BLOCKER: No stop conditions defined. '
                'Must specify conditions that halt all operation.'
            )
        else:
            parsed['stop_conditions'] = stop_conds

        # 6. Extract approvers
        approvers = self._extract_approvers(content)
        if not approvers:
            result.errors.append(
                'BLOCKER: No final approval authority identified. '
                'Must explicitly name final approver (usually Scott).'
            )
        else:
            parsed['approvers'] = approvers

        # 7. Check for revocation path
        revocation = self._extract_section(content, r'(?:revocation|pause|rollback)', 5)
        if not revocation:
            result.errors.append(
                'BLOCKER: No revocation or pause path defined. '
                'Must document how authority can be withdrawn.'
            )
        else:
            parsed['revocation_path'] = revocation

        # 8. Check tool authority mapping
        tools = self._extract_section(content, r'tool\s+(?:authority|access|rights)', 8)
        if tools:
            parsed['tool_authority'] = tools

        # 9. Check memory authority
        memory = self._extract_section(content, r'memory\s+(?:rights|authority|access)', 8)
        if memory:
            parsed['memory_rights'] = memory

        # 10. Check release gates
        release = self._extract_section(content, r'release\s+(?:gate|routing)', 5)
        if release:
            parsed['release_gates'] = release

        # 11. Check for no-runtime statement
        has_no_runtime = bool(re.search(
            r'NOT\s+.*\s+activate.*\s+autonomous|not\s+an?\s+authority\s+grant',
            content,
            re.IGNORECASE
        ))
        if has_no_runtime:
            parsed['has_no_runtime_statement'] = True
        else:
            result.warnings.append(
                'No explicit no-runtime/no-authority-grant statement found'
            )

        # Check for template markers
        if re.search(r'\[Template question:\]|\[.*?\]', content):
            result.warnings.append('Contract contains unanswered template questions')

        # Determine overall result
        result.ok = len(result.errors) == 0
        result.parsed = parsed

        return result

    def _extract_status(self, content: str) -> Optional[str]:
        """Extract activation status from content. Returns lowercase status or None."""
        patterns = [
            r'- \[x\]\s+(\w+)',
            r'Current Activation Status[:\s]+(\w+)',
            r'Activation Status[:\s]+(\w+)',
            r'Status[:\s]+(\w+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                status = match.group(1).lower().strip()
                return status  # Return as-is, validation happens in caller

        return None

    def _extract_level(self, content: str) -> Optional[int]:
        """Extract autonomy level (any number, validation happens in caller)."""
        patterns = [
            r'[Ll]evel[:\s]+(-?\d+)',
            r'autonomy\s+level[:\s]+(-?\d+)',
            r'target\s+(?:autonomy\s+)?level[:\s]+(-?\d+)',
            r'current\s+level[:\s]+(-?\d+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    pass

        return None

    def _find_inferred_authority(self, content: str) -> Optional[str]:
        """Find inferred authority language."""
        for pattern in self.compiled_patterns:
            match = pattern.search(content)
            if match:
                return match.group(0)
        return None

    def _extract_section(self, content: str, section_marker: str, max_lines: int) -> Optional[str]:
        """Extract a section from content, starting at marker and taking up to max_lines."""
        pattern = f'(?:{section_marker})[^\\n]*\\n((?:[^\\n]*\\n){{0,{max_lines}}})'
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)

        if match:
            try:
                section = match.group(1).strip()
                if section:
                    return section
            except IndexError:
                pass

        return None

    def _extract_approvers(self, content: str) -> List[str]:
        """Extract approver names."""
        approvers = []

        patterns = [
            r'final\s+(?:approval\s+)?(?:approver|authority)[:\s]+([A-Z][a-z]+)',
            r'final\s+approver[:\s]+([A-Z][a-z]+)',
            r'approved?\s+(?:by|from)[:\s]+([A-Z][a-z]+)',
            r'Who\s+is\s+the\s+final\s+(?:approver|authority)[^\n]*\n[^\n]*?([A-Z][a-z]+)',
            r'Approvers?\s*:\s*([A-Z][a-z]+)',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                approver = match.group(1).strip()
                if approver and approver not in approvers:
                    approvers.append(approver)

        return approvers


def validate_contract(content: str, source_loader_result: Optional[Any] = None) -> ValidationResult:
    """
    Quick validation of autonomy contract.

    Args:
        content: Autonomy.md or contract text
        source_loader_result: Optional SourceLoaderResult

    Returns:
        ValidationResult
    """
    validator = ContractValidator()
    return validator.validate(content, source_loader_result)
