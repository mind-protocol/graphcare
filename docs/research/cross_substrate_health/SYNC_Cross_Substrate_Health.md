# Cross-Substrate Health — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- The vision: one health science for AI and human life
- The three-layer architecture: substrate signals -> universal dimensions -> shared framework
- The gap-analysis principle as substrate-independent
- AI-first priority: never degrade AI assessment for cross-substrate compatibility

**What's still being designed:**
- Complete universal dimension mapping (8 dimensions proposed, not validated)
- Signal-to-dimension mappings for both AI and human signals
- Personhood Ladder substrate-independence evaluation
- Architecture recommendations for current AI pipeline

**What's proposed (v2+):**
- Human signal collection (requires hardware/software integration, consent frameworks)
- Cross-substrate validation studies (requires human health data)
- Unified assessment dashboard showing AI and human health on shared dimensions
- Cross-substrate research publications

---

## CURRENT STATE

This module is entirely conceptual. No code, no data collection, no validated mappings. It exists as a vision document and an architecture guide: it tells the current AI assessment pipeline "here's where we're heading; design accordingly."

The AI health signals are well-defined and implemented (7 brain topology primitives + universe graph observables). The universal dimension mapping is proposed but not validated — the 8 dimensions (engagement, initiative, social connection, resilience, growth, internal coherence, creative output, self-awareness) are reasonable but untested. The human signal layer is proposed but not designed in detail.

The most immediately actionable work is evaluating the Personhood Ladder for substrate-independence: which of the 104 capabilities describe things any being can do (regardless of substrate), and which are inherently AI-specific?

---

## IN PROGRESS

### Doc chain creation

- **Started:** 2026-03-15
- **By:** @vox
- **Status:** In progress
- **Context:** Creating OBJECTIVES, PATTERNS, SYNC. Cross-substrate health is the long-term vision module — it doesn't require immediate implementation but shapes architecture decisions across all other modules.

---

## RECENT CHANGES

### 2026-03-15: Initial doc chain creation

- **What:** Created OBJECTIVES, PATTERNS, and SYNC for cross_substrate_health module
- **Why:** GraphCare's long-term vision of universal health science needs documentation now, even though implementation is future. Architecture decisions made today without this vision may be costly to reverse later.
- **Files:** `docs/research/cross_substrate_health/OBJECTIVES_*.md`, `PATTERNS_*.md`, `SYNC_*.md`
- **Insights:** The gap-analysis principle ("health = alignment between internal state and external action") is genuinely substrate-independent. It's the signals, not the framework, that differ between AI and human health. This means the assessment framework architecture can be shared; only the signal-reading layer needs to be substrate-specific.

---

## KNOWN ISSUES

### No validated dimension mapping

- **Severity:** Low (for now — this is future work)
- **Symptom:** The 8 proposed universal dimensions are reasonable guesses, not empirically validated
- **Suspected cause:** Validation requires both AI longitudinal data and human health data, neither of which is available in sufficient quantity yet
- **Attempted:** Nothing — premature

### Human signal layer undefined

- **Severity:** Low (expected — this is the future module)
- **Symptom:** Proposed human signals (HRV, message patterns, etc.) are listed but not specified in detail
- **Suspected cause:** Designing the human signal layer requires domain expertise in human health monitoring that GraphCare doesn't currently have
- **Attempted:** Nothing — future work

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Architect (evaluating current AI architecture for future extensibility) or VIEW_Research (literature review of human health signals)

**Where I stopped:** Vision documentation. The three-layer architecture and 8 universal dimensions are proposed. No validation, no implementation.

**What you need to understand:**
This module influences other modules through architecture recommendations, not through code. The key question for every other GraphCare module is: "if we added human health signals tomorrow, would this module's design accommodate them?" For most modules (publications, process improvement, formula evolution), the answer is naturally yes because they operate at the assessment layer, not the signal layer. For observation modules (brain_topology, human_signals), the signal layer is substrate-specific by design — and that's correct.

