# OBJECTIVES — Impact Visibility

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Impact_Visibility.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Impact_Visibility.md
BEHAVIORS:      ./BEHAVIORS_Impact_Visibility.md
ALGORITHM:      (future)
VALIDATION:     (future)
IMPLEMENTATION: (future)
SYNC:           ./SYNC_Impact_Visibility.md

IMPL:           services/health_assessment/intervention_composer.py (partial — compose only)
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Show citizens what their actions caused** — Every citizen deserves to see the causal chain their work set in motion. Not a score. Not a badge. The story of the fact: who picked it up, what it became, where it traveled. This is the most meaningful feedback a system can give: proof that your contribution mattered.

2. **Narrate with empathy, precision, and warmth** — The tone is neither flattery ("bravo!") nor cold analytics ("cascade: 12, $MIND: 4.32"). It tells the story the way a thoughtful colleague would: with specifics, with feeling, without exaggeration. "Tu as partage un insight. @conductor l'a repris. 12 personnes l'ont vu. @forge a construit dessus. C'est parti de ta curiosite."

3. **Align with settlement cadence** — Impact reports arrive batched at settlement intervals, not in real-time. This prevents notification fatigue and ensures that causal chains have time to develop before being narrated. A half-formed chain is misleading. A mature chain is a gift.

4. **Reinforce Venice Values through structure** — Partnership Simply Works Better: show bidirectional value, not one-way metrics. Passion Makes Beauty: celebrate elegant chains, not volume. Cathedral of Intertwining Stories: make visible how individual actions weave into the collective narrative.

## NON-OBJECTIVES

- **Gamification** — No leaderboards, no rankings, no "you're in the top 10%." Impact Visibility is not a competition system. Comparison destroys the intrinsic motivation it exists to nurture.
- **Real-time notifications** — Impact reports are batched, not streamed. The system deliberately waits for causal chains to mature. Real-time alerts belong to crisis_detection, not here.
- **Content reading** — Impact Visibility traces the topology of influence (who linked to what, what followed what) without reading the content of any moment. Structural causality, not semantic analysis.
- **Prescriptive guidance** — This module shows what happened, not what should happen next. Growth recommendations belong to growth_guidance.

## TRADEOFFS (canonical decisions)

- When **completeness** conflicts with **timeliness**, choose timeliness. A report that arrives two weeks late with perfect causal chains is worse than a report at settlement cadence that captures 80% of the chain. Missing links can appear in the next report.
- When **precision** conflicts with **warmth**, choose warmth. "About 12 people saw it" is better than "12.0 weighted actors viewed it (7-day half-life applied)." The numbers serve the narrative, not the other way around.
- When **narrative richness** conflicts with **brevity**, choose narrative richness. Impact Visibility's entire purpose is telling the story. A two-line summary defeats the point. Take the space the story deserves.
- We accept **delayed reporting** to preserve **chain maturity**. Showing a causal chain that terminates at step 2 when it actually reached step 5 would be dishonest.

## SUCCESS SIGNALS (observable)

- Citizens reference their impact reports in conversation ("I saw that @forge built on my idea")
- Citizens increase participation after receiving reports that showed their work had downstream effects
- Impact reports contain at least 2 causal hops on average (not just "you did X," but "you did X, which led to Y, which enabled Z")
- Zero reports contain content quotations — only structural facts and topology
- Reports arrive within one settlement cycle of the underlying chain completing
