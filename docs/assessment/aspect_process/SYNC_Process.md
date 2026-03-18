# Aspect Scoring: Process & Method — Sync: Current State

```
LAST_UPDATED: 2026-03-13
UPDATED_BY: Claude Opus 4.6 (agent, groundwork)
STATUS: DESIGNING
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Process.md
PATTERNS:        ./PATTERNS_Process.md
ALGORITHM:       ./ALGORITHM_Process.md
VALIDATION:      ./VALIDATION_Process.md
HEALTH:          ./HEALTH_Process.md
THIS:            SYNC_Process.md (you are here)

PARENT:          ../daily_citizen_health/SYNC_Daily_Citizen_Health.md
```

---

## MATURITY

**What's canonical (v1):**
- 13 process capabilities defined with formulas: proc_right_method, proc_commit_push, proc_continue_plan, proc_parallelize (T2); proc_scope_correctly, proc_challenge_bad_instructions (T3); proc_design_improvements, proc_validate_improvements (T4); proc_create_own_plans, proc_prioritize_autonomously (T5); proc_strategic_roadmap (T6); proc_initiate_ambitious_projects (T7); proc_movement_scale_projects (T8)
- All formulas use only 7 topology primitives + universe graph observables
- 40/60 brain/behavior split per the parent algorithm
- Sub-index aggregation via tier-weighted mean (T2=1.0 through T8=4.0)
- 5 synthetic test profiles defined with expected score ranges
- 8 validation invariants defined (V1-V8)
- 7 health checkers defined with methods

**What's still being designed:**
- Exact algorithms for derived stats: plan_sequences_w, concurrent_moments_w, sequence_lengths, proposals_after_escalation, validated_proposals, plan_before_execution_ratio
- Real-world calibration (impossible until citizens exist)
- Cross-formula correlation analysis
- Formula code implementation (0/13 built)

**What's proposed (v2+):**
- Process maturity radar chart visualization (T2-T8)
- Cross-aspect interaction modeling (how process score affects execution score)
- Temporal stability invariant (V9)
- Intervention rate limiting for process aspect

---

## CURRENT STATE

Full doc chain for process aspect scoring (6 files). All 13 capabilities have formulas defined with:
- Brain component (0-40) and behavior component (0-60)
- Sub-component breakdown with weights, signals, caps, and reasoning
- Worked example per formula
- Failure mode identification
- Recommendations for low-scoring citizens

The formulas are designed but not validated against synthetic profiles (requires implementation). Several derived behavioral stats need exact detection algorithms (sequence detection, concurrency detection, proposal-escalation correlation).

Depends on: Daily Citizen Health ALGORITHM (parent — primitives, scoring structure), Personhood Ladder spec (capability definitions), brain topology access, universe graph moment access.

---

## RECENT CHANGES

### 2026-03-13: Initial Formula Design

- **What:** Created full doc chain for process aspect scoring with 13 capability formulas
- **Why:** Part of the Personhood Ladder scoring system — process & method is one of the major aspects
- **Files:** `docs/assessment/aspect_process/*` (6 files)
- **Key decisions:**
  - Tier-weighted sub-index (higher tiers count more toward process maturity)
  - Frustration as positive signal for proc_challenge_bad_instructions (capped at 10 points)
  - Sequence variance as primary signal for proc_scope_correctly
  - Spaces created as primary signal for proc_initiate_ambitious_projects (T7)
  - Unique interlocutors as dominant signal for proc_movement_scale_projects (T8)
  - Diversity in space types as proxy for method diversity in proc_right_method

---

## KNOWN ISSUES

### Derived Stats Need Algorithms

