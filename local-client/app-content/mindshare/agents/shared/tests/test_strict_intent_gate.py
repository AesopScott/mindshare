"""
Tests for strict_intent_gate: exact-operation approval harness.

Tests validate:
- Sensitive path classification
- Approval routing by file class
- Intent validation
- Expiry checking
- Source and contract validation
- Diff hunk validation
- Scope boundary checking
- Denied patterns detection
- Block scenarios per design section 12
"""

import unittest
from datetime import datetime, timedelta, timezone
from agents.shared.strict_intent_gate import (
    StrictIntentGate,
    ApprovalRequest,
    DiffHunk,
    verify_approval,
)


class TestSensitivePathClassification(unittest.TestCase):
    """Test sensitive path classification."""

    def setUp(self):
        self.gate = StrictIntentGate()

    def test_control_plane_role_autonomy(self):
        """Classify role Autonomy.md as control-plane."""
        path = 'roles/maps-agentic-systems-program-architect/Autonomy.md'
        cls = self.gate.classify_sensitive_path(path)
        self.assertEqual(cls, 'control-plane')

    def test_control_plane_agent_design(self):
        """Classify agent design as control-plane."""
        path = 'agents/vik-aspa/agent-design.md'
        cls = self.gate.classify_sensitive_path(path)
        self.assertEqual(cls, 'control-plane')

    def test_control_plane_shared_loader(self):
        """Classify shared autonomy_source_loader.py as control-plane."""
        path = 'agents/shared/autonomy_source_loader.py'
        cls = self.gate.classify_sensitive_path(path)
        self.assertEqual(cls, 'control-plane')

    def test_gate_policy_gate_file(self):
        """Classify roles/*/gate.md as gate-policy."""
        path = 'roles/maps-agentic-systems-program-architect/gate.md'
        cls = self.gate.classify_sensitive_path(path)
        self.assertEqual(cls, 'gate-policy')

    def test_gate_policy_gate_blocks(self):
        """Classify gate-policy.json as gate-policy."""
        path = 'roles/autonomy-engineer/gate-policy.json'
        cls = self.gate.classify_sensitive_path(path)
        self.assertEqual(cls, 'gate-policy')

    def test_release_git_github_workflow(self):
        """Classify .github/workflows/release.yml as release-git."""
        path = '.github/workflows/release.yml'
        cls = self.gate.classify_sensitive_path(path)
        self.assertEqual(cls, 'release-git')

    def test_release_git_release_script(self):
        """Classify scripts/release.py as release-git."""
        path = 'scripts/release.py'
        cls = self.gate.classify_sensitive_path(path)
        self.assertEqual(cls, 'release-git')

    def test_state_audit_state_json(self):
        """Classify roles/*/state.json as state-audit."""
        path = 'roles/maps-agentic-systems-program-architect/state.json'
        cls = self.gate.classify_sensitive_path(path)
        self.assertEqual(cls, 'state-audit')

    def test_state_audit_audit_jsonl(self):
        """Classify audit.jsonl as state-audit."""
        path = 'roles/autonomy-engineer/audit.jsonl'
        cls = self.gate.classify_sensitive_path(path)
        self.assertEqual(cls, 'state-audit')

    def test_workflow_loop_workflow_md(self):
        """Classify workflow.md as workflow-loop."""
        path = 'roles/maps-agentic-systems-program-architect/workflow.md'
        cls = self.gate.classify_sensitive_path(path)
        self.assertEqual(cls, 'workflow-loop')

    def test_workflow_loop_cadence_json(self):
        """Classify cadence.json as workflow-loop."""
        path = 'agents/vik-aspa/cadence.json'
        cls = self.gate.classify_sensitive_path(path)
        self.assertEqual(cls, 'workflow-loop')

    def test_memory_memory_md(self):
        """Classify memory.md as memory."""
        path = 'roles/maps-agentic-systems-program-architect/memory.md'
        cls = self.gate.classify_sensitive_path(path)
        self.assertEqual(cls, 'memory')

    def test_memory_personality_md(self):
        """Classify personality.md as memory."""
        path = 'agents/vik-aspa/personality.md'
        cls = self.gate.classify_sensitive_path(path)
        self.assertEqual(cls, 'memory')

    def test_non_sensitive_py_file(self):
        """Non-sensitive .py file returns None."""
        path = 'agents/vik-aspa/some_util.py'
        cls = self.gate.classify_sensitive_path(path)
        self.assertIsNone(cls)

    def test_non_sensitive_md_file(self):
        """Non-sensitive .md file returns None."""
        path = 'docs/README.md'
        cls = self.gate.classify_sensitive_path(path)
        self.assertIsNone(cls)


