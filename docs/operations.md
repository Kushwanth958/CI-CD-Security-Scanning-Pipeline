# Setup, Operation, and Troubleshooting

## Prerequisites

Linux x86_64, Bash, Git, Python 3.11 or newer, GNU Make, curl, and tar. Internet access is required for official release archives and the Trivy database. On Windows, use a suitable Linux environment such as WSL; the installer does not support native Windows or ARM platforms.

## Initial setup

```sh
git clone https://github.com/Kushwanth958/CI-CD-Security-Scanning-Pipeline.git
cd CI-CD-Security-Scanning-Pipeline
make tools
make test
make scan
make verify
```

`make scan` requires Git history. Tool binaries are installed in `.tools/bin`; generated reports go to `reports/`. Both directories are ignored by Git. Do not add live credentials to test detection.

## Commands and outputs

| Command | Purpose | Expected clean result |
| --- | --- | --- |
| `make tools` | Install fixed scanner versions after digest verification | Both versions printed |
| `make test` | Five standard-library regression tests | All tests pass |
| `bash scripts/scan.sh secrets` | Scan fetched Git history | Exit 0; `reports/gitleaks.json` |
| `bash scripts/scan.sh vulnerabilities` | Scan recognized dependency manifests | Exit 0; `reports/trivy.json` |
| `make scan` | Run both production scans | Exit 0 only if both pass |
| `make verify` | Six real-scanner acceptance cases | Exit 0; `reports/detection-tests.json` |

Individual scanners are configured to return 10 for findings; any unexpected nonzero result is also a failure. The aggregate `all` shell command returns a nonzero combined status when either scan fails and is not designed to preserve the individual scanner's exact code. Operational errors must be investigated separately from security findings.

## GitHub Actions

Push to main or open a PR to run automatically. For a manual run, open **Actions → Security pipeline → Run workflow**. Check **Security checks**, inspect failed steps, then download **security-reports** from the run summary. Treat reports according to their contents, even with secret values redacted: paths and vulnerability details may still be sensitive in a private project.

Raw artifacts expire after seven days. The checked-in evidence file records one verified baseline; it does not update automatically or replace per-run artifacts.

## Merge policy

In repository settings, create or update a main-branch ruleset requiring PRs and the **Security checks** status. Review who can bypass it. This setup is not performed by the workflow, and no merge-blocking enforcement is claimed by this lab.

## Troubleshooting

| Symptom | Check and resolution |
| --- | --- |
| Binary download fails | Confirm GitHub release access, proxy policy, and release existence; retain the failure |
| Checksum mismatch | Stop; investigate the release and approved digest before any change |
| Unsupported platform | Use Linux x86_64 locally or the configured hosted runner |
| Trivy DB download fails | Confirm access to the reported database registry; rerun after connectivity is restored |
| No package findings | Confirm the manifest is supported and contains pinned dependencies; use `make verify` as the positive control |
| `site-packages` license warning | This lab scans manifests without installing packages; license scanning is outside scope |
| Historical secret still detected | Confirm revocation and follow the rotation/history-cleanup procedure; deleting only the latest value is insufficient |
| Seeded acceptance case fails | Check tool versions, config parsing, expected exit 10, report rule/package, and database availability |
| Older run cancelled | Same-reference concurrency cancels superseded runs; inspect the latest commit's run |
| Actions runtime deprecation warning | Review the automated action-update PRs and their checks before upgrading; do not remove digest pinning |

## Maintenance

Review dependency-update PRs, official scanner releases, the weekly run, and report-retention needs. For scanner upgrades, review release notes, update version and digest together in the installer, rerun both unit and acceptance tests, then update the evidence record with the new commit and run. Keep historical evidence identified by date and source run; never relabel old results as a new execution.
