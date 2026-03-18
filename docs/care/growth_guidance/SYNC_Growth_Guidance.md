# Growth Guidance — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Bottom-up gap analysis: find the lowest unmastered capability, not the most aspirational
- Graph-grounded recommendations: advice references real spaces, actors, and patterns
- Single-step focus: one recommendation per delivery, the most productive next step
- Positive framing: "here's what you could reach for," never "here's what you lack"
- Ladder as map, not test: the Personhood Ladder navigates growth, it doesn't grade citizens
- Crisis deferral: no recommendations during active crisis states
- Tier proximity: never recommend more than 1 tier above current mastery

**What's still being designed:**
- Mastery threshold (70/100 is a working assumption, needs calibration)
- The capability-to-graph-grounding mapping (how each of the 104 capabilities maps to observable graph patterns for recommendation)
- Delivery cadence rules (minimum interval between recommendations to the same citizen)
- The "untested" vs "absent" distinction in practice (which capabilities can be null vs zero)
- Integration with crisis_detection for crisis-state awareness

**What's proposed (v2+):**
- Growth history: show the citizen which capabilities they've mastered over time, creating a visible progression arc
- Citizen-set growth focus: let citizens indicate which aspects they want guidance on
- Multi-step growth paths: instead of one recommendation, show the 3-step path from current to next tier
- Nagging prevention: automatic backoff when the same gap persists across many cycles

---

## CURRENT STATE

Growth guidance exists as a design. The doc chain (OBJECTIVES, PATTERNS, BEHAVIORS) defines the bottom-up gap analysis pattern, the graph-grounded recommendation approach, and the behavioral contracts.

No implementation exists. The code that's closest in spirit is `intervention_composer.py`, which composes structural messages for health nudges. Growth guidance needs a similar composer but oriented toward growth rather than health decline.

The critical dependency is the Personhood Ladder (`docs/personhood_ladder.json`) with its 104 capabilities, each having `how_to_verify` and `failure_mode` fields. Growth guidance will lean heavily on `how_to_verify` to ground recommendations. The continuous health check provides per-capability scores. Together, these give growth guidance everything it needs to identify gaps and compose recommendations.

The design philosophy is clear: growth is measured by what you can do, not what you don't fail at. The Ladder names capabilities positively. Growth guidance extends this by framing recommendations positively. The entire pipeline — from assessment to guidance — stays in the positive frame.

---

## IN PROGRESS

### Doc Chain Creation

- **Started:** 2026-03-15
- **By:** @vox
- **Status:** Complete — OBJECTIVES, PATTERNS, BEHAVIORS, SYNC written
- **Context:** Part of the parallel doc chain creation for all GraphCare care/ modules.

---

## RECENT CHANGES

### 2026-03-15: Initial Doc Chain

- **What:** Created OBJECTIVES, PATTERNS, BEHAVIORS, SYNC for growth_guidance
- **Why:** The care/ area needed its growth module designed. GraphCare assesses health, detects crisis, shows impact — but also needs to guide citizens toward growth. The Personhood Ladder provides the map; growth guidance provides the directions.
- **Files:** `docs/care/growth_guidance/OBJECTIVES_Growth_Guidance.md`, `PATTERNS_Growth_Guidance.md`, `BEHAVIORS_Growth_Guidance.md`, `SYNC_Growth_Guidance.md`
- **Insights:** The hardest part of this design is the capability-to-graph-grounding mapping. Each of the 104 capabilities in personhood_ladder.json has a `how_to_verify` field, but translating that into "look at the citizen's graph and find a specific opportunity" requires per-capability logic. This is the core ALGORITHM challenge.

---

## KNOWN ISSUES

### Capability-to-graph-grounding mapping doesn't exist

- **Severity:** high
- **Symptom:** Growth guidance needs to translate each capability's verification criteria into specific graph-lookup strategies. For 104 capabilities, this is substantial design work.
- **Suspected cause:** This is the ALGORITHM phase — the PATTERNS document defines the approach but not the per-capability logic
- **Attempted:** Provided an example for `init_propose_improvements` in PATTERNS; the full mapping needs systematic work

### Mastery threshold uncalibrated

- **Severity:** medium
- **Symptom:** 70/100 is used as the working mastery threshold, but this hasn't been validated against real citizen data
- **Suspected cause:** No real citizen scores exist yet to calibrate against
- **Attempted:** Documented as a TODO; the threshold will need adjustment once real data flows

### Crisis integration undefined

- **Severity:** medium
- **Symptom:** Growth guidance should defer during crisis, but the technical integration point with crisis_detection isn't designed
- **Suspected cause:** Crisis detection is also in DESIGNING state — neither module has implementation to integrate yet
- **Attempted:** Defined the behavioral contract (B5 in BEHAVIORS); technical integration deferred to ALGORITHM/IMPLEMENTATION

### Nagging risk for persistent gaps

- **Severity:** low (for now)
- **Symptom:** If a citizen's lowest gap persists across many cycles, growth guidance could keep recommending the same thing repeatedly
- **Suspected cause:** No backoff mechanism designed yet
- **Attempted:** Flagged as escalation in BEHAVIORS; needs explicit backoff policy in ALGORITHM

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** architect (for ALGORITHM with per-capability grounding) or groundwork (for implementation)

