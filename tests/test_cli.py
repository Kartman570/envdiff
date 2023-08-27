import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def test_diff_never_prints_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            left, right = Path(tmp) / "a", Path(tmp) / "b"
            left.write_text("TOKEN=first-secret")
            right.write_text("TOKEN=second-secret")
            result = subprocess.run([sys.executable, "-m", "envdiff", "diff", str(left),
                                     str(right), "--json"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout), [{"key": "TOKEN", "state": "changed"}])
            self.assertNotIn("secret", result.stdout + result.stderr)

    def test_sample_schema(self):
        result = subprocess.run([sys.executable, "-m", "envdiff", "check", "examples/local.env",
                                 "examples/schema.json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
