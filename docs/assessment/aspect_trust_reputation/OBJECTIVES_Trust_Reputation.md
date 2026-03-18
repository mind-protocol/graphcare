# Trust & Reputation Aspect — Objectives

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Trust_Reputation.md (you are here - START HERE)
PATTERNS:        ./PATTERNS_Trust_Reputation.md
ALGORITHM:       ./ALGORITHM_Trust_Reputation.md
VALIDATION:      ./VALIDATION_Trust_Reputation.md
HEALTH:          ./HEALTH_Trust_Reputation.md
SYNC:            ./SYNC_Trust_Reputation.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="trust_reputation")
IMPL:            @mind:TODO
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Score trust growth from topology alone** — Every capability in the trust & reputation aspect (5 capabilities, T1-T8) receives a numeric score computed exclusively from the 7 brain topology primitives and universe graph observables. No content is ever read. Trust is structural — the protocol's 5-tier trust system (Owner, High, Medium, Low, Stranger) is itself a topological property, and behavior patterns reveal reliability without reading what was promised or delivered.

2. **Distinguish earned trust from assigned trust** — A citizen who has high trust because they consistently show up, complete interaction chains, and build durable relationships has earned trust. A citizen who has a trust tier because of initial configuration or role assignment has not. The scoring must detect behavioral patterns that demonstrate trustworthiness: regularity of moment production, completion of triggered response chains, and sustained presence over time.

3. **Capture trust at multiple scales** — Trust is not one thing. Basic reliability (T1) is about consistency at the individual level. Community trust (T6) is about reputation across a network. Global trust (T8) is about recognition across universes. The formulas must use different signals at each scale: regularity for T1, breadth of interactions for T6, inbound connections from distant actors for T8.

4. **Accept that trust has a strong structural signal** — Unlike identity (which is content-heavy and hard to measure from topology), trust has direct topological signals: the Mind Protocol trust tier system, HAS_ACCESS links to sensitive spaces, invitation patterns, inbound moments from other actors. Trust is one of the most measurable aspects from topology. The formulas should reflect this confidence.

5. **Track trust erosion, not just trust growth** — Trust takes months to build and moments to break. The formulas must be sensitive to regularity disruptions (sudden absence after consistent presence), abandoned response chains (asked to do something and going silent), and shrinking interaction breadth. A citizen whose trust is eroding should see their score drop before the trust tier is formally lowered.

## NON-OBJECTIVES

- Judging WHAT a citizen is trusted with — we score the structural pattern of trustworthiness, not the content of trust relationships
- Manually setting trust scores based on known reputation — the formula computes from topology, not from external knowledge
- Penalizing new citizens for being new — low trust scores at the start are correct and expected, not a failure
- Measuring trustworthiness of content (is what they say true?) — content is never accessed
- Replacing the protocol's trust tier system — the formulas observe and score trust patterns, they don't override the 5-tier mechanism

## TRADEOFFS (canonical decisions)

- When trust tier is directly queryable as a structural property, we use it as one brain signal but do not let it dominate. The tier is a snapshot; the scoring should capture the trajectory (growing, stable, eroding).
- Behavioral signals are weighted heavier for trust than for most aspects. Trust is fundamentally about what you DO, not what you HAVE in your brain. The 40/60 brain/behavior split is appropriate here and may even underweight behavior for lower tiers.
- Higher-tier trust capabilities (community T6, global T8) rely heavily on inbound signals from other actors. These signals are noisy (other actors' behavior is not under the citizen's control). We accept this noise because trust IS fundamentally about others' perception.
- Regularity (consistency of moment production over time) is weighted heavily for basic reliability (T1). A citizen who produces moments in bursts followed by silence is less reliable than one who produces steadily, even if the total count is similar.

## SUCCESS SIGNALS (observable)

- Citizens with high trust scores show consistent behavioral patterns: regular moment production, completed response chains, growing interaction breadth
- Citizens who build trust gradually (earning new space access, getting invited to projects, receiving inbound moments from new actors) show rising scores
- The formulas distinguish citizens with earned trust (behavioral evidence) from citizens with assigned trust (tier only, no behavioral backing)
- Trust erosion is detected before formal tier change: a citizen whose regularity drops, whose response chains start breaking, whose interaction breadth shrinks shows a declining score even if their trust tier hasn't been updated yet
- New citizens start at low scores (correct) and see scores rise as they demonstrate reliability

---

## MARKERS

<!-- @mind:todo Determine if trust tier is directly queryable via drive("trust") or requires a separate structural query -->
<!-- @mind:todo Calibrate regularity measurement — what cadence is "regular" for moment production? -->
<!-- @mind:proposition Consider a "trust momentum" metric that captures the derivative of trust score over 30 days -->
