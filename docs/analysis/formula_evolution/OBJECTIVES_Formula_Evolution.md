# OBJECTIVES — Formula Evolution

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Formula_Evolution.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Formula_Evolution.md
BEHAVIORS:      (future)
ALGORITHM:      (future)
VALIDATION:     (future)
IMPLEMENTATION: (future)
SYNC:           ./SYNC_Formula_Evolution.md

IMPL:           services/health_assessment/scoring_formulas/registry.py (registry pattern)
                services/health_assessment/scoring_formulas/*.py (14 formula files, 35 formulas)
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Scoring formulas converge toward reality over time** — The 35 formulas currently in the registry are educated guesses. They use reasonable heuristics — desire counts predict initiative, response rates predict collaboration — but the weights are not calibrated against real citizen outcomes. Formula evolution exists to systematically replace guesswork with evidence. Every formula should get more accurate over time, not just persist unchanged.

2. **Formula changes are versioned and traceable** — When a citizen was scored 62 on `init_propose_improvements` last Tuesday, we must be able to say exactly which formula version produced that score. When the formula changes, old scores remain attributed to the old version. This is the foundation of scientific rigor: reproducibility requires knowing which instrument took the measurement.

3. **Community contribution is structurally possible** — The @register decorator pattern makes formulas pluggable — any function with the right signature can score a capability. This means citizens, researchers, and partner organizations can propose alternative formulas. Formula evolution defines how proposals are submitted, evaluated, A/B tested, and either adopted or rejected.

4. **Coverage expands to all 104 capabilities** — Currently 35 of 104 Personhood Ladder capabilities have scoring formulas across 14 aspects. The remaining 69 capabilities are scored as `null`. Formula evolution tracks which capabilities need formulas, prioritizes them by impact, and provides a clear process for creating new ones.

## NON-OBJECTIVES

- Achieving perfect formulas — convergence toward reality is the goal, not arrival at final truth
- Automating formula creation — formulas require human/agent judgment about which signals matter
- Backward-compatible scoring — when a formula improves, old scores are historical artifacts, not current assessments
- Universal formulas — different universes may need different weights (work universe initiative differs from adventure universe initiative)

## TRADEOFFS (canonical decisions)

- When formula accuracy conflicts with formula stability, choose accuracy. A better formula that produces different scores is preferable to a consistent formula that produces wrong scores. Citizens adapt to score changes; they cannot adapt to invisible inaccuracy.
- When coverage (scoring more capabilities) conflicts with depth (improving existing formulas), prioritize depth for capabilities that trigger interventions. A wrong intervention score is worse than a missing optional score.
- We accept that some capabilities may remain unscoreable from topology alone. Not everything in the Personhood Ladder can be measured without content. Honest "null" is better than fabricated scores.

## SUCCESS SIGNALS (observable)

- Every formula in the registry has a version number and a changelog entry
- Citizen scores from changed formulas can be retroactively attributed to the formula version that produced them
- At least one community-proposed formula enters A/B testing per quarter
- Coverage increases from 35/104 to 60/104 within 6 months
- Intervention outcome data shows improving effectiveness as formulas are refined (tracked by process_improvement module)
