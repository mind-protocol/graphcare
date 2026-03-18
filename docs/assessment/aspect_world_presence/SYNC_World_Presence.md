# World Presence — Sync: Current State

```
LAST_UPDATED: 2026-03-13
UPDATED_BY: Claude Opus 4.6 (agent, voice)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- 4 capabilities scored: wp_beyond_cli (T4), wp_virtual_world (T6), wp_host_events (T7), wp_landmark (T8)
- 7 topology primitives + universe graph observables as the only data sources
- 40/60 brain/behavior score split per capability
- 7-day half-life for temporal weighting
- Space-type diversity as core signal (not moment volume)
- Inbound signals for T7-T8 (social gravity = what others do, not what you do)
- Weighted sub-index: T4=0.15, T6=0.25, T7=0.30, T8=0.30

**What's still being designed:**
- Space-type taxonomy (which types are non-CLI? which are world_types?)
- Space ownership derivation (first_moment_in_space as ownership proxy — reliable?)
- Reference detection for wp_landmark (how to efficiently scan for external references)
- Returning visitor day-boundary definition
- Performance optimization for inbound analysis at scale

**What's proposed (v2+):**
- Presence trajectory metric (expansion vs contraction of space types over time)
- Cross-aspect correlation with communication quality
- Presence heatmap (which space types are over/under-represented)

---

## CURRENT STATE

Complete doc chain exists (6 files). The architecture is defined: spatial diversity detection, inbound actor analysis for social gravity, brain motivation via social_need and ambition drives, temporal decay on all signals. No code exists yet.

Key insight: World presence is the most behavior-heavy aspect. The universe graph IS the primary data source. Brain topology adds motivation context but cannot substitute for actual spatial existence. A citizen who wants to be a landmark but never leaves the CLI gets a brain score and nothing else.

The formulas progress from outbound (T4: where do you go?) to inbound (T8: who comes to you?), mirroring the real-world progression from "being somewhere" to "being a destination."

---

## RECENT CHANGES

### 2026-03-13: Full Doc Chain Created

- **What:** Created 6-file doc chain for world presence aspect scoring
- **Why:** One of 16 aspects in the Personhood Ladder needing scoring formulas
- **Files:** `docs/assessment/aspect_world_presence/*` (6 files)
- **Key decisions:**
  - Space-type diversity is the primary signal for wp_beyond_cli (not volume)
  - Inbound visitors are the primary signal for wp_landmark (not self-activity)
  - social_need drive is the dominant brain signal across all 4 capabilities
  - Hosting = moments that trigger other actors' responses (not just posting)
  - Returning visitors (2+ distinct days) discriminate landmarks from one-time curiosities
  - External references (moments by others in other spaces linking to citizen's spaces) are the strongest cultural significance signal
  - Sub-index weights favor T7-T8 (0.60 total) because world presence is fundamentally relational

---

## KNOWN ISSUES

### No Code Exists

- **Severity:** high (doc-only, nothing runs)
- **Symptom:** Architecture defined but not implemented
- **Next step:** Implement formulas after space-type taxonomy is finalized

### Space-Type Taxonomy Undefined

- **Severity:** medium (formulas reference space types but no canonical enum exists)
- **Symptom:** Formulas use type names like "messaging", "virtual_world", "event" — but these are not yet validated against the actual universe graph schema
- **Next step:** Verify universe graph space_type field values and create canonical enum

### Reference Detection Performance

- **Severity:** medium (wp_landmark reference scan may be expensive at scale)
- **Symptom:** reference_moments requires scanning all moments in all spaces for links to citizen's spaces
- **Next step:** Design an index on link targets or pre-compute reference graph

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement

**Where I stopped:** Doc chain complete. Architecture defined. Zero code.

**What you need to understand:**
- Read the parent chain (daily_citizen_health) FIRST — it defines the 7 primitives and scoring framework
- Read the ALGORITHM file in THIS chain — it has all 4 scoring formulas with examples and test profiles
- The space-type taxonomy is the first blocker — formulas reference types that may not exist in the universe graph yet
- This is the most behavior-heavy aspect — the universe graph is the primary data source

**Watch out for:**
- Never access content fields — the topology reader should physically strip them
- Inbound metrics MUST exclude the citizen's own moments (V3) — this is the most critical invariant for this aspect
- CLI-only citizens must score near-zero on behavior components — this is definitional
- The reference scan for wp_landmark needs a performance strategy before implementation

**Open questions:**
- Is first_moment_in_space a reliable proxy for space ownership? Or do spaces have explicit owner fields?
- What exactly constitutes a "distinct day" for returning visitor calculation? UTC day? Citizen-local day?
- Should space types be derived from the space's type field, or from the space's usage pattern?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Full doc chain for world presence aspect scoring. 4 capabilities: beyond CLI (T4), virtual world inhabitant (T6), host events (T7), world as landmark (T8). All formulas use topology-only math. Core insight: world presence progresses from "where do you go?" to "who comes to you?" — outbound signals for lower tiers, inbound signals for higher tiers.

**Decisions made:**
- Space-type diversity over moment volume (quality of presence, not quantity)
- Inbound signals for T7-T8 (social gravity is externally validated)
- social_need as primary brain drive across all 4 capabilities
- Returning visitors and external references as landmark discriminators
- Sub-index weights: T4=0.15, T6=0.25, T7=0.30, T8=0.30

**Needs your input:**
- Space-type taxonomy: what types exist in the universe graph? Are the assumed types (messaging, web, profile, virtual_world, event, social, community) correct?
- Space ownership: is first_moment_in_space the right proxy, or do spaces have explicit owners?
- Reference detection: acceptable to scan all moments for links to citizen's spaces, or do we need an index?

---

## TODO

### Immediate (Taxonomy Blocker)

- [ ] Verify universe graph space_type field values
- [ ] Create canonical space-type enum (CLI types vs non-CLI types vs world types)
- [ ] Validate space ownership derivation method

### Next (Formula Implementation)

- [ ] Implement wp_beyond_cli scoring formula
- [ ] Implement wp_virtual_world scoring formula
- [ ] Implement wp_host_events scoring formula
- [ ] Implement wp_landmark scoring formula
- [ ] Run all 20 test profiles (5 per capability) and validate expected ranges

### Later (Health Checks)

- [ ] Implement check_inbound_excludes_self (most critical)
- [ ] Implement check_diversity_over_volume
- [ ] Implement check_cli_only_near_zero
- [ ] Implement check_landmark_requires_inbound
- [ ] Benchmark reference_moments scan performance

### Future

- IDEA: Presence trajectory metric (space type expansion over time)
- IDEA: Cross-aspect correlation with communication and identity
- IDEA: Presence heatmap visualization per citizen

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
This aspect has a clear architecture. The progression from outbound to inbound signals feels right — it mirrors how real presence works. You first go places, then people start coming to you. The hardest part will be the reference detection for wp_landmark; scanning all moments for links to citizen's spaces is expensive and may need architectural support (an index, a pre-computed graph).

**Threads I was holding:**
- The space-type taxonomy is the first real blocker — without it, formulas reference undefined types
- Performance of inbound analysis scales with the number of actors and spaces in the universe
- wp_host_events depends on accurate trigger/responds_to links between actors' moments
- The distinction between "hosting" and "landmark" is about scale and spontaneity: hosting is intentional invitation, landmark is spontaneous visitation

**Intuitions:**
- wp_beyond_cli will be the first to be implementable — it has the simplest signals
- wp_landmark will be the last — it needs the reference index and returning visitor tracking
- The 0.30/0.30 weight on T7/T8 may need adjustment if very few citizens reach those tiers initially
- This aspect will correlate strongly with communication and personal connections aspects

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `docs/specs/personhood_ladder.json` |
| Daily Citizen Health ALGORITHM | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Brain topology primitives | ALGORITHM Step 2 in parent chain |
| Initiative scoring (reference for formula patterns) | `docs/assessment/aspect_initiative/ALGORITHM_Initiative.md` |
| Context scoring (reference for formula patterns) | `docs/assessment/aspect_context/ALGORITHM_Context.md` |