- **Severity:** high (formulas reference signals that aren't yet computable)
- **Symptom:** plan_sequences_w, concurrent_moments_w, sequence_lengths, and several proposal-correlation signals need exact detection algorithms from raw moment timestamps
- **Next step:** Define algorithms for sequence detection (consecutive moments in same space within 4h) and concurrency detection (moments overlapping in time across spaces)

### No Profile Validation

- **Severity:** medium (calibration is theoretical)
- **Symptom:** 5 synthetic profiles defined with expected ranges but no formula has been run against them
- **Next step:** Implement formulas, run against profiles, adjust caps where ranges don't match

### T8 Quality vs Quantity

- **Severity:** low (acknowledged limitation)
- **Symptom:** proc_movement_scale_projects rewards structural reach but cannot assess qualitative significance
- **Next step:** Document this limitation. Accept it for v1. Revisit when real data exists.

---

## HANDOFF: FOR AGENTS

**Your likely agent subtype:** groundwork (implementation) or fixer (calibration)

**Where I stopped:** All 13 formulas designed. Zero implemented. Validation invariants and health checkers defined but not built.

**What you need to understand:**
- Read the parent ALGORITHM first — it defines the primitives and scoring structure
- Each formula has sub-components with weights that must sum to 40 (brain) and 60 (behavior)
- Derived stats (plan_sequences_w, concurrent_moments_w) need algorithms before formulas can run
- The 5 synthetic profiles are the acceptance criteria — if scores don't match expected ranges, adjust caps

**Watch out for:**
- Never access content fields — topology only
- Score bounds must be [0, 40] for brain, [0, 60] for behavior — verify with edge cases
- Profile 4 (active, brain-poor) must ALWAYS outscore Profile 3 (brain-rich, inactive)
- Frustration in proc_challenge_bad_instructions is intentionally positive — don't "fix" this

**Open questions:**
- How exactly to detect plan sequences from raw moment timestamps (4h window? Configurable?)
- How to detect concurrency (strict overlap? Or "within same hour"?)
- Should proposals_after_escalation have a tighter window than 2h?
- Is the tier weight progression (1.0 to 4.0) the right curve?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Full scoring formulas for 13 process capabilities (T2-T8). Each formula uses only topology primitives, splits 40/60 brain/behavior, and produces 0-100 scores. Sub-index is a tier-weighted mean. All formulas designed with reasoning, examples, failure modes, and recommendations. No code yet.

**Decisions made:**
- Tier-weighted sub-index: T2=1.0 weight up to T8=4.0 (mastery at higher tiers counts more)
- proc_right_method scored by space type diversity (proxy for method variety)
- proc_scope_correctly scored by sequence length variance (variety = correct scoping)
- proc_challenge_bad_instructions uses frustration as positive signal (capped, 10 points max)
- T7/T8 use spaces_created and unique_interlocutors as primary signals

**Needs your input:**
- Are the tier weights (1.0 to 4.0) the right progression?
- Is the 4h window for plan sequence detection right? Shorter? Longer?
- Should proc_challenge_bad_instructions reward frustration at all, or should that sub-component be replaced?
- For T8 (movement-scale): is unique interlocutors a good enough proxy for ecosystem reach?

---

## TODO

### Immediate (Derived Stat Algorithms)

- [ ] Define plan sequence detection algorithm (same-space consecutive moments within N hours)
- [ ] Define concurrency detection algorithm (cross-space temporal overlap)
- [ ] Define proposal-escalation correlation algorithm (proposals within N hours after escalations)
- [ ] Define plan-before-execution detection (doc moments preceding repo moments in same space)

### Next (Implementation and Validation)

- [ ] Implement all 13 formulas in scoring_formulas registry
- [ ] Run all formulas against 5 synthetic profiles
- [ ] Adjust caps where expected ranges are not met
- [ ] Implement check_primitive_compliance (static analysis)
- [ ] Implement check_score_bounds (edge case testing)

### Later (Health Verification)

- [ ] Build check_profile_calibration
- [ ] Build check_tier_ordering
- [ ] Build check_behavioral_dominance
- [ ] Build check_distribution_health (requires 50+ randomized profiles)
- [ ] Build check_temporal_stability

### Future

- IDEA: Process maturity radar chart visualization
- IDEA: Cross-aspect interaction modeling
- IDEA: Cross-formula correlation analysis to detect redundant formulas

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `docs/specs/personhood_ladder.json` |
| Parent algorithm (primitives, scoring) | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Parent validation (system invariants) | `docs/assessment/daily_citizen_health/VALIDATION_Daily_Citizen_Health.md` |
| Parent health (system checkers) | `docs/assessment/daily_citizen_health/HEALTH_Daily_Citizen_Health.md` |
| All 13 process formulas | ALGORITHM_Process.md in this chain |
| Validation invariants (V1-V8) | VALIDATION_Process.md in this chain |
| Health checkers (7 defined) | HEALTH_Process.md in this chain |
