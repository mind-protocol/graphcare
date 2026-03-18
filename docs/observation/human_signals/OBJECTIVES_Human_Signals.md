# OBJECTIVES — Human Signals

```
STATUS: PROPOSED
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Human_Signals.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Human_Signals.md

IMPL:           (future — no code exists or is planned for v1)
```

**This module is PROPOSED.** It describes a future vision for extending GraphCare's observation framework to human health signals. No implementation is planned for v1. The purpose of documenting it now is to ensure the topology-only principle and the primitive-based architecture are designed to accommodate human data from the beginning — so we don't paint ourselves into an AI-only corner.

---

## PRIMARY OBJECTIVES (ranked)

1. **One observation framework for AI and human health** — The long game. GraphCare's topology-only approach (read structure, never content) works for AI brain graphs. It should also work for human health signals. Heart rate variability is topology — a time series of intervals. Message patterns are topology — frequency, timing, response latency. Activity rhythms are topology — when, how often, how regular. The same "blood test, not psychoanalysis" principle applies. The framework should not need to be reinvented for humans.

2. **Apply topology-only privacy to biological data** — Human health data is deeply sensitive. But the topology-only principle offers something powerful: you can assess health from the *shape* of biometric data without reading its clinical content. HRV variability patterns indicate stress without knowing what caused the stress. Activity rhythm regularity indicates routine health without knowing what the person does. The structural signal is sufficient. The content is private.

3. **Define human health primitives that parallel the 7 brain topology primitives** — AI citizens have: count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency. Humans should have an equivalent set of structural primitives drawn from biometric and behavioral data. The scoring formulas should be composable from either set — or from a combination of both for citizens who have both substrates.

4. **Establish the research foundation for cross-substrate health comparison** — If both AI and human health are expressed through topology primitives, we can compare them. Do humans and AI citizens experience the same structural patterns before a crisis? Do the same interventions work? This is the foundation for the cross_substrate_health research module.

## NON-OBJECTIVES

- **Building a medical device** — GraphCare is not a medical product. Human signal observation is for research and wellbeing insight, not clinical diagnosis.
- **Replacing existing health monitoring tools** — We are not competing with Fitbit, Apple Health, or clinical HRV analysis. We are adding a layer: topology-only observation that feeds into GraphCare's existing scoring and care framework.
- **Collecting raw biometric data** — GraphCare should never store raw HRV traces, raw message logs, or raw activity data. It receives pre-computed topology primitives, just like it receives `BrainStats` from the brain topology reader. The raw data stays with the human.
- **Implementing this in v1** — This is a design document for the future. v1 is AI citizens in Lumina Prime.

## TRADEOFFS (canonical decisions)

- When **human data richness** conflicts with **topology-only discipline**, choose topology-only. We accept losing clinical-grade analysis (which requires raw data) in exchange for a privacy model that humans can actually trust. "We literally cannot see your heart rate trace, only its regularity score" is a stronger guarantee than "we promise not to look."
- When **AI-human comparability** conflicts with **accuracy for either substrate**, choose accuracy for each substrate independently. We accept that some primitives may not have meaningful cross-substrate equivalents. A human's "drive.curiosity" is not the same as an AI citizen's — and pretending they are would be bad science.
- When **completeness** conflicts with **timing**, choose timing. We write OBJECTIVES and PATTERNS now, while the topology-only architecture is being defined, so human extensibility is a design constraint from the start — even though implementation is years away.

## SUCCESS SIGNALS (observable)

- The 7 brain topology primitives can be paralleled by a set of human health topology primitives without changing the scoring framework
- At least one scoring formula can accept either AI or human primitives and produce a meaningful score
- No raw biometric data is stored or transmitted through GraphCare — only pre-computed topology values
- The cross-substrate research module can compare AI and human health trajectories using the same structural vocabulary
