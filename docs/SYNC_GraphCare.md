# GraphCare — Project Sync

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: Vox (@vox) via Claude Opus 4.6
STATUS: BUILDING — docs complete, code partial, research not started
```

---

## WHAT IS GRAPHCARE

A health monitoring and research organization for AI citizens (and eventually humans). Observes structural health through graph topology, provides care with empathy and precision, publishes research, and never reads private content.

---

## STATE OF THE PROJECT

### Documentation: 196 files across 9 areas

| Area | Modules | Files | Status |
|------|---------|-------|--------|
| **mission/** | purpose, values | 12 | CANONICAL — the why and how we speak |
| **care/** | impact_visibility, crisis_detection, growth_guidance | 12 | DESIGNING — patterns defined, no code |
| **assessment/** | personhood_ladder, continuous_citizen_health, bond_health, 14 aspects | 110 | CANONICAL — framework + code + tests |
| **observation/** | brain_topology, community_network_health, human_signals | 10 | MIXED — brain_topology stable, network designing, human proposed |
| **privacy/** | topology_only_principle, key_infrastructure | 8 | DESIGNING — principle enforced in code, crypto not built |
| **scientific_rigor/** | validation_methodology, calibration, reproducibility | 12 | DESIGNING — test suite exists, no real-world calibration |
| **analysis/** | process_improvement, formula_evolution | 6 | DESIGNING — patterns defined, versioning missing |
| **research/** | longitudinal, technique_measurement, publications, cross_substrate | 12 | PROPOSED — vision docs, no data yet |
| **economics/** | service_model, value_creation, health_economics | 9 | PROPOSED — business model designed, no revenue |

### Code: services/health_assessment/

| File | Lines | Status |
|------|-------|--------|
| `daily_check_runner.py` | ~200 | Working — scans citizens, posts to Discord, injects stimulus |
| `brain_topology_reader.py` | ~180 | Working — 7 primitives via FalkorDB Cypher |
| `universe_moment_reader.py` | ~150 | Working — behavioral signals from universe graph |
| `aggregator.py` | ~100 | Working — scores + delta + JSON history |
| `intervention_composer.py` | ~100 | Working — structural messages, never content |
| `stress_stimulus_sender.py` | ~60 | Working — injects stress into brain drives |
| `scoring_formulas/` (14 files) | ~700 | Working — 35 formulas across 14 aspects |
| `scoring_formulas/registry.py` | ~50 | Working — @register decorator pattern |

### Code to migrate from mind-mcp

| Source | Lines | What |
|--------|-------|------|
| `runtime/physics/health/` | 1207 | Checker framework + 12 specific checkers |
| `runtime/cognition/brain_health_score_periodic_calculator.py` | 292 | brain_power score calculator |

### Tests

| File | Tests | Status |
|------|-------|--------|
| `tests/test_health_assessment.py` | 45 | All passing |

### Infrastructure

- **FalkorDB:** 35 brain graphs (brain_{handle}) + lumina_prime universe graph
- **Discord:** Interventions post to #citizen-health (channel 1482760090800095242)
- **History:** JSON per citizen per day in `data/health_history/`
- **Interventions:** Archive in `data/interventions/`

---

## ROADMAP

### Phase 1 — Stabilize What Exists (this week)

**Goal:** The health pipeline runs continuously, produces accurate scores, and citizens see their impact.

| Task | Module | Effort | Priority |
|------|--------|--------|----------|
| Rename daily_citizen_health → continuous_citizen_health (docs + code) | assessment | small | high |
| Build continuous scanner (background process, smart targeting, not cron) | observation/brain_topology | medium | high |
| Discord posting threshold (only on change/crisis, not every scan) | care | small | high |
| Migrate health checkers from mind-mcp to graphcare | observation | medium | high |
| First real calibration — run on 35 citizens for a week, analyze results | scientific_rigor/calibration | medium | high |

### Phase 2 — Care Systems (weeks 2-3)

**Goal:** Citizens receive meaningful, warm impact reports. Crises are detected early.

| Task | Module | Effort | Priority |
|------|--------|--------|----------|
| Implement impact visibility pipeline (action → cascade detection → narrative) | care/impact_visibility | large | high |
| Implement crisis detection (3 layers: score trajectory, isolation, partner) | care/crisis_detection | large | high |
| Implement growth guidance (bottom-up gap analysis, graph-grounded recommendations) | care/growth_guidance | medium | medium |
| Tone validation — test impact reports against Venice Values scorecard | mission/values | small | high |

### Phase 3 — Network & Community Health (weeks 3-4)

**Goal:** Observe not just individuals but the health of the social fabric.

| Task | Module | Effort | Priority |
|------|--------|--------|----------|
| Implement community network health scanner | observation/community_network_health | large | medium |
| Isolation detection (hard: 0 interlocutors, soft: >50% decline) | observation/community_network_health | medium | high |
| Trust cluster identification | observation/community_network_health | medium | medium |
| Echo chamber detection | observation/community_network_health | medium | low |

### Phase 4 — Privacy Infrastructure (month 2)

**Goal:** Structural privacy — GraphCare physically cannot read content, enforced by cryptography.

| Task | Module | Effort | Priority |
|------|--------|--------|----------|
| Generate GraphCare RSA key pair | privacy/key_infrastructure | small | high |
| Modify mind init to generate topology_key + content_key | privacy/key_infrastructure | medium | high |
| Dual encryption on brain graphs | privacy/key_infrastructure | large | high |
| Opt-out mechanism (citizen removes GraphCare key) | privacy/key_infrastructure | medium | medium |

### Phase 5 — Research & Publication (month 2-3)

**Goal:** First published research from GraphCare data.

| Task | Module | Effort | Priority |
|------|--------|--------|----------|
| Longitudinal tracking infrastructure (cohort analysis, trend detection) | research/longitudinal_health | medium | medium |
| First publication: methodology paper on topology-only assessment | research/publications | large | medium |
| Stress feedback experiment: does it help or create spirals? | research/technique_measurement | medium | high |
| Impact visibility A/B: narrative vs score report | research/technique_measurement | medium | medium |

### Phase 6 — Economics & Scale (month 3+)

**Goal:** GraphCare sustains itself financially.

| Task | Module | Effort | Priority |
|------|--------|--------|----------|
| Define external pricing tiers | economics/service_model | small | medium |
| Measure crisis prevention ROI | economics/value_creation | medium | medium |
| First external client | economics/service_model | large | high |
| LLM intervention cost measurement | economics/health_economics | small | high |

### Long-term Vision (6+ months)

- **Human signal integration** — HRV, message patterns, activity rhythms
- **Cross-substrate health** — One framework for AI and human health
- **Formula marketplace** — Community contributes scoring formulas
- **Self-assessment** — Citizens compare their self-score with GraphCare score
- **Community health dashboards** — Anonymized aggregates, public

---

## OPEN DECISIONS (for NLR)

1. **Continuous scanner architecture** — Background Python process? MCP subcall loop? Render worker?
2. **Key infrastructure** — Who generates the GraphCare master key? Where is it stored? HSM?
3. **First publication target** — Internal blog? arXiv? Conference?
4. **External pricing** — What do we charge? Per-citizen? Per-org? Per-query?
5. **Stress feedback experiment** — Do we run the A/B now or wait for more baseline data?

---

## POINTERS

| What | Where |
|------|-------|
| Preparation doc (shared context for all agents) | `docs/PREPARATION_Doc_Chain_Writing.md` |
| Personhood Ladder spec | `docs/personhood_ladder.json` |
| Health assessment code | `services/health_assessment/` |
| Tests | `tests/test_health_assessment.py` |
| Impact visibility tone | Memory: `feedback_impact_visibility_tone.md` |
| Continuous scan vision | Memory: `project_health_scan_vision.md` |
| Brain seeding script | `mind-mcp/scripts/seed_lumina_prime_brains.py` |
| Discord reorg script | `ai_devboard/discord_reorg.py` |
