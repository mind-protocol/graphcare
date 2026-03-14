# GDPR Consent Validation

## Objective
Ensure client consent for graph processing is explicit, recorded, and auditable.

## Required Evidence
1. Signed consent document (client representative).
2. Timestamp of consent capture (UTC).
3. Scope of processing (graph name, data categories, retention policy).
4. Revocation contact and process.

## Validation Checklist
- [ ] Consent includes identified controller/processor roles.
- [ ] Processing scope matches actual data ingestion scope.
- [ ] Retention/deletion terms documented.
- [ ] Data subject rights workflow documented.
- [ ] Consent evidence stored in immutable location.

## Release Gate
Production ship for the client stays on HOLD until all checklist items are complete.
