# Credential exposure response

1. Record the finding and limit further exposure. Preserve redacted evidence and coordinate with the credential owner.
2. Revoke the exposed credential promptly; if service continuity requires a replacement first, coordinate the shortest possible overlap.
3. Create a least-privilege replacement in the provider console or secret manager. Store it in the deployment secret store, never in source control, workflow YAML, logs, or issue text.
4. Update consumers, deploy, verify health, and confirm the old credential is disabled.
5. Review provider audit logs from the earliest possible exposure until revocation for unexpected use. Escalate suspected misuse through incident response.
6. Remove the secret from current files. Coordinate history cleanup where needed; rewriting history alone does not revoke a credential. Check forks, logs, artifacts, caches, and downstream copies according to the exposure scope.
7. Rescan, document revocation and service validation, and close with the owner. Full-history scanning may continue to flag historical revoked values: use reviewed exact fingerprints only after response is complete, or coordinate history cleanup.

The project uses synthetic values only. No real credential rotation or provider-account changes have been performed.