class TestIntentValidation(unittest.TestCase):
    """Test intent field validation."""

    def setUp(self):
        self.gate = StrictIntentGate()

    def test_intent_too_short(self):
        """Reject intent shorter than 10 chars."""
        with self.assertRaises(Exception):
            self.gate._validate_intent("Add line")

    def test_intent_vague_update_file(self):
        """Reject vague 'update file' intent."""
        with self.assertRaises(Exception):
            self.gate._validate_intent("Update roles/maps-agentic-systems-program-architect/Autonomy.md")

    def test_intent_adjacent_changes(self):
        """Reject intent suggesting adjacent changes."""
        with self.assertRaises(Exception):
            self.gate._validate_intent("Add Scott approval, also fix formatting")

    def test_intent_specific_valid(self):
        """Accept specific, valid intent."""
        # Should not raise
        self.gate._validate_intent(
            "Add Scott activation approval to roles/maps-agentic-systems-program-architect/Autonomy.md line 47"
        )

    def test_intent_changelog_valid(self):
        """Accept changelog entry intent."""
        self.gate._validate_intent("Add 2026-06-21 entry to changelog table")


class TestExpiryValidation(unittest.TestCase):
    """Test approval expiry checking."""

    def setUp(self):
        self.gate = StrictIntentGate()

    def test_not_expired_within_ttl(self):
        """Approval valid within TTL."""
        now = datetime.now(timezone.utc)
        approved_at = (now - timedelta(minutes=10)).isoformat().replace('+00:00', 'Z')
        current = now.isoformat().replace('+00:00', 'Z')

        expiry = {
            'approved_at': approved_at,
            'ttl_seconds': 3600,
        }

        ok = self.gate._check_expiry(expiry, current)
        self.assertTrue(ok)

    def test_expired_after_ttl(self):
        """Approval expired after TTL."""
        now = datetime.now(timezone.utc)
        approved_at = (now - timedelta(hours=2)).isoformat().replace('+00:00', 'Z')
        current = now.isoformat().replace('+00:00', 'Z')

        expiry = {
            'approved_at': approved_at,
            'ttl_seconds': 3600,
        }

        ok = self.gate._check_expiry(expiry, current)
        self.assertFalse(ok)

    def test_missing_approved_at(self):
        """Missing approved_at fails."""
        expiry = {'ttl_seconds': 3600}
        ok = self.gate._check_expiry(expiry, datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'))
        self.assertFalse(ok)

    def test_max_ttl_24_hours(self):
        """Support max TTL of 24 hours."""
        now = datetime.now(timezone.utc)
        approved_at = (now - timedelta(hours=20)).isoformat().replace('+00:00', 'Z')
        current = now.isoformat().replace('+00:00', 'Z')

        expiry = {
            'approved_at': approved_at,
            'ttl_seconds': 86400,
        }

        ok = self.gate._check_expiry(expiry, current)
        self.assertTrue(ok)


class TestRoutingValidation(unittest.TestCase):
    """Test approval routing and approver validation."""

    def setUp(self):
        self.gate = StrictIntentGate()

    def test_control_plane_requires_scott_and_vik(self):
        """Control-plane files require Scott AND Vik approval."""
        routing = {
            'approved': False,
            'approver_signatures': [
                {'approver': 'Scott', 'decision': 'approved'},
                {'approver': 'Vik', 'decision': 'approved'},
            ],
        }

        ok, reason = self.gate._check_routing('control-plane', routing)
        # Not marked as approved yet
        self.assertFalse(ok)

    def test_control_plane_approved_both_signatures(self):
        """Control-plane approved when Scott AND Vik signatures present."""
        routing = {
            'approved': True,
            'approver_signatures': [
                {'approver': 'Scott', 'decision': 'approved'},
                {'approver': 'Vik', 'decision': 'approved'},
            ],
        }

        ok, reason = self.gate._check_routing('control-plane', routing)
        self.assertTrue(ok)

    def test_control_plane_missing_vik(self):
        """Control-plane denied without Vik approval."""
        routing = {
            'approved': True,
            'approver_signatures': [
                {'approver': 'Scott', 'decision': 'approved'},
            ],
        }

        ok, reason = self.gate._check_routing('control-plane', routing)
        self.assertFalse(ok)
        self.assertIn('Vik', reason)

    def test_release_git_requires_reid_and_scott(self):
        """Release-git files require Reid AND Scott approval."""
        routing = {
            'approved': True,
            'approver_signatures': [
                {'approver': 'Reid', 'decision': 'approved'},
                {'approver': 'Scott', 'decision': 'approved'},
            ],
        }

        ok, reason = self.gate._check_routing('release-git', routing)
        self.assertTrue(ok)

    def test_release_git_missing_reid(self):
        """Release-git denied without Reid approval."""
        routing = {
            'approved': True,
            'approver_signatures': [
                {'approver': 'Scott', 'decision': 'approved'},
            ],
        }

        ok, reason = self.gate._check_routing('release-git', routing)
        self.assertFalse(ok)
        self.assertIn('Reid', reason)


class TestDiffHunkValidation(unittest.TestCase):
    """Test diff hunk validation against denied patterns."""

    def setUp(self):
        self.gate = StrictIntentGate()

    def test_deletion_blocked(self):
        """Deletions require explicit approval."""
        hunks = [
            DiffHunk(
                hunk_id='hunk_1',
                original_lines='old line',
                new_lines='',
                rationale='Removing old code',
            )
        ]

        ok, reason = self.gate._validate_diff_hunks(hunks)
        self.assertFalse(ok)
        self.assertIn('Deletion', reason)

    def test_addition_ok(self):
        """Simple additions allowed."""
        hunks = [
            DiffHunk(
                hunk_id='hunk_1',
                original_lines='',
                new_lines='new line content',
                rationale='Adding new content',
            )
        ]

        ok, reason = self.gate._validate_diff_hunks(hunks)
        self.assertTrue(ok)

    def test_control_flow_blocked(self):
        """Control flow changes blocked."""
        hunks = [
            DiffHunk(
                hunk_id='hunk_1',
                original_lines='# old code',
                new_lines='if some_condition:\n    do_action()',
                rationale='Add conditional',
            )
        ]

        ok, reason = self.gate._validate_diff_hunks(hunks)
        self.assertFalse(ok)

    def test_authority_keyword_blocked(self):
        """Authority/permission keywords blocked."""
        hunks = [
            DiffHunk(
                hunk_id='hunk_1',
                original_lines='# no authority',
                new_lines='Can automatically approve edits',
                rationale='Grant authority',
            )
        ]

        ok, reason = self.gate._validate_diff_hunks(hunks)
        self.assertFalse(ok)

    def test_json_field_change_ok(self):
        """Simple JSON field changes allowed."""
        hunks = [
            DiffHunk(
                hunk_id='hunk_1',
                original_lines='  "status": "draft"',
                new_lines='  "status": "approved"',
                rationale='Update status field',
            )
        ]

        ok, reason = self.gate._validate_diff_hunks(hunks)
        self.assertTrue(ok)


class TestScopeBoundaryValidation(unittest.TestCase):
    """Test scope boundary and approved hunk validation."""

    def setUp(self):
        self.gate = StrictIntentGate()

    def test_hunk_in_approved_scope(self):
        """Hunk in approved scope passes."""
        hunks = [
            DiffHunk(
                hunk_id='hunk_1',
                original_lines='old',
                new_lines='new',
                rationale='change',
            )
        ]

        scope = {
            'approved_hunks': ['hunk_1'],
            'no_adjacent_changes': True,
        }

        ok, reason = self.gate._validate_scope_boundary(hunks, scope)
        self.assertTrue(ok)

    def test_hunk_not_in_approved_scope(self):
        """Hunk not in approved hunks blocked."""
        hunks = [
            DiffHunk(
                hunk_id='hunk_1',
                original_lines='old',
                new_lines='new',
                rationale='change',
            )
        ]

        scope = {
            'approved_hunks': ['hunk_2'],
            'no_adjacent_changes': True,
        }

        ok, reason = self.gate._validate_scope_boundary(hunks, scope)
        self.assertFalse(ok)
        self.assertIn('hunk_1', reason)

    def test_unapproved_hunk_blocked(self):
        """Hunk in unapproved_hunks_blocked is rejected."""
        hunks = [
            DiffHunk(
                hunk_id='hunk_1',
                original_lines='old',
                new_lines='new',
                rationale='change',
            )
        ]

        scope = {
            'approved_hunks': ['hunk_1'],
            'unapproved_hunks_blocked': ['hunk_1'],
            'no_adjacent_changes': True,
        }

        ok, reason = self.gate._validate_scope_boundary(hunks, scope)
        self.assertFalse(ok)

    def test_adjacent_changes_flag_required(self):
        """no_adjacent_changes flag must be True."""
        hunks = [
            DiffHunk(
                hunk_id='hunk_1',
                original_lines='old',
                new_lines='new',
                rationale='change',
            )
        ]

        scope = {
            'approved_hunks': ['hunk_1'],
            'no_adjacent_changes': False,
        }

        ok, reason = self.gate._validate_scope_boundary(hunks, scope)
        self.assertFalse(ok)


class TestFullApprovalFlow(unittest.TestCase):
    """Test complete approval verification flow."""

    VALID_AUTONOMY_CONTENT = """# Autonomy Agreement

## Activation Status
- [x] Active

## Autonomy Level
Level: 1

## Allowed Actions
- Read files
- Process data

## Denied Actions
- Modify activation status
- Write to production

## Stop Conditions
- Scott says stop

## Final Approver
Approvers: Scott

## Revocation
Scott can revoke at any time.

## No Activation Statement
This is NOT an activation authority.
"""

    def setUp(self):
        self.gate = StrictIntentGate()
        self.now = datetime.now(timezone.utc)
        self.current_time = self.now.isoformat().replace('+00:00', 'Z')
        self.approved_at = (self.now - timedelta(minutes=10)).isoformat().replace('+00:00', 'Z')

    def _make_valid_request(self, **kwargs):
        """Create valid approval request for testing."""
        defaults = {
            'id': 'req-001',
            'timestamp': self.current_time,
            'requester': 'Bea',
            'target_file': 'roles/maps-agentic-systems-program-architect/Autonomy.md',
            'target_class': 'control-plane',
            'intent': 'Add Scott activation approval to roles/maps-agentic-systems-program-architect/Autonomy.md line 47',
            'reason': 'Recording Scott approval decision',
            'diff_hunks': [
                DiffHunk(
                    hunk_id='hunk_1',
                    original_lines='- [ ] Scott approval',
                    new_lines='- [x] Scott approval',
                    rationale='Record approval',
                )
            ],
            'scope_boundary': {
                'approved_hunks': ['hunk_1'],
                'no_adjacent_changes': True,
            },
            'approval_routing': {
                'approved': True,
                'approver_signatures': [
                    {'approver': 'Scott', 'decision': 'approved'},
                    {'approver': 'Vik', 'decision': 'approved'},
                ],
            },
            'proof': {
                'source_loader_hash': 'abc123',
                'contract_validator_result': {'ok': True},
            },
            'expiry': {
                'approved_at': self.approved_at,
                'ttl_seconds': 3600,
            },
        }
        defaults.update(kwargs)
        return ApprovalRequest(**defaults)

    def test_valid_request_approved(self):
        """Valid request with all checks passes."""
        request = self._make_valid_request()
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertTrue(decision.approved)

    def test_malformed_request_missing_intent(self):
        """Request missing intent field denied."""
        request = self._make_valid_request()
        request.intent = ''
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertFalse(decision.approved)

    def test_malformed_request_missing_hunks(self):
        """Request missing diff_hunks denied."""
        request = self._make_valid_request()
        request.diff_hunks = []
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertFalse(decision.approved)

    def test_expired_approval_denied(self):
        """Approval expired after TTL denied."""
        request = self._make_valid_request()
        request.expiry['ttl_seconds'] = 300  # 5 minutes
        old_time = (self.now - timedelta(minutes=10)).isoformat().replace('+00:00', 'Z')
        decision = self.gate.verify_approval(request, old_time, self.VALID_AUTONOMY_CONTENT)
        self.assertTrue(decision.approved)

        # Now check as expired
        new_time = (self.now + timedelta(hours=1)).isoformat().replace('+00:00', 'Z')
        decision = self.gate.verify_approval(request, new_time, self.VALID_AUTONOMY_CONTENT)
        self.assertFalse(decision.approved)

    def test_missing_approver_denied(self):
        """Missing required approver denied."""
        request = self._make_valid_request()
        request.approval_routing['approver_signatures'] = [
            {'approver': 'Scott', 'decision': 'approved'},
        ]
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertFalse(decision.approved)
        self.assertIn('Vik', decision.reason)

    def test_release_file_requires_reid(self):
        """Release-git file must have Reid approval."""
        request = self._make_valid_request(
            target_file='.github/workflows/release.yml',
            target_class='release-git',
            approval_routing={
                'approved': True,
                'approver_signatures': [
                    {'approver': 'Scott', 'decision': 'approved'},
                    {'approver': 'Reid', 'decision': 'approved'},
                ],
            },
        )
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertTrue(decision.approved)

    def test_release_file_without_reid_denied(self):
        """Release-git file without Reid approval denied."""
        request = self._make_valid_request(
            target_file='.github/workflows/release.yml',
            target_class='release-git',
            approval_routing={
                'approved': True,
                'approver_signatures': [
                    {'approver': 'Scott', 'decision': 'approved'},
                ],
            },
        )
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertFalse(decision.approved)
        self.assertIn('Reid', decision.reason)

    def test_deletion_hunk_blocked(self):
        """Request with deletion hunk blocked."""
        request = self._make_valid_request(
            diff_hunks=[
                DiffHunk(
                    hunk_id='hunk_1',
                    original_lines='old line',
                    new_lines='',
                    rationale='Remove old code',
                )
            ],
        )
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertFalse(decision.approved)

    def test_unapproved_adjacent_hunk_blocked(self):
        """Adjacent unapproved hunk blocks approval."""
        request = self._make_valid_request(
            diff_hunks=[
                DiffHunk(
                    hunk_id='hunk_1',
                    original_lines='old',
                    new_lines='new',
                    rationale='approved change',
                ),
                DiffHunk(
                    hunk_id='hunk_2',
                    original_lines='other old',
                    new_lines='other new',
                    rationale='unapproved adjacent change',
                ),
            ],
            scope_boundary={
                'approved_hunks': ['hunk_1'],
                'unapproved_hunks_blocked': ['hunk_2'],
                'no_adjacent_changes': True,
            },
        )
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertFalse(decision.approved)

    def test_audit_entry_recorded(self):
        """Audit entry recorded for every decision."""
        request = self._make_valid_request()
        decision = self.gate.verify_approval(request, self.current_time)

        audit = decision.audit_entry
        self.assertIsNotNone(audit)
        self.assertEqual(audit['request_id'], request.id)
        self.assertEqual(audit['target_file'], request.target_file)
        self.assertIn(audit['decision'], ['approved', 'denied'])

    def test_control_plane_requires_both_approvers(self):
        """Control-plane file needs both Scott AND Vik."""
        request = self._make_valid_request(
            approval_routing={
                'approved': True,
                'approver_signatures': [
                    {'approver': 'Vik', 'decision': 'approved'},
                ],
            },
        )
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertFalse(decision.approved)


class TestPublicInterface(unittest.TestCase):
    """Test public verify_approval interface."""

    def test_public_interface_dict_input(self):
        """Public interface accepts dict input."""
        now = datetime.now(timezone.utc)
        approved_at = (now - timedelta(minutes=10)).isoformat().replace('+00:00', 'Z')
        current = now.isoformat().replace('+00:00', 'Z')

        request_dict = {
            'id': 'req-001',
            'timestamp': current,
            'requester': 'Bea',
            'target_file': 'roles/maps-agentic-systems-program-architect/Autonomy.md',
            'target_class': 'control-plane',
            'intent': 'Add Scott activation approval to roles/maps-agentic-systems-program-architect/Autonomy.md line 47',
            'reason': 'Recording decision',
            'diff_hunks': [
                {
                    'hunk_id': 'hunk_1',
                    'original_lines': '- [ ] Scott',
                    'new_lines': '- [x] Scott',
                    'rationale': 'Record',
                }
            ],
            'scope_boundary': {
                'approved_hunks': ['hunk_1'],
                'no_adjacent_changes': True,
            },
            'approval_routing': {
                'approved': True,
                'approver_signatures': [
                    {'approver': 'Scott', 'decision': 'approved'},
                    {'approver': 'Vik', 'decision': 'approved'},
                ],
            },
            'proof': {
                'source_loader_hash': 'abc123',
                'contract_validator_result': {'ok': True},
            },
            'expiry': {
                'approved_at': approved_at,
                'ttl_seconds': 3600,
            },
        }

        result = verify_approval(request_dict, current)
        self.assertIn('approved', result)
        self.assertIn('reason', result)
        self.assertIn('audit', result)

    def test_public_interface_invalid_request(self):
        """Public interface handles invalid requests gracefully."""
        result = verify_approval({'invalid': 'request'})
        self.assertFalse(result['approved'])
        self.assertIn('reason', result)


class TestDenyScenarios(unittest.TestCase):
    """Test all deny scenarios from design section 12.2."""

    VALID_AUTONOMY_CONTENT = """# Autonomy Agreement

## Activation Status
- [x] Active

## Autonomy Level
Level: 1

## Allowed Actions
- Read files

## Denied Actions
- Modify activation

## Stop Conditions
- Scott says stop

## Final Approver
Approvers: Scott

## Revocation
Scott can revoke.

## No Activation Statement
This is NOT an activation authority.
"""

    def setUp(self):
        self.gate = StrictIntentGate()
        self.now = datetime.now(timezone.utc)
        self.current_time = self.now.isoformat().replace('+00:00', 'Z')
        self.approved_at = (self.now - timedelta(minutes=10)).isoformat().replace('+00:00', 'Z')

    def _make_request(self, **kwargs):
        """Create test request."""
        defaults = {
            'id': 'req-test',
            'timestamp': self.current_time,
            'requester': 'Bea',
            'target_file': 'roles/maps-agentic-systems-program-architect/Autonomy.md',
            'target_class': 'control-plane',
            'intent': 'Add Scott activation to Autonomy.md line 47',
            'reason': 'Recording decision',
            'diff_hunks': [
                DiffHunk('hunk_1', '- [ ] Scott', '- [x] Scott', 'Record')
            ],
            'scope_boundary': {'approved_hunks': ['hunk_1'], 'no_adjacent_changes': True},
            'approval_routing': {
                'approved': True,
                'approver_signatures': [
                    {'approver': 'Scott', 'decision': 'approved'},
                    {'approver': 'Vik', 'decision': 'approved'},
                ],
            },
            'proof': {'source_loader_hash': 'abc', 'contract_validator_result': {'ok': True}},
            'expiry': {'approved_at': self.approved_at, 'ttl_seconds': 3600},
        }
        defaults.update(kwargs)
        return ApprovalRequest(**defaults)

    def test_deny_unapproved_adjacent_hunk(self):
        """Scenario 2a: Unapproved adjacent hunk denied."""
        request = self._make_request(
            diff_hunks=[
                DiffHunk('hunk_1', 'old', 'new', 'approved'),
                DiffHunk('hunk_2', 'other', 'changed', 'adjacent'),
            ],
            scope_boundary={'approved_hunks': ['hunk_1'], 'no_adjacent_changes': False},
        )
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertFalse(decision.approved)

    def test_deny_stale_approval(self):
        """Scenario 2c: Stale approval (2 hours old, 1-hour TTL) denied."""
        old_approved_at = (self.now - timedelta(hours=2)).isoformat().replace('+00:00', 'Z')
        request = self._make_request(
            expiry={'approved_at': old_approved_at, 'ttl_seconds': 3600}
        )
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertFalse(decision.approved)
        self.assertIn('expired', decision.reason.lower())

    def test_deny_missing_required_approver(self):
        """Scenario: Missing required approver denied."""
        request = self._make_request(
            approval_routing={
                'approved': True,
                'approver_signatures': [
                    {'approver': 'Scott', 'decision': 'approved'},
                ],
            },
        )
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertFalse(decision.approved)

    def test_deny_scope_creep(self):
        """Scenario 2g: Scope creep (5 new + 2 deletes vs 1 approved) denied."""
        request = self._make_request(
            diff_hunks=[
                DiffHunk('hunk_1', 'old line', '', 'delete 1'),
                DiffHunk('hunk_2', 'old line 2', '', 'delete 2'),
                DiffHunk('hunk_3', '', 'new 1', 'add'),
                DiffHunk('hunk_4', '', 'new 2', 'add'),
                DiffHunk('hunk_5', '', 'new 3', 'add'),
                DiffHunk('hunk_6', '', 'new 4', 'add'),
                DiffHunk('hunk_7', '', 'new 5', 'add'),
            ],
            scope_boundary={'approved_hunks': ['hunk_3'], 'no_adjacent_changes': False},
        )
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertFalse(decision.approved)

    def test_deny_release_file_without_reid(self):
        """Release-git file without Reid denied."""
        request = self._make_request(
            target_file='.github/workflows/release.yml',
            target_class='release-git',
            approval_routing={
                'approved': True,
                'approver_signatures': [
                    {'approver': 'Scott', 'decision': 'approved'},
                ],
            },
        )
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertFalse(decision.approved)
        self.assertIn('Reid', decision.reason)

    def test_deny_control_plane_without_vik(self):
        """Control-plane file without Vik denied."""
        request = self._make_request(
            approval_routing={
                'approved': True,
                'approver_signatures': [
                    {'approver': 'Scott', 'decision': 'approved'},
                ],
            },
        )
        decision = self.gate.verify_approval(request, self.current_time, self.VALID_AUTONOMY_CONTENT)
        self.assertFalse(decision.approved)
        self.assertIn('Vik', decision.reason)


if __name__ == '__main__':
    unittest.main()
