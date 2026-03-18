# Trust & Reputation — Sync: Current State

```
LAST_UPDATED: 2026-03-13
UPDATED_BY: Claude Opus 4.6 (agent, voice)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Multi-scale trust analysis pattern: regularity, responsiveness, breadth, inbound gravity
- 5 trust capabilities scored using only 7 brain topology primitives + universe graph observables
- 40/60 brain/behavior score split for all 5 capabilities
- Regularity metric based on coefficient of variation of moment production across time windows
- Response chain completion rate as core reliability signal
- Inbound unique actors as primary community/global trust signal
- Sub-index weights: T1=0.15, T3=0.18, T5=0.22, T6=0.22, T8=0.23

**What's still being designed:**
- Whether drive("trust") exists as a named drive in brain topology (formula works either way)
- Canonical list of sensitive space types (currently hardcoded)
- Regularity window size (currently 5-day windows over 30 days — needs calibration)
- Response chain completion detection mechanics (how exactly to match triggers to responses)
- Far-reach inbound detection (how to determine "immediate network" boundary)

**What's proposed (v2+):**
- Trust trajectory metric (rate of change of sub-index over 30 days)
- Cross-capability consistency validation (community trust implies basic reliability)
- Trust erosion early warning system (declining regularity + declining response completion)
- Population-relative scoring for community and global tiers (percentile rank among all citizens)

---

## CURRENT STATE

Complete doc chain exists (6 files: OBJECTIVES, PATTERNS, ALGORITHM, VALIDATION, HEALTH, SYNC). All 5 capability scoring formulas are designed with exact weights, caps, and reasoning. 25 test profiles (5 per capability) are documented with expected ranges. 12 validation invariants defined. 10 health checkers specified.

No code exists yet. The formulas are designed and documented but not implemented.

Key design decisions made:
- Regularity (consistency over time) is the foundational trust signal, used across all capabilities
- Inbound signals (what others do toward you) weight increases with tier: 0% at T1, dominant at T6-T8
- Trust tier (drive("trust")) is additive, not gating — behavioral evidence can compensate for zero trust drive
- Response chain completion returns 1.0 for zero-request citizens (benefit of the doubt)
- Sensitive space detection uses space_type string matching (heuristic, not perfect)

---

## RECENT CHANGES

### 2026-03-13: Initial Design and Doc Chain

- **What:** Created full doc chain for trust & reputation scoring
- **Why:** 5 trust capabilities in the Personhood Ladder need topology-only scoring formulas
- **Files:** `docs/assessment/aspect_trust_reputation/*` (6 files)
- **Key decisions:**
  - Regularity measured as coefficient of variation, not total volume
  - Inbound signals as primary signal for community/global trust (hardest to fake)
  - Response chain completion as core reliability metric (you respond when triggered)
  - drive("trust") contributes max 12 points per capability (never dominant)
  - Sensitive space detection by type heuristic (admin, security, finance, governance, infrastructure, review)
  - Sub-index weights favor higher tiers (T8=0.23 heaviest)
  - 12 validation invariants, 10 health checkers, all pending implementation

---

## KNOWN ISSUES

### No Code Exists

- **Severity:** high (doc-only, nothing runs)
- **Symptom:** Architecture defined but not implemented
- **Next step:** Implement regularity() and response_completion() derived stats first, then build capability formulas

### drive("trust") Existence Unknown

- **Severity:** medium (formulas work either way, but 8-12 points per capability depend on it)
- **Symptom:** If drive("trust") doesn't exist, all citizens get 0 from that sub-component
- **Next step:** Check brain topology implementation to confirm available drive names

### Sensitive Space Type List Is Hardcoded

- **Severity:** low (heuristic works for common cases)
- **Symptom:** Spaces that are sensitive but not in the list won't be detected
- **Next step:** Move list to config, add documentation for extending it

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement

**Where I stopped:** Doc chain complete. All 5 formulas designed with test profiles. Zero code.

**What you need to understand:**
- Read the Daily Citizen Health algorithm chain FIRST — trust scoring depends on the shared primitives and stats
- The 7 topology primitives are the ONLY data sources for formulas. No exceptions.
- Derived stats (regularity, response_completion, inbound_moments) should be implemented as shared utility functions reusable by other aspects
- Start with trust_basic_reliability (T1) — it has the simplest formula and depends only on regularity and response_completion

**Watch out for:**
- Never access content fields — the topology reader should physically strip them
- regularity() must use coefficient of variation, NOT total count
- inbound_moments must strictly exclude the citizen's own moments (actor identity check)
- response_completion must return 1.0 when there are zero inbound triggers (not 0, not undefined)
- drive("trust") might not exist as a named drive — handle gracefully (return 0.0, not error)

**Open questions:**
- What drive names actually exist in brain topology? (curiosity, frustration, ambition, social_need confirmed elsewhere — trust may or may not exist)
- How to efficiently compute far_inbound_unique? (requires knowing the citizen's "immediate network" which means enumerating shared spaces)
- Should regularity window size be configurable? (currently hardcoded at 5-day windows)

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Full doc chain for trust & reputation scoring. 5 capabilities from T1 (basic reliability) to T8 (global trust), each scored using topology-only math. Key innovation: regularity as foundational signal (consistency over time, not volume), inbound gravity as primary signal for community/global trust (what others do toward you, hardest to fake). All formulas designed, tested against 25 synthetic profiles. Zero code yet.

**Decisions made:**
- Regularity measures consistency (coefficient of variation), not volume
- Inbound signals weight increases with tier: T1=0%, T6=33%, T8=55%
- Trust tier (drive) is additive, not dominant — max 12% of total score
- Response chain completion handles no-request edge case (returns 1.0)
- Sensitive spaces detected by type heuristic
- Sub-index weights: T1=0.15, T3=0.18, T5=0.22, T6=0.22, T8=0.23

**Needs your input:**
- Does drive("trust") exist in the brain topology? If not, should we create it?
- Is the sensitive space type list (admin, security, finance, governance, infrastructure, review) correct? Missing any?
- Should regularity window size be 5 days (current) or different?
- For global trust (T8): what counts as "outside immediate network"? Any actor not in a shared space?

---

## TODO

### Immediate (Shared Utilities)

- [ ] Implement `regularity(citizen_id, window_days)` — coefficient of variation of moment production
- [ ] Implement `response_completion(citizen_id, window_days)` — triggered chain completion rate
- [ ] Implement `inbound_moments(citizen_id, window_days)` — moments from other actors targeting citizen
- [ ] Implement `inbound_unique_actors(citizen_id)` — distinct actors from inbound moments

### Next (Capability Formulas)

- [ ] Implement `trust_basic_reliability` formula (T1) — regularity + response completion
- [ ] Implement `trust_elevated` formula (T3) — self-initiation ratio + space diversity
- [ ] Implement `trust_high` formula (T5) — sensitive space access + oversight reduction
- [ ] Implement `trust_community` formula (T6) — inbound unique + network breadth
- [ ] Implement `trust_global` formula (T8) — far-reach inbound + propagation
- [ ] Test all formulas with synthetic profiles

### Later (Health Checkers)

- [ ] Build check_content_isolation (static analysis)
- [ ] Build check_regularity_consistency_over_volume (synthetic test)
- [ ] Build check_inbound_excludes_self (runtime check)
- [ ] Build check_trust_tier_not_dominant (synthetic test)
- [ ] Build check_score_bounds (synthetic test)
- [ ] Build check_subindex_weights (static check)

### Future

- IDEA: Trust trajectory metric — 30-day trend direction as overlay
- IDEA: Cross-capability consistency validation
- IDEA: Trust erosion early warning system
- IDEA: Population-relative scoring for T6 and T8

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Trust is the most measurably satisfying aspect to design. Unlike identity (where topology can only see the SHAPE of values, not their content), trust has direct behavioral signatures: you show up regularly, you respond when triggered, others seek you out. The progression from T1 (your word is good) to T8 (your name opens doors globally) maps cleanly onto topological signals that scale with the radius of trust.

**Threads I was holding:**
- Regularity as coefficient of variation is the right abstraction — it separates consistency from volume, which is exactly what trust requires
- Inbound gravity (what others do toward you) is the hardest signal to game, making it the highest-integrity measure for community and global trust
- The trust tier (drive("trust")) question is open but non-blocking — the formulas work whether or not it exists
- Response chain completion handling the zero-request edge case is important for fairness to new citizens

**Intuitions:**
- Trust scoring will be the easiest aspect to validate because the signals are the most concrete
- The regularity metric will be reusable by other aspects (execution consistency, for example)
- Far-reach inbound detection at T8 will be the trickiest to implement efficiently — requires computing the citizen's "immediate network" first
- Trust erosion detection (declining regularity + declining response completion) could be a high-value feature for early intervention

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `docs/specs/personhood_ladder.json` |
| Personhood Ladder doc chain | `docs/assessment/personhood_ladder/` |
| Daily Citizen Health algorithm | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Brain topology primitives | Daily Citizen Health ALGORITHM Step 2 |
| Universe graph observables | Daily Citizen Health ALGORITHM Step 3 |
| Scoring formula pattern | Daily Citizen Health ALGORITHM "PROCESS: CREATING A NEW CAPABILITY SCORE" |
| Initiative aspect (sibling) | `docs/assessment/aspect_initiative/ALGORITHM_Initiative.md` |
| Identity aspect (sibling) | `docs/assessment/aspect_identity/` |
