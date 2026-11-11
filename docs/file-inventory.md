# Repository File Inventory

| File | Responsibility |
| --- | --- |
| `README.md` | Project overview, quick start, and documentation index |
| `.github/workflows/security.yml` | Triggers, least-privilege runner job, scans, acceptance tests, and artifact upload |
| `.github/dependabot.yml` | Weekly GitHub Actions update checks |
| `.gitleaks.toml` | Extend built-in secret rules without project-specific production exceptions |
| `.gitignore` | Exclude local tools, generated reports, environments, and Python caches |
| `Makefile` | Shared setup, test, scan, and verification commands |
| `app/health.py` | Dependency-free example application |
| `app/requirements.txt` | Explicitly empty third-party dependency manifest |
| `scripts/install-tools.sh` | Platform check, pinned release downloads, SHA256 verification, and installation |
| `scripts/scan.sh` | Full-history secret scan, dependency scan, and aggregate failure handling |
| `scripts/verify_detection.py` | Temporary fixtures, real-scanner checks, cleanup, and acceptance report |
| `tests/test_pipeline.py` | Five regression tests for exit handling and scan orchestration |
| `docs/project-report.md` | Scope, design, evidence, assessment, and limitations |
| `docs/operations.md` | Setup, commands, troubleshooting, maintenance, and merge policy |
| `docs/verification.md` | Verified baseline and source run links |
| `docs/evidence/verification-2026-11-11.json` | Curated machine-readable test evidence with source identifiers |
| `docs/triage.md` | Alert validation, prioritization, and exception governance |
| `docs/credential-rotation.md` | Credential exposure and recovery procedure |
| `docs/demo.md` | Reproduction and interview demonstration steps |
| `docs/file-inventory.md` | This inventory |

## Generated files

| Output | Availability |
| --- | --- |
| `reports/gitleaks.json` | Redacted secret findings from a production scan |
| `reports/trivy.json` | Dependency vulnerability results from a production scan |
| `reports/detection-tests.json` | Acceptance results, written after all cases succeed |
| `security-reports` Actions artifact | Up to three generated JSON files, retained for seven days |

Generated reports and downloaded binaries are intentionally not versioned. A failed acceptance run may not produce `detection-tests.json`; inspect the failing step rather than assuming missing evidence means a pass. The dated checked-in evidence is a summarized historical record, not the generated scanner output.
