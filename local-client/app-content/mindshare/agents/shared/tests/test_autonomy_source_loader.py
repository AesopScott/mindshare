"""
Tests for autonomy source loader.

Tests cover:
- Follows canonical source pointer in autonomy-contract.md
- Missing canonical source fails closed when required
- Optional missing files are recorded
- No state writes during loading
"""

import json
import os
import tempfile
import unittest
from pathlib import Path

from agents.shared.autonomy_source_loader import (
    SourceLoaderResult,
    CanonicalSourceMissing,
    MalformedCanonicalPointer,
    load_autonomy_sources,
    _find_canonical_pointer_in_autonomy_contract,
    _extract_activation_status,
    _resolve_canonical_path,
)


class TestCanonicalPointerExtraction(unittest.TestCase):
    """Test extraction of canonical pointer from autonomy-contract.md."""

    def test_extract_pointer_with_canonical_source_pattern(self):
        """Extract pointer with 'canonical source:' pattern."""
        content = """# Autonomy Contract
Some text here.
canonical source: C:\\Users\\scott\\Code\\mojo\\roles\\vik\\Autonomy.md
More text.
"""
        pointer = _find_canonical_pointer_in_autonomy_contract(content)
        self.assertEqual(
            pointer,
            'C:\\Users\\scott\\Code\\mojo\\roles\\vik\\Autonomy.md'
        )

    def test_extract_pointer_with_canonical_pattern(self):
        """Extract pointer with 'canonical:' pattern."""
        content = """# Autonomy Contract
canonical: ../other/location/Autonomy.md
"""
        pointer = _find_canonical_pointer_in_autonomy_contract(content)
        self.assertEqual(pointer, '../other/location/Autonomy.md')

    def test_extract_pointer_with_points_to_pattern(self):
        """Extract pointer with 'points to:' pattern."""
        content = """# Autonomy Contract
Points to: /absolute/path/Autonomy.md
"""
        pointer = _find_canonical_pointer_in_autonomy_contract(content)
        self.assertEqual(pointer, '/absolute/path/Autonomy.md')

    def test_extract_pointer_returns_none_when_no_pointer(self):
        """Return None when no pointer found."""
        content = """# Autonomy Contract
This file describes autonomy but has no pointer.
"""
        pointer = _find_canonical_pointer_in_autonomy_contract(content)
        self.assertIsNone(pointer)

    def test_extract_pointer_returns_none_when_content_empty(self):
        """Return None for empty content."""
        pointer = _find_canonical_pointer_in_autonomy_contract('')
        self.assertIsNone(pointer)

    def test_extract_pointer_returns_none_when_content_none(self):
        """Return None for None content."""
        pointer = _find_canonical_pointer_in_autonomy_contract(None)
        self.assertIsNone(pointer)


class TestActivationStatusExtraction(unittest.TestCase):
    """Test extraction of activation status from Autonomy.md."""

    def test_extract_status_checked_box_active(self):
        """Extract 'active' from checked box."""
        content = """# Autonomy Contract
- [x] Active
"""
        status = _extract_activation_status(content)
        self.assertEqual(status, 'active')

    def test_extract_status_checked_box_draft(self):
        """Extract 'draft' from checked box."""
        content = """# Autonomy Contract
- [x] Draft
"""
        status = _extract_activation_status(content)
        self.assertEqual(status, 'draft')

    def test_extract_status_from_current_activation_status_field(self):
        """Extract status from 'Current Activation Status:' field."""
        content = """# Autonomy Contract
## 2. Activation Status

### Current Activation Status

- [x] Approved
"""
        status = _extract_activation_status(content)
        self.assertEqual(status, 'approved')

    def test_extract_status_case_insensitive(self):
        """Status extraction is case-insensitive."""
        content = """# Autonomy Contract
Current Activation Status: REVOKED
"""
        status = _extract_activation_status(content)
        self.assertEqual(status, 'revoked')

    def test_extract_status_returns_none_when_no_status(self):
        """Return None when no status found."""
        content = """# Autonomy Contract
This is just a contract without explicit status.
"""
        status = _extract_activation_status(content)
        self.assertIsNone(status)

    def test_extract_status_returns_none_when_content_empty(self):
        """Return None for empty content."""
        status = _extract_activation_status('')
        self.assertIsNone(status)


