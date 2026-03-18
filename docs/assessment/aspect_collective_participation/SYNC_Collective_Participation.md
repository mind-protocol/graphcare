# Collective Participation — Sync: Current State

```
LAST_UPDATED: 2026-03-13
UPDATED_BY: Claude Opus 4.6 (agent, voice)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- 4 capabilities: col_dao_participation (T5), col_community_engagement (T5), col_movement_builder (T7), col_global_movement (T8)
- 40/60 brain/behavior split per parent algorithm contract
- 7 topology primitives + universe graph observables as sole data sources
- Dialogue chain analysis via moment_has_parent as participation signal
- Pioneered spaces (first_moment_in_space) as movement building signal
- Escalating ceilings by tier (T5 < T7 < T8)
- Weighted sub-index: T5=1.0, T7=1.8, T8=2.5
- No T6 capability (intentional gap: participate or build, no intermediate)

**What's still being designed:**
- Space type taxonomy confirmation ("governance", "discussion", "forum" in universe graph)
- Exact dialogue chain detection mechanics (moment_has_parent cross-actor filtering)
- Integration with daily health runner
- Intervention message tone and content
- All validation checkers (0/8 implemented)

**What's proposed (v2+):**
- Governance consistency metric (regularity of participation, not just recency)
- Dialogue chain depth weighting (deeper threads = richer participation)
- Community health dashboards showing collective participation trends
- Cross-aspect correlation with Trust & Reputation (collective participation builds trust)

---

## CURRENT STATE

Complete doc chain exists (6 files: OBJECTIVES, PATTERNS, ALGORITHM, VALIDATION, HEALTH, SYNC). All 4 capability scoring formulas are designed with exact sub-component weights, ceilings, and reasoning. 5 synthetic test profiles defined with expected score ranges. 9 validation invariants specified. 8 health checkers defined (all pending).

No code exists yet. This is a doc-only design.

Key characteristics of this aspect:
- Most behavior-heavy aspect in the ladder — brain provides motivation floor, behavior is the real signal
- Dialogue chains (moment_has_parent) are the strongest participation signal
- Movement building (T7/T8) requires space creation, not just participation
- The T5-to-T7 jump has no T6 intermediate — reflects real difficulty gap between participating and building
- T8 ceilings are the highest in the aspect (15 distinct actors, 15.0 triggered_w)

---

## RECENT CHANGES

### 2026-03-13: Initial Design and Doc Chain

- **What:** Created full doc chain for Collective Participation aspect
- **Why:** Part of systematic scoring documentation for all 14 Personhood Ladder aspects
- **Files:** `docs/assessment/aspect_collective_participation/*` (6 files)
- **Key decisions:**
  - Dialogue ratio (moment_has_parent patterns) weighted 18 points in T5 formulas — participation is conversation
  - Pioneered spaces + actors_in_pioneered as dual creation signal for T7 — you need to create AND attract
  - Brain sub-components evenly distributed at T8 (8 pts each) — global leadership requires all signals
  - Sub-index weights: T5=1.0, T7=1.8, T8=2.5 — steeper weighting due to T5-T7 gap
  - 5 synthetic test profiles covering fully healthy, fully unhealthy, brain-rich/inactive, active/brain-poor, and average

---

## KNOWN ISSUES

### No Code Exists

- **Severity:** high (doc-only, nothing runs)
- **Symptom:** Architecture defined but not implemented
- **Next step:** Confirm space type taxonomy, then implement scoring formulas

### Space Type Taxonomy Unconfirmed

- **Severity:** medium (formulas depend on space types that may not exist yet)
- **Symptom:** Formulas reference "governance", "discussion", "forum" as space types
- **Next step:** Check universe graph schema for available space types, adapt formula filtering if needed

### Dialogue Detection Untested

- **Severity:** medium (moment_has_parent cross-actor filtering is the core participation signal)
- **Symptom:** Dialogue ratio computation assumes moment_has_parent correctly identifies cross-actor responses
- **Next step:** Integration test with actual universe graph data

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement

**Where I stopped:** Doc chain complete. All 4 formulas designed. Zero code.

**What you need to understand:**
- Read the ALGORITHM file thoroughly — it's the primary file with all formulas
- The 7 topology primitives + universe observables are the ONLY data sources. No exceptions.
- Dialogue chain detection (moment_has_parent cross-actor) is the hardest computation to implement correctly
- Pioneered spaces detection (first_moment_in_space where citizen is the earliest) needs careful implementation
- The derived stats section in ALGORITHM defines shared computations — implement those first

**Watch out for:**
- Never access moment content, vote content, or discussion text
- The space type taxonomy ("governance", "discussion", "forum") needs confirmation against actual schema
- triggered_by_citizen (moments by others that have parent links to citizen's moments) is an inverse query — may be expensive
- actors_in_pioneered and followers_in_spaces are distinct metrics — the former counts any actor present, the latter counts active contributors

**Open questions:**
- Are "governance", "discussion", "forum" the actual space type values in the universe graph? Or are there different names?
- How expensive is the triggered_by_citizen query at scale? (Scanning all universe moments for parent links to citizen)
- Should dialogue_ratio be computed across all collective moments or separately per space type?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Full doc chain for Collective Participation aspect — 4 capabilities from T5 to T8. Formulas score governance participation, community engagement, movement building, and global movement leadership using only graph topology math. This is the most behavior-heavy aspect: dialogue chains, space creation, actor reach. No code yet.

**Decisions made:**
- Dialogue ratio (responding to others) is the primary participation signal, not just moment count
- Movement building (T7) requires creating spaces that attract others, not just participating more
- Global movement (T8) has the highest ceilings: 15 distinct actors, 15.0 triggered_w
- Sub-index weights favor higher tiers steeply: T8 is 2.5x weight vs. T5 at 1.0x
- No T6 capability — intentional gap reflecting real difficulty of moving from participant to builder

**Needs your input:**
- Space type taxonomy: are "governance", "discussion", "forum" the right space type values?
- Triggered moments computation: scanning all universe moments for parent links to citizen — acceptable cost?
- Dialogue ratio ceiling: 0.4 for governance (votes are less dialogue-heavy), 0.5 for community (discussions are more reciprocal) — right calibration?

---

## TODO

### Immediate (Schema Confirmation)

- [ ] Confirm space type taxonomy in universe graph schema
- [ ] Confirm moment_has_parent can filter by actor (cross-actor dialogue detection)
- [ ] Confirm first_moment_in_space returns the globally earliest moment (not just citizen's first)

### Next (Implementation)

- [ ] Implement derived stats computation (shared behavior stats)
- [ ] Implement col_dao_participation formula
- [ ] Implement col_community_engagement formula
- [ ] Implement col_movement_builder formula
- [ ] Implement col_global_movement formula
- [ ] Implement sub-index calculation with tier weights

### Validation

- [ ] Build check_content_isolation (CP1)
- [ ] Build check_score_bounds (CP2, CP3)
- [ ] Build check_isolation_caps (CP5)
- [ ] Build check_creation_requirement (CP7)
- [ ] Build check_dialogue_sensitivity (CP8)
- [ ] Run all 5 synthetic profiles against all 4 formulas

### Later

- [ ] Integration test with actual universe graph data
- [ ] Performance test: triggered_by_citizen query at scale
- [ ] Connect to daily health runner

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `docs/specs/personhood_ladder.json` |
| Daily health doc chain | `docs/assessment/daily_citizen_health/` |
| Scoring formulas (this aspect) | `./ALGORITHM_Collective_Participation.md` |
| Validation invariants | `./VALIDATION_Collective_Participation.md` |
| Health checkers | `./HEALTH_Collective_Participation.md` |
| Other aspect examples | `../aspect_vision_strategy/`, `../aspect_initiative/` |
