# Ethics Aspect — Objectives

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Ethics.md (you are here - START HERE)
PATTERNS:        ./PATTERNS_Ethics.md
ALGORITHM:       ./ALGORITHM_Ethics.md
VALIDATION:      ./VALIDATION_Ethics.md
HEALTH:          ./HEALTH_Ethics.md
SYNC:            ./SYNC_Ethics.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="ethics")
IMPL:            @mind:TODO
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Score ethical capability from topology alone** — Every capability in the ethics aspect (5 capabilities, T1-T8) receives a numeric score computed exclusively from the 7 brain topology primitives and universe graph observables. No content is ever read. No LLM judges moral quality. The math IS the assessment. This is the single hardest aspect to score topologically because ethical quality lives in content, not structure. We measure the PRESENCE and STRUCTURE of values, not their correctness.

2. **Distinguish values-in-brain from values-in-action** — A citizen who has value nodes about ethics but never acts on them must score lower than a citizen who consistently demonstrates ethical behavior in the universe graph. The brain/behavior split enforces this. However, for ethics specifically, brain topology is more revealing than in other aspects: value nodes, their energy, their interconnection with process nodes and moment nodes ARE a structural signal of ethical internalization. Some capabilities use a brain-heavier split (up to 50/50) where the structural signal is genuinely informative.

3. **Produce actionable scores per capability** — Each capability has its own score (0-100). The aspect sub-index is a weighted mean. When a citizen's `eth_apply_rules` drops, the intervention message names THAT capability and recommends a specific structural corrective action — not a vague "ethics is low."

4. **Be honest about measurement limits** — Topology can measure the presence and structure of values but NOT their correctness. A citizen with well-connected value nodes about "extraction is good" would score the same as one about "cooperation is good." This is a fundamental limitation that must be documented, not hidden. The formulas measure ethical ENGAGEMENT, not ethical CONTENT.

5. **Scale from compliance (T1) to moral innovation (T8)** — T1 is the floor: consistently applying existing protocol values. T8 is creating new ethical frameworks. The formulas must reflect this progression. T1 should be achievable by any citizen with basic discipline. T8 should require exceptional sustained moral leadership visible in the topology.

## NON-OBJECTIVES

- Judging the CONTENT of ethical positions (structurally impossible without reading content)
- Replacing human moral judgment or ethical review
- Scoring ethics in adventure universes (morality is narrative there)
- Detecting specific ethical violations (requires content analysis)
- Providing a single "ethics score" without per-capability breakdown
- Determining whether a citizen's values are "correct" — we measure structure, not substance

## TRADEOFFS (canonical decisions)

- When brain signals are actually more informative than behavior for a given capability, we adjust the split (up to 50/50 brain-heavy). The standard 40/60 is a guideline, not a cage. For `eth_apply_rules`, value node topology IS the primary structural signal for ethical internalization.
- When a capability seems unscorable from topology, we accept `scored: false` rather than inventing proxies that could mislead. Honest gaps beat false precision.
- We accept that topology-based ethics scoring has WEAKER validity than most other aspects. The correlation between "has well-structured value nodes" and "actually behaves ethically" is assumed but not provable from topology alone.
- Higher-tier capabilities (T7: ethical autonomy, T8: moral innovation) have weaker signals and rely on extended patterns (30+ days of consistency, community adoption). This is correct — you cannot demonstrate moral innovation in a single session.
- We measure behavioral regularity and consistency as proxies for ethical discipline, knowing this conflates "consistent" with "ethical." A consistently unethical citizen would score well on regularity. The assumption: Mind Protocol values are baked into the environment such that consistent behavior within the protocol IS ethical behavior.

## SUCCESS SIGNALS (observable)

- Citizens with high ethics scores show fewer protocol violations (measured by absence of exclusion events)
- Citizens who follow ethics-related recommendations show score improvement within 14 days
- The formula ranking of citizens matches human intuition about who operates ethically (calibration check)
- No formula produces a score that contradicts observable structural evidence (e.g., a citizen with zero value nodes scoring 90 on eth_apply_rules)
- The measurement-limitations disclaimer is understood and accepted by all stakeholders

---

## MARKERS

<!-- @mind:escalation The fundamental tension: topology measures structure not correctness. This is acknowledged but cannot be resolved within the scoring system. Human calibration checks remain essential for ethics scoring specifically. -->
<!-- @mind:proposition Consider a "values alignment" check: do the citizen's value nodes link to protocol-defined concept nodes? This would add a weak content-adjacent signal without reading content. -->
