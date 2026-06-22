#!/usr/bin/env python3
"""
Backup autonomous roles and automation configs.

Discovers roles from roles/ directory, identifies source files per role,
excludes volatile logs, writes manifest with hashes/sizes/mtimes.

Usage:
    python scripts/backup_roles.py                    # dry-run (default)
    python scripts/backup_roles.py --execute          # perform backup
    python scripts/backup_roles.py --root C:\\custom\\path --execute

Manifest written to: {backup_root}/latest/manifest.json
Backups copied to: {backup_root}/latest/{category}/

No scheduler activation; manual run only.
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any


BACKUP_ROOT_DEFAULT = Path("C:\\Users\\scott\\Code\\mindshare-backup-proof")

# File categories by role structure
ROLE_FILE_CATEGORIES = {
    "role_contract": [
        "role-agent.md",
        "Autonomy.md",
        "autonomy-requirements.md",
    ],
    "role_memory": [
        "memory.md",
        "personality.md",
        "name.md",
        "WhoAmI.md",
    ],
    "role_workflow": [
        "workflow.md",
        "loop.md",
        "gate-blocks.md",
    ],
    "role_automation": [
        "automation.md",
        "heartbeat-automation.md",
        "hook-spec.md",
    ],
    "role_state": [
        "state.json",
        "memory-state.json",
    ],
    "agent_profile": [
        "agent-profile.md",
        "agent-design.md",
        "agent-backlog.md",
        "agent-brief.md",
    ],
    "agent_eval": [
        "eval-suite.md",
        "eval-report.md",
    ],
}

# Role-local subdirectories to scan for files
# Maps subdirectory name to default category
ROLE_LOCAL_SUBDIRS = {
    "memory-archive": "role_memory_archive",
    "evals": "role_support",
    "tests": "role_support",
    "runtime": "role_support",
    "scripts": "role_support",
}

# Directories and files to exclude (volatile, logs, archives)
EXCLUDE_PATTERNS = [
    "__pycache__",
    ".pytest_cache",
    "*.pyc",
    ".git",
    "last-resume-error",
    "file-watch-runner.log",
    ".log",
    "*.log",
]


def should_exclude(path: Path) -> bool:
    """Check if path matches exclusion patterns."""
    parts = path.parts
    for pattern in EXCLUDE_PATTERNS:
        if pattern in parts:
            return True
        if path.name == pattern:
            return True
    return False


def get_file_sha256(fpath: Path) -> str:
    """Compute SHA256 hash of file."""
    sha256_hash = hashlib.sha256()
    with open(fpath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def discover_roles(roles_root: Path) -> Dict[str, Path]:
    """Discover roles from roles/ directory structure."""
    roles = {}
    if not roles_root.exists():
        return roles

    for role_dir in sorted(roles_root.iterdir()):
        if role_dir.is_dir() and not role_dir.name.startswith("."):
            roles[role_dir.name] = role_dir

    return roles


def discover_agents(agents_root: Path) -> Dict[str, Path]:
    """Discover agents from agents/ directory structure."""
    agents = {}
    if not agents_root.exists():
        return agents

    for agent_dir in sorted(agents_root.iterdir()):
        if agent_dir.is_dir() and not agent_dir.name.startswith("."):
            agents[agent_dir.name] = agent_dir

    return agents


def collect_backup_files(
    roles_root: Path,
    agents_root: Path,
) -> List[Dict[str, Any]]:
    """Collect files to backup with metadata."""
    files = []

    roles = discover_roles(roles_root)
    agents = discover_agents(agents_root)

    # Collect role files
    for role_name, role_dir in sorted(roles.items()):
        # Collect from ROLE_FILE_CATEGORIES (existing behavior)
        for category, filenames in ROLE_FILE_CATEGORIES.items():
            for filename in filenames:
                fpath = role_dir / filename
                if fpath.exists() and not should_exclude(fpath):
                    stat = fpath.stat()
                    files.append({
                        "source": str(fpath),
                        "role": role_name,
                        "category": category,
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                        "filename": filename,
                    })

        # Collect from role-local subdirectories
        for subdir_name, default_category in ROLE_LOCAL_SUBDIRS.items():
            subdir_path = role_dir / subdir_name
            if subdir_path.exists() and subdir_path.is_dir():
                for file_path in sorted(subdir_path.rglob("*")):
                    if file_path.is_file() and not should_exclude(file_path):
                        stat = file_path.stat()
                        rel_path = file_path.relative_to(role_dir)
                        files.append({
                            "source": str(file_path),
                            "role": role_name,
                            "category": default_category,
                            "size": stat.st_size,
                            "mtime": stat.st_mtime,
                            "filename": str(rel_path),
                        })

    # Collect agent files
    for agent_name, agent_dir in sorted(agents.items()):
        # Collect from ROLE_FILE_CATEGORIES (existing behavior)
        for category, filenames in ROLE_FILE_CATEGORIES.items():
            for filename in filenames:
                fpath = agent_dir / filename
                if fpath.exists() and not should_exclude(fpath):
                    stat = fpath.stat()
                    files.append({
                        "source": str(fpath),
                        "agent": agent_name,
                        "category": category,
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                        "filename": filename,
                    })

        # Collect from role-local subdirectories
        for subdir_name, default_category in ROLE_LOCAL_SUBDIRS.items():
            subdir_path = agent_dir / subdir_name
            if subdir_path.exists() and subdir_path.is_dir():
                for file_path in sorted(subdir_path.rglob("*")):
                    if file_path.is_file() and not should_exclude(file_path):
                        stat = file_path.stat()
                        rel_path = file_path.relative_to(agent_dir)
                        files.append({
                            "source": str(file_path),
                            "agent": agent_name,
                            "category": default_category,
                            "size": stat.st_size,
                            "mtime": stat.st_mtime,
                            "filename": str(rel_path),
                        })

    return files


def compute_manifest(
    files: List[Dict[str, Any]],
    backup_root: Path,
) -> Dict[str, Any]:
    """Compute manifest with file hashes and destinations."""
    manifest = {
        "backup_root": str(backup_root),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "files": [],
    }

    for file_info in files:
        source_path = Path(file_info["source"])

        # Compute destination: {backup_root}/latest/{category}/{role_or_agent}/{filename}
        if "role" in file_info:
            dest_rel = Path("latest") / file_info["category"] / file_info["role"] / file_info["filename"]
        else:
            dest_rel = Path("latest") / file_info["category"] / file_info["agent"] / file_info["filename"]

        destination = backup_root / dest_rel

        sha256 = get_file_sha256(source_path)

        manifest["files"].append({
            "source": file_info["source"],
            "destination": str(destination),
            "category": file_info["category"],
            "size": file_info["size"],
            "mtime": file_info["mtime"],
            "sha256": sha256,
            "filename": file_info["filename"],
        })

    return manifest


def write_manifest(manifest: Dict[str, Any], backup_root: Path) -> Path:
    """Write manifest.json to backup location."""
    manifest_dir = backup_root / "latest"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = manifest_dir / "manifest.json"

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return manifest_path


def execute_backup(manifest: Dict[str, Any]) -> int:
    """Copy files according to manifest."""
    count = 0
    errors = 0

    for file_info in manifest["files"]:
        source = Path(file_info["source"])
        dest = Path(file_info["destination"])

        if not source.exists():
            print(f"ERROR: source missing {source}")
            errors += 1
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(source, "rb") as src_f:
                with open(dest, "wb") as dst_f:
                    dst_f.write(src_f.read())
            count += 1
            print(f"  copied {dest.name}")
        except Exception as e:
            print(f"ERROR: copy failed {dest}: {e}")
            errors += 1

    return count, errors


def main():
    parser = argparse.ArgumentParser(
        description="Backup autonomous roles and automation configs",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute backup (default is dry-run)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=BACKUP_ROOT_DEFAULT,
        help=f"Backup root directory (default: {BACKUP_ROOT_DEFAULT})",
    )
    parser.add_argument(
        "--project",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)",
    )

    args = parser.parse_args()

    project_root = args.project.resolve()
    roles_root = project_root / "roles"
    agents_root = project_root / "agents"
    backup_root = args.root.resolve()

    print(f"Backup roles and automation configs")
    print(f"Project root: {project_root}")
    print(f"Roles root: {roles_root}")
    print(f"Agents root: {agents_root}")
    print(f"Backup root: {backup_root}")
    print(f"Dry-run: {not args.execute}")
    print()

    # Collect files
    files = collect_backup_files(roles_root, agents_root)

    if not files:
        print("No backup files found.")
        return 0

    print(f"Found {len(files)} files to backup:")
    for f in files:
        entity = f.get("role") or f.get("agent", "?")
        print(f"  {f['category']:20} {entity:30} {f['filename']}")
    print()

    # Compute manifest
    manifest = compute_manifest(files, backup_root)

    print(f"Manifest entries: {len(manifest['files'])}")
    print()

    if args.execute:
        print("EXECUTING BACKUP...")
        count, errors = execute_backup(manifest)
        print(f"Copied: {count}, Errors: {errors}")
        print()

        # Write manifest
        manifest_path = write_manifest(manifest, backup_root)
        print(f"Manifest written: {manifest_path}")

        if errors > 0:
            print(f"BACKUP COMPLETED WITH {errors} ERRORS")
            return 1
        else:
            print("BACKUP SUCCESSFUL")
            return 0
    else:
        print("DRY-RUN MODE (no files copied, no manifest written)")
        print(f"To execute: python scripts/backup_roles.py --execute")
        print()

        # Print manifest summary without writing
        print("Manifest summary (not written to disk in dry-run):")
        print(f"  Backup root: {manifest['backup_root']}")
        print(f"  Timestamp: {manifest['timestamp']}")
        print(f"  Files: {len(manifest['files'])}")
        print()

        if manifest['files']:
            print("Sample entries (first 5):")
            for entry in manifest['files'][:5]:
                print(f"  {entry['category']:20} {entry['filename']:30} {entry['size']:8} bytes")
            print()

        return 0


if __name__ == "__main__":
    sys.exit(main())
