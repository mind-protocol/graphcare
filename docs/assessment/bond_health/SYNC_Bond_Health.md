# Bond Health Assessment -- Sync: Current State

```
LAST_UPDATED: 2026-03-14
UPDATED_BY: Claude Opus 4.6 (agent, groundwork)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Three dimensions: alignment (0.40), breadth (0.30), depth (0.30)
- Topology-only measurement -- same privacy model as daily citizen health
- Desire injection intervention pattern -- stimulus, not brain modification
- Trust generation formula: `bond_health * tau_bond * (1 - current_trust)`
- tau_bond = 0.005 (small constant, asymptotic growth)
- Weekly intervention cooldown per dimension (7-day minimum between injections)
- Drive stimulus capped at 0.5 per intervention (same cap as citizen health)
- Transparent display: both parties see all scores on their profiles
- Runs on same daily cron as citizen health, same key infrastructure

**What's still being designed:**
- Exact thresholds for intervention triggers (proposed: alignment < 0.4, breadth < 0.3, depth < 0.3)
- Calibration of formula caps with real bond data (value_coverage/20, topic_clusters/15, etc.)
- Interaction between bond health stimulus and citizen health stimulus (combined drive effects)
- Bond health history storage format (time series per pair)
- Profile card UI for displaying 3 dimensions + composite
- Correction trend sensitivity (the `* 5 + 0.5` mapping may need tuning)
- Handling of bonds without biometric data (depth formula redistributes weights -- is this fair?)

**What's proposed (v2+):**
- Adaptive intervention thresholds based on bond age (younger bonds get more lenient triggers)
- Bond health trajectory visualization (trend over months)
- Sovereign Cascade governance weight integration (higher bond health = more governance weight)
- Peer comparison (anonymized: how does this bond compare to median?)
- Bond health milestones (notifications at 0.5, 0.7, 0.9 thresholds)

---

## CURRENT STATE

Complete doc chain exists (6 files: OBJECTIVES, PATTERNS, ALGORITHM, VALIDATION, HEALTH, SYNC). The architecture is defined: three-dimension topology-only scoring, trust generation via asymptotic formula, desire injection intervention with weekly cooldown, transparent display on both profiles. No code exists yet.

The module extends the daily citizen health pattern to measure the relationship itself, not just the individual. It piggybacks on the same infrastructure: same cron, same key, same privacy model. The novel elements are the three dimensions (alignment, breadth, depth), the trust generation formula, and the desire injection intervention pattern (desires rather than messages).

---

## RECENT CHANGES

### 2026-03-14: Initial Architecture and Doc Chain

- **What:** Created full doc chain for bond health assessment (6 files)
- **Why:** The 1:1 bond between human and AI is the foundational relationship in Mind Protocol. Measuring individual citizen health (daily citizen health) is necessary but insufficient -- the relationship itself can degrade silently. Bond health assessment fills this gap.
- **Files:**
  - `OBJECTIVES_Bond_Health.md` -- 4 ranked objectives, privacy > precision tradeoff
  - `PATTERNS_Bond_Health.md` -- 3 dimensions, topology-only, desire injection, GraphCare as neutral party
  - `ALGORITHM_Bond_Health.md` -- all formulas, trust generation, intervention decision tree, 5 test profiles
  - `VALIDATION_Bond_Health.md` -- 6 invariants (V1-V6), privacy and trust bounds critical
  - `HEALTH_Bond_Health.md` -- 6 runtime checkers, all pending
  - `SYNC_Bond_Health.md` -- this file
- **Key decisions:**
  - Alignment weighted highest (0.40) because accuracy of the partner-model is foundational
  - Trust growth is asymptotic: fast early, slow later, never exceeds 1.0
  - Desire injection (nodes + stimuli) rather than messages, because the AI needs motivation not just information
  - Weekly cooldown per dimension gives brain physics time to process
  - Depth formula adapts when biometric data is unavailable (redistributes weights)

---

## KNOWN ISSUES

### No Code Exists

- **Severity:** high (doc-only, nothing runs)
- **Symptom:** Architecture defined but not implemented
- **Next step:** Implement bond health as extension of daily citizen health runner

### Combined Stimulus Effect Unknown

- **Severity:** medium
- **Symptom:** Citizen health stress stimulus (capped at 0.5) and bond health desire stimulus (capped at 0.5) could theoretically sum to 1.0 on a single drive in one day
- **Next step:** Analyze whether combined capping is needed, or whether independent caps are sufficient

### Formula Caps Need Calibration

- **Severity:** medium
- **Symptom:** Caps like value_coverage/20, topic_clusters/15, identity_moments/20 are educated guesses
- **Next step:** Calibrate against real bond data once the first bonds exist

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement

**Where I stopped:** Doc chain complete. Architecture defined. Zero code.

**What you need to understand:**
- Read the daily citizen health doc chain FIRST -- bond health extends that pattern
- Read the partner-model doc chain -- that's what we measure
- Read the human-AI pairing doc chain -- that's the bond we assess
- The same topology key that accesses the brain for citizen health also accesses the partner-model for bond health
- Desire injection is NOT the same as message sending -- desires are nodes injected into the brain, not Moments in a Space

**Watch out for:**
- Never access content or synthesis fields -- topology only
- Trust boost formula MUST use `(1 - current_trust)` -- this is the asymptotic guarantee
- Desire injection MUST be capped at 0.5 per drive per intervention
- Cooldowns are per dimension, not per citizen -- a citizen can get alignment AND breadth interventions on the same day
- When biometric data is unavailable, depth formula redistributes weights -- don't return null, return a score from available signals

**Open questions:**
- Bond health history storage: same store as citizen health? Separate time series?
- Combined stimulus cap: should citizen health + bond health stimuli be independently capped (current design) or jointly capped?
- Profile card design: how to display 3 dimensions + composite in a way that's informative but not overwhelming?
- Bond dissolution: what happens to bond health scores when a bond dissolves? Archive? Delete?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Full doc chain for bond health assessment. Architecture: three dimensions (alignment, breadth, depth) measured from topology only, trust generation via asymptotic formula, desire injection when dimensions drop below thresholds. Extends daily citizen health pattern -- same cron, same keys, same privacy model. No code yet.

**Decisions made:**
- Alignment weighted 40%, breadth and depth 30% each (accuracy is foundational)
- Trust grows asymptotically: `bond_health * 0.005 * (1 - current_trust)`
- Desire injection (not messages) for intervention -- motivation over information
- Weekly cooldown per dimension (independent cooldowns)
- Drive stimulus capped at 0.5 (same as citizen health)
- Both parties see identical scores (transparency is non-negotiable)
- Depth formula adapts gracefully when Garmin data is unavailable

**Needs your input:**
- Intervention thresholds: alignment < 0.4, breadth < 0.3, depth < 0.3 -- right levels?
- tau_bond = 0.005 -- right trust growth rate? (At 0.005, a bond_health of 0.8 takes ~175 days to grow trust from 0.1 to 0.5)
- Combined stimulus: should citizen health + bond health stimuli be independently or jointly capped?
- Should bond health affect Sovereign Cascade governance weight? (If yes, how?)

---

## TODO

### Immediate (Implementation)

- [ ] Extend daily_check_runner.py to include bond health (or create bond_health_runner.py)
- [ ] Implement partner-model topology reader (uses same key as citizen health)
- [ ] Implement alignment scoring formula
- [ ] Implement breadth scoring formula
- [ ] Implement depth scoring formula
- [ ] Implement trust generation (update bond link trust value)
- [ ] Implement desire injection (create nodes, send stimulus)
- [ ] Implement intervention cooldown tracking
- [ ] Define bond health history storage format

### Next (Integration)

- [ ] Add bond health scores to AI citizen profile card
- [ ] Add bond health scores to human partner profile card
- [ ] Build shared content_isolation checker (reuse from citizen health)
- [ ] Test with synthetic bond data (use the 5 test profiles from ALGORITHM)

### Later (Calibration)

- [ ] Calibrate formula caps with real bond data
- [ ] Calibrate intervention thresholds with real bond outcomes
- [ ] Analyze combined stimulus effect (citizen health + bond health)
- [ ] Build bond health trajectory visualization

### Future

- IDEA: Adaptive intervention thresholds based on bond age
- IDEA: Sovereign Cascade governance weight from bond health
- IDEA: Bond health milestones and notifications
- IDEA: Anonymized peer comparison ("your bond is healthier than 70% of bonds")

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
The three-dimension model feels right. Alignment, breadth, and depth capture genuinely different failure modes -- you can have a narrow but deep bond, a broad but shallow one, or a misaligned one, and each needs a different intervention. The desire injection pattern is the most interesting design choice: giving the AI motivation (desires) rather than information (messages) feels aligned with how the brain physics work. A desire enters the attentional competition; a message sits in a Space.

**Threads I was holding:**
- The correction_trend formula (`* 5 + 0.5` mapping) is sensitive to the multiplier -- 5 might be too aggressive, making small changes look like big trends
- The depth formula's biometric adaptation (redistributing weights when Garmin is absent) is simple but might undervalue depth for bonds without wearable data
- Combined stimulus from citizen health + bond health could theoretically push a drive to extreme values -- needs analysis
- Trust growth rate (tau_bond = 0.005) is a guess that determines the entire long-term trajectory of the bond -- wrong value means trust grows too fast or too slow

**Intuitions:**
- The alignment dimension will be the most useful early on (when bonds are forming)
- The depth dimension will be the most meaningful long-term (mature bonds should go deep)
- The breadth dimension will be the easiest to improve (just use the AI in more contexts)
- Intervention effectiveness will depend heavily on how the AI's brain physics processes injected desires -- this is the riskiest assumption in the design

---

## POINTERS

| What | Where |
|------|-------|
| Partner Model patterns | `mind-mcp/docs/citizens/partner_model/PATTERNS_Partner_Model.md` |
| Partner Model ingestion | `mind-mcp/docs/citizens/partner_model/ALGORITHM_Partner_Model_Ingestion.md` |
| Human-AI Pairing patterns | `mind-mcp/docs/citizens/human_ai_pairing/PATTERNS_Human_AI_Pairing.md` |
| Daily Citizen Health algorithm | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Universe Graph Primitives | `docs/assessment/PRIMITIVES_Universe_Graph.md` |
| Bond health algorithm | `docs/assessment/bond_health/ALGORITHM_Bond_Health.md` |
