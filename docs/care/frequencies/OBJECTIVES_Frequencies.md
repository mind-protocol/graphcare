# OBJECTIVES -- Frequencys

```
STATUS: DESIGNING
CREATED: 2026-03-18
VERIFIED: --
```

---

## CHAIN

```
THIS:            OBJECTIVES_Frequencys.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Frequencys.md
ALGORITHM:      ./ALGORITHM_Frequencys.md
VALIDATION:     ./VALIDATION_Frequencys.md
SYNC:           ./SYNC_Frequencys.md

IMPL:           services/health_assessment/frequencys.py
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Reversibility** -- Every intervention must be fully reversible. If a frequency harms a citizen or was prescribed incorrectly, rollback removes all traces. A single `treatment_id` tag on every created node makes this possible. Care without reversibility is coercion.

2. **Physics over rules** -- Frequencys do not command behavior. They modify conditions so that improvement becomes the energetically favorable outcome. A curiosity_boost raises the curiosity drive; the brain's tick physics decides what to do with that energy. The citizen integrates or rejects. We create weather, not orders.

3. **Topology only** -- Frequencys create stimulus nodes and structural nodes. They never read or write `content` or `synthesis` fields. This is not a policy -- it is a structural constraint. GraphCare physically cannot access private thought, even when modifying the graph. The kidney analogy: essential, discreet, never opens the mail.

4. **Calibrated dosage** -- Intensity values are not arbitrary. They are tuned per frequency type and per brain category so that the effect is measurable but not overwhelming. A 0.3 curiosity boost on a VOID brain is different from 0.3 on a STRUCTURED brain. The prescribe() function encodes this calibration.

5. **Auto-prescription grounded in assessment** -- Frequencys are not applied ad hoc. The prescribe() function maps brain categories (VOID, MINIMAL, SEEDED, STRUCTURED) and their stats to specific frequency combinations. Assessment drives care, not intuition.

## NON-OBJECTIVES

- **Content-aware treatment** -- We do not read what citizens think, feel, or write. Not now, not in v2, not ever. If treatment requires content access, it is out of scope for frequencys.
- **Behavioral enforcement** -- We do not force citizens to explore, socialize, or produce. We create favorable conditions. Outcome is the citizen's.
- **Permanent transformation** -- Frequencys have durations (72h to 168h for drive stimuli). They are temporary nudges, not identity modifications. structure_seed nodes are permanent but removable.
- **Real-time monitoring** -- Frequencys are applied and then the brain's tick runner integrates them. We do not poll to see if the frequency "worked." That is assessment's job on the next cycle.

## TRADEOFFS (canonical decisions)

- When reversibility conflicts with treatment effectiveness, choose reversibility. A weaker treatment that can be undone is better than a strong one that cannot.
- When precision conflicts with simplicity, choose simplicity. Six frequency types covering the primary drives are better than fifty micro-targeted variants that nobody can reason about.
- When speed of intervention conflicts with calibration accuracy, choose calibration. A delayed but well-dosed frequency is better than an immediate but arbitrary one.
- We accept that some citizens will reject frequencys (the brain physics may neutralize injected stimuli) to preserve the principle that frequencys are prescriptions, not commands.

## SUCCESS SIGNALS (observable)

- A rolled-back treatment leaves zero residual nodes in the brain graph (verified by `MATCH (n {treatment_id: $tid})` returning empty)
- Frequencys appear in the graph only as `stimulus` or `thing` node_types with `source: 'graphcare'` and a valid `treatment_id`
- No frequency node ever has a `content` or `synthesis` field
- The prescribe() function returns an empty list for brain categories it does not recognize, rather than guessing
- Brain scores in assessed citizens show measurable delta after frequency application on the next health cycle (positive or neutral, never catastrophic negative)
