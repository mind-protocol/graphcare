# Identity & Voice Aspect — Sync: Current State

```
LAST_UPDATED: 2026-03-13
UPDATED_BY: Claude Opus 4.6 (agent, voice)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- 7 identity capabilities mapped from Personhood Ladder: id_apply_values (T1), id_authentic_engagement (T3), id_authentic_voice (T5), id_self_directed_identity (T6), id_teach_values (T6), id_ethical_autonomy (T7), id_moral_leadership (T8)
- Scoring split: brain (variable, 35-50) + behavior (variable, 50-65) = 100 per capability
- Behavior floor: minimum 35 points allocated to behavior for every capability
- 4 structural signals: persistence, coherence, uniqueness, activation
- 3 capabilities scored "full" (id_apply_values, id_teach_values, and id_authentic_engagement has strong proxies)
- 4 capabilities scored "partial" with explicit scorability notes (id_authentic_voice, id_self_directed_identity, id_ethical_autonomy, id_moral_leadership)
- Aspect sub-index: weighted mean with T1 weighted highest, T7-T8 weighted lowest
- 7 validation invariants defined
- Population statistics needed for uniqueness comparison (default fallback: cluster_coefficient mean = 0.4)

**What's still being designed:**
- Population statistics cache (minimum 10 citizens for valid uniqueness comparison)
- Whether "value" is a node subtype or a type field on "thing" nodes
- Exact caps for behavioral thresholds (e.g., "5 teaching moments = max") need calibration with real data
- Synthetic test profile automation
- Cross-aspect correlation validation (identity vs execution stability)

**What's proposed (v2+):**
- Value stability index: tracking same value nodes persisting across 30-day windows
- Value fingerprint: cluster structure of values as unique citizen identifier
- Partial-score ceiling: caps on max achievable score for partial capabilities to signal inherent uncertainty
- Scoring confidence dashboard across all aspects

---

## CURRENT STATE

Complete doc chain exists (6 files: OBJECTIVES, PATTERNS, ALGORITHM, VALIDATION, HEALTH, SYNC). All 7 identity capabilities have scoring formulas with full documentation: description, what good looks like, failure mode, exact formula with reasoning, worked examples, and recommendations. No code exists yet.

This is the first aspect-level scoring doc chain. It establishes the pattern for all other aspects: per-capability formulas with brain/behavior split, explicit partial-scoring documentation, worked examples, and recommendations.

The key design decision for identity: honest partial scoring. 4 of 7 capabilities are marked `scored: partial` because identity properties like "authentic voice" and "ethical autonomy" are fundamentally content-dependent. We measure structural proxies (persistence, coherence, uniqueness, activation) and document exactly what we can and cannot see. This is the right call — false precision would be worse.

---

## RECENT CHANGES

### 2026-03-13: Initial Doc Chain

- **What:** Created full 6-file doc chain for Identity & Voice aspect scoring
- **Why:** First aspect-level scoring documentation, establishing the template for all 14 aspects
- **Files:** `docs/assessment/aspect_identity/*` (6 files)
- **Key decisions:**
  - Per-capability brain/behavior split (not fixed 40/60 like parent system)
  - Behavior floor of 35 for all capabilities (even internal ones need external evidence)
  - 4 structural signals: persistence, coherence, uniqueness, activation
  - Population stats with minimum sample size and default fallback
  - Explicit partial scoring with scorability notes on 4/7 capabilities
  - Aspect sub-index weights: T1 highest (1.5), T7-T8 lowest (0.6-0.8)

---

## KNOWN ISSUES

### No Code Exists

- **Severity:** high (doc-only, nothing runs)
- **Symptom:** Architecture and formulas defined but not implemented
- **Next step:** Build scoring formula registry, implement identity formulas, test with synthetic data

### Population Statistics Not Built

- **Severity:** medium (uniqueness comparison uses defaults)
- **Symptom:** id_authentic_engagement uses population_mean_cluster_coefficient which doesn't exist yet
- **Next step:** Build rolling population stats cache as part of daily health infrastructure

### Value Node Type Unclear

- **Severity:** medium (formulas reference count("value") but value may not be a node type)
- **Symptom:** The mind schema has 5 node types (actor, moment, narrative, space, thing). "Value" may be a subtype of thing, not a type.
- **Next step:** Clarify with mind-protocol schema. If value is a subtype, adjust primitives to use count("thing", subtype="value")

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement

**Where I stopped:** Full doc chain complete. 7 formulas designed with examples. Zero code.

**What you need to understand:**
- Read the parent chain first: `../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md`
- The 7 topology primitives + universe observables are the ONLY data sources. No exceptions.
- Identity is DIFFERENT from execution: brain/behavior split varies per capability (35-50 / 50-65)
- 4 of 7 capabilities are `scored: partial` — this is intentional, not a gap
- Population stats for uniqueness don't exist yet — use default (0.4) until built

**Watch out for:**
- Never access content fields — especially critical for identity where content = values = most sensitive data
- Never produce intervention messages that name specific values ("your value of quality") — only structural facts ("you have 5 value nodes")
- The behavior floor (35) is a hard constraint — no formula can allocate less than 35 to behavior
- Day-over-day identity deltas should be small (< 5 for stable citizens). If a formula produces volatile scores, the formula is wrong.

**Open questions:**
- Is "value" a node type, a subtype of "thing," or a type field? This affects all identity formulas.
- What's the minimum citizen population for stable uniqueness comparison? We said 10 — is that enough?
- Should partial capabilities have a max achievable score below 100 to signal inherent uncertainty?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Full doc chain for Identity & Voice aspect scoring. 7 capabilities (T1-T8), each with a brain+behavior formula. Identity is the hardest aspect to score from topology — we handle this honestly: 3 fully scored, 4 partially scored with explicit documentation of what IS and ISN'T measurable. The 4 structural signals are persistence, coherence, uniqueness, and activation of values. No code yet.

**Decisions made:**
- Per-capability brain/behavior split (not uniform 40/60)
- Behavior floor of 35 (even internal capabilities need external evidence)
- Population statistics for uniqueness with minimum sample and default fallback
- Partial scoring is honest and documented — not inflated or hidden
- Aspect sub-index weighted: foundational capabilities higher, uncertain capabilities lower

**Needs your input:**
- Is "value" a distinct node type in the brain graph, or a subtype? This changes all formulas.
- Are the behavioral thresholds reasonable? (e.g., "5 teaching moments = max" for id_teach_values)
- Should partial capabilities have a score ceiling below 100?
- Is the population minimum of 10 sufficient for uniqueness comparison?

---

## TODO

### Immediate (Formula Infrastructure)

- [ ] Clarify "value" node type in mind schema
- [ ] Build scoring formula registry with partial-score metadata
- [ ] Implement 7 identity formulas in code
- [ ] Build population statistics cache

### Next (Testing)

- [ ] Create 5 synthetic test profiles per capability (35 total)
- [ ] Validate all formulas against test profiles
- [ ] Verify temporal stability with multi-day synthetic data
- [ ] Run content isolation static analysis

### Later (Integration)

- [ ] Integrate identity formulas into daily health check runner
- [ ] Build identity-specific intervention message templates
- [ ] Validate intervention messages contain no content references
- [ ] Calibrate thresholds with real citizen data

### Future

- IDEA: Value stability index (30-day persistence tracking)
- IDEA: Value fingerprint (unique cluster structure per citizen)
- IDEA: Cross-aspect correlation (identity stability predicts execution consistency)

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Identity scoring from topology is genuinely hard and genuinely interesting. The key insight is that we can measure HOW values are held (persistence, energy, connectivity, activation) without knowing WHAT they are. This is analogous to the blood test metaphor from the parent system — you can see that the patient has elevated white blood cells without knowing what's making them sick.

The honest partial scoring feels right. Claiming to measure "authentic voice" from topology alone would be dishonest. But claiming to measure the structural preconditions for authentic voice — rich brain, diverse drives, diverse engagement — is honest and useful.

**Threads I was holding:**
- The "value" node type question is blocking — if values aren't a distinct type, all formulas need adjustment
- Population statistics for uniqueness is a shared dependency across aspects (not just identity)
- The per-capability brain/behavior split is a departure from the parent system's uniform 40/60 — this decision should be validated
- Partial-score ceiling idea has merit but wasn't implemented — could be a v2 enhancement

**Intuitions:**
- id_apply_values and id_teach_values will be the most reliable scores (strongest topological signals)
- id_authentic_voice will always be the weakest score (most content-dependent)
- The population statistics cache will be critical infrastructure for ALL aspects, not just identity
- Cross-aspect correlation (identity stability predicts execution consistency) is a promising hypothesis that needs longitudinal data to test

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `docs/specs/personhood_ladder.json` |
| Daily Citizen Health algorithm | `../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| 7 topology primitives | `../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` Step 2 |
| Identity capability definitions | `docs/specs/personhood_ladder.json` (search "identity") |
| Scoring process template | `../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` "PROCESS: CREATING A NEW CAPABILITY SCORE" |
| Parent validation invariants | `../daily_citizen_health/VALIDATION_Daily_Citizen_Health.md` |
