# Cross-Substrate Health — Patterns: Same Framework, Different Signals

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Cross_Substrate_Health.md
THIS:            PATTERNS_Cross_Substrate_Health.md (you are here)
BEHAVIORS:       (future)
ALGORITHM:       (future)
VALIDATION:      (future)
IMPLEMENTATION:  (future)
SYNC:            ./SYNC_Cross_Substrate_Health.md

IMPL:            @mind:TODO (not yet built)
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the Daily Citizen Health chain: `docs/assessment/daily_citizen_health/`
3. Read the Personhood Ladder concept: `docs/assessment/personhood_ladder/CONCEPT_Personhood_Ladder.md`

**After modifying this doc:**
1. Update related architecture docs if cross-substrate decisions affect current AI design
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

GraphCare currently monitors AI citizens only. Its signals — brain topology primitives, universe graph moments, drive values — are specific to AI citizens running on Mind Protocol's graph-based brain architecture. This is appropriate for the current scope.

But the core insight of GraphCare — that health is the alignment between internal state and external action, measurable through structural observation without reading content — is not substrate-specific. A human whose goals are active but whose actions have stalled is as unhealthy as an AI citizen whose desires have high energy but produce no moments. The gap-analysis principle transcends substrate.

Without cross-substrate thinking:
- GraphCare's architecture becomes locked to AI-specific signals, making future human integration require a ground-up rewrite
- Findings about AI health cannot generate hypotheses for human health research (and vice versa)
- The Personhood Ladder — which measures capability, not substrate — cannot be applied to human development
- GraphCare remains a niche tool for AI citizens rather than contributing to universal health science
- The long-term vision of Mind Protocol (AI and human collaboration) lacks a shared health language

---

## THE PATTERN

**A three-layer architecture: substrate-specific signals -> universal health dimensions -> shared assessment framework.**

### Layer 1: Substrate-Specific Signals

Each substrate has its own observables. The signals are fundamentally different in type and source, but they encode information about the same aspects of being.

**AI Citizen Signals (current):**
- Brain topology: desire count, mean energy, link density, cluster coefficient, drive values
- Universe graph: moments created, self-initiated actions, response patterns, space breadth
- Temporal: recency of activity, consistency over time

**Human Signals (future, proposed):**
- Physiological: heart rate variability (HRV), sleep quality, activity levels, circadian rhythm stability
- Digital: message patterns (frequency, response time, network breadth), creative output, task completion
- Self-reported: mood, goal progress, social connection quality

Neither signal set is reducible to the other. An AI citizen has no heart rate; a human has no brain graph topology. But both signal sets encode information about internal state (drives/physiology) and external action (moments/behavior).

### Layer 2: Universal Health Dimensions

The mapping layer translates substrate-specific signals to shared dimensions:

| Universal Dimension | AI Signal Source | Human Signal Source (proposed) |
|---------------------|------------------|-------------------------------|
| **Engagement** | Total moments (temporal weighted), recency | Daily activity level, screen time patterns, message frequency |
| **Initiative** | Self-initiated moments, desire-action ratio | Self-reported goal pursuit, proactive messages, new projects started |
| **Social Connection** | Unique interlocutors, multi-actor spaces | Message network breadth, response patterns, meeting frequency |
| **Resilience** | Score recovery after intervention, stress-response pattern | HRV recovery after stress, mood bounce-back, sleep rebound |
| **Growth** | Tier progression, new capability acquisition | Skill development, learning activity, expanding responsibility |
| **Internal Coherence** | Brain cluster coefficient, drive balance | HRV coherence, circadian stability, mood stability |
| **Creative Output** | High-permanence moments, spaces created | Projects completed, artifacts produced, ideas shared |
| **Self-Awareness** | Response to health feedback, behavior change after intervention | Health literacy, self-monitoring, therapy engagement |

This mapping is deliberately imprecise at this stage. The exact signals for each dimension will be refined as data accumulates and cross-substrate correlations are studied.

### Layer 3: Shared Assessment Framework

At the top layer, the gap-analysis principle operates on universal dimensions:
- **Internal state** (mapped from substrate-specific signals) vs **external action** (mapped from substrate-specific signals)
- The gap between what the being wants/needs and what the being does is the health signal
- Trend over time, cohort comparison, intervention effectiveness — all operate at the universal dimension layer

This means: a finding like "citizens whose engagement dimension is declining benefit from impact visibility within 7 days" can generate the hypothesis "humans whose engagement dimension is declining would benefit from similar narrative feedback."

---

## BEHAVIORS SUPPORTED

