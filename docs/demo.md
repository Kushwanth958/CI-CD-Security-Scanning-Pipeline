# Demonstration

1. Run `make tools`, then `make test`.
2. Run `make scan` on the clean checkout. The dependency-free app should have no package findings; the history must contain no secrets.
3. Run `make verify`. Inspect `reports/detection-tests.json`. Six cases must pass. The seeded secret and vulnerable manifest correctly produce findings while the harness exits successfully because detection was expected.
4. Push a branch and open a PR. Inspect **Security checks**, its job summary, and the report artifact.
5. To demonstrate a failing PR, add a `requirements.txt` containing `Django==2.2.0` under a temporary demo directory on an unmerged branch. Do not install it. The production Trivy gate should fail; remove the manifest and rerun. Close the demonstration PR afterward.
6. Enable the main ruleset requiring Security checks if you want failure to prevent merging.

Discuss in an interview: why full history matters, why scanner failures differ from findings, why fake fixtures are temporary, why a narrow exception needs a negative control, and why credential rotation precedes history cleanup.
