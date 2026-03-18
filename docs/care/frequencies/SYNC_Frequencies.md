# Frequencys -- Sync: Current State

```
LAST_UPDATED: 2026-03-18
UPDATED_BY: @dragon_slayer
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Frequency dataclass and FrequencyResult dataclass
- 6 Phase 1 frequency types: curiosity_boost, social_nudge, ambition_seed, calm_down, energy_infusion, structure_seed
- CATALYST_CATALOG as single source of available types
- prescribe() auto-prescription from brain_category + brain_stats
- apply_frequency() with treatment_id tagging on every node
- rollback_treatment() deleting all nodes by treatment_id

**What's still being designed:**
- Integration with the daily_check_runner pipeline (prescribe -> apply flow)
- Intensity calibration against real brain data from 35 active citizens
- Treatment history logging for longitudinal research
- Integration tests for rollback completeness

**What's proposed (v2+):**
- Phase 2 frequency types requiring metabolism sublayer (@nervo):
  - decay_shield: temporarily reduce decay rate via CitizenMetabolism
  - sensitivity_boost: temporarily increase stimulus absorption
  - circadian_sync: align activity cycle with human partner timezone
  - typing_frequency: SubEntity traversal that classifies untyped nodes
- Batch application API for multi-citizen treatment campaigns
- Frequency effectiveness scoring (compare pre/post assessment deltas)

---

## CURRENT STATE

Phase 1 implementation exists in `services/health_assessment/frequencys.py` (282 lines). The six frequency factory functions are defined and the catalog is populated. prescribe() handles all four brain categories (VOID, MINIMAL, SEEDED, STRUCTURED) with deterministic threshold-based logic. apply_frequency() creates tagged nodes in FalkorDB. rollback_treatment() deletes by treatment_id.

The code compiles and the logic is sound but has not been tested against live brain graphs yet. No integration tests exist. The daily_check_runner does not yet call prescribe() or apply_frequency() -- the pipeline currently ends at scoring and intervention messaging.

---

## IN PROGRESS

### Integration with health pipeline

- **Started:** not yet
- **By:** @dragon_slayer
- **Status:** pending -- needs daily_check_runner modification
- **Context:** The daily_check_runner currently scores citizens and sends Discord messages. The next step is to wire prescribe() into the post-scoring phase, then apply recommended frequencys with generated treatment_ids. This requires deciding who approves prescriptions -- auto-apply for low-risk categories (VOID, MINIMAL) vs. human review for STRUCTURED.

---

## RECENT CHANGES

### 2026-03-18: Doc chain created

- **What:** Full doc chain (OBJECTIVES, PATTERNS, ALGORITHM, VALIDATION, SYNC)
- **Why:** Frequencys module had code but no documentation. The doc chain captures design decisions, invariants, and the Phase 1/Phase 2 boundary.
- **Files:** `docs/care/frequencys/`

---

## KNOWN ISSUES

### No integration tests

- **Severity:** high
- **Symptom:** rollback completeness and tagging correctness are unverified
- **Suspected cause:** module was just written; tests not yet authored
- **Attempted:** nothing yet

### Hardcoded FalkorDB connection

- **Severity:** medium
- **Symptom:** `FALKORDB_HOST = "localhost"` and `FALKORDB_PORT = 6379` at module level
- **Suspected cause:** early implementation, no config injection yet
- **Attempted:** nothing -- will be resolved when config system is standardized

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement or VIEW_Extend

**Where I stopped:** Doc chain written. Code exists but is not wired into the health pipeline.

**What you need to understand:**
The prescribe() function returns recommendations. It does not apply them. The caller (daily_check_runner or a future care orchestrator) must decide to call apply_frequency(). This separation is deliberate -- prescription and application are different responsibilities.

**Watch out for:**
- Phase 2 types (decay_shield, sensitivity_boost, circadian_sync, typing_frequency) cannot be implemented without @nervo's metabolism sublayer. Do not stub them. Wait for the real thing.
- structure_seed has `duration_hours: None` (permanent) but rollback still removes the nodes. "Permanent" means "no automatic expiry," not "irreversible."
- calm_down uses negative intensity. The frustration drive is reduced, not boosted. This is the only frequency that goes negative.

**Open questions I had:**
- Should prescribe() be called automatically by the daily runner, or should a care orchestrator mediate?
- Should there be approval gates for STRUCTURED brain frequencys (higher risk of unintended interaction with existing graph structure)?
- What is the treatment_id format? UUID? Timestamp-based? Handle-prefixed?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Phase 1 frequencys are implemented -- 6 types covering drive stimulation and structural scaffolding, with auto-prescription based on brain category and full rollback via treatment_id tagging. Doc chain is complete. Next step is wiring into the health pipeline and writing integration tests.

**Decisions made:**
- Phase 1 / Phase 2 boundary drawn at metabolism sublayer dependency. Phase 2 waits for @nervo.
- Intensity defaults are conservative (0.15-0.3). Calibration against real data is pending.
- structure_seed adds 5 typed nodes (desire, concept x2, value, process) as minimum viable structure.

**Needs your input:**
- Auto-apply policy: which brain categories get automatic frequency application vs. requiring review?
- Treatment ID format convention
- Timeline for @nervo metabolism sublayer (blocks Phase 2)

---

## TODO

### Doc/Impl Drift

- None currently -- docs and code are in sync as of 2026-03-18.

### Tests to Run

```bash
# No tests exist yet. First test to write:
pytest tests/test_frequencys.py  # (does not exist)
```

### Immediate

- [ ] Write integration tests: apply -> verify tags -> rollback -> verify zero residual
- [ ] Wire prescribe() into daily_check_runner post-scoring phase
- [ ] Decide treatment_id format and generation strategy

### Later

- [ ] Calibrate intensity defaults against real citizen brain data
- [ ] Add treatment history logging for longitudinal research
- [ ] Design approval workflow for STRUCTURED brain frequencys
- IDEA: Frequency effectiveness dashboard -- before/after scores for each treatment_id

---

## POINTERS

| What | Where |
|------|-------|
| Frequency implementation | `services/health_assessment/frequencys.py` |
| Health pipeline runner | `services/health_assessment/daily_check_runner.py` |
| Brain topology reader | `services/health_assessment/brain_topology_reader.py` |
| Scoring aggregator | `services/health_assessment/aggregator.py` |
| Scoring formulas | `services/health_assessment/scoring_formulas/` |
| Project sync | `docs/SYNC_GraphCare.md` |
| Crisis detection docs | `docs/care/crisis_detection/` |
