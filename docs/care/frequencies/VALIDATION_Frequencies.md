# Frequencys -- Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-18
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Frequencys.md
PATTERNS:        ./PATTERNS_Frequencys.md
ALGORITHM:       ./ALGORITHM_Frequencys.md
THIS:            VALIDATION_Frequencys.md (you are here)
SYNC:            ./SYNC_Frequencys.md

IMPL:            services/health_assessment/frequencys.py
```

---

## PURPOSE

**Validation = what we care about being true.**

Not mechanisms. Not test paths. Not how things work.

What properties, if violated, would mean the frequencys system has failed its purpose?

These are the value-producing invariants -- the things that make frequencys trustworthy as a care mechanism. A frequency system that cannot be rolled back, or that leaks content, or that creates untagged nodes, has failed regardless of whether individual frequency types work correctly.

---

## INVARIANTS

### V1: Every Intervention Is Reversible

**Why we care:** Without reversibility, frequencys are irreversible modifications to a citizen's brain. A bad prescription or a bug becomes permanent damage. Reversibility is what separates care from coercion.

```
MUST:   Every node created by apply_frequency carries a treatment_id property
        matching the treatment_id argument.
MUST:   rollback_treatment(handle, tid) deletes ALL nodes with that treatment_id
        and ONLY those nodes.
MUST:   After rollback, MATCH (n {treatment_id: $tid}) returns zero results.
NEVER:  A frequency node exists without a treatment_id property.
NEVER:  rollback_treatment deletes a node that was not created by the matching treatment.
```

### V2: Content Privacy Is Structurally Enforced

**Why we care:** GraphCare's credibility depends on the guarantee that it cannot access citizen thoughts. If a frequency node contains content or synthesis fields, even accidentally, the privacy contract is broken. This is not a policy violation -- it is a structural failure.

```
MUST:   No node created by apply_frequency has a 'content' field.
MUST:   No node created by apply_frequency has a 'synthesis' field.
MUST:   apply_frequency never executes a MATCH query that reads content or synthesis
        from existing nodes.
NEVER:  A Cypher query in frequencys.py references the content or synthesis property
        on any node (created or existing).
```

### V3: All Frequency Nodes Are Identifiable

**Why we care:** If frequency-created nodes are indistinguishable from citizen-created nodes, we lose the ability to audit what GraphCare has done, rollback treatments, and verify that interventions are contained. Identifiability is the foundation of accountability.

```
MUST:   Every frequency-created node has source: 'graphcare'.
MUST:   Every frequency-created node has frequency_type set to a valid catalog key.
MUST:   Every frequency-created node has created_at set to the creation timestamp.
MUST:   Drive stimulus nodes have node_type: 'stimulus' and type: 'frequency'.
MUST:   Structural nodes have node_type: 'thing' and a valid type field
        (desire, concept, value, process).
NEVER:  A frequency-created node has node_type outside of {'stimulus', 'thing'}.
```

### V4: Prescription Fails Safe

**Why we care:** An incorrect prescription is worse than no prescription. If prescribe() encounters a brain category it does not recognize, it must return nothing rather than guess. Silence is safer than noise when modifying someone's brain.

```
MUST:   prescribe() returns an empty list for any brain_category not in
        {VOID, MINIMAL, SEEDED, STRUCTURED}.
MUST:   prescribe() returns only frequencys from CATALYST_CATALOG
        (no ad hoc Frequency construction).
NEVER:  prescribe() raises an exception for unknown input.
NEVER:  prescribe() returns a frequency type not defined in the catalog.
```

### V5: Dosage Stays Within Bounds

**Why we care:** An intensity value that is too high could overwhelm a brain's physics, causing erratic drive behavior or score instability. Conservative dosage is a safety constraint, not a tuning preference.

```
MUST:   Drive stimulus intensity values are in the range [-1.0, 1.0].
MUST:   Structural node energy values are in the range [0.0, 1.0].
MUST:   energy_infusion sub-drive intensities are strictly less than the primary
        intensity (ambition at 0.8x, social_need at 0.6x).
NEVER:  A frequency factory function returns intensity > 1.0 or < -1.0.
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | System purpose fails | Unusable |
| **HIGH** | Major value lost | Degraded severely |
| **MEDIUM** | Partial value lost | Works but worse |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Reversibility -- every treatment can be fully undone | CRITICAL |
| V2 | Content privacy -- frequency nodes never carry private data | CRITICAL |
| V3 | Identifiability -- frequency nodes are distinguishable and auditable | HIGH |
| V4 | Safe prescription -- unknown conditions get no treatment | HIGH |
| V5 | Dosage bounds -- intensity stays within safe range | MEDIUM |

---

## MARKERS

<!-- @mind:todo Write integration test: apply frequency, verify tags, rollback, verify zero residual -->
<!-- @mind:todo Write property test: no factory function in CATALYST_CATALOG produces intensity outside [-1.0, 1.0] -->
<!-- @mind:todo Verify V2 statically: grep frequencys.py for 'content' and 'synthesis' field references -->
<!-- @mind:proposition Consider adding V6: treatment_id uniqueness -- no two treatments share a treatment_id -->
