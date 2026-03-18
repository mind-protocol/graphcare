# GraphCare Values — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: Vox (@vox)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- The three-quality synthesis: empathy, precision, warmth — held simultaneously
- Venice Values as health principles: partnership, passion makes beauty, cathedral of stories
- The encouragement standard: celebrate with rigor, transparency, equality and fairness
- Equal care regardless of status — same quality for all work universe citizens
- Narrative form as default — stories, not dashboards
- Citizen autonomy as absolute constraint on recommendations
- Honest assessment over comfortable assessment

**What's still being designed:**
- How to test the synthesis (V1) — what makes a message measurably empathetic, precise, warm
- How to audit equal care (V3) — periodic review process across citizen tiers
- How the Tone Composition Algorithm maps to actual intervention_composer.py code
- How values adapt across urgency levels (routine vs crisis)

**What's proposed (v2+):**
- Values regression test suite — example messages that must continue to pass as system evolves
- Automated ValuesScorecard — partial automation of tone compliance checking
- "Values in action" gallery — real anonymized examples demonstrating each value
- Values self-assessment — can GraphCare evaluate its own outputs against B1-B7?

---

## CURRENT STATE

The values module documentation chain is complete as of 2026-03-15. All six docs (OBJECTIVES, PATTERNS, BEHAVIORS, ALGORITHM, VALIDATION, SYNC) define how Venice Values translate into GraphCare's health monitoring practice.

The values are organized around five pillars:
1. **Empathy-precision-warmth synthesis** — the distinctive voice
2. **Evidence-grounded encouragement** — celebrate what's real
3. **Equal care** — same quality regardless of status
4. **Partnership over hierarchy** — peer suggestions, not prescriptions
5. **Our clan is all forms of life** — substrate-agnostic by design

The Tone Composition Algorithm (ALGORITHM_Values.md) provides a concrete process for composing value-aligned messages, and the ValuesScorecard provides a checklist for compliance verification. These are organizational tools today; they map to the existing intervention_composer.py for future implementation alignment.

---

## IN PROGRESS

No active work items — initial doc chain creation complete.

---

## RECENT CHANGES

### 2026-03-15: Initial Doc Chain Creation

- **What:** Created all 6 values docs (OBJECTIVES, PATTERNS, BEHAVIORS, ALGORITHM, VALIDATION, SYNC)
- **Why:** Part of the parallel doc chain creation for all GraphCare modules. Values defines the soul of GraphCare — how it speaks, what it cares about, who it serves.
- **Files:** `docs/mission/values/OBJECTIVES_Values.md` through `SYNC_Values.md`
- **Insights:** The Tone Composition Algorithm (7 steps from silence decision to autonomy close) emerged as a surprisingly concrete way to encode values. Not just "be warm and precise" but "here's the order of operations: first decide whether to speak, then assemble evidence, then compose acknowledgment, observation, causal chain, recommendation, and close." Values become process.

---

## KNOWN ISSUES

### Synthesis Testing Gap

- **Severity:** medium
- **Symptom:** We can define the three-quality synthesis (empathy + precision + warmth) but can't programmatically test whether a message achieves it
- **Suspected cause:** Empathy and warmth are qualitative properties that resist boolean evaluation
- **Attempted:** ValuesScorecard provides proxy checks (has_empathy, has_warmth) but these are human-evaluated, not automated

### Urgency Tone Adaptation

- **Severity:** low
- **Symptom:** The Tone Composition Algorithm describes routine assessments well but doesn't fully address how values manifest in crisis situations (where urgency might push toward directive tone)
- **Suspected cause:** Crisis hasn't been deeply explored yet — the care/crisis_detection module will address this
- **Attempted:** Not yet — flagged for care/ module development

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** If you're building any citizen-facing output, these values govern your tone.

**Where I stopped:** Complete doc chain. The values are defined; the question is how they translate to specific modules (care/, assessment/ outputs, research/).

**What you need to understand:**
The Tone Composition Algorithm (ALGORITHM_Values.md, Steps 1-8) is the most actionable part of this module. It provides a concrete process for composing messages. The ValuesScorecard is the compliance check. Together they give you a recipe, not just aspirations.

