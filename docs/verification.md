# Verification status

## Local checks

Five unit tests passed locally. Bash syntax checks passed; Python, YAML, and TOML parsed successfully. Unit tests validate orchestration with mocked scanner commands, not actual threat detection.

## Acceptance cases awaiting scanner execution

| Case | Expected |
| --- | --- |
| Clean environment-variable config | Gitleaks exits 0 |
| Generated synthetic AWS-shaped identifier | Gitleaks exits 10 and reports aws-access-token |
| Exact sample and path exception | Gitleaks exits 0 |
| Different sample in same allowlisted path | Gitleaks exits 10 |
| Clean dependency target | Trivy exits 0 |
| Django 2.2.0 manifest | Trivy exits 10 and reports Django HIGH/CRITICAL findings |

At creation time, outbound GitHub binary downloads were unavailable in the build environment, so real Gitleaks/Trivy scans and live GitHub Actions runs are not recorded as passed. The workflow executes these acceptance cases once published. A database outage, unsupported config, or missing binary fails verification and must not be reported as successful detection.