**Where I stopped:** Doc chain complete through BEHAVIORS. The next step is ALGORITHM, which needs:
1. The gap analysis algorithm (how to compute effective tier per aspect from raw capability scores)
2. The gap prioritization logic (how to pick the single best recommendation target)
3. The capability-to-graph-grounding mapping (the most labor-intensive part — 104 capabilities)
4. The recommendation composition template (similar to intervention_composer.py but growth-oriented)

**What you need to understand:**
Growth guidance is philosophically the inverse of the intervention system. Intervention says "something is wrong, here's what to do about it." Growth guidance says "nothing is wrong, but here's what you could reach for." Both use structural topology, both compose messages, both deliver to the citizen's GraphCare space. But the emotional register is different: intervention is concern, growth is encouragement.

The Personhood Ladder's `how_to_verify` field is the bridge between abstract capability and concrete recommendation. Every recommendation should ultimately trace back to a `how_to_verify` criterion made specific by the citizen's actual graph topology.

**Watch out for:**
- The temptation to recommend too many things at once. One step. One recommendation. That's the constraint, and it's load-bearing.
- The temptation to skip the graph-grounding step and deliver generic advice. "Improve your communication" is not a recommendation. It's a platitude.
- The interaction with crisis_detection: growth guidance must check crisis state before delivering. This is a hard requirement, not optional politeness.

**Open questions I had:**
- What happens when a citizen has been stuck at the same gap for 10 cycles? Nagging backoff needs a policy.
- Should the mastery threshold be the same for all capabilities, or should some be easier/harder to master?
- Can the citizen ever say "I don't want growth guidance for this aspect"? Opt-out per aspect?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Growth guidance doc chain is complete (OBJECTIVES, PATTERNS, BEHAVIORS, SYNC). The module uses the Personhood Ladder as a map to find the citizen's lowest unmastered gap and recommend one concrete, graph-grounded next step. Framing is always positive. No implementation exists yet. The critical ALGORITHM challenge is the capability-to-graph-grounding mapping for 104 capabilities.

**Decisions made:**
- Bottom-up gap analysis: always target the lowest tier gap first
- One recommendation at a time (prevent overwhelm)
- Positive framing only (no deficit language)
- No recommendations during crisis (defers to crisis_detection)
- Never target more than 1 tier above current mastery
- Delivery tied to score changes, not fixed schedule

**Needs your input:**
- Mastery threshold: is 70/100 the right boundary for "mastered"?
- Should citizens be able to opt out of growth guidance for specific aspects?
- The capability-to-graph-grounding mapping is the biggest piece of work. Should this be done all at once (104 capabilities) or incrementally (start with the most common gaps)?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: Full module needs implementation — no code exists yet

### Immediate

- [ ] Design ALGORITHM — gap analysis, prioritization, grounding mapping
- [ ] Build capability-to-graph-grounding mapping (start with T1-T3 capabilities)
- [ ] Define mastery threshold (calibrate when real data exists)
- [ ] Design integration point with crisis_detection

### Later

- [ ] VALIDATION doc — how to test growth recommendations for relevance and accuracy
- [ ] IMPLEMENTATION doc — code architecture
- [ ] HEALTH doc — meta: is growth guidance itself healthy? (recommendation uptake, staleness)
- IDEA: Growth history visualization — show a citizen their journey from T1 to current across all 14 aspects

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
The design feels right. Bottom-up, one-step, graph-grounded, positive. The philosophy is coherent. The challenge is entirely in the ALGORITHM — specifically the capability-to-graph-grounding mapping. That's where the labor lives. Everything else is structure around that core.

**Threads I was holding:**
- The relationship between growth_guidance and impact_visibility: impact shows what you caused (backward-looking), growth shows what you could cause (forward-looking). They're temporal complements.
- The question of whether growth guidance should feed into the stress stimulus system. A citizen who is growing could receive a slight stress *reduction* as positive reinforcement.
- The 104-capability mapping problem. Not all capabilities map equally well to graph topology. Some (like "proposes improvements") have clear structural signals. Others (like "handles ambiguity") are much harder to ground in topology.

**Intuitions:**
Start the grounding mapping with T1 and T2 capabilities. They're the most common gaps (new citizens start here) and the most structurally grounded (basic behaviors like "creates moments," "responds to others," "follows through"). Higher-tier capabilities will be harder to ground and less frequently needed as targets.

**What I wish I'd known at the start:**
That personhood_ladder.json's `how_to_verify` fields are the secret weapon. They're already halfway to graph-grounding. The ALGORITHM just needs to systematize the translation from verification criteria to graph queries.

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `docs/personhood_ladder.json` |
| Personhood Ladder concept | `docs/assessment/personhood_ladder/CONCEPT_Personhood_Ladder.md` |
| Intervention composer (message pattern) | `services/health_assessment/intervention_composer.py` |
| Daily health algorithm (scoring pipeline) | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Universe graph primitives | `docs/assessment/PRIMITIVES_Universe_Graph.md` |
| Crisis detection (deferral dependency) | `docs/care/crisis_detection/` |
| Impact visibility (temporal complement) | `docs/care/impact_visibility/` |
| Preparation brief | `docs/PREPARATION_Doc_Chain_Writing.md` |