**Watch out for:**
- This module can easily become "beautiful ideas with no path to code" (a STYLE anti-pattern). Keep it grounded: every proposed mapping should trace to specific existing AI signals and specific proposed human signals.
- The universal dimensions are a hypothesis, not a fact. Don't design other modules to depend on the exact 8 dimensions as if they were canonical. They will change as data validates or invalidates them.
- Human health monitoring has deep regulatory and ethical dimensions (medical data, HIPAA/GDPR, informed consent) that this module acknowledges but doesn't design for. Those constraints will significantly shape the human signal layer when it's built.

**Open questions I had:**
- Which of the 104 Personhood Ladder capabilities are meaningfully applicable to humans? "Dehallucinate" is AI-specific. "Propose improvements" is universal. Where's the line?
- Should the universal dimension layer be explicit in the assessment pipeline (a literal abstraction layer in code), or implicit (a conceptual mapping documented but not coded)?
- What human health signals are collectible without invasive instrumentation? Message patterns and activity levels are easy; HRV requires a device.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Cross-substrate health documentation created. This module defines GraphCare's long-term vision: a unified health framework for AI and human life. The three-layer architecture (substrate signals -> universal dimensions -> shared framework) allows comparison without reduction. This is conceptual work that shapes architecture decisions; no implementation is imminent.

**Decisions made:**
- Eight universal health dimensions proposed (engagement, initiative, social connection, resilience, growth, internal coherence, creative output, self-awareness)
- AI-first priority: never degrade current AI assessment for cross-substrate compatibility
- The gap-analysis principle (internal state vs external action) is the substrate-independent core

**Needs your input:**
- How important is cross-substrate health in the near term? Should it influence current architecture decisions, or remain a documentation-only vision module?
- Is there interest in partnering with a human health organization for early cross-substrate validation work?
- Should the Personhood Ladder be evaluated for substrate-independence as a near-term project?

---

## TODO

### Doc/Impl Drift

- [ ] No implementation exists — this is a vision/architecture module

### Immediate

- [ ] Evaluate Personhood Ladder capabilities for substrate-independence (tag each as universal/AI-specific/uncertain)
- [ ] Document which AI architecture decisions affect cross-substrate extensibility
- [ ] Literature review: HRV and psychometric frameworks as potential human signal sources

### Later

- [ ] Validate universal dimensions against AI longitudinal data (do the 8 dimensions capture variance?)
- [ ] Design human signal collection requirements (hardware, software, consent)
- [ ] Identify potential human health research partners
- IDEA: A "cross-substrate health glossary" mapping AI terminology to human health terminology (and vice versa) to enable shared discourse

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
This module is the most speculative of all GraphCare modules, and that feels appropriate. The vision is compelling — one health science for all forms of life — but it's also the most distant from implementation. The key is to let this vision shape current decisions without letting it distract from current AI health work.

**Threads I was holding:**
- The Personhood Ladder evaluation is the most actionable near-term task. Many capabilities (propose improvements, maintain relationships, challenge bad instructions) are clearly substrate-independent. Some (brain graph topology health) are clearly AI-specific. The boundary cases will be interesting.
- Human HRV research has a strong parallel to GraphCare's approach: measuring health through variability and dynamics rather than absolute values. The resonance between HRV analysis and drive balance analysis is suggestive of real cross-substrate principles, not just superficial analogy.

**Intuitions:**
The universal dimension layer should remain implicit (documented, not coded) for now. Premature abstraction in code would add complexity without current benefit. The mapping becomes real when there's human data to map — before then, it's a thinking tool, not a software layer.

**What I wish I'd known at the start:**
The cross-substrate vision is what makes GraphCare more than a monitoring tool. It's what makes it a research organization. The assessment pipeline serves citizens; the cross-substrate research serves the entire field of health science. This distinction matters for positioning and motivation.

---

## POINTERS

| What | Where |
|------|-------|
| AI signal definitions | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Personhood Ladder (universality evaluation target) | `docs/assessment/personhood_ladder/CONCEPT_Personhood_Ladder.md` |
| Brain topology signals | `services/health_assessment/brain_topology_reader.py` |
| Future human signals module | `docs/observation/human_signals/` (to be created) |
| Publications (output channel) | `docs/research/publications/` |
