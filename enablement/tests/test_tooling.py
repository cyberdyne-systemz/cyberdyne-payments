"""Exercise public process boundaries, not just the helper implementations."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PLUGIN = REPO / "plugins/coding-policy"
if not PLUGIN.exists():  # Source template in the presentation workspace.
    PLUGIN = REPO.parents[1] / "plugins/coding-policy"
GATE = REPO / ".github/codex/gate.py"


def finding(severity="blocking"):
    return {"severity": severity, "rule": "PAY-001", "file": "src/main/java/TransferRequest.java",
            "line": 12, "message": "Zero is valid but the new constraint rejects it."}


class GateTests(unittest.TestCase):
    def run_gate(self, review, raw=False):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review.json"
            path.write_text(review if raw else json.dumps(review))
            return subprocess.run([sys.executable, str(GATE), str(path)], capture_output=True, text=True)

    def test_blocking_fails_even_with_advisory(self):
        result = self.run_gate({"summary": "Boundary defect", "findings": [finding(), finding("advisory")]})
        self.assertEqual(1, result.returncode)
        self.assertIn("1 blocking, 1 advisory", result.stdout)

    def test_advisory_only_passes(self):
        result = self.run_gate({"summary": "Add an example", "findings": [finding("advisory")]})
        self.assertEqual(0, result.returncode)
        self.assertIn("0 blocking, 1 advisory", result.stdout)

    def test_clean_passes(self):
        self.assertEqual(0, self.run_gate({"summary": "No actionable defects", "findings": []}).returncode)

    def test_malformed_and_incomplete_fail_closed(self):
        for review in ("", "not JSON", "{}", '{"summary":"ok","findings":null}',
                       '{"summary":"ok","findings":[],"findings":[]}'):
            with self.subTest(review=review):
                self.assertEqual(2, self.run_gate(review, raw=True).returncode)

    def test_invalid_finding_types_and_paths_fail_closed(self):
        for key, value in (("severity", "warning"), ("rule", "PAY-999"), ("line", True),
                           ("line", 0), ("file", "../secret"), ("file", "/tmp/x"), ("message", "")):
            with self.subTest(key=key, value=value):
                item = finding()
                item[key] = value
                self.assertEqual(2, self.run_gate({"summary": "Review", "findings": [item]}).returncode)

    def test_missing_output_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(GATE), str(Path(directory) / "absent.json")], capture_output=True)
            self.assertEqual(2, result.returncode)


class PluginTests(unittest.TestCase):
    def test_hook_reports_version_without_writing_workspace(self):
        with tempfile.TemporaryDirectory(prefix="policy hook ") as directory:
            result = subprocess.run([sys.executable, str(PLUGIN / "scripts/session_start.py")],
                                    input=json.dumps({"hook_event_name": "SessionStart", "cwd": directory}),
                                    text=True, capture_output=True, cwd=directory, check=True)
            output = json.loads(result.stdout)["hookSpecificOutput"]
            self.assertEqual("SessionStart", output["hookEventName"])
            self.assertIn("coding-policy 0.1.0", output["additionalContext"])
            self.assertEqual([], list(Path(directory).iterdir()))

    def test_hook_ignores_other_events(self):
        result = subprocess.run([sys.executable, str(PLUGIN / "scripts/session_start.py")],
                                input='{"hook_event_name":"Stop"}', text=True, capture_output=True, check=True)
        self.assertEqual("", result.stdout)

    def test_mcp_stdio_round_trip_and_bad_input_recovery(self):
        calls = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_policy", "arguments": {"topic": "workflow"}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_policy", "arguments": {"topic": "../../secret"}}},
            {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "get_pr_template", "arguments": {}}},
            {"jsonrpc": "2.0", "id": 6, "method": "ping"}
        ]
        data = "not-json\n" + "\n".join(json.dumps(call) for call in calls) + "\n"
        config = json.loads((PLUGIN / ".mcp.json").read_text())["mcpServers"]["cyberdyne-policy"]
        result = subprocess.run([config["command"], *config["args"]], cwd=PLUGIN / config["cwd"],
                                input=data, capture_output=True, text=True, check=True, timeout=5)
        replies = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(7, len(replies))
        self.assertEqual(-32700, replies[0]["error"]["code"])
        self.assertEqual("2025-06-18", replies[1]["result"]["protocolVersion"])
        self.assertEqual(2, len(replies[2]["result"]["tools"]))
        self.assertTrue(all(tool["annotations"]["readOnlyHint"] for tool in replies[2]["result"]["tools"]))
        self.assertIn("Source: coding-policy 0.1.0", replies[3]["result"]["content"][0]["text"])
        self.assertEqual(-32602, replies[4]["error"]["code"])
        self.assertIn("## Verification", replies[5]["result"]["content"][0]["text"])
        self.assertEqual({}, replies[6]["result"])


if __name__ == "__main__":
    unittest.main()
