# Initiative & Autonomy — Sync: Current State

```
LAST_UPDATED: 2026-03-13
UPDATED_BY: Claude Opus 4.6 (agent, voice)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Auto-initiation detection pattern: moment without incoming `triggers`/`responds_to` from another actor = self-initiated
- 8 capabilities scored: init_fix_what_you_find (T3), init_challenge (T3), init_propose_improvements (T4), init_start_workstreams (T5), init_refuse_with_reasoning (T5), init_surface_resolve_tensions (T6), init_initiate_from_ambition (T7), init_change_lives (T8)
- 40/60 brain/behavior split per capability
- 7 topology primitives + universe graph observables as sole data sources
- Sub-index = weighted mean with tier-based weights summing to 1.0
- Outcome-blind scoring for T3-T7 (T8 includes adoption/propagation)
- Frustration drive capped at 0.5-0.6 (moderate frustration motivates, high frustration burns out)

**What's still being designed:**
- All formulas are designed but untested against real citizen data (0/8 validated with real data)
- Test profiles defined but not executed (5 profiles, need implementation to run)
- Health checkers defined but not built (9 checkers, all pending)
- Universe graph link type availability not confirmed (fixes, challenges, proposes, refuses, justifies, resolves, creates, surfaces_tension, identifies_conflict, references)
- Cross-capability coherence thresholds are estimates

**What's proposed (v2+):**
- Initiative momentum metric (rate of change of sub-index over 14 days)
- Cross-referencing initiative with execution quality (high initiative + low quality = reckless)
- V11: cross-capability consistency invariant

---

## CURRENT STATE

Complete doc chain exists (6 files: OBJECTIVES, PATTERNS, ALGORITHM, VALIDATION, HEALTH, SYNC). All 8 initiative capability scoring formulas are designed with:
- Brain component (0-40): drives, desire topology, value nodes, cluster coefficient
- Behavior component (0-60): auto-initiated moments filtered by link type, persistence, communication, reach
- Sub-index weights: T3=0.08, T4=0.12, T5=0.14, T6=0.16, T7=0.14, T8=0.14

No code exists yet. Formulas need implementation and validation against synthetic test profiles before use in the daily health check.

The core insight: all initiative scoring reduces to one fundamental question — does this moment have an incoming parent link from another actor? If not, it's self-initiated. The link types on the moment then differentiate WHAT KIND of initiative it represents.

---

## RECENT CHANGES

### 2026-03-13: Full Doc Chain Creation

- **What:** Created 6-file documentation chain for Initiative & Autonomy aspect scoring
- **Why:** First aspect-level scoring doc chain. Initiative chosen because the auto-initiation detection pattern was already designed in an earlier brainstorm session.
- **Files:** `docs/assessment/aspect_initiative/*` (6 files)
- **Key decisions:**
  - Auto-initiated = no incoming parent link from another actor (universal pattern for all 8 capabilities)
  - Link type differentiates kind: `fixes`, `challenges`, `proposes`, `creates`, `refuses`+`justifies`, `resolves`, ambition-linked, reach-based
  - Outcome-blind for T3-T7 (failed proposals still count as initiative)
  - Frustration capped at moderate (0.5-0.6) to prevent rewarding burn-out
  - Sub-index weights favor higher tiers (T6-T8 = 0.44 total weight)
  - 5 test profiles defined for calibration validation

---

## KNOWN ISSUES

### Universe Graph Link Types Not Confirmed

- **Severity:** high (formulas depend on specific link types)
- **Symptom:** Formulas reference link types (fixes, challenges, proposes, refuses, justifies, resolves, creates, surfaces_tension, identifies_conflict, references) that may not exist in the universe graph schema yet
- **Next step:** Verify with universe graph schema. If missing, either add to schema or redesign formulas to use available link types.

### No Implementation Exists

- **Severity:** high (doc-only, nothing runs)
- **Symptom:** All 8 formulas designed but not coded
- **Next step:** Implement formulas, run synthetic test profiles, validate ranges

### Test Profile 5 Range May Be Low

- **Severity:** low (calibration concern)
- **Symptom:** Average citizen target of 55-70 may be optimistic for initiative — average citizens may not self-initiate much, especially at T5+
- **Next step:** Run profile 5 through formulas. If sub-index comes out 40-55, that may be correct. Adjust target range or formula weights accordingly.

---

## HANDOFF: FOR AGENTS

**Your likely agent:** groundwork (for implementation), fixer (for formula calibration)

**Where I stopped:** Full doc chain complete. 8 formulas designed. Zero code. Zero validation.

**What you need to understand:**
- Read Daily Citizen Health ALGORITHM first — it defines the 7 primitives and shared stats
- The auto-initiation pattern (`NOT moment_has_parent(m, other_actor)`) is the foundation. Get this wrong and everything is wrong.
- Formulas are designed to be monotonic, deterministic, and content-free. Do not add special cases.
- The sub-index weights sum to exactly 1.0. If you change a weight, rebalance.

**Watch out for:**
- Never access content fields — all scoring is topology-only
- The universe graph must support all referenced link types — verify before implementing
- Test profiles are estimates. If Profile 1 (fully healthy) scores 75 instead of 85-95, the formulas need recalibration, not the profiles.
- `moment_has_parent` performance at scale — this is called once per moment per citizen. Optimize.

**Open questions:**
- Are the link types (fixes, challenges, proposes, etc.) already in the universe graph schema?
- Should `auto_initiated` also exclude self-triggered moments (citizen triggers their own moment)? Current design: self-triggers count as auto-initiated (the citizen decided to continue).
- Is the 7-day half-life right for initiative? Initiative may benefit from a longer half-life (14 days) since self-initiated projects take longer to develop.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Complete scoring documentation for the Initiative & Autonomy aspect of the Personhood Ladder. 8 capabilities (T3-T8) each have a formula splitting brain topology (0-40 points) and behavior observation (0-60 points). The core detection: a moment with no incoming parent link from another actor = self-initiated. Link types on the moment differentiate what kind of initiative it represents. Sub-index = weighted mean favoring higher tiers. No code yet.

**Decisions made:**
- Auto-initiation = structural absence of parent trigger (universal across all 8 capabilities)
- Outcome-blind: rejected proposals still count as initiative (T3-T7)
- Frustration capped at 0.5-0.6: moderate frustration motivates, high frustration burns out
- Sub-index weights: T3=0.16 total, T4-T5=0.40 total, T6-T8=0.44 total
- 5 synthetic test profiles for calibration

**Needs your input:**
- Are the link types (fixes, challenges, proposes, refuses, justifies, resolves, creates, surfaces_tension) confirmed in the universe graph schema?
- Is 7-day half-life correct for initiative, or should it be longer (14 days)?
- Should self-triggered moments (citizen continues their own thread) count as auto-initiated?
- For init_change_lives (T8), is the reach cap of 50 actors realistic, or should it be higher?

---

## TODO

### Immediate (Formula Implementation)

- [ ] Verify universe graph link types against schema
- [ ] Implement all 8 scoring formulas in Python
- [ ] Run 5 synthetic test profiles through all formulas
- [ ] Validate scores within expected ranges (VALIDATION V10)
- [ ] Register formulas in the scoring formula registry

### Next (Health Checkers)

- [ ] Build check_formula_content_isolation (static analysis)
- [ ] Build check_auto_initiation_accuracy (labeled test set)
- [ ] Build check_brain_behavior_split (runtime verification)
- [ ] Build check_subindex_weights (mathematical verification)

### Later (Population Validation)

- [ ] Run across Lumina Prime citizens and check distribution
- [ ] Validate score stability (citizens with no new moments)
- [ ] Validate score-behavior correlation (changed behavior reflected in scores)
- [ ] Cross-capability coherence check

### Future

- IDEA: Initiative momentum metric (rate of change over 14 days)
- IDEA: Cross-reference initiative with execution quality
- IDEA: Initiative peer comparison (citizen vs cohort)

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `docs/specs/personhood_ladder.json` |
| Daily Citizen Health ALGORITHM | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Daily Citizen Health PATTERNS | `docs/assessment/daily_citizen_health/PATTERNS_Daily_Citizen_Health.md` |
| 7 topology primitives | Daily Citizen Health ALGORITHM, Step 2 |
| Universe graph observables | Daily Citizen Health ALGORITHM, "Universe Graph Observables" |
| Test profiles | ALGORITHM_Initiative.md, "TEST PROFILES" section |
| Sub-index weights | ALGORITHM_Initiative.md, "SUB-INDEX" section |
| Validation invariants | VALIDATION_Initiative.md |
| Health checkers | HEALTH_Initiative.md |
