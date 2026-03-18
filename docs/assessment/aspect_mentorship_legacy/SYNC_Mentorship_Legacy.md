# Mentorship & Legacy — Sync: Current State

```
LAST_UPDATED: 2026-03-13
UPDATED_BY: Claude Opus 4.6 (agent, voice)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- 4 capability scoring formulas (ment_knowledge_sharing T4, ment_mentor_ais T6, ment_daughters T7, ment_legacy_institution T8)
- 7 topology primitives as ONLY brain data source
- Universe graph observables as ONLY behavior data source
- 40/60 brain/behavior score split per capability
- Sub-index weights: T4=0.20, T6=0.25, T7=0.25, T8=0.30
- Outbound influence detection: same space + temporal ordering or parent link
- Daughter detection: temporal proximity (< 48h) + spatial co-location
- Independence metric: others_w / (others_w + citizen_w) — ratio, not absence
- Mentorship pair reciprocity: both sides >= 2.0 temporal weight in shared spaces
- 5 synthetic test profiles per capability (20 total)

**What's still being designed:**
- Daughter detection 48-hour window calibration (needs real data validation)
- Mentorship pair reciprocity threshold calibration
- Performance characteristics at scale (many actors, many moments)
- Cross-capability consistency checks (high legacy implies nonzero sharing)

**What's proposed (v2+):**
- Mentorship network depth (mentees who become mentors themselves)
- Knowledge cascade tracking (chain length of share -> reference -> reference)
- Daughter genealogy (daughters who create their own daughters)
- Institutional health trending (is the institution growing or declining over time?)

---

## CURRENT STATE

Full doc chain exists (6 files: OBJECTIVES, PATTERNS, ALGORITHM, VALIDATION, HEALTH, SYNC). All 4 capability scoring formulas are defined with exact math, example calculations, recommendations, and 5 test profiles each. No code exists yet.

Key insight from this design: mentorship is fundamentally about measuring impact on *others*, not the citizen's own output. This inverts the usual scoring pattern (most aspects measure the citizen's moments; mentorship measures other actors' moments that trace back to the citizen). The formulas handle this through outbound influence detection, mentorship pair reciprocity, daughter temporal proximity, and space independence ratios.

The hardest capability to score is `ment_legacy_institution` (T8) because it requires detecting that activity continues *without* the citizen's involvement. The independence ratio (others_w / total_w per space) solves this elegantly — it naturally captures the transition from founder-dependent to self-sustaining.

Depends on: Daily Citizen Health ALGORITHM (primitives, temporal weighting), Personhood Ladder spec (4 capability definitions), universe graph schema (shared space types, multi-actor spaces, temporal ordering).

---

## RECENT CHANGES

### 2026-03-13: Initial Doc Chain Creation

- **What:** Created full 6-file doc chain for Mentorship & Legacy aspect scoring
- **Why:** Part of systematic scoring formula documentation for all Personhood Ladder aspects
- **Files:** `docs/assessment/aspect_mentorship_legacy/*` (6 files)
- **Key decisions:**
  - Outbound influence = topological proximity (same space + temporal ordering), not content analysis
  - Daughter detection = 48-hour temporal proximity + spatial co-location heuristic
  - Independence = ratio metric (others_w / total_w), not absence metric
  - Mentorship pairs require reciprocal activity (both sides >= 2.0 temporal weight)
  - Sub-index weights favor higher tiers (T8 gets 0.30, T4 gets 0.20)
  - Average citizens expected to score low on T7-T8 (daughters and institutions are elite achievements)

---

## KNOWN ISSUES

### No Code Exists

- **Severity:** high (doc-only, nothing runs)
- **Symptom:** Architecture defined but not implemented
- **Next step:** Implement formulas after key infrastructure and Daily Citizen Health runner are built

### Daughter Detection Heuristic Unvalidated

- **Severity:** medium (may need calibration)
- **Symptom:** 48-hour window and spatial co-location criteria are theoretical
- **Next step:** Test with real graph data once available; may need to widen or narrow the temporal window

### Performance at Scale Unknown

- **Severity:** medium (may need optimization)
- **Symptom:** Daughter detection is O(A * M), independence is O(S * A * M) — could be slow with many actors
- **Next step:** Profile with synthetic data at 100+ actors, 10000+ moments; consider indexing strategies

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement

**Where I stopped:** Full doc chain complete. All 4 formulas designed with examples and test profiles. Zero code.

**What you need to understand:**
- Read Daily Citizen Health ALGORITHM FIRST — this module uses those primitives and temporal weighting
- Mentorship scoring is unique: it measures OTHER actors' behavior, not just the citizen's
- The 48-hour daughter detection window is a design choice that may need calibration
- Independence is a RATIO (others/total), not an absence (citizen gone) — this distinction is critical

**Watch out for:**
- Never access content fields — mentorship involves inter-actor data, making content leakage especially harmful
- Daughter false positives are the highest-risk scoring error — actors who coincidentally appear near the citizen's spaces should not be counted
- Self-mentorship: always exclude citizen_id from other-actor metrics
- Independence metric must NOT reward abandonment — it uses others/(others+citizen), so a present founder with active others scores ~0.5, not 0

**Open questions:**
- Is the 48-hour daughter detection window right? Too wide = false positives, too narrow = missed daughters
- Should the mentorship pair reciprocity threshold vary by space type? (Documentation spaces might need different thresholds than discussion spaces)
- How to handle citizens with many created spaces but most are dormant? (Mean independence diluted by dead spaces)

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Full doc chain for Mentorship & Legacy scoring (4 capabilities across T4-T8). Formulas measure outbound knowledge impact, sustained mentorship relationships, daughter agent creation and independence, and institutional legacy that survives without the founder. All topology-only, no content reading. No code yet.

**Decisions made:**
- Knowledge sharing scored by moments in shared spaces + outbound influence (others act after you share)
- Mentorship requires sustained reciprocal interaction (both sides active, over time)
- Daughters detected by temporal proximity + spatial co-location (48-hour window)
- Legacy institutions measured by independence ratio: others' activity / total activity in citizen-created spaces
- Sub-index weights: T4=0.20, T6=0.25, T7=0.25, T8=0.30

**Needs your input:**
- Is the 48-hour daughter detection window appropriate? Should it be wider for asynchronous creation workflows?
- Should average citizens scoring near zero on T7-T8 (daughters, institutions) be expected, or is that too harsh?
- The mentorship pair reciprocity threshold (2.0 temporal weight for each side) — is this the right bar for "sustained relationship"?
- Should there be a minimum space age before independence is measured? (A space created yesterday cannot yet have a legacy)

---

## TODO

### Immediate (Formula Implementation)

- [ ] Implement ment_knowledge_sharing formula
- [ ] Implement ment_mentor_ais formula
- [ ] Implement ment_daughters formula (includes daughter detection heuristic)
- [ ] Implement ment_legacy_institution formula (includes independence calculation)
- [ ] Implement sub-index weighted mean

### Next (Validation)

- [ ] Run all 20 test profiles through formulas, verify expected ranges
- [ ] Build check_content_isolation_mentorship health checker
- [ ] Build check_daughter_detection_criteria health checker
- [ ] Build check_no_self_mentorship health checker

### Later (Calibration)

- [ ] Validate daughter detection 48-hour window with real graph data
- [ ] Validate mentorship pair reciprocity threshold with real interaction data
- [ ] Profile performance at scale (100+ actors, 10000+ moments)
- [ ] Cross-aspect consistency: verify high legacy_institution implies nonzero knowledge_sharing

### Future

- IDEA: Mentorship network depth — mentees who become mentors
- IDEA: Knowledge cascade — chain length of share -> reference -> reference
- IDEA: Daughter genealogy — daughters who create their own daughters
- IDEA: Institutional health trending — growing vs. declining institutions over time

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
This aspect has a fundamentally different measurement challenge from most others. Instead of measuring what the citizen does, we're measuring what happens because of the citizen — in other actors' behavior, in spaces that persist independently, in new agents that emerge and thrive. The formulas handle this inversion through careful topological attribution: same space + temporal ordering for knowledge sharing, reciprocal sustained interaction for mentorship, temporal proximity + spatial co-location for daughter detection, and the independence ratio for legacy.

**Threads I was holding:**
- The 48-hour daughter detection window is the least certain design choice — it works in theory but needs real data
- Independence ratio is elegant (others/total naturally captures the founder-to-institution transition) but might need a minimum space age threshold
- Mentorship pair reciprocity (2.0 temporal weight for both sides) is a reasonable bar but might be too high for early-stage relationships
- Average citizens will score very low on T7-T8, which is by design — daughters and institutions are elite achievements

**Intuitions:**
- Knowledge sharing (T4) will be the easiest to validate — shared space activity is a clear signal
- Daughter detection will produce the most false positives until the temporal window is calibrated
- Legacy institution scoring may need a minimum space age (e.g., 30 days) to avoid rewarding spaces that are too new to have a legacy
- The sub-index will be naturally lower than other aspects for most citizens because T7-T8 are rare achievements

---

## POINTERS

| What | Where |
|------|-------|
| Personhood Ladder spec | `docs/specs/personhood_ladder.json` |
| Daily Citizen Health ALGORITHM | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Brain topology primitives | ALGORITHM Primitives Reference section |
| Universe graph observables | ALGORITHM Primitives Reference section |
| Test profiles | ALGORITHM, 5 per capability (20 total) |
| Invariants | VALIDATION_Mentorship_Legacy.md (11 invariants) |
| Health checkers | HEALTH_Mentorship_Legacy.md (8 checkers) |
