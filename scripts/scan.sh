#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
export PATH="$root/.tools/bin:$PATH"
mkdir -p reports
case "${1:-all}" in
  secrets)
    # Scan complete checked-out history; checkout must use fetch-depth: 0.
    gitleaks git . --config .gitleaks.toml --redact=100 --exit-code 10       --report-format json --report-path reports/gitleaks.json ;;
  vulnerabilities)
    # Scan all project manifests, including any subsequently added outside app/.
    trivy fs --scanners vuln --severity HIGH,CRITICAL --exit-code 10       --skip-dirs .git --skip-dirs .tools --skip-dirs reports       --format json --output reports/trivy.json . ;;
  all)
    secret_rc=0; vuln_rc=0
    bash scripts/scan.sh secrets || secret_rc=$?
    bash scripts/scan.sh vulnerabilities || vuln_rc=$?
    (( secret_rc == 0 && vuln_rc == 0 )) ;;
  *) echo 'Usage: bash scripts/scan.sh [all|secrets|vulnerabilities]' >&2; exit 2 ;;
esac