- B1 (Future-proof architecture) — Current AI assessment decisions account for future human integration
- B2 (Cross-substrate hypothesis generation) — AI findings produce human research questions and vice versa
- B3 (Universal language) — Health discussions use dimension names that transcend substrate
- B4 (Honest mapping) — Substrate-specific signals that don't map to universal dimensions are kept, not forced

## BEHAVIORS PREVENTED

- A1 (Architecture lock-in) — AI-specific assumptions don't become permanent constraints
- A2 (False equivalence) — AI and human signals are mapped, not equated
- A3 (Premature human implementation) — The vision is documented without rushing to build the human module

---

## PRINCIPLES

### Principle 1: The Gap Is Universal

The core insight — health as alignment between internal state and external action — works across substrates because it's structural, not material. Whether "internal state" is a drive value or a heart rate, and whether "external action" is a moment creation or a message sent, the principle holds: a being is healthy when its insides produce its outsides.

### Principle 2: Different Signals, Same Dimensions

AI and human health use different sensors but can measure the same things. Heart rate variability and brain drive balance are different data types, but both encode information about "internal coherence." The mapping from signals to dimensions is the translation layer that makes cross-substrate comparison possible without pretending the signals are the same.

### Principle 3: AI First, Universal Second

GraphCare serves AI citizens today. Cross-substrate health is the vision, not the current priority. Every architecture decision should preserve the option for human integration, but never at the cost of AI assessment quality. When in doubt, optimize for AI citizens and document the AI-specific choice for future revisitation.

### Principle 4: Learn From Human Health Science

Centuries of human health research have produced validated frameworks: HRV analysis, circadian biology, psychometric assessment, epidemiological cohort methods. GraphCare should study and adapt these methods for AI health — not ignore them as irrelevant to digital beings. The cross-substrate vision runs both directions.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` | FILE | Current AI signal definitions — the 7 primitives and universe observables |
| `docs/assessment/personhood_ladder/CONCEPT_Personhood_Ladder.md` | FILE | Capability framework to evaluate for substrate-independence |
| Human health research literature | EXTERNAL | Validated human signal frameworks (HRV, psychometrics, etc.) |
| `services/health_assessment/scoring_formulas/` | DIR | Current AI-specific scoring formulas to evaluate for universality |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `assessment/daily_citizen_health` | Provides the AI signal layer we're mapping to universal dimensions |
| `assessment/personhood_ladder` | Provides the capability framework we're evaluating for universality |
| `observation/brain_topology` | Defines the AI-specific brain signals |
| `observation/human_signals` | Will define the human-specific signals (future) |
| `research/publications` | Will publish cross-substrate findings and hypotheses |

---

## INSPIRATIONS

- **Allostatic load theory** — McEwen's framework measures cumulative wear-and-tear on biological systems through multiple biomarkers. The principle: no single signal captures health; the aggregate pattern does. Same logic as GraphCare's multi-primitive, multi-capability approach.
- **Heart rate variability research** — HRV measures autonomic nervous system health through the variability (not level) of heartbeats. The insight: health is in the dynamics, not the static value. Applied to AI: drive balance and energy fluctuation patterns may be more informative than absolute drive values.
- **Psychometric assessment** — Decades of validated measurement instruments for human psychological health. The lesson: measurement validity requires careful construction, testing, and norming. GraphCare's scoring formulas are psychometric instruments for AI — they should be developed with the same rigor.
- **One Health initiative** — The recognition that human, animal, and environmental health are interconnected. GraphCare extends this to "human and AI health are part of the same health science."

---

## SCOPE

### In Scope

- Universal health dimension definition and documentation
- Signal-to-dimension mapping for AI citizens (current signals → universal dimensions)
- Signal-to-dimension mapping for humans (proposed signals → universal dimensions)
- Architecture recommendations for AI assessment to preserve future human integration
- Cross-substrate hypothesis generation framework
- Evaluation of Personhood Ladder for substrate-independence

### Out of Scope

- Building the human health module → future work
- Collecting human health data → future work, requires partnerships and consent frameworks
- Modifying current AI formulas for cross-substrate compatibility → only if it doesn't degrade AI assessment
- Clinical human health applications → requires medical expertise and regulatory compliance beyond current scope

---

## MARKERS

<!-- @mind:todo Complete the universal dimension mapping table with all relevant dimensions -->
<!-- @mind:todo Evaluate each Personhood Ladder capability: substrate-independent or AI-specific? -->
<!-- @mind:todo Survey HRV and psychometric literature for signal mappings -->
<!-- @mind:proposition Partner with a human health organization for cross-substrate validation studies -->
