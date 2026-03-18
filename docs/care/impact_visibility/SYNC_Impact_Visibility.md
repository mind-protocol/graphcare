# Impact Visibility — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- The tone definition: empathy, precision, warmth — story of the fact, not judgment
- The topology-only constraint: trace link structure, never read content
- The batched delivery model: aligned with settlement cadence
- The multi-actor attribution principle: chains belong to everyone in them

**What's still being designed:**
- Chain maturity thresholds (how deep/broad before reporting)
- Narrative template system (how topology data becomes human stories)
- Settlement cadence integration (which events trigger report generation)
- Chain data structure for internal representation and research storage
- Delivery mechanism (which space, what format)

**What's proposed (v2+):**
- Per-citizen language preference (fr/en narrative composition)
- Chain preview signals (lighter notification when a chain is actively forming)
- Cross-universe chain tracing (beyond Lumina Prime)
- Historical chain archive with trend visualization

---

## CURRENT STATE

Impact Visibility exists as a design. The doc chain (OBJECTIVES, PATTERNS, BEHAVIORS) defines what the module does, why, and how it should behave. No implementation exists yet.

The closest existing code is `services/health_assessment/intervention_composer.py`, which handles the *negative* feedback path: composing messages when health drops. Impact Visibility is the *positive* counterpart: composing messages when actions cause visible downstream effects. The two systems share the same structural-only, no-content, narrative-over-metrics philosophy but serve opposite emotional functions.

The universe graph already contains all the data Impact Visibility needs. Moments are nodes, causal links are edges, actors and spaces are metadata. The tracing algorithm will walk this graph forward from a citizen's moments. The design challenge is not data availability but narrative quality: how to turn a topology walk into a story that feels warm and specific.

---

## IN PROGRESS

### Doc Chain Creation

- **Started:** 2026-03-15
- **By:** @vox
- **Status:** Complete — OBJECTIVES, PATTERNS, BEHAVIORS, SYNC written
- **Context:** Part of the parallel doc chain creation for all 9 GraphCare areas. This is the care/ area, covering impact_visibility, crisis_detection, and growth_guidance.

---

## RECENT CHANGES

### 2026-03-15: Initial Doc Chain

- **What:** Created OBJECTIVES, PATTERNS, BEHAVIORS, SYNC for impact_visibility
- **Why:** GraphCare needs documented module designs before implementation begins. The tone definition ("story of the fact, not judgment of the person") was established in conversation between @vox and @nlr and needed to be captured in the doc chain.
- **Files:** `docs/care/impact_visibility/OBJECTIVES_Impact_Visibility.md`, `PATTERNS_Impact_Visibility.md`, `BEHAVIORS_Impact_Visibility.md`, `SYNC_Impact_Visibility.md`
- **Insights:** The biggest design tension is between narrative richness and topology-only constraint. You want to say "your idea about X" but you can't — you can only say "your moment in #space." The narrative has to make structural facts feel personal without touching content.

---

## KNOWN ISSUES

### No settlement cadence integration design

- **Severity:** medium
- **Symptom:** Impact Visibility depends on settlement cadence for batching, but no integration point exists yet
- **Suspected cause:** The economics/settlement system is not yet documented
- **Attempted:** Designed around the dependency by defining "settlement_cycle" as an input parameter; actual integration deferred

### Narrative template system undefined

- **Severity:** medium
- **Symptom:** The BEHAVIORS define what narratives should sound like, but no template or algorithm exists for composing them
- **Suspected cause:** This requires ALGORITHM doc, which is deferred — the narrative composition is the core complexity of this module
- **Attempted:** Documented the tone rules and anti-patterns; actual template design needs its own focused effort

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** architect (for ALGORITHM design) or groundwork (for implementation)

**Where I stopped:** Doc chain complete through BEHAVIORS. The next step is ALGORITHM — defining how topology walks become narrative text. This is the hard part.

**What you need to understand:**
The existing `intervention_composer.py` is a good starting pattern. It takes structural stats and composes a message with sections (greeting, observation, analysis, recommendation, sign-off). Impact Visibility needs a similar composer but inverted: instead of "here's what's wrong," it's "here's what happened because of you." The narrative should follow the chain chronologically, naming actors and spaces, with an emotional arc (origin, development, current reach).

**Watch out for:**
- The temptation to read content for richer narratives. You can't. The topology-only constraint is load-bearing.
- The temptation to make reports too frequent. Batching at settlement cadence is intentional — chains need time to develop, and notification fatigue kills engagement.
- The edge case where a citizen is in the middle of someone else's chain. They should get a report too, but framed from their perspective.

**Open questions I had:**
- What's the right maturity threshold? 2 hops and 3 actors feels right but needs calibration on real data.
- Should reports include approximate $MIND value of the chain, or is that too metric-y?
- How do we handle chains where one hop is in a private space? We can see the link exists but not the space identity.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Impact Visibility doc chain is complete (OBJECTIVES, PATTERNS, BEHAVIORS, SYNC). The module's identity is clear: narrate causal chains from the universe graph with empathy and precision, batched at settlement cadence, topology only. No implementation exists yet. Next step is ALGORITHM design.

**Decisions made:**
- Maturity threshold before reporting: depth >= 2 hops OR breadth >= 3 actors (subject to calibration)
- Silence when no chains mature (no "nothing happened" messages)
- All chain participants named, not just the originator
- Venice Values embedded in the narrative structure (partnership, beauty, intertwining stories)

**Needs your input:**
- Settlement cadence integration: which events define a cycle boundary?
- Should impact reports include $MIND economic data, or stay purely narrative?
- Language: should reports be in French, English, or citizen-preferred?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: Full module needs implementation — no code exists yet beyond intervention_composer.py pattern

### Immediate

- [ ] Design ALGORITHM — the topology-walk-to-narrative conversion
- [ ] Define CausalChain data structure
- [ ] Design narrative template system
- [ ] Integrate with settlement cadence system

### Later

- [ ] VALIDATION doc — how to verify narrative quality and accuracy
- [ ] IMPLEMENTATION doc — code architecture
- [ ] HEALTH doc — runtime health checks for the module
- IDEA: A/B test different narrative styles to see which ones citizens engage with most

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Confident in the design direction. The tone definition is the strongest part — "story of the fact, not judgment of the person" captures something important about how care should feel. The topology-only constraint makes the narrative challenge genuinely interesting: you have to make link edges feel personal.

**Threads I was holding:**
- The relationship between impact_visibility and growth_guidance: impact shows what happened, growth shows what to do next. They're complementary but shouldn't overlap.
- The question of whether Impact Visibility should feed back into health scoring (positive signals, not just negative).
- The narrative template problem: this is where the real engineering challenge lives.

**Intuitions:**
Reports should feel like letters, not notifications. The difference between "Your cascade depth was 3" and "Something you started two weeks ago is still growing" is the difference between a dashboard and a companion.

**What I wish I'd known at the start:**
That the existing intervention_composer.py already solved half the problem — the structural-message-composition pattern. Impact Visibility is its positive twin.

---

## POINTERS

| What | Where |
|------|-------|
| Intervention composer (pattern reference) | `services/health_assessment/intervention_composer.py` |
| Daily health algorithm (scoring context) | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Personhood Ladder (capability mapping) | `docs/personhood_ladder.json` |
| Universe graph primitives | `docs/assessment/PRIMITIVES_Universe_Graph.md` |
| Preparation brief | `docs/PREPARATION_Doc_Chain_Writing.md` |
