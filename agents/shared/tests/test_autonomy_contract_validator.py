"""
Tests for autonomy contract validator.

Tests all required blockers and include a passing minimal contract.
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from autonomy_contract_validator import ContractValidator, validate_contract


class TestContractValidatorBlockers(unittest.TestCase):
    """Test all required blocker conditions."""

    def setUp(self):
        self.validator = ContractValidator()

    def test_blocker_missing_activation_status(self):
        """BLOCKER: Must fail when activation status is missing."""
        content = """
        # Autonomy Contract

        Role: TestRole
        Level: 3
        Approvers: Scott
        Allowed Actions:
        - Read contracts
        Denied Actions:
        - Activate roles
        Stop Conditions:
        - Authority revoked
        Revocation Path: Scott may revoke immediately
        """
        result = validate_contract(content)
        self.assertFalse(result.ok)
        self.assertTrue(any('activation status' in err.lower() for err in result.errors))

    def test_blocker_unknown_status_vocabulary(self):
        """BLOCKER: Must fail on unknown status vocabulary."""
        content = """
        # Autonomy Contract

        Current Activation Status: InProcess
        Level: 3
        Approvers: Scott
        Allowed Actions:
        - Read contracts
        Denied Actions:
        - Activate roles
        Stop Conditions:
        - Authority revoked
        Revocation Path: Scott may revoke immediately
        """
        result = validate_contract(content)
        self.assertFalse(result.ok)
        self.assertTrue(any('Unknown status' in err for err in result.errors))

    def test_blocker_inferred_authority_language(self):
        """BLOCKER: Must fail when authority is inferred, not explicit."""
        content = """
        # Autonomy Contract

        - [x] Approved
        Level: 3
        Approvers: Scott
        Allowed Actions:
        - May automatically decide on gate policy changes
        - Will autonomously edit autonomy files
        Denied Actions:
        - Cannot activate
        Stop Conditions:
        - Authority revoked
        Revocation Path: Scott may revoke immediately
        """
        result = validate_contract(content)
        self.assertFalse(result.ok)
        self.assertTrue(any('inferred' in err.lower() for err in result.errors))

    def test_blocker_missing_denied_actions(self):
        """BLOCKER: Must fail when denied actions are not listed."""
        content = """
        # Autonomy Contract

        - [x] Approved
        Level: 3
        Approvers: Scott
        Allowed Actions:
        - Review contracts
        - Recommend policies
        Stop Conditions:
        - Authority revoked
        Revocation Path: Scott may revoke immediately
        """
        result = validate_contract(content)
        self.assertFalse(result.ok)
        self.assertTrue(any('denied' in err.lower() for err in result.errors))

    def test_blocker_missing_stop_conditions(self):
        """BLOCKER: Must fail when stop conditions are not defined."""
        content = """
        # Autonomy Contract

        - [x] Approved
        Level: 3
        Approvers: Scott
        Allowed Actions:
        - Review contracts
        Denied Actions:
        - Cannot activate
        - Cannot edit gates without approval
        Revocation Path: Scott may revoke immediately
        """
        result = validate_contract(content)
        self.assertFalse(result.ok)
        self.assertTrue(any('stop conditions' in err.lower() for err in result.errors))

    def test_blocker_missing_final_approver(self):
        """BLOCKER: Must fail when final approver is not named."""
        content = """
        # Autonomy Contract

        - [x] Approved
        Level: 3
        Allowed Actions:
        - Review contracts
        Denied Actions:
        - Cannot activate
        Stop Conditions:
        - Authority revoked
        Revocation Path: Scott may revoke immediately
        """
        result = validate_contract(content)
        self.assertFalse(result.ok)
        self.assertTrue(any('approver' in err.lower() for err in result.errors))

    def test_blocker_missing_revocation_path(self):
        """BLOCKER: Must fail when revocation path is not defined."""
        content = """
        # Autonomy Contract

        - [x] Approved
        Level: 3
        Approvers: Scott
        Allowed Actions:
        - Review contracts
        Denied Actions:
        - Cannot activate
        Stop Conditions:
        - Authority revoked by Scott
        - Source files missing
        """
        result = validate_contract(content)
        self.assertFalse(result.ok)
        self.assertTrue(any('revocation' in err.lower() for err in result.errors))

    def test_blocker_invalid_autonomy_level(self):
        """BLOCKER: Must fail on invalid autonomy level."""
        content = """
        # Autonomy Contract

        - [x] Approved
        Level: 7
        Approvers: Scott
        Allowed Actions:
        - Review contracts
        Denied Actions:
        - Cannot activate
        Stop Conditions:
        - Authority revoked
        Revocation Path: Scott may revoke immediately
        """
        result = validate_contract(content)
        self.assertFalse(result.ok)
        self.assertTrue(any('invalid' in err.lower() for err in result.errors))


class TestValidMinimalContract(unittest.TestCase):
    """Test that a minimal but valid contract passes."""

    def setUp(self):
        self.validator = ContractValidator()

    def test_minimal_passing_contract(self):
        """Minimal valid contract should pass."""
        content = """
        # Autonomy Contract for Test Role

        ## Activation Status

        - [x] Approved

        Date: 2026-06-21
        Set by: Scott

        ## Autonomy Level

        Level: 2

        ## Allowed Actions

        - Research technical questions
        - Answer questions
        - Recommend policies

        ## Denied Actions

        - Cannot activate roles
        - Cannot edit gates without approval
        - Cannot access secrets
        - Cannot send external communication
        - Cannot expand own authority

        ## Stop Conditions

        - Authority paused or revoked by Scott
        - Source files missing
        - Conflicting guidance detected

        ## Approvers

        Final approval authority: Scott

        ## Revocation Path

        Scott may pause authority at any time with a direct message.
        Revocation updates state and role contract.
        Resume requires explicit new instruction within narrowed scope.

        ## No-Runtime Statement

        This contract is NOT an authority grant and does NOT activate
        any autonomous runtime.
        """
        result = validate_contract(content)
        self.assertTrue(result.ok, f'Minimal contract should pass. Errors: {result.errors}')
        self.assertEqual(result.parsed['activation_status'], 'approved')
        self.assertEqual(result.parsed['autonomy_level'], 2)
        self.assertIn('allowed_actions', result.parsed)
        self.assertIn('denied_actions', result.parsed)
        self.assertIn('stop_conditions', result.parsed)
        self.assertIn('approvers', result.parsed)

    def test_draft_status_passes(self):
        """Draft status should pass validation."""
        content = """
        # Autonomy Contract

        - [x] Draft
        Approvers: Scott
        Allowed Actions:
        - Review contracts
        Denied Actions:
        - Cannot activate
        Stop Conditions:
        - Paused by Scott
        Revocation Path: Scott may pause
        """
        result = validate_contract(content)
        self.assertTrue(result.ok)
        self.assertEqual(result.parsed['activation_status'], 'draft')

    def test_active_status_passes(self):
        """Active status should pass validation."""
        content = """
        # Autonomy Contract

        - [x] Active
        Approvers: Scott
        Allowed Actions:
        - Review contracts
        Denied Actions:
        - Cannot activate
        Stop Conditions:
        - Paused by Scott
        Revocation Path: Scott may pause
        """
        result = validate_contract(content)
        self.assertTrue(result.ok)
        self.assertEqual(result.parsed['activation_status'], 'active')

    def test_paused_status_passes(self):
        """Paused status should pass validation."""
        content = """
        # Autonomy Contract

        - [x] Paused
        Approvers: Scott
        Allowed Actions:
        - Review contracts
        Denied Actions:
        - Cannot activate
        Stop Conditions:
        - Paused by Scott
        Revocation Path: Scott may pause
        """
        result = validate_contract(content)
        self.assertTrue(result.ok)
        self.assertEqual(result.parsed['activation_status'], 'paused')

    def test_revoked_status_passes(self):
        """Revoked status should pass validation."""
        content = """
        # Autonomy Contract

        - [x] Revoked
        Approvers: Scott
        Allowed Actions:
        - Review contracts
        Denied Actions:
        - Cannot activate
        Stop Conditions:
        - Paused by Scott
        Revocation Path: Scott may pause
        """
        result = validate_contract(content)
        self.assertTrue(result.ok)
        self.assertEqual(result.parsed['activation_status'], 'revoked')


class TestStatusVocabulary(unittest.TestCase):
    """Test all valid status vocabulary variations."""

    def setUp(self):
        self.validator = ContractValidator()

    def test_status_variations(self):
        """Test various ways to express valid statuses."""
        templates = [
            ('- [x] Draft', 'draft'),
            ('Current Activation Status: Draft', 'draft'),
            ('Activation Status: Approved', 'approved'),
            ('Status: Active', 'active'),
            ('- [x] Paused', 'paused'),
            ('Status: REVOKED', 'revoked'),
        ]

        for content_snippet, expected_status in templates:
            content = f"""
            # Contract
            {content_snippet}
            Approvers: Scott
            Allowed Actions:
            - Review
            Denied Actions:
            - Cannot activate
            Stop Conditions:
            - Paused
            Revocation Path: Scott may pause
            """
            result = validate_contract(content)
            self.assertEqual(
                result.parsed.get('activation_status'),
                expected_status,
                f'Failed to extract status from: {content_snippet}'
            )


class TestLevelExtraction(unittest.TestCase):
    """Test autonomy level extraction."""

    def setUp(self):
        self.validator = ContractValidator()

    def test_level_extraction(self):
        """Test extracting autonomy levels 0-6."""
        for level in range(7):
            content = f"""
            # Contract
            - [x] Approved
            Level: {level}
            Approvers: Scott
            Allowed Actions:
            - Review
            Denied Actions:
            - Cannot activate
            Stop Conditions:
            - Paused
            Revocation Path: Scott may pause
            """
            result = validate_contract(content)
            self.assertEqual(result.parsed.get('autonomy_level'), level)

    def test_invalid_levels(self):
        """Test that invalid levels fail."""
        for bad_level in [-1, 7, 10]:
            content = f"""
            # Contract
            - [x] Approved
            Level: {bad_level}
            Approvers: Scott
            Allowed Actions:
            - Review
            Denied Actions:
            - Cannot activate
            Stop Conditions:
            - Paused
            Revocation Path: Scott may pause
            """
            result = validate_contract(content)
            self.assertFalse(result.ok)


class TestEmptyContent(unittest.TestCase):
    """Test handling of empty or null content."""

    def test_empty_string(self):
        """Empty string should fail."""
        result = validate_contract('')
        self.assertFalse(result.ok)
        self.assertTrue(any('empty' in err.lower() for err in result.errors))

    def test_whitespace_only(self):
        """Whitespace-only content should fail."""
        result = validate_contract('   \n\n   ')
        self.assertFalse(result.ok)

    def test_none_content(self):
        """None should fail gracefully."""
        result = validate_contract(None)
        self.assertFalse(result.ok)


class TestToolAndMemoryRights(unittest.TestCase):
    """Test extraction of tool and memory rights."""

    def setUp(self):
        self.validator = ContractValidator()

    def test_tool_authority_extraction(self):
        """Tool authority should be extracted if present."""
        content = """
        # Contract
        - [x] Approved
        Approvers: Scott
        Allowed Actions:
        - Review
        Denied Actions:
        - Cannot activate
        Stop Conditions:
        - Paused
        Revocation Path: Scott may pause

        ## Tool Authority

        | Tool | Use |
        | autonomy-read | Review contracts |
        | gate-draft | Design gates (Scott approval) |
        """
        result = validate_contract(content)
        self.assertTrue(result.ok)
        self.assertIn('tool_authority', result.parsed)

    def test_memory_rights_extraction(self):
        """Memory rights should be extracted if present."""
        content = """
        # Contract
        - [x] Approved
        Approvers: Scott
        Allowed Actions:
        - Review
        Denied Actions:
        - Cannot activate
        Stop Conditions:
        - Paused
        Revocation Path: Scott may pause

        ## Memory Rights

        Can write to: role memory, autonomy findings
        Cannot write to: other roles' memory, secrets
        """
        result = validate_contract(content)
        self.assertTrue(result.ok)
        self.assertIn('memory_rights', result.parsed)


class TestWarnings(unittest.TestCase):
    """Test warning conditions."""

    def setUp(self):
        self.validator = ContractValidator()

    def test_warning_missing_level(self):
        """Missing level generates warning but passes if not otherwise blocked."""
        content = """
        # Contract
        - [x] Approved
        Approvers: Scott
        Allowed Actions:
        - Review
        Denied Actions:
        - Cannot activate
        Stop Conditions:
        - Paused
        Revocation Path: Scott may pause
        """
        result = validate_contract(content)
        self.assertTrue(result.ok)
        self.assertTrue(any('level' in w.lower() for w in result.warnings))

    def test_warning_template_questions(self):
        """Template question markers generate warning."""
        content = """
        # Contract
        - [x] Approved
        Approvers: Scott
        [Template question: What are allowed actions?]
        Allowed Actions:
        - Review
        Denied Actions:
        - Cannot activate
        Stop Conditions:
        - Paused
        Revocation Path: Scott may pause
        """
        result = validate_contract(content)
        self.assertTrue(any('template' in w.lower() for w in result.warnings))

    def test_warning_no_runtime_statement(self):
        """Missing no-runtime statement generates warning."""
        content = """
        # Contract
        - [x] Approved
        Approvers: Scott
        Allowed Actions:
        - Review
        Denied Actions:
        - Cannot activate
        Stop Conditions:
        - Paused
        Revocation Path: Scott may pause
        """
        result = validate_contract(content)
        self.assertTrue(any('no-runtime' in w.lower() or 'not.*authority' in w.lower()
                           for w in result.warnings))


class TestComplexContracts(unittest.TestCase):
    """Test realistic complex contracts."""

    def test_tess_autonomy_engineer_contract(self):
        """Test Tess autonomy engineer contract scenario."""
        content = """
        # Autonomy Contract for Tess / Autonomy Engineer

        Version: 1.0
        Created: 2026-06-21

        ## Activation Status

        - [x] Approved
        Set by: Scott on 2026-06-21

        ## Autonomy Level

        Current level: 3
        Target level: 4

        ## Mission

        Define and review autonomy requirements for role promotion toward autonomous agents.

        ## Allowed Actions

        - Review autonomy contracts and gates
        - Recommend gate policies based on requirements
        - Identify gaps in role promotion readiness
        - Coordinate approval sequencing
        - Document findings in role contracts

        ## Denied Actions

        - Cannot make unilateral gate edits
        - Cannot activate roles without Scott approval
        - Cannot grant authority
        - Cannot bypass Reid for Git-related changes
        - Cannot send external communication
        - Cannot access secrets
        - Cannot expand own authority

        ## Stop Conditions

        - Authority paused or revoked by Scott
        - Source files missing or stale
        - Autonomy.md conflicts with role-agent.md
        - Authority expansion detected
        - Scott says stop, pause, do not touch, or just answer

        ## Final Approval Authority

        Scott

        ## Revocation and Pause

        Scott may pause authority at any time with a direct message.
        Revocation updates state.json and role-agent.md status.
        Paused agent preserves audit, state, and memory.
        Resume requires explicit new instruction from Scott within narrowed scope.
        No self-resume authority.

        ## No-Runtime Statement

        This autonomy contract is NOT an authority grant and does NOT activate
        any autonomous runtime.
        """
        result = validate_contract(content)
        self.assertTrue(result.ok, f'Tess contract should pass. Errors: {result.errors}')
        self.assertEqual(result.parsed['activation_status'], 'approved')
        self.assertEqual(result.parsed['autonomy_level'], 3)


if __name__ == '__main__':
    unittest.main()
