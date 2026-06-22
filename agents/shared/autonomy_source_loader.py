"""
Canonical source loader for autonomy contracts and role definitions.

Loads role source files and follows compatibility pointers to canonical
Autonomy.md. Fails closed when required canonical source is missing.

Does not activate anything. Does not write state. Returns structured metadata.
"""

import json
import os
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Dict, Any, List


class CanonicalSourceMissing(Exception):
    """Raised when canonical autonomy source is missing and required."""
    pass


class MalformedCanonicalPointer(Exception):
    """Raised when autonomy-contract.md has invalid canonical pointer."""
    pass


@dataclass
class SourceLoaderResult:
    """Result of source loading operation."""
    paths: Dict[str, Optional[str]] = field(default_factory=dict)
    present_files: List[str] = field(default_factory=list)
    missing_files: List[str] = field(default_factory=list)
    canonical_autonomy_path: Optional[str] = None
    activation_status: Optional[str] = None
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for JSON serialization."""
        return asdict(self)


def _read_file(path: str) -> Optional[str]:
    """Read file if it exists, return None otherwise."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, IOError):
        return None


def _find_canonical_pointer_in_autonomy_contract(content: str) -> Optional[str]:
    """
    Extract canonical Autonomy.md path from autonomy-contract.md.

    Looks for patterns like:
    - "canonical source: <path>"
    - "canonical: <path>"
    - "points to: <path>"
    - "pointer to canonical Autonomy.md: <path>"

    Returns path if found, None otherwise.
    """
    if not content:
        return None

    patterns = [
        r'canonical\s+(?:source|autonomy)[:\s]+([^\n]+\.md)',
        r'canonical[:\s]+([^\n]+\.md)',
        r'points?\s+to[:\s]+([^\n]+\.md)',
        r'pointer\s+to\s+canonical\s+Autonomy\.md[:\s]+([^\n]+\.md)',
        r'canonical\s+Autonomy\.md[:\s]+([^\n]+\.md)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            pointer = match.group(1).strip()
            if pointer and pointer.endswith('.md'):
                return pointer
    return None


def _extract_activation_status(autonomy_content: str) -> Optional[str]:
    """
    Extract activation status from Autonomy.md content.

    Looks for explicit status markers like:
    - "- [x] Active"
    - "- [x] Draft"
    - "Current Activation Status: Active"
    - etc.

    Returns status string or None if not found.
    """
    if not autonomy_content:
        return None

    valid_statuses = ['draft', 'approved', 'active', 'paused', 'revoked']

    patterns = [
        r'- \[x\]\s+(draft|approved|active|paused|revoked)',
        r'Current Activation Status[:\s]+([a-z]+)',
        r'Activation Status[:\s]+([a-z]+)',
        r'Status[:\s]+(draft|approved|active|paused|revoked)',
    ]

    for pattern in patterns:
        match = re.search(pattern, autonomy_content, re.IGNORECASE)
        if match:
            status = match.group(1).lower().strip()
            if status in valid_statuses:
                return status

    return None


def _resolve_canonical_path(root_dir: str, pointer: str) -> str:
    """
    Resolve canonical path from pointer.

    If pointer is absolute, return it. If relative, resolve relative to root_dir.
    """
    pointer = pointer.strip()

    if os.path.isabs(pointer):
        return pointer

    resolved = os.path.join(root_dir, pointer)
    return os.path.normpath(resolved)


def load_autonomy_sources(
    role_root: str,
    agent_root: Optional[str] = None,
    require_canonical: bool = False,
) -> SourceLoaderResult:
    """
    Load autonomy contract and role source files.

    Args:
        role_root: Path to role directory (required, contains role-agent.md, Autonomy.md, etc)
        agent_root: Path to agent directory (optional, may contain agent-profile.md, etc)
        require_canonical: If True, raise exception when canonical Autonomy.md is missing

    Returns:
        SourceLoaderResult with paths, present/missing files, canonical location, status, warnings

    Raises:
        CanonicalSourceMissing: If require_canonical=True and no canonical Autonomy.md found
        MalformedCanonicalPointer: If autonomy-contract.md has unparseable pointer
    """
    result = SourceLoaderResult()

    if not role_root or not os.path.isdir(role_root):
        raise ValueError(f"Invalid role_root: {role_root}")

    if agent_root and not os.path.isdir(agent_root):
        raise ValueError(f"Invalid agent_root: {agent_root}")

    role_root = os.path.normpath(role_root)
    agent_root = os.path.normpath(agent_root) if agent_root else None

    required_role_files = [
        'role-agent.md',
    ]

    optional_role_files = [
        'autonomy-contract.md',
        'Autonomy.md',
        'workflow.md',
        'loop.md',
        'memory.md',
        'personality.md',
        'name.md',
        'agent-profile.md',
        'agent-design.md',
        'agent-backlog.md',
        'gate.md',
        'state.json',
        'audit.jsonl',
    ]

    optional_agent_files = [
        'agent-profile.md',
        'agent-design.md',
    ]

    canonical_autonomy_path = None
    has_autonomy_contract = False

    for filename in required_role_files:
        path = os.path.join(role_root, filename)
        result.paths[filename] = path
        if os.path.isfile(path):
            result.present_files.append(filename)
        else:
            result.missing_files.append(filename)

    for filename in optional_role_files:
        path = os.path.join(role_root, filename)
        result.paths[filename] = path

        if os.path.isfile(path):
            result.present_files.append(filename)
        else:
            result.missing_files.append(filename)

        if filename == 'autonomy-contract.md' and os.path.isfile(path):
            has_autonomy_contract = True

    if agent_root:
        for filename in optional_agent_files:
            path = os.path.join(agent_root, filename)
            result.paths[f'agent_{filename}'] = path
            if os.path.isfile(path):
                result.present_files.append(f'agent_{filename}')
            else:
                result.missing_files.append(f'agent_{filename}')

    has_local_autonomy = 'Autonomy.md' in result.present_files

    if has_autonomy_contract:
        contract_path = os.path.join(role_root, 'autonomy-contract.md')
        contract_content = _read_file(contract_path)

        pointer = _find_canonical_pointer_in_autonomy_contract(contract_content)

        if pointer:
            canonical_path = _resolve_canonical_path(role_root, pointer)
            if os.path.isfile(canonical_path):
                canonical_autonomy_path = os.path.normpath(canonical_path)
                result.canonical_autonomy_path = canonical_autonomy_path
            else:
                msg = (
                    f"autonomy-contract.md points to canonical Autonomy.md at "
                    f"{canonical_path}, but file does not exist"
                )
                result.warnings.append(msg)
                if require_canonical:
                    raise CanonicalSourceMissing(msg)
        else:
            msg = (
                "autonomy-contract.md found but does not contain a canonical "
                "Autonomy.md pointer (should have pattern like "
                "'canonical source: <path>')"
            )
            result.warnings.append(msg)
            if require_canonical:
                raise CanonicalSourceMissing(msg)

    elif has_local_autonomy:
        canonical_autonomy_path = os.path.join(role_root, 'Autonomy.md')
        result.canonical_autonomy_path = os.path.normpath(canonical_autonomy_path)

    else:
        if require_canonical:
            msg = (
                f"No canonical Autonomy.md found in {role_root} and "
                "require_canonical=True. Either autonomy-contract.md must "
                "point to a canonical Autonomy.md, or Autonomy.md must exist "
                "in role_root."
            )
            raise CanonicalSourceMissing(msg)

    if result.canonical_autonomy_path:
        autonomy_content = _read_file(result.canonical_autonomy_path)
        if autonomy_content:
            status = _extract_activation_status(autonomy_content)
            result.activation_status = status

    if require_canonical and not result.canonical_autonomy_path:
        raise CanonicalSourceMissing(
            f"Canonical Autonomy.md is required but not found for {role_root}"
        )

    return result


def load_autonomy_sources_for_role(
    root_base: str,
    role_id: str,
    project_name: str = 'mindshare',
    require_canonical: bool = False,
) -> SourceLoaderResult:
    """
    Load autonomy sources for a role given standard path structure.

    Args:
        root_base: Base directory (e.g., C:\\Users\\scott\\Code\\)
        role_id: Role identifier (e.g., 'vik')
        project_name: Project name (e.g., 'mindshare', 'mojo')
        require_canonical: If True, raise exception when canonical is missing

    Returns:
        SourceLoaderResult
    """
    role_root = os.path.join(root_base, project_name, 'roles', role_id)
    agent_root = os.path.join(root_base, project_name, 'agents', f'{role_id}-aspa')

    if not os.path.isdir(agent_root):
        agent_root = None

    return load_autonomy_sources(
        role_root=role_root,
        agent_root=agent_root,
        require_canonical=require_canonical,
    )


if __name__ == '__main__':
    pass
