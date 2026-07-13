import tempfile
import unittest
from pathlib import Path

import port_agent_rules as port


class RulesPortTests(unittest.TestCase):
    def test_nested_codex_rules_become_nested_claude_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("root rules\n", encoding="utf-8")
            (root / "api").mkdir()
            (root / "api" / "AGENTS.md").write_text("api rules\n", encoding="utf-8")
            items, warnings = port.discover(root, "to-claude")
            self.assertEqual(len(items), 2)
            self.assertEqual(warnings, [])
            for item in items:
                port.write_conversion(item, force=False, dry_run=False)
            self.assertIn("api rules", (root / "api" / "CLAUDE.md").read_text())

    def test_round_trip_removes_generated_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original = "# Rules\n\n- Run tests.\n"
            (root / "AGENTS.md").write_text(original, encoding="utf-8")
            item = port.discover(root, "to-claude")[0][0]
            port.write_conversion(item, force=False, dry_run=False)
            (root / "AGENTS.md").unlink()
            item = port.discover(root, "to-codex")[0][0]
            port.write_conversion(item, force=False, dry_run=False)
            result = (root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(port.portable_body(result), original)

    def test_unmanaged_destination_is_protected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("codex", encoding="utf-8")
            (root / "CLAUDE.md").write_text("hand written", encoding="utf-8")
            item = port.discover(root, "to-claude")[0][0]
            with self.assertRaises(RuntimeError):
                port.write_conversion(item, force=False, dry_run=False)

    def test_override_wins_at_same_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("base", encoding="utf-8")
            (root / "AGENTS.override.md").write_text("override", encoding="utf-8")
            items, warnings = port.discover(root, "to-claude")
            self.assertEqual(items[0].source.name, "AGENTS.override.md")
            self.assertTrue(warnings)


if __name__ == "__main__":
    unittest.main()
