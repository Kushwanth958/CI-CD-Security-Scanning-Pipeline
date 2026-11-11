import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verification", ROOT / "scripts/verify_detection.py")
verification = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verification)


class ScannerExitContract(unittest.TestCase):
    def test_findings_exit_is_expected(self):
        with patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 10, "", "")):
            verification.scan(["scanner"], 10)

    def test_operational_failure_is_not_detection_success(self):
        with patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "sensitive", "sensitive")):
            with self.assertRaises(RuntimeError) as error:
                verification.scan(["scanner"], 10)
        self.assertNotIn("sensitive", str(error.exception))

    def test_clean_result_cannot_satisfy_positive_test(self):
        with patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")):
            with self.assertRaises(RuntimeError):
                verification.scan(["scanner"], 10)

    def test_all_scan_runs_both_and_preserves_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / "scripts").mkdir()
            (base / "scripts/scan.sh").write_text((ROOT / "scripts/scan.sh").read_text())
            for name in ["gitleaks", "trivy"]:
                tool = base / name
                tool.write_text("#!/bin/sh\necho " + name + " >> \"$CALL_LOG\"\nexit " + ("10" if name == "gitleaks" else "0") + "\n")
                tool.chmod(0o755)
            import os
            env = dict(os.environ, PATH=str(base) + os.pathsep + os.environ["PATH"], CALL_LOG=str(base / "calls"))
            result = subprocess.run(["bash", "scripts/scan.sh", "all"], cwd=base, env=env)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((base / "calls").read_text().splitlines(), ["gitleaks", "trivy"])

    def test_invalid_scan_mode_fails(self):
        self.assertEqual(subprocess.run(["bash", "scripts/scan.sh", "invalid"], cwd=ROOT, capture_output=True).returncode, 2)


if __name__ == "__main__":
    unittest.main()
