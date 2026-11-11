# Alert validation and false-positive handling

1. Open the failed Actions run and download the report. Record the commit, file, line, rule or CVE, and scanner version. Do not paste raw secret values into tickets.
2. For a secret, determine whether it was ever valid using ownership records. Do not authenticate with a suspected exposed credential. Treat uncertain credentials as exposed and follow the rotation runbook.
3. For a dependency, verify the installed version, advisory, affected range, fixed version, runtime use, and exploitability. Update the manifest and lockfile together, rerun application tests, then rescan.
4. Mark a false positive only with evidence: public documentation sample, a non-secret identifier, or an advisory that does not apply. A credential being expired is not a false positive.
5. Any exception needs an owner, ticket, exact rule/CVE and file/package scope, rationale, compensating controls, approver, and expiry. Review before expiry and remove the exception when resolved.

## Secret suppression

Production has no allowlist. The acceptance test builds an isolated temporary config with an exact rule, path, and value combined with AND. It then verifies a different credential in the same file still fails. Never allowlist an entire application directory or turn off built-in rules to make CI pass.

## Vulnerability exceptions

No `.trivyignore` is provided. Prefer remediation. If the organization approves a time-limited exception, add the smallest supported ignore entry, record the decision in a reviewed PR, and add expiry enforcement before adopting the exception in production. This lab does not implement automated exception expiry.

## Example record (template, not a completed incident)

- Ticket / owner / approver:
- Finding / commit / affected file:
- Validation evidence:
- Decision and remediation:
- Exception scope, compensating controls, expiry (if applicable):
- Rescan evidence and closure time:
