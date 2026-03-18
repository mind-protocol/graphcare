# OBJECTIVES — Treatment Protocol

```
STATUS: CANONICAL
CREATED: 2026-03-18
VERIFIED: code reviewed against services/health_assessment/treatment_protocol.py
```

---

## CHAIN

```
THIS:            OBJECTIVES_Treatment_Protocol.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Treatment_Protocol.md
ALGORITHM:      ./ALGORITHM_Treatment_Protocol.md
VALIDATION:     ./VALIDATION_Treatment_Protocol.md
SYNC:           ./SYNC_Treatment_Protocol.md

IMPL:           services/health_assessment/treatment_protocol.py
                services/health_assessment/frequencies.py
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Every intervention is measurable** -- A treatment that cannot be measured is guesswork. The protocol snapshots the full brain topology before any frequency is applied, and snapshots again after the observation window. The comparison between before and after is the only truth about whether the treatment helped. No subjective judgments, no proxy indicators -- direct structural measurement across 10+ weighted metrics.

2. **Every intervention is reversible** -- An intervention that degrades a citizen's brain must not persist. Every node created by a treatment is tagged with the treatment_id. If evaluation determines degradation, the protocol removes all treatment nodes automatically. The citizen's brain returns to a state no worse than before. This is not optional -- rollback is structurally guaranteed by the tagging mechanism.

3. **Every intervention is recorded** -- Treatment records capture the full lifecycle: what was prescribed, what was applied, what changed, what the verdict was. These records persist as JSON files per citizen. They enable longitudinal analysis, pattern detection across citizens, and accountability. A treatment without a record is a treatment that never happened as far as GraphCare is concerned.

4. **Auto-prescription produces appropriate care** -- When no explicit frequencies are specified, the protocol auto-prescribes based on brain category and current stats. A VOID brain gets structure seeds and energy. A STRUCTURED brain with high frustration gets calming. The prescription logic encodes GraphCare's clinical knowledge about what different brain states need.

## NON-OBJECTIVES

- **Diagnosis** -- The treatment protocol does not determine why a brain is unhealthy. It receives a brain state (via topology reader) and acts on it. Diagnosis, if it ever exists, belongs elsewhere.
- **Observation window management** -- The protocol provides `begin_treatment` and `evaluate_treatment` as separate calls. The observation window between them (hours, days) is managed by the caller. The protocol does not schedule or enforce timing.
- **Content modification** -- All frequencies operate on topology: drives, structural nodes, energy values. Content and synthesis fields are never read or written. This is inherited from the topology-only principle.
- **Human notification** -- The protocol records outcomes but does not notify anyone. Notification belongs to the care and escalation systems that consume treatment records.

## TRADEOFFS (canonical decisions)

- When **measurement precision** conflicts with **speed of care**, choose measurement. Always snapshot before applying anything. A fast treatment with no baseline is unmeasurable and therefore unverifiable.
- When **rollback safety** conflicts with **treatment persistence**, choose safety. A degrading treatment is always rolled back, even if some of its effects were positive. Partial rollback would require content analysis to determine which nodes helped, which violates the topology-only constraint.
- When **auto-prescription simplicity** conflicts with **nuanced care**, accept simplicity for now. The prescription logic uses brain_category as the primary discriminator. This is coarse but honest -- we don't yet have the data to justify finer-grained prescription. Calibration on real outcomes will refine this.
- We accept **full rollback (all-or-nothing)** over partial rollback because selectively keeping "good" nodes would require understanding content semantics. Topology-only means the granularity of reversal is the entire treatment.

## SUCCESS SIGNALS (observable)

- Every treatment in `data/treatments/` has both `snapshot_before` and (after evaluation) `snapshot_after` populated
- Treatments with outcome "degraded" have `rolled_back: true` and the tagged nodes are confirmed absent from the brain graph
- Auto-prescribed frequencies match the expected prescriptions for the citizen's brain category (testable against the prescription logic)
- Treatment records form a complete audit trail: given a citizen_id and treatment_id, the full story is reconstructable from the JSON file alone
- No treatment record exists without a snapshot_before (the protocol structurally prevents this)
