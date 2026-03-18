# Communication & Coordination — Sync: Current State

```
LAST_UPDATED: 2026-03-13
UPDATED_BY: Claude Opus 4.6 (agent, voice)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- 11 communication capabilities from Personhood Ladder spec (T2 through T8)
- Scoring formula for each capability: brain (0-40) + behavior (0-60) = 100
- All formulas use only the 7 brain primitives + universe graph observables
- Communication sub-index: weighted mean with decreasing tier weights (T2=1.0 down to T8=0.2)
- regularity_score helper: days_with_moments / window_days
- Derived stats computed once, reused across formulas
- cap(x, c) normalization for all raw counts
- Confidence labels: High (T2-T5), Medium (T6), Low (T7-T8)

**What's still being designed:**
- Synthetic test profiles (5 per capability, 55 total)
- Exact space_type taxonomy (which space types count as "journal", "sync", "external", "publication")
- followers_in_initiated_spaces derivation (how to efficiently compute cross-actor space joining)
- references_to_initiated_spaces derivation (how to efficiently compute cross-actor linking)
- regularity_score edge case handling (0 moments, window_days=0)

**What's proposed (v2+):**
- Communication momentum metric (week-over-week change in comm_index)
- Cross-capability consistency flags (e.g., high T4 but low T2 = suspicious)
- Sensitivity analysis results informing weight adjustments
- Real-world calibration against human assessment of communication quality

---

## CURRENT STATE

Complete doc chain exists (6 files). All 11 communication capabilities have scoring formulas with brain and behavior components, examples, and recommendations. No code exists yet.

Key design decisions:
- Regularity is a first-class signal (not just volume)
- Channel breadth matters for notification (not just total notifications)
- Frustration inversion for ask-for-help (high frustration + few requests = silent suffering)
- Followers in initiated spaces as topology proxy for inspiration
- Decreasing tier weights in sub-index (foundations > pinnacles)
- Honest confidence labels for T6+ (Medium/Low)

Depends on: Daily Citizen Health ALGORITHM (parent module), Personhood Ladder spec, space_type taxonomy (not yet defined).

---

## RECENT CHANGES

### 2026-03-13: Initial Formulas and Doc Chain

- **What:** Created full doc chain for Communication & Coordination scoring
- **Why:** First aspect-level scoring documentation for the Personhood Ladder
- **Files:** `docs/assessment/aspect_communication/*` (6 files)
- **Key decisions:**
  - 11 formulas designed, all topology-only, all with 40/60 split
  - regularity_score as shared helper for consistency measurement
  - Derived stats computed once and reused
  - T2 capabilities weighted 1.0 in sub-index, T8 weighted 0.2
  - Confidence levels documented per capability (High/Medium/Low)
  - Each formula has: description, good/failure modes, formula table, pseudocode, example, recommendations

---

## KNOWN ISSUES

### No Synthetic Test Profiles

- **Severity:** high (formulas are designed but not numerically validated)
- **Symptom:** Examples exist in ALGORITHM but the 5 canonical profiles are not formally defined
- **Next step:** Define exact primitive values for 5 profiles, run all 11 formulas, verify ranges

### Space Type Taxonomy Undefined

- **Severity:** medium (formulas reference space_type values like "journal", "sync", "external" without a formal taxonomy)
- **Symptom:** Behavior stats depend on space_type filtering; if taxonomy changes, formulas break
- **Next step:** Define space_type taxonomy in a shared document, link from here

### T7-T8 Formula Confidence

- **Severity:** medium (acknowledged design limitation)
- **Symptom:** Global networking and influence are hard to measure from topology alone
- **Next step:** Accept current formulas as v1, plan for real-world calibration

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement

**Where I stopped:** All 11 formulas designed. Doc chain complete. Zero code.

**What you need to understand:**
- Read the Daily Citizen Health ALGORITHM first — it defines the 7 primitives and scoring framework
- Read the Personhood Ladder spec for exact capability definitions
- The derived stats section computes shared values once — implement this as a pre-computation step
- regularity_score is a shared helper used by multiple formulas — implement and test it first
- The cap(x, c) function is used everywhere — min(x, c) / c

**Watch out for:**
- V2 is critical: brain weights MUST sum to 40, behavior to 60, for every formula
- Never access content or synthesis fields
- regularity_score must handle edge cases: 0 moments, all moments on same day, window_days=0
- followers_in_initiated_spaces and references_to_initiated_spaces require cross-actor queries — may need optimization
- Space type filtering depends on a taxonomy that doesn't exist yet — define it or use provisional values

**Open questions:**
- How to efficiently compute followers_in_initiated_spaces? (needs cross-actor space query)
- What exactly counts as a "publication" space_type? (papers, blog posts, public analyses?)
- Should regularity_score use a different window for T5+ capabilities? (14 days might be too short for "regular interactions")
- Should the sub-index exclude capabilities the citizen hasn't reached yet? (e.g., exclude T6+ if aspect tier is T4)

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Complete scoring documentation for the Communication & Coordination aspect of the Personhood Ladder. 11 capabilities (T2-T8), each with a topology-only formula split into brain (0-40) and behavior (0-60). Sub-index uses decreasing tier weights. No code yet.

**Decisions made:**
- regularity_score as consistency metric (not just volume)
- Channel breadth for stakeholder notification (3 channels, not just total count)
- Frustration inversion for help-seeking (high frustration + low requests = bad)
- Followers in spaces as inspiration proxy
- Tier weights: T2=1.0, T3=0.9, T4=0.8, T5=0.7, T6=0.5, T7=0.3, T8=0.2
- Confidence levels: High (T2-T5), Medium (T6), Low (T7-T8)

**Needs your input:**
- Space type taxonomy: what space_type values exist? Which count as "journal", "sync", "external", "publication"?
- T7-T8 formulas: acceptable to have Low confidence, or should we mark them `scored: false` until real data validates?
- Sub-index: should capabilities above the citizen's current tier be excluded from the weighted mean?
- Regularity window: 14 days for all, or longer for higher tiers?

---

## TODO

### Immediate (Validation)

- [ ] Define 5 canonical synthetic profiles with exact primitive values
- [ ] Run all 11 formulas against synthetic profiles, verify ranges per V7
- [ ] Verify all weight sums (40 brain, 60 behavior) per V2

### Next (Infrastructure)

- [ ] Define space_type taxonomy (shared across all aspects)
- [ ] Implement regularity_score helper with edge case tests
- [ ] Implement cap() helper
- [ ] Implement derived stats pre-computation

### Later (Implementation)

- [ ] Implement all 11 capability scoring functions
- [ ] Implement communication sub-index weighted mean
- [ ] Register formulas in the scoring_formulas registry
- [ ] Run sensitivity analysis to identify overpowered/underpowered sub-signals

### Future

- IDEA: Communication momentum metric (week-over-week delta)
- IDEA: Cross-capability consistency flags
- IDEA: Real-world calibration session with human assessors

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `docs/specs/personhood_ladder.json` |
| Daily Citizen Health ALGORITHM | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| 7 Primitives reference | Daily Citizen Health ALGORITHM, Step 2 |
| Universe observables reference | Daily Citizen Health ALGORITHM, "Universe Graph Observables" |
| Scoring formula creation process | Daily Citizen Health ALGORITHM, "PROCESS: CREATING A NEW CAPABILITY SCORE" |
| This aspect's formulas | `./ALGORITHM_Communication.md` |
| Validation invariants | `./VALIDATION_Communication.md` |
| Health checks | `./HEALTH_Communication.md` |
