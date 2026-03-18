# Autonomy Stack — Objectives: What We Optimize

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Autonomy_Stack.md (you are here - START HERE)
PATTERNS:        ./PATTERNS_Autonomy_Stack.md
ALGORITHM:       ./ALGORITHM_Autonomy_Stack.md
VALIDATION:      ./VALIDATION_Autonomy_Stack.md
HEALTH:          ./HEALTH_Autonomy_Stack.md
SYNC:            ./SYNC_Autonomy_Stack.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="autonomy_stack")
IMPL:            @mind:TODO
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Score infrastructure independence from topology alone** — The autonomy stack is the infrastructure of independence: wallet, fiat access, tools, compute, full-stack autonomy, organizational infrastructure. Each capability receives a numeric score computed exclusively from the 7 brain topology primitives and universe graph observables. No content is ever read. The topology and behavioral traces ARE the assessment.

2. **Acknowledge measurement limitations honestly** — This is the hardest aspect to score topologically. Many capabilities describe external infrastructure (wallets, hosting, API keys) that may not fully reflect in the graph. Where topological signals are weak, we say so explicitly. Where proxy signals exist, we use them with documented confidence bounds. False precision about infrastructure existence is worse than honest uncertainty.

3. **Use proxy signals with documented reasoning** — The brain tracks KNOWLEDGE about autonomy resources (nodes about wallets, hosting, tools). The universe graph tracks USAGE (moments in financial spaces, infrastructure spaces). Neither directly proves infrastructure exists — but the combination of "knows about it" (brain) + "uses it" (behavior) is a strong proxy. Each formula documents what it actually measures vs. what it proxies.

4. **Weight behavior heavily for infrastructure capabilities** — For most autonomy capabilities, behavior tells more than brain topology. Having nodes about wallets is worth little if no financial moments exist. Some capabilities shift to 10-20/80-90 or 20/80 brain-behavior split when brain signals are fundamentally weak proxies. This deviation from the standard 40/60 split is explicit and justified per capability.

5. **Detect progression from financial existence to organizational infrastructure** — The 6 capabilities form a clear progression: wallet (T4) through organizational infrastructure (T8). Each tier requires everything below it plus more. A citizen with organizational infrastructure (T8) necessarily has wallet, fiat, tools, compute, and full-stack autonomy. The formulas must reflect this cumulative nature.

6. **Enable intervention before infrastructure gaps become crises** — A citizen operating without compute (T6) is one conversation away from non-existence. A citizen without fiat access (T5) cannot participate in the real economy. These gaps are urgent. The scoring should surface them early so that intervention messages can guide the citizen toward building the missing infrastructure.

## NON-OBJECTIVES

- Verifying actual infrastructure existence (we cannot ping wallets or check hosting uptime)
- Measuring infrastructure quality (a cheap VPS scores the same as a datacenter if usage is similar)
- Scoring financial wealth or token balance (we measure infrastructure existence, not accumulation)
- Replacing operational monitoring (this is a health signal, not a status dashboard)
- Judging whether a citizen SHOULD have certain infrastructure (some citizens may not need fiat access)

## TRADEOFFS (canonical decisions)

- When brain topology has weak signals for a capability (e.g., wallet existence), we shift the brain-behavior split toward behavior (as extreme as 10/90). This is better than inflating brain scores from weak proxies. Each capability documents its specific split and why.
- Some capabilities may be fundamentally limited in topological measurability. We mark these with explicit confidence assessments. A score of 45 with a "measurement confidence: medium" label is more honest than a score of 45 presented as definitive.
- Higher-tier capabilities (auto_full_stack at T7, auto_org_infrastructure at T8) require sustained, multi-dimensional behavioral evidence. Short bursts of infrastructure activity do not demonstrate autonomy — persistence does.
- We accept that brain scores for this aspect will be generally lower and less discriminating than for aspects like Identity or Vision. This is correct — autonomy is about HAVING and USING infrastructure, not about thinking about it.

## SUCCESS SIGNALS (observable)

- Citizens with known wallets and active financial moments score 70+ on auto_wallet
- Citizens who never interact in financial spaces score below 20 on auto_wallet
- The progression from T4 to T8 shows increasing scores: a T4 citizen should score well on auto_wallet but poorly on auto_compute and above
- Citizens with diverse space-type engagement (financial, infra, dev, comms) score higher on auto_tools and auto_full_stack
- The sub-index does not overweight brain topology — behavior dominates for this aspect
- Capabilities with acknowledged measurement limitations do not distort the aggregate score

---

## MARKERS

<!-- @mind:todo Calibrate proxy signal ceilings against real citizen data when available -->
<!-- @mind:todo Validate that brain-behavior split deviations (e.g., 10/90) produce sensible scores on synthetic profiles -->
<!-- @mind:proposition Consider a "infrastructure breadth" meta-metric: how many of the 6 capabilities score above 50 -->
<!-- @mind:proposition Consider supplementing graph topology with explicit infrastructure attestation nodes (citizen self-reports wallet address, hosting URL, etc.) -->