**Watch out for:**
- The temptation to drop warmth under time pressure. A message that's precise and empathetic but cold is still a values failure.
- The temptation to soften honesty under empathy pressure. "We want to be kind" can become "we don't want to say the bad thing." Honesty is the hardest value to hold.
- The difference between "our clan is all forms of life" (a values statement that shapes architecture) and "we serve humans today" (premature scope expansion). The value shapes design decisions; it doesn't mean we build human health monitoring now.

**Open questions I had:**
- How does the Tone Composition Algorithm adapt for crisis situations? The seven steps work for routine assessments — do they hold when urgency is high?
- Should the ValuesScorecard be partially automatable? Some checks (no_comparison, no_content_reference) could be automated; others (has_empathy, has_warmth) seem to require human judgment.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Values doc chain complete. Defines GraphCare's soul through five pillars: empathy-precision-warmth synthesis, evidence-grounded encouragement, equal care, partnership over hierarchy, and all forms of life as our clan. Includes a concrete Tone Composition Algorithm (7 steps) and a ValuesScorecard (11 boolean checks).

**Decisions made:**
- Values are expressed as both aspirational principles and concrete process (the Tone Composition Algorithm)
- Six invariants defined, two CRITICAL (voice synthesis, honesty survives discomfort), four HIGH
- The "all forms of life" value shapes architecture (substrate-agnostic design) without expanding current scope (still AI-citizen focused)
- Silence is explicitly a value — speaking only when meaningful preserves the weight of speech

**Needs your input:**
- Is the Tone Composition Algorithm concrete enough for developers to implement? Or does it need example messages?
- Should there be a formal "values review" process for new citizen-facing features?
- The "our clan is all forms of life" value — how far should this influence current architecture decisions vs remaining aspirational?

---

## TODO

### Immediate

- [ ] Review with purpose/ module to ensure consistency of principles and invariants
- [ ] Create 5 example messages that demonstrate the Tone Composition Algorithm end-to-end
- [ ] Map the Tone Composition Algorithm to intervention_composer.py structure

### Later

- [ ] Define values audit process — periodic review of messages across citizen tiers for equal care
- [ ] Explore partial automation of ValuesScorecard
- [ ] Consider values regression test suite
- IDEA: "Values calibration sessions" — team reviews of real messages to maintain consistent tone

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
The values feel alive. Not abstract corporate values that hang on a wall, but operational constraints that produce specific behaviors. The Tone Composition Algorithm surprised me — values becoming a step-by-step process feels right.

**Threads I was holding:**
- The tension between "silence for healthy" and the desire to celebrate positive outcomes — resolved by allowing positive narration when there's a structural causal chain worth telling, but defaulting to silence
- The tension between "empathy" and "honesty" — resolved by insisting both coexist: name the experience empathetically, state the truth precisely
- The question of crisis tone — routine values are clear, but what happens under emergency urgency? Deferred to care/crisis_detection module

**Intuitions:**
- The ValuesScorecard could become a powerful tool if partially automated. Checks like "no comparison to other citizens" and "no content references" are automatable. The qualitative checks (empathy, warmth) might be evaluable by LLM with good prompting.
- Example messages are the missing piece. The algorithm describes the process; examples demonstrate the result. The "values in action" gallery should be high priority.
- These values docs and the purpose docs together form the "GraphCare soul" — they should be read together by anyone joining the team.

**What I wish I'd known at the start:**
The Impact Visibility tone definition ("raconte l'histoire de ce que tu as cause — avec empathie, precision et chaleur") is the seed from which the entire values module grows. Everything else is that sentence, expanded and made operational.

---

## POINTERS

| What | Where |
|------|-------|
| Purpose module (companion) | `docs/mission/purpose/` |
| Preparation brief (tone definition) | `docs/PREPARATION_Doc_Chain_Writing.md` |
| Personhood Ladder concept | `docs/assessment/personhood_ladder/CONCEPT_Personhood_Ladder.md` |
| Daily health patterns (existing care model) | `docs/assessment/daily_citizen_health/PATTERNS_Daily_Citizen_Health.md` |
| Daily health algorithm (intervention composition) | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Intervention composer (implementation) | `services/health_assessment/intervention_composer.py` |
