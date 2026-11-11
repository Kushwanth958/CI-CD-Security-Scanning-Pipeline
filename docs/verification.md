# Verification results

Verified on November 11, 2026 using GitHub-hosted Ubuntu 24.04 runners.

[Successful main-branch run](https://github.com/Kushwanth958/CI-CD-Security-Scanning-Pipeline/actions/runs/43076129032)

## Results

| Check | Observed result |
| --- | --- |
| Unit tests | 5 passed |
| Pinned scanner installation | Gitleaks 8.30.1 and Trivy 0.76.1 installed after SHA256 verification |
| Full-history secret scan | Passed; no leaks found |
| Repository dependency scan | Passed; dependency-free app has no package findings |
| Clean secret fixture | Passed; 0 findings |
| Synthetic AWS-shaped identifier | Passed; 1 aws-access-token finding and expected exit 10 |
| Exact rule/path/value exception | Passed; expected exit 0 |
| Different identifier in same file | Passed; expected exit 10 |
| Clean dependency fixture | Passed; 0 findings |
| Django 2.2.0 manifest | Passed; 22 HIGH/CRITICAL findings and expected exit 10 |
| Report artifact | Uploaded gitleaks.json, trivy.json, and detection-tests.json |

The positive fixtures exist only in disposable temporary storage. No vulnerable dependency was installed, and no real credential was used. Counts reflect the vulnerability database at scan time and can change.

[Successful pull-request run](https://github.com/Kushwanth958/CI-CD-Security-Scanning-Pipeline/actions/runs/43076230531) also exercised the PR trigger. Reports are retained for seven days; job logs provide the recorded acceptance outcomes.

Local Bash syntax checks and Python/YAML/TOML parsing passed. The orchestration unit test was additionally isolated from installed scanner binaries so rerunning tests after installing tools remains deterministic. Scanner operational errors are distinguished from expected findings.

Passing checks do not automatically prevent merging. Enable a main-branch ruleset requiring **Security checks** to enforce that policy. No branch protection settings were changed.
