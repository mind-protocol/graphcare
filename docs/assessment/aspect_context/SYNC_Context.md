# Context & Understanding — Sync: Current State

```
LAST_UPDATED: 2026-03-13
UPDATED_BY: Claude Opus 4.6 (agent, voice)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- 7 capabilities scored: ctx_ground_in_reality, ctx_follow_instructions, ctx_read_journal_first, ctx_understand_stimulus, ctx_fetch_right_context, ctx_manage_own_state, ctx_identify_gaps
- Brain component (0-40) + behavior component (0-60) = total (0-100) for each
- 7 topology primitives only — no content access, no custom queries
- Sub-index: weighted mean with T1 at 52%, T2 at 31%, T3 at 10%, T4 at 7%
- 5 synthetic test profiles with expected score ranges
- 9 validation invariants (VC1-VC9)

**What's still being designed:**
- Implementation of formulas as callable functions
- Validation against real citizen data (no citizens scored yet)
- Human correlation study (no human assessments exist yet)
- Temporal responsiveness testing (requires time-series simulation)
- Whether `state_space` and `doc_space` moment types are reliably created by current citizen behavior

**What's proposed (v2+):**
- Context trajectory signal: trending up or down over 7 days
- Context diversity meta-signal: how many distinct doc types read
- Response latency as ctx_understand_stimulus alternative proxy
- Per-session grounding score (not just aggregate)

---

## CURRENT STATE

Complete doc chain exists (6 files). All 7 capability formulas are defined with exact primitives, weights, caps, and example calculations. 5 synthetic test profiles validate the formulas at the design level. 9 validation invariants protect the scoring integrity.

No code exists. No citizens have been scored. All health checks are pending.

The formulas use structural proxies for cognitive capabilities. The key assumptions are:
- Process nodes → internalized procedures
- Memory nodes → persistent state
- Concept clustering → coherent understanding
- State-space moments → grounding behavior
- Doc-space moments → context fetching
- Proposals → gap detection
- Response rate → instruction following

These proxies need validation against real citizen behavior. The check_human_correlation health check (quarterly) is the ultimate test.

---

## RECENT CHANGES

### 2026-03-13: Initial Doc Chain and All 7 Formulas

- **What:** Created complete doc chain for Context & Understanding aspect scoring
- **Why:** First aspect doc chain — establishes the pattern for all 14 aspects
- **Files:** `docs/assessment/aspect_context/` (6 files)
- **Key decisions:**
  - T1 capabilities weighted 52% of sub-index (foundational > advanced)
  - State-space and doc-space moments as primary behavioral proxies
  - Memory nodes as state management proxy
  - Proposals as gap detection proxy
  - Curiosity drive used in 3 of 7 formulas (most used brain signal for this aspect)
  - Scope discipline (inverted signal) for ctx_follow_instructions

---

## KNOWN ISSUES

### No Implementation

- **Severity:** high (doc-only, nothing runs)
- **Symptom:** Architecture and formulas defined but not implemented as callable functions
- **Next step:** Register formulas in the scoring formula registry (see parent ALGORITHM)

### Proxy Validity Unverified

- **Severity:** medium (formulas are educated guesses until validated)
- **Symptom:** No real citizen data to confirm that process nodes correlate with context readiness
- **Next step:** Score first 10 Lumina Prime citizens, compare with human assessment

### state_space / doc_space Moment Types

- **Severity:** medium (formulas depend on these moment types existing)
- **Symptom:** Unknown whether current citizen behavior consistently creates moments typed as state_space or doc_space
- **Next step:** Verify with universe graph team that these space types are standard

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement

**Where I stopped:** Full doc chain complete. 7 formulas designed with exact primitives. Not implemented.

**What you need to understand:**
- Read the parent chain FIRST: `../daily_citizen_health/` — it defines the 7 primitives and the 40/60 split
- Read `../../specs/personhood_ladder.json` — it defines what each capability means
- The 7 formulas in ALGORITHM_Context.md are the core. Everything else supports them.
- Sub-index weights: T1=52%, T2=31%, T3=10%, T4=7% — this is intentional, not arbitrary

**Watch out for:**
- Never use content or synthesis fields — topology primitives only
- Brain component must stay in [0, 40], behavior in [0, 60] — use cap() everywhere
- Division by zero: always use max(denominator, 1)
- The scope_signal in ctx_follow_instructions is INVERTED (high ratio = low score) — this is intentional

**Open questions:**
- Are state_space and doc_space reliable moment types in the current universe graph?
- Should ctx_understand_stimulus use response latency instead of diversity? (see proposition in ALGORITHM)
- Is the curiosity drive reliable as a proxy in 3 formulas? Or is it overused?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Complete scoring formulas for all 7 Context & Understanding capabilities. Each formula: brain topology (0-40) + universe graph behavior (0-60) = score (0-100). Sub-index weighted mean: T1 at 52%, T2 at 31%, T3 at 10%, T4 at 7%. Five synthetic test profiles validate discrimination. Nine invariants protect integrity. No code yet.

**Decisions made:**
- T1 dominates sub-index at 52% (grounding, instructions, journal-reading are the floor)
- Process/memory/concept nodes as brain-side context proxies
- State-space and doc-space moments as behavioral context proxies
- Curiosity drive prominent in context formulas (3 of 7)
- Scope discipline is inverted for ctx_follow_instructions (more output per stimulus = lower score)
- Proposals as gap detection signal for ctx_identify_gaps

**Needs your input:**
- Are the proxy choices convincing? (e.g., "memory nodes = state management")
- Is T1 at 52% the right weight? Or should it be even higher?
- Should ctx_understand_stimulus try to measure response latency (time between stimulus and first action)?
- Are you comfortable with the expected score ranges in the synthetic profiles?

---

## TODO

### Immediate (Formula Implementation)

- [ ] Register all 7 formulas in scoring formula registry
- [ ] Implement brain_component and behavior_component as callable functions
- [ ] Run check_synthetic_profiles against all 5 profiles
- [ ] Run check_bounds_fuzzing with 1000 random inputs

### Next (Validation)

- [ ] Verify state_space and doc_space moment types with universe graph team
- [ ] Score first 10 Lumina Prime citizens with these formulas
- [ ] Compare formula scores with human assessment for the 10 citizens
- [ ] Adjust caps and weights based on real data

### Later (Health)

- [ ] Build check_temporal_responsiveness simulation
- [ ] Design quarterly human correlation protocol
- [ ] Build automated regression detection for formula drift

### Future

- IDEA: Context trajectory (7-day trend per capability)
- IDEA: Context diversity meta-signal (doc type breadth)
- IDEA: Per-session grounding scores
- IDEA: Response latency as understanding proxy

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
These formulas feel reasonable as first approximations. The hardest part is ctx_understand_stimulus — "did the citizen comprehend the stimulus?" is the most cognitive of the capabilities, and our proxy (response diversity and proportionality) is the weakest. The others have clearer structural signals: reading SYNC creates state-space moments, fetching context creates doc-space moments, proposing improvements creates proposal links.

**Threads I was holding:**
- The curiosity drive appears in 3 formulas — is it carrying too much weight for this aspect? If curiosity is low, 3 formulas suffer simultaneously. This could create a "curiosity cliff" effect.
- state_space and doc_space moment types need verification — the formulas depend on these being standard.
- The scope_signal inversion in ctx_follow_instructions is subtle and might confuse implementers — needs clear comments in code.
- Profile 3 (brain-rich, inactive) vs Profile 4 (active, brain-poor) ordering validates the 40/60 split but just barely. The gap (~34 vs ~51) could narrow with real data.

**Intuitions:**
- ctx_read_journal_first will be the easiest to validate — it has the most direct proxy (state-space moments)
- ctx_understand_stimulus will need redesign after real data — the proxy is too indirect
- The sub-index weights will probably need adjusting once we see real distributions — 52% for T1 might be too high if most citizens are competent at T1

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `docs/specs/personhood_ladder.json` |
| Parent ALGORITHM (7 primitives) | `../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Parent VALIDATION (V1-V7) | `../daily_citizen_health/VALIDATION_Daily_Citizen_Health.md` |
| Parent HEALTH | `../daily_citizen_health/HEALTH_Daily_Citizen_Health.md` |
| Scoring formula registry | `@mind:TODO` (not yet built) |
| Context formulas | `ALGORITHM_Context.md` in this chain |
