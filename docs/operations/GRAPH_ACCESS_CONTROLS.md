# Graph Access Controls

## Scope
Defines who can query GraphCare-managed graphs and under which conditions.

## Access Model
- **Public:** No direct graph access.
- **Client users:** Access only org-scoped views exposed by approved APIs.
- **GraphCare operators:** Access for operations and incident response, least-privilege.
- **Automation/service accounts:** Token-bound access with explicit scope.

## Enforcement Rules
1. All requests must include organization scope (`org` / `scope_ref`).
2. No cross-org query execution.
3. Admin query endpoints require API key and operation audit trail.
4. Emergency elevated access must be time-bounded and ticket-linked.

## Credentials & Rotation
- API keys are stored in environment secrets, never hardcoded.
- Rotation interval: every 90 days or immediately after incident.
- Revocation must be documented in incident timeline.

## Review Cadence
- Weekly: access review for active service accounts.
- Monthly: permission inventory and stale credential cleanup.
