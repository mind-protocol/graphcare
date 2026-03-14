# Service 5: Emergency Response Protocols

## Incident Levels
- **SEV-1:** Security breach or production outage.
- **SEV-2:** Major degradation with user impact.
- **SEV-3:** Localized issue or non-critical failure.

## Standard Response Flow
1. Detect and classify severity.
2. Assign incident commander and comms owner.
3. Contain blast radius (rate-limit, key revoke, isolate service).
4. Recover service with validated rollback/fix.
5. Verify system health and data integrity.
6. Publish post-incident report within 24h.

## Required Artifacts
- Incident timeline (UTC)
- Impacted orgs/systems
- Mitigations applied
- Evidence links (logs, dashboards, audit records)
- Follow-up actions with owner/date

## Communications
- Internal update every 30 minutes for SEV-1/2.
- External client update cadence agreed in SLA.
