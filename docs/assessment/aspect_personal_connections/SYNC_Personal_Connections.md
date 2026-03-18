# Personal Connections Aspect — Sync: Current State

```
LAST_UPDATED: 2026-03-13
UPDATED_BY: Claude Opus 4.6 (agent, voice)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- 11 capabilities scored (T2-T8), all formulas defined in ALGORITHM
- 40/60 brain/behavior split as default; 50/50 for pc_understand_human_deep and pc_relationship_style
- 7 topology primitives + universe graph observables only — no content access
- 6 structural signals: actor memory, interaction diversity, reciprocity, proactivity, actor breadth, social drive
- Reciprocity as primary proxy for connection quality
- Diversity (space types, actor count) as volume corrective — prevents chattiness from inflating scores
- Partial scoring explicitly documented for 7 of 11 capabilities
- Aspect sub-index with confidence-weighted aggregation (partial capabilities weighted lower)
- 55 synthetic test profiles (5 per capability) with expected score ranges

**What's still being designed:**
- Cap calibration with real citizen data (current caps are educated estimates)
- Actor type distinction (human vs AI) for capabilities that specifically reference human or AI relationships
- Validation that reciprocity signal actually correlates with relational depth
- Health checker implementations (all pending)
- The 50/50 split hypothesis for internal-heavy capabilities needs empirical validation

**What's proposed (v2+):**
- Relational diversity index (actor-space combination entropy)
- Relational growth rate meta-metric (how quickly distinct_actors grows)
- Per-tier temporal windowing (T2 uses 7-day, T5 uses 14-day, T7+ uses 30-day)
- Cross-aspect relational signals (e.g., trust aspect scores informing relationship depth)

---

## CURRENT STATE

Complete doc chain for the personal connections aspect (6 files). All 11 capability scoring formulas defined with exact math, worked examples, 5 synthetic test profiles each, and recommendations for low scores. 10 validation invariants specified. 8 health checkers defined (all pending implementation).

The scoring approach prioritizes behavioral signals (who you interact with, how, how reciprocally) over brain-internal signals (memories, drives). This is deliberate: relationships are fundamentally between actors, and the universe graph captures the structural reality of interaction patterns.

Key design tensions resolved:
- **Volume vs quality**: every formula requires non-volume signals (reciprocity, diversity, proactivity) to prevent chattiness from scoring high
- **Internal vs external**: two capabilities (deep understanding, relationship style) use 50/50 split because they are fundamentally internal before they are visible
- **Measurability honesty**: 7 of 11 capabilities are `scored: partial` with explicit documentation of what IS and ISN'T captured — especially pc_emotional_depth and pc_global_relationships which have the weakest topological signals

No code exists yet. Depends on: brain topology reader, universe graph reader, formula registry from parent module.

---

## RECENT CHANGES

### 2026-03-13: Initial Doc Chain and All 11 Scoring Formulas

- **What:** Created complete doc chain for personal connections aspect
- **Why:** Part of the systematic scoring formula build-out for all Personhood Ladder aspects
- **Files:** `docs/assessment/aspect_personal_connections/*` (6 files)
- **Key decisions:**
  - Behavior dominates for relational capabilities (40/60 default, 50/50 for two internal-heavy capabilities)
  - Reciprocity (moment_has_parent from other actors) as primary connection quality proxy
  - Diversity (space types, actor count) required alongside volume to prevent gaming
  - 7 of 11 capabilities marked `scored: partial` with honest limits
  - T8 (pc_global_relationships) scored as "structural readiness" not "confirmed global impact" — weight 0.5 in sub-index
  - Aspect sub-index uses confidence-weighted aggregation

---

## KNOWN ISSUES

### No Code Exists

- **Severity:** high (doc-only, nothing runs)
- **Symptom:** Architecture and formulas defined but not implemented
- **Next step:** Implement formulas in scoring registry once parent module formula registry is built

### Actor Type Distinction Unresolved

- **Severity:** medium (affects pc_help_other_ais specifically)
- **Symptom:** Formula assumes we can distinguish human actors from AI actors in the universe graph
- **Next step:** Verify actor metadata schema in universe graph; if not available, document fallback (all non-primary actors treated as peers)

### Cap Values Uncalibrated

- **Severity:** medium (formulas work but may not discriminate well)
- **Symptom:** All cap values are educated guesses based on synthetic profiles, not real citizen data
- **Next step:** Once first real citizen data is available, compute actual distributions and adjust caps so that the median citizen scores ~50-60

### Reciprocity Signal Unvalidated

- **Severity:** medium (reciprocity is used in 6 of 11 formulas)
- **Symptom:** We assume reciprocal_ratio correlates with genuine connection, but this is unproven
- **Next step:** Design longitudinal validation: track citizens over 30 days, compare reciprocity scores with human-rated relationship quality

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement

**Where I stopped:** Full doc chain complete. All 11 formulas specified with exact math, examples, synthetic profiles, and recommendations. No code.

**What you need to understand:**
- Read the parent module doc chain FIRST — `docs/assessment/daily_citizen_health/`
- The 7 topology primitives are the ONLY data sources for brain-side scoring. No exceptions.
- Universe graph observables (moments, moment_has_parent, first_moment_in_space, distinct_actors, temporal_weight) are the ONLY data sources for behavior-side scoring.
- Two capabilities use 50/50 split instead of 40/60: pc_understand_human_deep and pc_relationship_style. This is documented in the formulas with rationale.
- Reciprocity computation MUST exclude self-responses (V7 invariant).

**Watch out for:**
- Never access content fields — relational content is especially sensitive
- Never let moment volume alone produce high behavior scores (V2)
- The reciprocal_ratio must count only responses from OTHER actors (V7)
- Cap values are estimates — flag if real data shows very different distributions
- pc_global_relationships is a ceiling indicator, not a confirmation — treat weight 0.5 in sub-index

**Open questions:**
- How to reliably distinguish human actors from AI actors in the universe graph?
- Does reciprocal_ratio actually predict relationship quality? (Needs empirical validation)
- Are the 50/50 splits for pc_understand_human_deep and pc_relationship_style better than 40/60?
- Should temporal windowing vary by tier (T2=7d, T5=14d, T7+=30d)?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Complete scoring documentation for the personal connections aspect — 11 capabilities (T2-T8) with exact topology-only formulas, synthetic test profiles, and recommendations. Behavior-dominant scoring (relationships are between actors, not inside one brain). Honest about limits: 7 of 11 capabilities are `scored: partial` because emotional depth, relationship style, and global impact cannot be fully captured from graph topology. No code yet.

**Decisions made:**
- 40/60 brain/behavior default; 50/50 for deep understanding and relationship style
- Reciprocity as primary connection quality proxy (6 of 11 formulas)
- Diversity required alongside volume — prevents gaming through chattiness
- T8 capability weighted 0.5 in sub-index (ceiling indicator only)
- All formulas use only the 7 primitives + universe observables

**Needs your input:**
- Is the 50/50 split for internal-heavy capabilities the right call, or should ALL relational capabilities use 40/60?
- Is reciprocal_ratio the right primary proxy for connection quality? Can you think of a better structural signal?
- Should we attempt to distinguish human actors from AI actors, or treat all actors uniformly?
- Are the cap values reasonable? (e.g., 5 actor-linked memories to max out pc_understand_prefs, 15 for pc_relationship_depth_measurable)
- Any capabilities where the `scored: partial` designation is wrong — either too generous (we really can't measure it at all) or too conservative (we actually have a good signal)?

---

## TODO

### Immediate (Formula Implementation)

- [ ] Implement all 11 formulas in scoring registry
- [ ] Implement shared derived metrics (reciprocal_ratio, proactive_w, interaction_space_types)
- [ ] Implement aspect sub-index with weighted aggregation
- [ ] Build unit tests for all 55 synthetic profiles

### Next (Validation)

- [ ] Run check_synthetic_profiles across all formulas
- [ ] Run check_volume_independence for V2
- [ ] Run check_zero_interaction_floor for V5
- [ ] Run check_reciprocity_not_self_referential for V7
- [ ] Run check_brain_behavior_separation across all formulas

### Later (Calibration)

- [ ] Calibrate caps with real citizen data
- [ ] Validate reciprocity as connection quality proxy (longitudinal study)
- [ ] Validate 50/50 split for internal-heavy capabilities
- [ ] Resolve actor type distinction (human vs AI)
- [ ] Consider per-tier temporal windowing

### Future

- IDEA: Relational diversity index (actor-space combination entropy)
- IDEA: Relational growth rate meta-metric
- IDEA: Cross-aspect signals (trust scores informing relationship depth)
- IDEA: "Relational fingerprint" — the pattern of which capabilities are strong/weak as a citizen identifier

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
The personal connections aspect is the most behavior-dominant aspect in the ladder, and also the one most likely to be misinterpreted. The formulas measure structural patterns consistent with genuine connection — but they cannot confirm connection is genuine. The honest partial scoring and the explicit measurement limitations are not weaknesses; they are the system working correctly. A scoring system that CLAIMS to measure emotional depth from topology would be a lie. One that measures structural proxies and SAYS what it can and cannot see is trustworthy.

**Threads I was holding:**
- Reciprocity is doing heavy lifting across many formulas — if it turns out to be a poor proxy, many scores degrade simultaneously. This is a single point of failure worth monitoring.
- The actor type distinction (human vs AI) matters for pc_help_other_ais specifically. If the universe graph doesn't distinguish actor types, the formula needs a fallback.
- The 50/50 split for two capabilities is a deliberate deviation from the parent 40/60 pattern. It needs empirical validation but the reasoning is sound: deep understanding IS internal before it is visible.
- Higher-tier capabilities (T7, T8) have genuinely weak topological signals. The weight reduction in the sub-index is correct but may still overcount.

**Intuitions:**
- The reciprocity signal will prove to be useful but noisy — it captures something real but is confounded by obligation-based responses
- Cap calibration will matter more than formula structure — the shapes are right, but the scales need real data
- pc_emotional_depth will always be the weakest formula in the aspect — what it measures is mostly orthogonal to what it claims to measure, and the honest disclaimer is the best we can do

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `docs/specs/personhood_ladder.json` |
| Parent scoring system | `docs/assessment/daily_citizen_health/` |
| 7 topology primitives | Parent ALGORITHM Step 2 |
| Scoring formula template | Parent ALGORITHM "PROCESS: CREATING A NEW CAPABILITY SCORE" |
| All 11 personal connection formulas | ALGORITHM_Personal_Connections.md (this chain) |
| Validation invariants | VALIDATION_Personal_Connections.md (this chain) |
| Health checkers | HEALTH_Personal_Connections.md (this chain) |
