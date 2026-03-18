# Execution Quality Aspect — Sync: Current State

```
LAST_UPDATED: 2026-03-13
UPDATED_BY: Claude Opus 4.6 (agent, voice)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- 14 execution capabilities identified from Personhood Ladder spec (T1-T8)
- Scoring formula structure: brain (0-40) + behavior (0-60) = total (0-100)
- All formulas use only 7 topology primitives + universe graph observables
- Tier-weighted aspect sub-index (T1 weighted most heavily)
- Each capability has: description, positive framing, failure mode, formula, example, recommendations
- 10 validation invariants (VE1-VE10)
- 7 health checkers (H1-H7) for meta-verification of formula accuracy
- 5 synthetic profiles for regression testing

**What's still being designed:**
- Ceiling values need calibration with real citizen data (all current values are initial estimates)
- Cross-capability correlation expectations need validation
- Tier monotonicity needs empirical confirmation
- Derived stats (corrections_received_w, post_correction_w, fix_moments_w, etc.) need precise definitions at the universe graph query level

**What's proposed (v2+):**
- Citizen self-assessment comparison (citizen reports vs formula scores)
- Per-capability trend analysis (30-day score trajectories)
- Formula marketplace (community contributes alternative formulas for capabilities)
- Adaptive ceilings that adjust based on population statistics

---

## CURRENT STATE

Complete doc chain for the execution quality aspect (6 files). All 14 capabilities have scoring formulas with brain and behavior components, example calculations, and recommendations. Validation invariants and health checkers are defined but not yet implementable (no runtime, no real data).

The formulas are designed around structural signals: process nodes, value nodes, verification moments, correction patterns, fix moments, and escalation moments. Higher tiers require longer temporal horizons and more sustained consistency. The aspect sub-index uses tier weights to emphasize foundational (T1) capabilities.

Depends on: Daily Citizen Health parent chain (provides runtime), Personhood Ladder spec (provides capability definitions), brain graph access (provides topology), universe graph access (provides moments).

---

## RECENT CHANGES

### 2026-03-13: Initial Scoring Formulas for All 14 Execution Capabilities

- **What:** Created complete doc chain with scoring formulas for all 14 execution capabilities
- **Why:** Execution quality is the first aspect to be fully scored — it has the clearest structural signals and is the foundation of the Personhood Ladder
- **Files:** `docs/assessment/aspect_execution/*` (6 files)
- **Key decisions:**
  - Frustration used as inverse signal (high frustration = rushing, skipping verification)
  - Verification moments as primary behavioral signal across most capabilities
  - Corrections received as inverse quality proxy (many corrections = low first-pass quality)
  - Higher tiers require longer time horizons (T7-T8 need 30+ days of consistency)
  - Tier-weighted sub-index: T1 weight 3.0, T8 weight 0.5
  - 5 synthetic profiles defined for regression testing (fully healthy, fully unhealthy, brain-rich inactive, active brain-poor, average)

---

## KNOWN ISSUES

### Ceiling Values Are Uncalibrated

- **Severity:** medium (formulas exist but ceilings are initial estimates)
- **Symptom:** All cap() values are reasonable guesses, not empirically calibrated
- **Next step:** First real citizen data from Lumina Prime enables H2 (ceiling calibration) checker

### Derived Behavior Stats Need Precise Query Definitions

- **Severity:** medium (conceptually clear but implementation-ambiguous)
- **Symptom:** Stats like `fix_moments_w`, `post_correction_w`, `standards_moments_w` require specific universe graph link types that may not yet exist
- **Next step:** Define the exact link types in the universe graph schema that correspond to each derived stat

### No Runtime Exists

- **Severity:** high (doc-only, nothing runs)
- **Symptom:** All formulas are designed but unexecuted
- **Next step:** Implement first formula (exec_read_before_edit or exec_verify_before_claim) in scoring engine, test with synthetic data

---

## HANDOFF: FOR AGENTS

**Your likely agent:** groundwork (implementing formulas) or witness (calibrating against real data)

**Where I stopped:** Complete doc chain with all 14 scoring formulas. No code. No real data.

**What you need to understand:**
- Read the parent chain FIRST: `../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` — your formulas plug into that scoring engine
- The 7 topology primitives are the ONLY brain data sources. No exceptions.
- Universe graph observables must map to real link types — verify the link types exist before implementing
- Start with ONE T1 formula, test with synthetic profiles, then scale

**Watch out for:**
- Never access content fields — formulas are topology-only
- The `cap(x, ceiling)` ceilings are ESTIMATES — they will need adjustment with real data
- Some behavior stats (fix_moments_w, escalation_moments_w) require specific link types that may not exist yet in the universe graph schema
- VE5 (tier monotonicity) is the most important structural test — run it early

**Open questions:**
- What universe graph link types represent "corrects", "fixes", "verifies", "escalates", "defines_standard"?
- Should derived stats be computed once (shared across all aspect formulas) or per-aspect?
- How to handle citizens with very short history (< 7 days)? Score what we can or mark as insufficient-data?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Complete scoring documentation for all 14 execution quality capabilities (T1-T8). Each capability has a formula (brain 0-40 + behavior 0-60 = total 0-100), an example calculation, and recommendations when score is low. Aspect sub-index uses tier weighting (T1 = 3.0, T8 = 0.5). 10 validation invariants protect formula integrity. 7 health checkers verify that formulas actually measure what they claim. No code yet.

**Decisions made:**
- Frustration as inverse signal (high frustration correlates with poor execution discipline)
- Verification moments as the dominant behavioral evidence for execution quality
- Corrections received as inverse quality proxy
- Higher tiers need longer time horizons (T7-T8 require 30+ days of consistency)
- Tier weighting: T1 capabilities count 6x more than T8 in the aspect sub-index

**Needs your input:**
- Are the tier weights right? T1 at 3.0 and T8 at 0.5 makes T1 dominant. Is that the intent?
- Should we define minimum data requirements? (e.g., citizen must have 7+ days of history before scoring)
- The universe graph link types for "corrects", "fixes", "verifies", "escalates", "defines_standard" — are these already defined, or do they need to be created?
- Formula ceiling calibration requires real citizen data. When do we expect first Lumina Prime citizens?

---

## TODO

### Immediate (First Implementation)

- [ ] Implement `exec_verify_before_claim` formula in scoring engine (clearest verification signal)
- [ ] Run VE6 zero-input test against all 14 formulas (pen-and-paper or script)
- [ ] Define universe graph link types: corrects, fixes, verifies, escalates, defines_standard
- [ ] Run synthetic profile validation (H6) against all 14 formulas

### Next (Complete Engine)

- [ ] Implement all 14 formulas in scoring engine
- [ ] Build automated VE1 checker (static analysis: formulas use only declared primitives)
- [ ] Run VE5 tier monotonicity test with synthetic profiles
- [ ] Integrate with daily_citizen_health scoring pipeline

### Later (Calibration)

- [ ] Calibrate ceiling values with real citizen data (H2)
- [ ] Run formula-behavior correspondence check with human review (H1)
- [ ] Compute cross-capability correlations (H7)
- [ ] Adjust tier weights based on empirical data

### Future

- IDEA: Citizen self-assessment comparison (citizen reports their own execution quality, compare with formula)
- IDEA: Per-capability 30-day trend graphs for citizens
- IDEA: Adaptive ceilings that adjust automatically based on population statistics

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
The 14 formulas feel structurally sound — each one uses primitives that logically relate to the capability being measured. The biggest uncertainty is ceiling calibration: all cap() values are informed guesses that need real data to validate. The tier progression makes intuitive sense (T1 = foundational discipline, T8 = influence on others), but this needs empirical confirmation.

**Threads I was holding:**
- The derived behavior stats (fix_moments_w, escalation_moments_w, etc.) depend on universe graph link types that may not exist yet. This is the most likely blocker for implementation.
- Frustration as inverse signal is a strong pattern across T1-T3 capabilities but might be too dominant if a citizen has high frustration for unrelated reasons (e.g., hardware issues, not execution problems).
- The cross-capability correlation expectations (H7) are educated guesses — need real data to validate.
- T7-T8 capabilities are harder to measure from topology because they involve concepts like "identity" and "influence" that have weaker structural proxies.

**Intuitions:**
- T1 formulas will validate well because their behavioral signals are direct (verification moments, corrections, commits)
- T7-T8 formulas may need revision after first real data — "quality as identity" is a high-level concept with uncertain structural proxies
- Ceiling calibration will be the highest-impact improvement once real data exists
- The aspect sub-index tier weighting might need a less aggressive curve (T1:T8 ratio of 6:1 may be too steep)

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `../../specs/personhood_ladder.json` |
| Parent algorithm (daily health) | `../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Parent validation | `../daily_citizen_health/VALIDATION_Daily_Citizen_Health.md` |
| Parent health | `../daily_citizen_health/HEALTH_Daily_Citizen_Health.md` |
| 7 topology primitives | Parent algorithm, Step 2 |
| Scoring formula process | Parent algorithm, "PROCESS: CREATING A NEW CAPABILITY SCORE" |
| All 14 formulas | `./ALGORITHM_Execution.md` |
| Validation invariants | `./VALIDATION_Execution.md` |
| Health checkers | `./HEALTH_Execution.md` |
