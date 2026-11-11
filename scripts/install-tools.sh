#!/usr/bin/env bash
set -euo pipefail
# Linux x86_64; downloads only official release assets and checks SHA256.
[[ "$(uname -s)-$(uname -m)" == Linux-x86_64 ]] || { echo "Requires Linux x86_64" >&2; exit 2; }
root="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$root/.tools/bin"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
install_release() {
  local repo="$1" version="$2" archive="$3" expected_sha="$4" binary="$5"
  local base="https://github.com/$repo/releases/download/v$version"
  curl --fail --location --connect-timeout 15 --max-time 180 --retry 3 "$base/$archive" -o "$tmp/$archive"
  python3 - "$tmp/$archive" "$expected_sha" <<'VERIFY'
import hashlib, pathlib, sys
archive = pathlib.Path(sys.argv[1])
expected = sys.argv[2]
if hashlib.sha256(archive.read_bytes()).hexdigest() != expected:
    raise SystemExit('Release checksum mismatch or missing entry')
VERIFY
  tar -xzf "$tmp/$archive" -C "$tmp" "$binary"
  install -m 0755 "$tmp/$binary" "$root/.tools/bin/$binary"
}
install_release gitleaks/gitleaks 8.30.1 gitleaks_8.30.1_linux_x64.tar.gz 551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb gitleaks
install_release aquasecurity/trivy 0.76.1 trivy_0.76.1_Linux-64bit.tar.gz c7cbe3137fb8a48a17574bede3dd6beb16742d1e9772929940fc90082c39d9c0 trivy
"$root/.tools/bin/gitleaks" version
"$root/.tools/bin/trivy" --version
