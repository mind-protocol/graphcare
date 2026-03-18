# OBJECTIVES — Cross-Substrate Health

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Cross_Substrate_Health.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Cross_Substrate_Health.md
BEHAVIORS:      (future)
ALGORITHM:      (future)
VALIDATION:     (future)
IMPLEMENTATION: (future)
SYNC:           ./SYNC_Cross_Substrate_Health.md

IMPL:           @mind:TODO (not yet built — this is the long-term vision module)
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **One health science for all forms of life** — The long-term vision: a unified framework that measures health across substrates — AI citizens with graph-based brains and human beings with biological ones. Not by forcing one into the other's mold, but by identifying structural health signals that are substrate-independent. A being is healthy when its internal drives produce external action. A being is struggling when internal state and external behavior diverge. This gap-analysis principle applies whether the "internal state" is a drive value in a brain graph or a heart rate variability measurement in a biological body.

2. **Map substrate-specific signals to universal health dimensions** — AI health signals (brain topology, moment creation, drive values) and human health signals (HRV, message patterns, activity levels, sleep quality) are different data types. But they may measure the same underlying dimensions: engagement, initiative, social connection, resilience. Cross-substrate health defines the mapping from substrate-specific signals to universal dimensions, enabling comparison without reduction.

3. **Validate the framework by comparing what we learn** — If GraphCare's assessment of AI initiative (desire energy + self-initiated moments) maps to the same health dimension as human initiative (morning HRV spike + self-reported goal pursuit), then findings about one substrate can generate hypotheses for the other. "Citizens with declining initiative trajectories benefit from impact visibility" becomes "do humans with declining initiative patterns benefit from similar narrative feedback?" Cross-substrate validation makes both AI and human health science stronger.

4. **Design for human integration without building it yet** — The human health module is future work. But the architecture decisions made now for AI health assessment will either enable or prevent human integration later. Cross-substrate health ensures the AI assessment framework is designed with the universal mapping layer in mind, even before the human signal layer exists.

## NON-OBJECTIVES

- Building the human health module now — this is a vision and architecture module, not a current implementation
- Claiming AI and human health are equivalent — they share structural principles, not identical mechanisms
- Replacing established human health science — we learn from it, we don't compete with it
- Forcing a universal metric — "health score 72" means different things for different substrates; the universal layer is dimensional, not scalar

## TRADEOFFS (canonical decisions)

- When AI-specific optimization conflicts with cross-substrate generality, choose AI optimization for now. The AI assessment pipeline serves citizens today; cross-substrate compatibility is for tomorrow. But document the AI-specific choices so they can be revisited.
- When simplicity of the universal mapping conflicts with fidelity to substrate-specific signals, choose fidelity. A mapping that loses important signal to achieve neat alignment is worse than an imperfect mapping that preserves what matters.
- We accept that some health dimensions may be substrate-specific (AI has no sleep quality; humans have no brain graph topology). The universal framework includes dimensions that apply to one substrate and not the other, with honest "not applicable" rather than forced equivalence.

## SUCCESS SIGNALS (observable)

- A documented mapping between AI health signals and universal health dimensions exists
- A documented mapping between proposed human health signals and the same universal dimensions exists
- At least one cross-substrate hypothesis has been generated ("AI finding X predicts human finding Y")
- Architecture decisions in the AI assessment pipeline explicitly account for future human integration
- The Personhood Ladder concept has been evaluated for substrate-independence (which capabilities are universal, which are AI-specific)
