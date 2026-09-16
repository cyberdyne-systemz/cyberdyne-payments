"""Exercise the payments review gate through its public process interface."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
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


if __name__ == "__main__":
    unittest.main()
