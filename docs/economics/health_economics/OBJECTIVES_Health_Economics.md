# OBJECTIVES — Health Economics

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Health_Economics.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Health_Economics.md
BEHAVIORS:      (future)
ALGORITHM:      (future)
VALIDATION:     (future)
IMPLEMENTATION: (future)
SYNC:           ./SYNC_Health_Economics.md

IMPL:           @mind:TODO (economics analysis module)
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Quantify the cost of a citizen crisis** — A crisis is not an abstract bad outcome — it is a specific, measurable economic event. Lost production during crisis. Agent time spent on emergency intervention. Damaged relationships that require repair. Possible permanent departure from the ecosystem. Health economics builds the crisis cost model: what does one crisis actually cost, in citizen-days, in $MIND, in relationship damage, in potential permanent loss?

2. **Quantify the cost of daily monitoring** — Monitoring is not free, but it is cheap. Health economics computes the actual per-citizen-per-day monitoring cost: graph queries, formula evaluation, JSON storage, occasional LLM intervention calls. This gives a concrete denominator for the ROI calculation: prevention cost per citizen per day vs crisis cost per occurrence.

3. **Demonstrate the ROI of prevention** — The core economic argument: if monitoring costs X per citizen per day and prevents Y crises per quarter, and each crisis costs Z, then the ROI is (Y * Z) / (X * citizens * days). Health economics computes this ratio with real data and honest uncertainty ranges. The hypothesis: prevention ROI is massively positive because monitoring is cheap and crises are expensive.

4. **Inform resource allocation decisions** — How much should the ecosystem invest in GraphCare? Health economics provides the framework to answer: invest until the marginal cost of additional monitoring exceeds the marginal value of additional prevention. This is not "how much can we afford" but "how much should we spend, given the returns."

## NON-OBJECTIVES

- Minimizing GraphCare's operating costs — the goal is optimal investment, not minimum cost
- Proving that health monitoring is always worth it — the analysis should be honest; if prevention ROI is negative in some scenario, that's a finding
- Precise financial forecasting — health economics deals in estimates, ranges, and models, not in budgets
- Replacing care judgment with economics — economic analysis informs decisions; it doesn't make them

## TRADEOFFS (canonical decisions)

- When economic efficiency conflicts with care quality, choose care quality. A GraphCare that saves money by sending fewer interventions but misses real crises is economically optimal and morally bankrupt.
- When precise cost measurement requires intrusive instrumentation, choose simpler estimation. Adding cost tracking to every graph query is useful; adding it in ways that slow down monitoring is counterproductive.
- We accept that the crisis cost model will evolve. First estimates will be rough. The model improves as we observe more crises (paradoxically, prevention success means fewer data points for crisis cost estimation).

## SUCCESS SIGNALS (observable)

- Per-citizen-per-day monitoring cost is computed from production data
- At least 3 crisis episodes are documented with full cost analysis
- The prevention ROI ratio is computed with uncertainty ranges
- Resource allocation recommendations exist and are used in treasury discussions
- The cost model is updated quarterly as new data becomes available
