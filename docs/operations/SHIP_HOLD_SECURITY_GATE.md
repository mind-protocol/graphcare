# SHIP vs HOLD Security Gate Decision

## Decision
**Status:** HOLD

## Rationale
The referenced security audit artifact (`/home/mind-protocol/scopelock_security_audit.md`) is not versioned in this repository, so production ship cannot be justified from repository evidence alone.

## Exit Criteria to move from HOLD -> SHIP
1. Security audit report is attached to the repository (or linked in immutable storage).
2. Critical findings: 0 open.
3. High findings: explicit risk acceptance or remediated.
4. Data encryption at rest and in transit validated for FalkorDB path.
5. Access controls and query audit logging enabled and tested.
6. GDPR consent trail present for impacted client.

## Owner
GraphCare security/ops lead.

## Last Updated
2026-03-14
