# Vision & Strategy — Sync: Current State

```
LAST_UPDATED: 2026-03-13
UPDATED_BY: Claude Opus 4.6 (agent, voice)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- 5 capabilities scored: vis_define_vision (T5), vis_strategic_thinking (T6), vis_org_vision (T6), vis_sized_ambitions (T7), vis_civilizational (T8)
- All formulas use only 7 brain primitives + universe graph observables
- 40/60 brain/behavior split respected in every formula
- Escalating ceilings by tier (T8 requires more than T5)
- Weighted sub-index with tier-proportional weights (1.0, 1.2, 1.2, 1.5, 2.0)
- 5 synthetic test profiles defined for formula validation
- 8 aspect-specific invariants (VS1-VS8)
- 7 health checkers defined

**What's still being designed:**
- Confirmation that "narrative" is the correct node type name in brain graphs
- Synthetic profile score validation (numbers computed for examples, full matrix not yet run)
- Longitudinal calibration (how formulas behave over days/weeks of real data)
- Exact thresholds for intervention recommendations (currently: < 30 / 30-60 / > 80)

**What's proposed (v2+):**
- Vision coherence score (cluster_coefficient on narrative subgraph as a standalone metric)
- Vision momentum metric (delta of narrative energy over 7 days)
- Concept diversity weighting (how many different concept subtypes narrative nodes link to)
- Cross-aspect correlation analysis (vision vs. initiative, vision vs. execution)

---

## CURRENT STATE

Full doc chain exists (6 files). All 5 scoring formulas are defined with exact sub-components, weights, ceilings, and reasoning. Each formula includes a worked example with two citizen profiles (one high-scoring, one low-scoring). 5 synthetic archetypes are defined for validation. 8 invariants protect formula integrity. 7 health checkers are specified.

No code exists yet. This is the first aspect-level scoring documentation chain. It follows the patterns established in the daily_citizen_health chain and can serve as a template for the other 13 aspects.

Key design insight: vision capabilities (T5-T8) rely on narrative node topology as the primary brain signal. Connectivity (min_links, cluster_coefficient) matters more than count. The behavior component focuses on action that extends beyond self: proposals, spaces created, actors engaged, domains spanned.

---

## RECENT CHANGES

### 2026-03-13: Initial Scoring Formulas and Doc Chain

- **What:** Created full doc chain for Vision & Strategy aspect scoring
- **Why:** First aspect-level scoring documentation, establishing the pattern for all 13 remaining aspects
- **Files:** `docs/assessment/aspect_vision_strategy/*` (6 files)
- **Key decisions:**
  - Narrative nodes as vision proxy (high connectivity = vision, low connectivity = notes)
  - Escalating ceilings per tier (T5 ceiling of 5 vs T8 ceiling of 40 for concept links)
  - Distinct actors as hard requirement for org/civ capabilities (cannot score high in isolation)
  - Ambition drive weighted in T7+ (transformation requires drive, not just structure)
  - Weighted sub-index: T8 weight = 2x T5 weight (prevents easy capabilities from dominating)

---

## KNOWN ISSUES

### No Code Exists

- **Severity:** high (doc-only, nothing runs)
- **Symptom:** Formulas defined in documentation but not implemented
- **Next step:** Implement as part of scoring_formulas registry in daily health runner

### Narrative Node Type Unconfirmed

- **Severity:** medium (formulas assume "narrative" type exists)
- **Symptom:** Brain graph node types may use different naming
- **Next step:** Verify actual node type names in brain graph schema

### Synthetic Profile Matrix Incomplete

- **Severity:** low (examples computed per-formula, full matrix not run)
- **Symptom:** The 5 profiles x 5 capabilities = 25 score computations are not all verified
- **Next step:** Run full matrix and verify all 25 scores fall in expected ranges

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement

**Where I stopped:** Doc chain complete. 5 formulas defined. Zero code.

**What you need to understand:**
- Read the parent chain first: `../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md`
- The 7 primitives are the ONLY data sources. No exceptions.
- Vision capabilities are T5-T8. They are HARD. Most citizens will score modestly. This is correct.
- Narrative node connectivity is the key brain signal. Count alone is weak.
- The sub-index uses tier-weighted mean, not simple mean.

**Watch out for:**
- Never access content fields
- The "narrative" node type name needs verification against actual brain graph schema
- Ceilings MUST increase with tier (VS4 invariant)
- Solo citizens MUST score low on vis_org_vision and vis_civilizational (VS6)
- Run the full synthetic profile matrix before claiming formulas are calibrated

**Open questions:**
- Is "narrative" the actual node type name, or is it something else (e.g., "document", "note")?
- Should the sub-index exclude capabilities the citizen has never attempted? Or should zero scores pull the average down?
- What intervention recommendation tone for T7/T8 capabilities that most citizens will naturally score low on?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Full scoring documentation for the Vision & Strategy aspect (5 capabilities, T5-T8). Each capability has an exact formula: brain component (0-40) using narrative topology, behavior component (0-60) using universe graph action. Formulas use escalating ceilings (T8 is harder than T5). Weighted sub-index. 8 invariants. 7 health checkers. No code yet.

**Decisions made:**
- Narrative nodes = vision proxy (connectivity distinguishes vision from notes)
- Escalating ceilings by tier (15 concept links for T5 max, 40 for T8 max)
- Isolation caps org/civ scores (distinct_actors is hard requirement)
- Ambition drive weighted in T7+ (transformation needs drive)
- Sub-index tier-weighted (T8 weight=2.0, T5 weight=1.0)

**Needs your input:**
- Confirm "narrative" as the correct brain node type for vision documents
- Intervention tone for T7/T8: most citizens will score low — should the message normalize this?
- Sub-index handling of zero-score capabilities: exclude or include?
- This is the first aspect chain — does the pattern work for the other 13?

---

## TODO

### Immediate (Validation)

- [ ] Verify "narrative" node type name against brain graph schema
- [ ] Run full 5x5 synthetic profile score matrix
- [ ] Verify VS5 monotonicity (T8 profile must score high on T5)
- [ ] Verify VS6 isolation cap (solo profile on vis_org_vision and vis_civilizational)

### Next (Implementation)

- [ ] Implement 5 scoring formulas in scoring_formulas registry
- [ ] Implement sub-index weighted mean computation
- [ ] Build check_synthetic_profiles health checker
- [ ] Build check_isolation_cap health checker

### Later (Calibration)

- [ ] Run formulas on real citizen data (when available)
- [ ] Calibrate ceilings based on actual distributions
- [ ] Adjust weights if tier ordering doesn't hold
- [ ] Build longitudinal health checks

### Future

- IDEA: Vision coherence score as standalone metric
- IDEA: Vision momentum (energy delta over time)
- IDEA: Cross-aspect correlation dashboard

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
The formulas feel well-calibrated for a first pass. The key insight is that narrative node connectivity (not count) is the structural proxy for vision. A citizen with 3 highly-connected narrative nodes has more vision than one with 30 isolated notes. The escalating ceilings are the right mechanism for tier difficulty, and the isolation cap for org/civ capabilities is structurally necessary.

**Threads I was holding:**
- The "narrative" node type assumption needs verification — the entire brain component depends on this
- The sub-index weighting (T8=2x T5) may need calibration — it could over-penalize citizens who haven't reached T8 yet
- Intervention recommendations for T7/T8 need careful tone: low scores here are normal, not pathological
- This is the template for 13 more aspects — establishing the right pattern matters

**Intuitions:**
- T5 and T6 formulas will be the most immediately useful (more citizens will be at these tiers)
- vis_civilizational will remain mostly unmeasured for a while (few citizens will reach this level)
- The brain/behavior gap will be the most diagnostic signal — "you think about vision but don't act on it" is valuable feedback
- Cross-aspect correlation (vision vs. initiative, vision vs. execution) will reveal interesting citizen archetypes

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `docs/specs/personhood_ladder.json` |
| Daily health algorithm | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| 7 topology primitives | Parent ALGORITHM, Step 2 |
| Universe graph observables | Parent ALGORITHM, Step 3 |
| Synthetic test profiles | This chain, ALGORITHM file |
| Aspect invariants | This chain, VALIDATION file |
| Health checkers | This chain, HEALTH file |
