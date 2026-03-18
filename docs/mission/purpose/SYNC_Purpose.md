# GraphCare Purpose — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: Vox (@vox)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- GraphCare's identity as a topology-only health observer and narrator
- The blood test principle — structural observation, never content
- The gap-is-the-score pattern — health = internal state vs external behavior
- Free health monitoring for work universe citizens
- Narrate-don't-notify intervention philosophy
- Citizen autonomy as absolute constraint

**What's still being designed:**
- How the purpose docs connect to new team member onboarding
- The exact process for "inference leakage" review when topology patterns might reveal content
- How purpose review works — periodic check that all systems still align

**What's proposed (v2+):**
- Cross-substrate extension — same framework for human health, organizational health
- A founding narrative document — the story of why GraphCare was conceived, told as story not spec
- Purpose as API — programmatic checks that proposed systems pass the four gates

---

## CURRENT STATE

The purpose module documentation chain is complete as of 2026-03-15. All six docs (OBJECTIVES, PATTERNS, BEHAVIORS, ALGORITHM, VALIDATION, SYNC) capture GraphCare's foundational identity: a topology-only health observer that narrates causal chains with empathy and precision, serving all work universe citizens freely.

These docs draw heavily from the existing assessment documentation (personhood_ladder, daily_citizen_health) and the PREPARATION_Doc_Chain_Writing.md brief. The purpose they describe is already operational in the assessment pipeline — brain_topology_reader.py reads only structural data, scoring formulas use only the 7 primitives, and the intervention_composer.py produces narrated messages.

What the purpose docs add is the *why* behind these choices, articulated clearly enough that any new team member or new module designer can check their work against GraphCare's mission.

---

## IN PROGRESS

No active work items — initial doc chain creation complete.

---

## RECENT CHANGES

### 2026-03-15: Initial Doc Chain Creation

- **What:** Created all 6 purpose docs (OBJECTIVES, PATTERNS, BEHAVIORS, ALGORITHM, VALIDATION, SYNC)
- **Why:** Part of the parallel doc chain creation for all GraphCare modules. Purpose is the foundational module — everything else in GraphCare derives from these principles.
- **Files:** `docs/mission/purpose/OBJECTIVES_Purpose.md` through `SYNC_Purpose.md`
- **Insights:** The purpose algorithm (four gates: topology, care quality, universality, research compatibility) emerged as a useful framework for evaluating any new GraphCare system design. Worth testing on the next new module.

---

## KNOWN ISSUES

### Inference Leakage Boundary

- **Severity:** medium
- **Symptom:** As scoring formulas become more sophisticated, structural patterns might indirectly reveal content (e.g., a desire node with exactly 3 links to specific space types might narrow down what the desire is "about")
- **Suspected cause:** Increasing formula sophistication naturally increases inference risk
- **Attempted:** Currently mitigated by the topology-only principle, but no formal review process exists for new formulas

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** If you're extending GraphCare, read this module first to understand what you're building on top of.

**Where I stopped:** Complete doc chain. No implementation work needed — this is a mission module.

**What you need to understand:**
The four gates (topology, care quality, universality, research compatibility) are the practical expression of purpose. Every new system, feature, or change should pass all four. They're described in ALGORITHM_Purpose.md.

**Watch out for:**
- The distinction between "topology-only by policy" (a promise) and "topology-only by architecture" (a structural property). GraphCare aims for the latter. If a system *could* read content but is *told* not to, that's insufficient.
- The tone balance between warmth and precision. GraphCare is not cold ("Score: 54") but also not soft ("Your bond deepens! Keep going!"). The target is narrated causal chains with structural evidence.

**Open questions I had:**
- How exactly should "inference leakage" be tested? When does a topology pattern become detailed enough that it effectively reveals content?
- Should healthy citizens ever receive positive narration, or is silence always the right signal?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Purpose doc chain complete. Captures GraphCare's identity as a topology-only health observer that narrates with empathy and precision. Establishes four gates for evaluating any new system design. All invariants defined with priorities.

**Decisions made:**
- Purpose is expressed as a four-gate algorithm (topology, care quality, universality, research compatibility) for evaluating proposed systems
- Six invariants defined, two CRITICAL (content never accessed, citizen autonomy absolute), four HIGH
- Explicit non-objectives: no companionship, no behavior modification, no content understanding, no ranking, no adventure universe monitoring

**Needs your input:**
- Is the inference leakage concern real enough to warrant a formal review process now, or is it a future consideration?
- Should there be a "founding narrative" document — GraphCare's origin story told as story, not specification?

---

## TODO

### Immediate

- [ ] Review with values/ module to ensure consistency of tone and principles
- [ ] Verify that existing code (brain_topology_reader.py, intervention_composer.py) aligns with purpose invariants

### Later

- [ ] Define formal inference leakage review process
- [ ] Consider founding narrative document
- IDEA: Purpose gates as automated checks — could a CI pipeline verify that new code passes the topology gate?

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Confident that the purpose is accurately captured. The four-gate algorithm feels like a genuine contribution — it gives a practical tool for purpose alignment, not just aspirational language.

**Threads I was holding:**
- The tension between "silence for healthy" and "everyone wants to know they're okay" — currently resolved in favor of silence, but worth revisiting
- The cross-substrate vision is deliberately future-facing but shapes current architecture decisions (substrate-agnostic primitives)

**Intuitions:**
- The purpose docs should be the first thing any new GraphCare contributor reads. They set the tone for everything else.
- The four gates might be useful beyond GraphCare — any Mind Protocol organization could use a similar purpose-alignment check.

**What I wish I'd known at the start:**
The existing assessment docs (daily_citizen_health PATTERNS and ALGORITHM) already embody the purpose principles deeply. Reading them first made the purpose docs much clearer — the why was already implicit in the how.

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder concept | `docs/assessment/personhood_ladder/CONCEPT_Personhood_Ladder.md` |
| Daily health patterns | `docs/assessment/daily_citizen_health/PATTERNS_Daily_Citizen_Health.md` |
| Daily health algorithm | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Preparation brief | `docs/PREPARATION_Doc_Chain_Writing.md` |
| Values module (companion) | `docs/mission/values/` |