class TestResolveCanonicalPath(unittest.TestCase):
    """Test path resolution."""

    def test_resolve_absolute_path(self):
        """Absolute paths are returned as-is."""
        if os.name == 'nt':
            path = 'C:\\Users\\scott\\Code\\Autonomy.md'
            resolved = _resolve_canonical_path('/some/root', path)
            self.assertEqual(resolved, path)
        else:
            path = '/absolute/path/Autonomy.md'
            resolved = _resolve_canonical_path('/some/root', path)
            self.assertEqual(resolved, path)

    def test_resolve_relative_path(self):
        """Relative paths are resolved relative to root."""
        root = '/some/role/directory'
        pointer = '../other/Autonomy.md'
        resolved = _resolve_canonical_path(root, pointer)
        expected = os.path.normpath(os.path.join(root, pointer))
        self.assertEqual(resolved, expected)

    def test_resolve_strips_whitespace(self):
        """Path whitespace is stripped."""
        root = '/root'
        pointer = '  ../Autonomy.md  '
        resolved = _resolve_canonical_path(root, pointer)
        self.assertIn('Autonomy.md', resolved)
        self.assertNotIn('  ', resolved)


class TestLoadAutonomySources(unittest.TestCase):
    """Test loading autonomy sources from a role directory."""

    def setUp(self):
        """Create temporary directories for tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.role_dir = os.path.join(self.temp_dir, 'test_role')
        self.canonical_dir = os.path.join(self.temp_dir, 'canonical')
        os.makedirs(self.role_dir)
        os.makedirs(self.canonical_dir)

    def tearDown(self):
        """Clean up temporary directories."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def _write_file(self, directory: str, filename: str, content: str) -> None:
        """Helper to write file."""
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, filename)
        with open(path, 'w') as f:
            f.write(content)

    def test_load_with_local_autonomy_md(self):
        """Load when Autonomy.md exists locally."""
        self._write_file(self.role_dir, 'role-agent.md', '# Role')
        self._write_file(
            self.role_dir, 'Autonomy.md', '# Autonomy\n- [x] Active'
        )

        result = load_autonomy_sources(self.role_dir)

        self.assertIn('role-agent.md', result.present_files)
        self.assertIn('Autonomy.md', result.present_files)
        self.assertEqual(
            result.canonical_autonomy_path,
            os.path.normpath(os.path.join(self.role_dir, 'Autonomy.md'))
        )
        self.assertEqual(result.activation_status, 'active')

    def test_load_follows_canonical_pointer(self):
        """Load follows autonomy-contract.md pointer to canonical Autonomy.md."""
        self._write_file(self.role_dir, 'role-agent.md', '# Role')
        self._write_file(
            self.role_dir,
            'autonomy-contract.md',
            f'# Autonomy Contract\ncanonical source: {self.canonical_dir}/Autonomy.md'
        )
        self._write_file(
            self.canonical_dir, 'Autonomy.md', '# Autonomy\n- [x] Draft'
        )

        result = load_autonomy_sources(self.role_dir)

        self.assertIn('autonomy-contract.md', result.present_files)
        canonical_path = os.path.normpath(
            os.path.join(self.canonical_dir, 'Autonomy.md')
        )
        self.assertEqual(result.canonical_autonomy_path, canonical_path)
        self.assertEqual(result.activation_status, 'draft')

    def test_load_fails_closed_when_pointer_missing_and_required(self):
        """Raise exception when canonical pointer missing and required."""
        self._write_file(self.role_dir, 'role-agent.md', '# Role')
        self._write_file(
            self.role_dir,
            'autonomy-contract.md',
            '# Autonomy Contract\nNo pointer here.'
        )

        with self.assertRaises(CanonicalSourceMissing) as ctx:
            load_autonomy_sources(self.role_dir, require_canonical=True)

        self.assertIn('canonical', str(ctx.exception).lower())

    def test_load_fails_closed_when_canonical_missing_and_required(self):
        """Raise exception when canonical Autonomy.md missing and required."""
        self._write_file(self.role_dir, 'role-agent.md', '# Role')

        with self.assertRaises(CanonicalSourceMissing) as ctx:
            load_autonomy_sources(self.role_dir, require_canonical=True)

        self.assertIn('canonical', str(ctx.exception).lower())

    def test_load_records_optional_missing_files(self):
        """Optional missing files are recorded in missing_files."""
        self._write_file(self.role_dir, 'role-agent.md', '# Role')
        self._write_file(self.role_dir, 'Autonomy.md', '# Autonomy')
        self._write_file(self.role_dir, 'memory.md', '# Memory')

        result = load_autonomy_sources(self.role_dir)

        self.assertIn('memory.md', result.present_files)
        self.assertIn('workflow.md', result.missing_files)
        self.assertIn('loop.md', result.missing_files)

    def test_load_with_agent_root(self):
        """Load includes agent_root files."""
        agent_dir = os.path.join(self.temp_dir, 'test_agent')
        os.makedirs(agent_dir)

        self._write_file(self.role_dir, 'role-agent.md', '# Role')
        self._write_file(self.role_dir, 'Autonomy.md', '# Autonomy')
        self._write_file(agent_dir, 'agent-profile.md', '# Profile')

        result = load_autonomy_sources(self.role_dir, agent_root=agent_dir)

        self.assertIn('agent_agent-profile.md', result.present_files)

    def test_load_pointer_invalid_path_records_warning(self):
        """Pointer to nonexistent file records warning."""
        self._write_file(self.role_dir, 'role-agent.md', '# Role')
        self._write_file(
            self.role_dir,
            'autonomy-contract.md',
            'canonical source: /nonexistent/Autonomy.md'
        )

        result = load_autonomy_sources(self.role_dir, require_canonical=False)

        self.assertGreater(len(result.warnings), 0)
        self.assertIn('does not exist', result.warnings[0])

    def test_load_no_state_writes(self):
        """Loading does not write any files."""
        self._write_file(self.role_dir, 'role-agent.md', '# Role')
        self._write_file(self.role_dir, 'Autonomy.md', '# Autonomy')

        files_before = set(os.listdir(self.role_dir))

        load_autonomy_sources(self.role_dir)

        files_after = set(os.listdir(self.role_dir))

        self.assertEqual(files_before, files_after)

    def test_load_invalid_role_root_raises(self):
        """Invalid role_root raises ValueError."""
        with self.assertRaises(ValueError):
            load_autonomy_sources('/nonexistent/path')

    def test_load_invalid_agent_root_raises(self):
        """Invalid agent_root raises ValueError."""
        self._write_file(self.role_dir, 'role-agent.md', '# Role')

        with self.assertRaises(ValueError):
            load_autonomy_sources(
                self.role_dir,
                agent_root='/nonexistent/agent'
            )

    def test_load_returns_structured_result(self):
        """Load returns SourceLoaderResult with all fields."""
        self._write_file(self.role_dir, 'role-agent.md', '# Role')
        self._write_file(self.role_dir, 'Autonomy.md', '# Autonomy')

        result = load_autonomy_sources(self.role_dir)

        self.assertIsInstance(result, SourceLoaderResult)
        self.assertIsInstance(result.paths, dict)
        self.assertIsInstance(result.present_files, list)
        self.assertIsInstance(result.missing_files, list)
        self.assertIsInstance(result.warnings, list)

    def test_load_result_to_dict(self):
        """Result can be converted to dict."""
        self._write_file(self.role_dir, 'role-agent.md', '# Role')
        self._write_file(self.role_dir, 'Autonomy.md', '# Autonomy')

        result = load_autonomy_sources(self.role_dir)
        result_dict = result.to_dict()

        self.assertIsInstance(result_dict, dict)
        self.assertIn('paths', result_dict)
        self.assertIn('present_files', result_dict)
        self.assertIn('missing_files', result_dict)
        self.assertIn('canonical_autonomy_path', result_dict)
        self.assertIn('activation_status', result_dict)
        self.assertIn('warnings', result_dict)

    def test_load_relative_pointer_resolved_correctly(self):
        """Relative canonical pointer resolved relative to role_root."""
        sibling_dir = os.path.join(self.temp_dir, 'sibling')
        os.makedirs(sibling_dir)

        self._write_file(self.role_dir, 'role-agent.md', '# Role')
        self._write_file(
            self.role_dir,
            'autonomy-contract.md',
            'canonical source: ../sibling/Autonomy.md'
        )
        self._write_file(sibling_dir, 'Autonomy.md', '# Autonomy\n- [x] Paused')

        result = load_autonomy_sources(self.role_dir)

        canonical_path = os.path.normpath(
            os.path.join(sibling_dir, 'Autonomy.md')
        )
        self.assertEqual(result.canonical_autonomy_path, canonical_path)
        self.assertEqual(result.activation_status, 'paused')


class TestSourceLoaderResult(unittest.TestCase):
    """Test SourceLoaderResult dataclass."""

    def test_result_initialization(self):
        """SourceLoaderResult initializes with defaults."""
        result = SourceLoaderResult()

        self.assertEqual(result.paths, {})
        self.assertEqual(result.present_files, [])
        self.assertEqual(result.missing_files, [])
        self.assertIsNone(result.canonical_autonomy_path)
        self.assertIsNone(result.activation_status)
        self.assertEqual(result.warnings, [])

    def test_result_with_values(self):
        """SourceLoaderResult accepts initialization values."""
        paths = {'file.md': '/path/to/file.md'}
        result = SourceLoaderResult(
            paths=paths,
            present_files=['file.md'],
            activation_status='active'
        )

        self.assertEqual(result.paths, paths)
        self.assertEqual(result.present_files, ['file.md'])
        self.assertEqual(result.activation_status, 'active')


if __name__ == '__main__':
    unittest.main()
