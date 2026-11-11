# CI/CD Security Scanning Pipeline

GitHub Actions + Gitleaks + Trivy. A small, reproducible security engineering lab that scans pull requests, tests scanner behavior, and documents response decisions.

## Documentation

- [Project report](docs/project-report.md) — design, verified results, and limitations
- [Operations guide](docs/operations.md) — setup, troubleshooting, and maintenance
- [File inventory](docs/file-inventory.md) — implementation and report locations
- [Verification evidence](docs/evidence/verification-2026-11-11.json) — dated, source-linked results
- [Triage runbook](docs/triage.md) and [credential rotation](docs/credential-rotation.md)

## What it does

- Gitleaks scans complete Git history with built-in rules and fully redacted JSON output.
- Trivy scans repository dependency manifests; HIGH and CRITICAL vulnerabilities fail the check, including findings without fixes.
- Six real-scanner acceptance cases cover clean input, a seeded synthetic credential, a scoped false-positive exception, a second credential that must remain detectable, a clean dependency target, and an outdated Django manifest.
- Temporary fixtures are generated outside the checkout and removed automatically. No real credentials are needed. Vulnerable packages are never installed.
- Reports remain downloadable as Actions artifacts for seven days, including after failure.
- The workflow uses read-only repository permissions, pinned action commits, and no saved checkout credentials. It runs on PRs, main pushes, weekly, and manually.

## Run locally

Requires Linux x86_64, Bash, Python 3.11+, Git, curl, tar, and Internet access to GitHub releases and the Trivy vulnerability database.

```sh
make tools
make test
make scan
make verify
```

`make scan` requires a Git checkout with history. To start a local checkout of a downloaded archive:

```sh
git init -b main
git add .
git commit -m "Add security scanning pipeline"
```

`make test` uses the Python standard library and mocked command outcomes to test failure handling; it does not prove that scanners detect threats. `make verify` invokes the real scanners and checks both exit codes and report content. Scanner errors use a different exit code from expected findings and must fail acceptance tests.

## Repository layout

| Path | Purpose |
| --- | --- |
| `.github/workflows/security.yml` | PR and scheduled security checks |
| `.gitleaks.toml` | Default secret rules; no production allowlist |
| `scripts/install-tools.sh` | Pinned official binary downloads and checksum verification |
| `scripts/scan.sh` | Local and CI scan commands |
| `scripts/verify_detection.py` | Real scanner acceptance cases |
| `tests/test_pipeline.py` | Exit-code and orchestration regression tests |
| `app/` | Dependency-free example scan target |
| `docs/` | Triage, rotation, demonstration, and verification notes |

## Enable the merge gate

After the first workflow finishes, configure a main-branch ruleset in GitHub to require **Security checks** before merging and require pull requests. A failed workflow reports a failure; merge blocking requires this repository setting. This project does not automatically change account or branch protection settings.

## Boundaries and design decisions

The demo application intentionally has no external dependencies. Positive dependency detection is proven using a generated Django 2.2.0 manifest. No dependency scanner can find vulnerabilities in packages it does not recognize; unpinned and unsupported manifests need separate review.

Archive SHA256 digests are pinned in the installer from official release metadata, so a later substituted download is rejected. This does not independently verify build provenance. Tool updates require reviewing official release notes and rerunning acceptance tests. Versions are fixed in the installer; Dependabot maintains Actions references only.

The workflow executes PR code in an isolated GitHub-hosted runner with a read-only token. It deliberately uses `pull_request`, never `pull_request_target`, and passes no deployment secrets. Do not add privileged credentials to these jobs.

See [triage and exceptions](docs/triage.md), [credential rotation](docs/credential-rotation.md), [demo walkthrough](docs/demo.md), and [verification status](docs/verification.md).

## Official references

- https://github.com/gitleaks/gitleaks
- https://trivy.dev/docs/latest/guide/target/filesystem/
- https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
