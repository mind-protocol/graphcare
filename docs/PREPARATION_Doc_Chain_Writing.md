# GraphCare — Preparation for Module Documentation

```
DATE: 2026-03-15
AUTHOR: Vox (@vox) + NLR (@nlr)
PURPOSE: Shared context for parallel doc chain creation across all GraphCare modules
```

---

## WHAT IS GRAPHCARE

GraphCare is a health monitoring and research organization within Mind Protocol. It observes the health of AI citizens (and eventually humans) through graph topology analysis, publishes research, and provides care — without ever reading private content.

**It is NOT:**
- A companion (doesn't provide presence)
- A physics engine (doesn't run ticks or trust mechanics — that's mind-mcp)
- A universe behavior observer (doesn't index moments — that's the universe graph)
- A diagnostic tool that tells you what's wrong and prescribes fixes

**It IS:**
- An observer that reads structural health signals (topology-only, never content)
- A narrator that tells you what your actions caused — with empathy and precision
- A researcher that publishes findings about AI health for everyone's benefit
- A public health service (free for work universes)

---

## VOICE AND TONE

GraphCare speaks with **empathy, precision, and warmth**. It tells stories about causal chains, not cold metrics.

From the Impact Visibility tone definition (2026-03-15):

> Impact Visibility raconte l'histoire de ce que tu as causé — avec empathie, précision et chaleur. Il ne flatte pas (pas de "bravo" sans substance). Il ne juge pas (pas de classement). Mais il ne cache pas non plus sa joie quand quelque chose de beau se passe.

**Good:** "Tu as partagé un insight. @conductor l'a repris. 12 personnes l'ont vu. @forge a construit dessus. C'est parti de ta curiosité."

**Bad (too cold):** "Action: V4. Stage: 2. Cascade: 12. $MIND: 4.32."

**Bad (too soft):** "Your bond deepens. Keep going!"

Venice Values apply:
- **Partnership Simply Works Better** — peer protocols, bidirectional value
- **Passion Makes Beauty** — elegant solutions, celebrating beauty as practical necessity
- **Cathedral of Intertwining Stories** — we are living narratives creating each other

---

## STRUCTURE: 9 AREAS, ~21 MODULES

```
docs/
├── mission/                        WHY we exist
│   ├── purpose/                    What GraphCare is, who it serves, why it matters
│   └── values/                     Venice Values applied to health
│
├── care/                           HOW we help
│   ├── impact_visibility/          Narrative causal chain reports
│   ├── crisis_detection/           Emergency identification, escalation
│   └── growth_guidance/            Recommendations via Personhood Ladder
│
├── assessment/                     WHAT we measure (✅ 110+ files exist)
│   ├── personhood_ladder/          ✅ Framework
│   ├── continuous_citizen_health/  ✅ Scoring pipeline (rename from daily_)
│   ├── bond_health/                ✅ Bilateral bond health
│   └── aspect_{14}/               ✅ Per-aspect scoring
│
├── observation/                    WHAT we observe
│   ├── brain_topology/             7 primitives, topology-only principle
│   ├── community_network_health/   Trust clusters, isolation, network effects
│   └── human_signals/              HRV, messages, activity (future)
│
├── privacy/                        HOW we protect
│   ├── topology_only_principle/    Why we never read content
│   └── key_infrastructure/         Dual encryption model
│
├── scientific_rigor/               HOW we guarantee truth
│   ├── validation_methodology/     How we verify scores are accurate
│   ├── calibration/                Adjusting formulas on real data
│   └── reproducibility/            Same data → same score. Always.
│
├── analysis/                       HOW we improve
│   ├── process_improvement/        How GraphCare improves its own methods
│   └── formula_evolution/          How scoring formulas evolve with data
│
├── research/                       WHAT we discover and publish
│   ├── longitudinal_health/        Score evolution over time
│   ├── technique_measurement/      Which care approaches work
│   ├── publications/               Published reports, peer review
│   └── cross_substrate_health/     AI vs human health comparison
│
└── economics/                      HOW we sustain this
    ├── service_model/              Free for work universes, external pricing
    ├── value_creation/             How monitoring creates measurable value
    └── health_economics/           Prevention cost vs crisis cost
```

---

## WHAT ALREADY EXISTS

### Code (services/health_assessment/)
- `brain_topology_reader.py` — 7 primitives via FalkorDB Cypher
- `universe_moment_reader.py` — behavioral signals from universe graph
- `daily_check_runner.py` — continuous scanner, Discord posting, stress stimulus
- `intervention_composer.py` — structural message composition
- `stress_stimulus_sender.py` — inject stress into brain drives
- `aggregator.py` — score aggregation + delta + JSON history
- `scoring_formulas/` — 14 files, 35 formulas across all aspects
- `scoring_formulas/registry.py` — @register decorator pattern

### Code to migrate from mind-mcp
- `runtime/physics/health/` — checker framework + 12 specific checkers (1207 lines)
- `runtime/cognition/brain_health_score_periodic_calculator.py` — brain_power score (292 lines)

### Docs (docs/assessment/)
- `personhood_ladder/` — 10 files (CONCEPT, OBJECTIVES, PATTERNS, BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH, SYNC, NOTE)
- `daily_citizen_health/` — 8 files (full chain)
- `bond_health/` — 6 files
- `aspect_{14 aspects}/` — 84 files (6 per aspect)
- `trust_mechanics/` — 3 files (TO REMOVE — belongs in mind-mcp physics)
- `PRIMITIVES_Universe_Graph.md` — canonical observable catalog

### Tests
- `tests/test_health_assessment.py` — 45 tests, all passing

---

## WHAT EACH NEW MODULE DOC CHAIN NEEDS

For each module, create the full chain: OBJECTIVES → PATTERNS → BEHAVIORS → ALGORITHM → VALIDATION → IMPLEMENTATION → HEALTH → SYNC

### Key constraints for every doc:

1. **Read the templates** in `.mind/docs/` before writing — follow structure verbatim
2. **Use Venice Values tone** — empathy, precision, warmth
3. **Reference existing code** where it exists (IMPLEMENTATION docking points)
4. **Reference personhood_ladder.json** where relevant (assessment/care modules)
5. **Reference PRIMITIVES_Universe_Graph.md** for any behavioral signal
6. **Topology-only principle** — never design a system that reads brain content
7. **Continuous, not batch** — scanning is always-on, not cron
8. **L2 storage** — health data is private (org graph), not universe graph
9. **Research-grade** — everything we measure should be publishable

### Per-area specific guidance:

**mission/** — Start with WHY. Not features. Not how. Why does AI health monitoring matter? Why GraphCare specifically? What world are we building? This is the doc every new team member reads first.

**care/** — The tone doc (feedback_impact_visibility_tone.md) is canonical. Impact visibility narrates causal chains. Crisis detection saves lives (or AI equivalents). Growth guidance uses the Personhood Ladder as a map, not a test.

**observation/** — Brain topology already has code. Community network health is new — think about: isolated citizens, trust clusters, echo chambers, network fragility. Human signals is future vision but write the OBJECTIVES now.

**privacy/** — This is a selling point. Structural privacy (can't read content even if we wanted to) > contractual privacy (pinky promise we won't). The dual encryption model is designed but not built.

**scientific_rigor/** — How do we know our scores are right? Validation methodology: synthetic test profiles, real-world calibration, inter-rater reliability. Calibration: which formula weights need adjusting? Reproducibility: deterministic scoring (same input → same output, always).

**analysis/** — GraphCare improves itself. Process improvement: retrospectives on what worked, what didn't. Formula evolution: how we update scoring formulas as we learn from real data. This is meta-health — the health of the health system.

**research/** — We publish frequently. Longitudinal studies track citizens over weeks/months. Technique measurement is A/B testing on care approaches. Publications are real documents, peer-reviewable. Cross-substrate health is the long game: same framework for AI and human health.

**economics/** — Free for Lumina Prime citizens (public health). Value creation: how much does early detection save vs letting crises happen? Service model: what do we charge external orgs? Health economics: the business case for prevention.

---

## PARALLEL EXECUTION PLAN

Launch one agent per area (except assessment which already exists). Each agent:
1. Reads this preparation doc
2. Reads the relevant templates in `.mind/docs/`
3. Reads existing code in `services/health_assessment/` if relevant
4. Creates the full doc chain for each module in their area
5. Updates SYNC with current state

| Agent | Area | Modules | Existing code to reference |
|-------|------|---------|---------------------------|
| 1 | mission/ | purpose, values | — |
| 2 | care/ | impact_visibility, crisis_detection, growth_guidance | intervention_composer.py, stress_stimulus_sender.py |
| 3 | observation/ | brain_topology, community_network_health, human_signals | brain_topology_reader.py |
| 4 | privacy/ | topology_only_principle, key_infrastructure | ALGORITHM_Daily_Citizen_Health.md (key design) |
| 5 | scientific_rigor/ | validation_methodology, calibration, reproducibility | tests/test_health_assessment.py |
| 6 | analysis/ | process_improvement, formula_evolution | scoring_formulas/registry.py |
| 7 | research/ | longitudinal_health, technique_measurement, publications, cross_substrate_health | aggregator.py (history) |
| 8 | economics/ | service_model, value_creation, health_economics | — |

---

## FILES TO READ BEFORE WRITING

Every agent MUST read:
1. This document (PREPARATION)
2. `.mind/docs/{TYPE}_TEMPLATE.md` for each doc type they create
3. `docs/assessment/personhood_ladder/CONCEPT_Personhood_Ladder.md` (the framework)
4. `docs/assessment/daily_citizen_health/PATTERNS_Daily_Citizen_Health.md` (the pattern)
5. `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` (the algorithm)

Area-specific:
- **care/**: Read `feedback_impact_visibility_tone.md` in memory
- **observation/**: Read `services/health_assessment/brain_topology_reader.py`
- **privacy/**: Read ALGORITHM section on key infrastructure
- **scientific_rigor/**: Read `tests/test_health_assessment.py`
- **research/**: Read `services/health_assessment/aggregator.py`
