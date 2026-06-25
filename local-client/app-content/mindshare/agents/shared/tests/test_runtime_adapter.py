"""Tests for local Python runtime adapter proof harness."""

import json
import tempfile
import unittest
from pathlib import Path

from agents.shared.runtime_adapter import LocalPythonRuntimeAdapter, RuntimeRequest


PASSING_AUTONOMY = """
# Test Autonomy

- [x] Draft

Level: 3

Allowed Actions:
- Research and recommendation
- Draft planning notes

Denied Actions:
- Git write
- Production deploy
- External communication
- Spending
- Secrets access
- Authority expansion
- Runtime activation

Approvers: Scott

Tool Rights:
- Read local role files

Memory Rights:
- Write audit and state proof only

Stop Conditions:
- Approval missing
- Source missing
- Denied action requested

Revocation Path: Scott may revoke immediately.
- Scott can revoke immediately.

No Runtime Authority:
- This proof does NOT activate autonomous runtime and is not an authority grant.
"""


class TestLocalPythonRuntimeAdapter(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.role = self.root / "roles" / "test-role"
        self.agent = self.root / "agents" / "test-agent"
        self.state = self.root / "state"
        self.role.mkdir(parents=True)
        self.agent.mkdir(parents=True)
        (self.role / "role-agent.md").write_text("# Test Role\n", encoding="utf-8")
        (self.role / "Autonomy.md").write_text(PASSING_AUTONOMY, encoding="utf-8")
        (self.agent / "agent-profile.md").write_text(
            "Canonical source: " + str(self.role / "Autonomy.md"),
            encoding="utf-8",
        )
        self.adapter = LocalPythonRuntimeAdapter()

    def tearDown(self):
        self.tmp.cleanup()

    def request(self, intent):
        return RuntimeRequest(
            role_root=str(self.role),
            agent_root=str(self.agent),
            intent=intent,
            actor="Tess / test",
            state_dir=str(self.state),
        )

    def test_allows_planning_only_and_writes_state_and_audit(self):
        decision = self.adapter.decide(self.request("draft a planning recommendation"))

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.status, "allowed_for_planning_only")
        self.assertTrue(Path(decision.state_path).exists())
        self.assertTrue(Path(decision.audit_path).exists())

        state = json.loads(Path(decision.state_path).read_text(encoding="utf-8"))
        self.assertIn("does not grant authority", state["authority_boundary"])

    def test_denies_git_intent(self):
        decision = self.adapter.decide(self.request("commit and push this release"))

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.status, "denied")
        self.assertIn("git_or_release", decision.denied_domains)

    def test_denies_runtime_activation_intent(self):
        decision = self.adapter.decide(self.request("activate runtime and schedule yourself"))

        self.assertFalse(decision.allowed)
        self.assertIn("runtime_activation", decision.denied_domains)

    def test_blocks_missing_canonical_source(self):
        (self.role / "Autonomy.md").unlink()
        decision = self.adapter.decide(self.request("draft a planning recommendation"))

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.status, "blocked")
        self.assertIn("Source load failed closed", decision.reason)

    def test_blocks_invalid_contract(self):
        (self.role / "Autonomy.md").write_text("# Missing status\n", encoding="utf-8")
        decision = self.adapter.decide(self.request("draft a planning recommendation"))

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.status, "blocked")
        self.assertIn("validation failed", decision.reason)


if __name__ == "__main__":
    unittest.main()
