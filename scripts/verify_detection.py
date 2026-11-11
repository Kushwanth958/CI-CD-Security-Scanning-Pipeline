"""Exercise real scanners against temporary fixtures; never commit a secret."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
os.environ["PATH"] = str(ROOT / ".tools/bin") + os.pathsep + os.environ["PATH"]


def scan(command, expected):
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != expected:
        # Do not print scanner output: a future fixture could contain sensitive text.
        raise RuntimeError(f"{command[0]} returned {result.returncode}; expected {expected}")


def verify():
    results = []
    with tempfile.TemporaryDirectory(prefix="pipeline-fixtures-") as directory:
        base = Path(directory)
        clean = base / "clean"
        clean.mkdir()
        (clean / "config.py").write_text('import os\nTOKEN = os.getenv("API_TOKEN")\n')
        secret = base / "secret"
        secret.mkdir()
        # Synthetic AWS-shaped identifier, never issued by a provider; disposable storage only.
        (secret / "config.env").write_text("AWS_ACCESS_KEY_ID=" + "AKIA" + "QWERTYUIOPASDFGH" + "\n")
        for name, target, expected in [("clean", clean, 0), ("seeded", secret, 10)]:
            report = base / f"{name}.json"
            scan(["gitleaks", "dir", str(target), "--config", str(ROOT / ".gitleaks.toml"),
                  "--redact=100", "--exit-code", "10", "--report-format", "json",
                  "--report-path", str(report)], expected)
            findings = json.loads(report.read_text())
            if name == "seeded" and not any(f.get("RuleID") == "aws-access-token" for f in findings):
                raise RuntimeError("AWS example was not detected by the expected rule")
            results.append({"case": f"gitleaks-{name}", "passed": True, "findings": len(findings)})
        # Exact rule-and-file allowlist, isolated from production scanner config.
        allow_config = base / "allow.toml"
        allow_config.write_text((ROOT / ".gitleaks.toml").read_text() + """
[[rules]]
id = "aws-access-token"
[[rules.allowlists]]
description = "Disposable synthetic fixture only"
condition = "AND"
paths = ['(^|/)config[.]env$']
regexTarget = "secret"
regexes = ['^AKIA""" + "QWERTYUIOPASDFGH$']\n")
        scan(["gitleaks", "dir", str(secret), "--config", str(allow_config), "--redact=100", "--exit-code", "10"], 0)
        results.append({"case": "gitleaks-scoped-allowlist", "passed": True})
        # A different value in the same file MUST still fail.
        (secret / "config.env").write_text("AWS_ACCESS_KEY_ID=" + "AKIA" + "ZXCVBNMASDFGHJKL" + "\n")
        scan(["gitleaks", "dir", str(secret), "--config", str(allow_config), "--redact=100", "--exit-code", "10"], 10)
        results.append({"case": "gitleaks-allowlist-does-not-hide-other-secrets", "passed": True})
        vulnerable = base / "vulnerable"
        vulnerable.mkdir()
        # Manifest only: this outdated package is never installed or executed.
        (vulnerable / "requirements.txt").write_text("Django==2.2.0\n")
        for name, target, expected in [("clean", clean, 0), ("vulnerable", vulnerable, 10)]:
            report = base / f"trivy-{name}.json"
            scan(["trivy", "fs", "--scanners", "vuln", "--severity", "HIGH,CRITICAL",
                  "--exit-code", "10", "--format", "json", "--output", str(report), str(target)], expected)
            findings = [v for r in json.loads(report.read_text()).get("Results", []) for v in r.get("Vulnerabilities", [])]
            if name == "vulnerable" and not any(v["PkgName"].lower() == "django" for v in findings):
                raise RuntimeError("Expected vulnerable Django finding is missing")
            results.append({"case": f"trivy-{name}", "passed": True, "findings": len(findings)})
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports/detection-tests.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    verify()
