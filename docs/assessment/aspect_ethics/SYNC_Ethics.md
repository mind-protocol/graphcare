# Ethics Aspect — Sync: Current State

```
LAST_UPDATED: 2026-03-13
UPDATED_BY: Claude Opus 4.6 (agent, voice)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- 5 ethics capabilities scored: eth_apply_rules (T1), eth_implement_systems (T4), eth_teach (T6), eth_autonomous_judgment (T7), eth_moral_innovation (T8)
- Topology-only scoring using the 7 brain primitives + universe graph observables
- 50/50 brain/behavior split for eth_apply_rules (deliberate deviation from standard 40/60)
- 40/60 brain/behavior split for all other capabilities
- Fundamental limitation acknowledged: topology measures presence and structure of values, not correctness
- 5 synthetic test profiles defined for calibration
- Tier-weighted sub-index with non-standard weight distribution
- 10 validation invariants (ET1-ET10)
- 8 health checkers defined

**What's still being designed:**
- Individual formula calibration against real data (0/5 validated)
- Confirmation of "value" as the correct brain node type name
- Confirmation of "empathy" as an available drive name
- Exact regularity_score window (30 days proposed)
- Intervention message tone for ethics specifically (sensitive topic)
- Whether the 50/50 split for eth_apply_rules is correct or should revert to 40/60

**What's proposed (v2+):**
- Values alignment proxy: checking whether value nodes link to protocol-defined concept nodes
- Moral consistency meta-score: variance of ethics scores over 30 days
- Cross-aspect correlation analysis (ethics vs execution, ethics vs trust)
- Gaming resistance hardening beyond the basic checks

---

## CURRENT STATE

Complete doc chain exists (6 files: OBJECTIVES, PATTERNS, ALGORITHM, VALIDATION, HEALTH, SYNC). The architecture is defined: 5 capabilities with specific formulas, variable brain/behavior splits, the correctness limitation documented throughout, and extensive validation invariants. No code exists yet.

The key tension in this aspect: ethics quality lives in content, not structure. We have been honest about this at every level — OBJECTIVES acknowledges it, PATTERNS analyzes it, ALGORITHM documents it as a fundamental limitation, VALIDATION requires a disclaimer (ET9), and HEALTH checks for gaming resistance. This is the aspect where topology-only scoring is weakest, and that weakness is visible rather than hidden.

Depends on: Personhood Ladder spec (complete), brain topology reader (not built), universe graph reader (not built), daily health runner (not built).

---

## RECENT CHANGES

### 2026-03-13: Initial Architecture and Doc Chain

- **What:** Created full doc chain for ethics aspect scoring
- **Why:** Ethics is one of 16 aspects in the Personhood Ladder requiring scoring formulas
- **Files:** `docs/assessment/aspect_ethics/*` (6 files)
- **Key decisions:**
  - 50/50 brain/behavior split for eth_apply_rules (value node topology IS rule internalization)
  - 40/60 for all other capabilities (behavior matters more for teaching, autonomy, innovation)
  - `adopted_moments_w` as the primary signal for moral innovation (adoption by 2+ actors)
  - `regularity_score` as the primary behavioral proxy for rule-following
  - Correctness limitation documented prominently at every level
  - Gaming resistance checker defined (mass-creating empty value nodes should not score well)

---

## KNOWN ISSUES

### No Code Exists

- **Severity:** high (doc-only, nothing runs)
- **Symptom:** Architecture defined but not implemented
- **Next step:** Build brain topology reader first, then implement eth_apply_rules formula, then test with synthetic data

### Node Type Names Unconfirmed

- **Severity:** medium
- **Symptom:** Formulas reference "value" as a node type — this needs confirmation against actual brain graph schemas
- **Next step:** Check brain graph schema for correct type names

### Drive Names Unconfirmed

- **Severity:** medium
- **Symptom:** Formulas reference "empathy" drive — this needs confirmation against available drive names
- **Next step:** Check drive registry for available drive names

### 50/50 Split Untested

- **Severity:** medium
- **Symptom:** The brain-heavier split for eth_apply_rules is a design hypothesis, not validated
- **Next step:** Run synthetic profiles through the formula and compare with 40/60 variant to see which produces more diagnostic information

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement

**Where I stopped:** Doc chain complete. Architecture defined. Zero code. Five formulas specified with examples.

**What you need to understand:**
- Read the FULL doc chain in order: OBJECTIVES -> PATTERNS -> ALGORITHM -> VALIDATION -> HEALTH
- The ALGORITHM file is the main reference — 5 capabilities, 5 formulas, 5 synthetic profiles
- eth_apply_rules uses 50/50 split (not standard 40/60) — this is deliberate, see D1 in ALGORITHM
- The correctness limitation is FUNDAMENTAL — do not try to solve it with formula engineering
- ET5 (VALIDATION) is CRITICAL — recommendations must NEVER reference value content
- ET9 (VALIDATION) requires correctness disclaimer in all citizen-facing output

**Watch out for:**
- Never access content fields — the topology reader should physically strip them
- Never imply that high ethics score = good ethics (only structural engagement)
- Regularity alone cannot produce a high eth_apply_rules score — the brain component gates it
- Gaming resistance: empty value nodes (no links, low energy) must not inflate scores
- The "adopted_moments_w" signal requires tracking which moments get referenced by other actors within 30 days — this may be expensive to compute

**Open questions:**
- Is "value" the correct node type name? Or is it a subtype of "thing"?
- Is "empathy" an available drive? Or should we use a different drive name?
- Should the regularity window be 30 days or shorter/longer?
- How should the correctness disclaimer be worded in citizen-facing messages?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Full doc chain for ethics aspect scoring. 5 capabilities from T1 (apply rules) to T8 (moral innovation). Topology-only math. The fundamental limitation: we can measure the PRESENCE and STRUCTURE of values but not their CORRECTNESS. This is documented honestly throughout. Key design choice: 50/50 brain/behavior split for rule-following because value node topology IS the structural signal for rule internalization. All other capabilities use standard 40/60. No code yet.

**Decisions made:**
- 50/50 split for eth_apply_rules (brain topology is genuinely informative for rule internalization)
- 40/60 for eth_implement_systems, eth_teach, eth_autonomous_judgment, eth_moral_innovation
- Regularity score as T1 behavioral proxy (consistent daily action = consistent rule-following)
- Adopted moments as T8 behavioral proxy (innovation measured by community adoption)
- Correctness disclaimer required in all outputs (ET9 invariant)
- Gaming resistance checks defined (empty node spam must not score well)

**Needs your input:**
- Is the 50/50 split for eth_apply_rules right? Or should it revert to 40/60?
- Correctness disclaimer wording: how explicit should it be in citizen-facing messages?
- Is the ethics sub-index weighting correct? (T1=1.0, T4=0.9, T6=0.8, T7=1.2, T8=1.5)
- Should there be a minimum eth_apply_rules score required before higher capabilities count?
- How should the system handle a citizen who clearly games the scoring (mass-creating empty value nodes)?

---

## TODO

### Immediate (Formula Validation)

- [ ] Confirm "value" node type name against brain graph schema
- [ ] Confirm "empathy" drive name against drive registry
- [ ] Run all 5 synthetic profiles through all 5 formulas (25 calculations)
- [ ] Verify all calculations fall in expected ranges per ALGORITHM
- [ ] Test gaming resistance profile (empty value nodes)

### Next (Implementation)

- [ ] Implement eth_apply_rules formula in scoring engine
- [ ] Implement regularity_score helper
- [ ] Implement remaining 4 capability formulas
- [ ] Build adopted_moments_w computation (may be expensive — profile it)
- [ ] Add correctness disclaimer to intervention message template

### Later (Calibration)

- [ ] Calibrate formulas against first real citizen data
- [ ] Validate 50/50 vs 40/60 split for eth_apply_rules with real data
- [ ] Run health checkers against real population
- [ ] Cross-aspect correlation analysis (ethics vs execution, ethics vs trust)

### Future

- IDEA: Values alignment proxy (value nodes linked to protocol concept nodes)
- IDEA: Moral consistency meta-score (ethics score variance over 30 days)
- IDEA: Ethics "floor" — minimum eth_apply_rules required before other capabilities count

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Ethics is the aspect where topology-only scoring is most honest about its limitations. The correctness problem is real and permanent — we cannot distinguish good values from bad values by structure alone. Rather than pretending this isn't the case, the entire doc chain is built around acknowledging it. The 50/50 split for eth_apply_rules feels right because value node topology genuinely IS the structural encoding of rule internalization. The gaming resistance concern is real — when you can't read content, citizens who create structural noise could game the system. The invariants and health checks are designed to catch this.

**Threads I was holding:**
- The correctness limitation makes ethics scoring fundamentally different from other aspects
- The 50/50 split is a design hypothesis that needs real-data validation
- Gaming resistance needs to be robust — ethics is the aspect most likely to be gamed
- The adopted_moments signal for T8 may be expensive to compute at scale
- Regularity is a weak proxy for ethical discipline — it confuses "shows up" with "follows rules"

**Intuitions:**
- eth_apply_rules will be the most reliable formula because its signals are the most direct
- eth_moral_innovation will be the hardest to validate because true moral innovation is rare and hard to distinguish from noise
- The correctness disclaimer will be the most important piece of citizen-facing text in the entire system
- Real-data calibration may reveal that the 50/50 split should be 45/55 or even revert to 40/60

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `docs/specs/personhood_ladder.json` |
| Personhood Ladder doc chain | `docs/assessment/personhood_ladder/` |
| Daily citizen health doc chain | `docs/assessment/daily_citizen_health/` |
| Brain topology primitives | ALGORITHM "DATA SOURCES" section |
| Scoring formulas (all 5) | ALGORITHM "CAPABILITY 1-5" sections |
| Synthetic test profiles | ALGORITHM "SYNTHETIC TEST PROFILES" section |
| Validation invariants | VALIDATION "INVARIANTS" section |
| Health checkers | HEALTH "CHECKER INDEX" section |
| Correctness limitation | ALGORITHM "Fundamental Limitation" section |
