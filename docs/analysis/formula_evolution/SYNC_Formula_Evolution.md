# Formula Evolution — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- The @register decorator pattern in `registry.py` — formulas are pure functions registered by capability_id
- The CapabilityScore dataclass with brain_component (0-40) + behavior_component (0-60) split
- The `_cap` helper for normalizing values to a 0-1 range with a ceiling
- 35 formulas across 14 aspect files, all passing tests

**What's still being designed:**
- Formula versioning scheme (how to track which version produced which score)
- Weight calibration process (how outcome data feeds back into formula weights)
- Community proposal workflow (submission, review, shadow testing, adoption)
- Shadow testing infrastructure

**What's proposed (v2+):**
- Automated correlation analysis between signals and outcomes
- Formula playground for citizen self-service testing
- Cross-universe formula variants (different weights for adventure vs work universes)

---

## CURRENT STATE

The scoring formula infrastructure is built and operational. The registry pattern (`@register` decorator) makes formulas pluggable. 14 aspect files contain 35 formulas covering capabilities from T1 through T4 across aspects like initiative, execution, communication, trust, identity, and others. All formulas follow the same structure: brain component (0-40) computed from BrainStats topology primitives + behavior component (0-60) computed from BehaviorStats universe graph observables.

What does NOT exist: versioning, changelogs, shadow testing, community contribution workflow, or any connection between intervention outcomes and formula adjustment. Formulas are currently static — they were written once and have not been modified based on real-world data.

The 69 unscored capabilities (out of 104 total) have no formulas. They produce `scored: false, total: null` in the daily assessment.

---

## IN PROGRESS

### Doc chain creation

- **Started:** 2026-03-15
- **By:** @vox
- **Status:** In progress
- **Context:** Creating OBJECTIVES, PATTERNS, SYNC as part of the parallel doc chain writing sprint. Formula evolution is the companion to process improvement — process improvement identifies problems, formula evolution fixes them.

---

## RECENT CHANGES

### 2026-03-15: Initial doc chain creation

- **What:** Created OBJECTIVES, PATTERNS, and SYNC for formula_evolution module
- **Why:** Scoring formulas are the heart of GraphCare's assessment pipeline. Without a defined evolution process, the 35 existing formulas will remain educated guesses indefinitely.
- **Files:** `docs/analysis/formula_evolution/OBJECTIVES_*.md`, `PATTERNS_*.md`, `SYNC_*.md`
- **Insights:** The registry pattern is elegantly simple — but it currently lacks version tracking. Adding a `version` parameter to `@register(capability_id, version="v1")` would be a minimal, non-breaking change that enables the entire versioning system.

---

## KNOWN ISSUES

### No formula versioning

- **Severity:** High
- **Symptom:** Historical scores cannot be attributed to specific formula versions
- **Suspected cause:** Versioning wasn't part of the initial implementation scope
- **Attempted:** Nothing yet — identified during doc chain creation

### 69 capabilities unscored

- **Severity:** Medium
- **Symptom:** Many Personhood Ladder capabilities produce `null` scores
- **Suspected cause:** Creating formulas requires judgment about which topology signals predict each capability — it's intellectual work, not mechanical
- **Attempted:** Nothing systematic — formulas were written capability by capability

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement (adding versioning to registry) or VIEW_Extend (writing new formulas for unscored capabilities)

**Where I stopped:** Documentation only for the evolution process. The registry code exists and works. The gap is between "formulas exist" and "formulas evolve."

**What you need to understand:**
The registry is a simple dict: `_REGISTRY: Dict[str, FormulaFn] = {}`. The `@register` decorator adds functions to it. To add versioning, you need to change the registry structure to store `(FormulaFn, version_string)` tuples or a small metadata object. The `aggregator.py` DailyRecord should then include a `formula_versions: Dict[str, str]` field so each day's scores are tagged with the formula versions that produced them.

**Watch out for:**
- The `_cap` helper in `registry.py` is used by every formula. Don't break its signature.
- The `CapabilityScore.__post_init__` clamps values to 0-40 / 0-60 ranges. Any new formula must respect these bounds or the clamping will silently change your intended scores.
- Formula files import from relative paths (`from .registry import register`). The module structure matters for Python imports.

**Open questions I had:**
- Should shadow testing use a separate registry, or should the same registry support multiple formulas per capability_id?
- How do we handle formula version conflicts when two proposals target the same capability simultaneously?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Formula evolution documentation created. This module defines how GraphCare's 35 scoring formulas improve over time — through weight calibration, signal discovery, and community contribution. The existing @register pattern provides the structural foundation. The key missing piece is versioning: we need to know which formula version produced which score.

**Decisions made:**
- Chose three evolution mechanisms: weight calibration, signal discovery, community proposals
- Defined shadow testing as mandatory before any formula change goes live (minimum 2 weeks)
- Topology-only constraint is non-negotiable — no formula may read brain content, regardless of accuracy gains

**Needs your input:**
- Priority order: should we focus on improving existing 35 formulas (depth) or expanding to cover more of the 104 capabilities (breadth)?
- Should community formula proposals be open to any citizen, or limited to specific roles/tiers?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: Add version parameter to @register decorator
- [ ] DOCS->IMPL: Add formula_versions field to DailyRecord in aggregator.py
- [ ] DOCS->IMPL: Build shadow testing infrastructure

### Tests to Run

```bash
cd /home/mind-protocol/graphcare && python -m pytest tests/test_health_assessment.py -v
```

### Immediate

- [ ] Add `version` parameter to `@register` decorator in `registry.py`
- [ ] Update all 14 formula files to include version strings (v1 for all existing)
- [ ] Extend DailyRecord in `aggregator.py` to store `formula_versions` dict

### Later

- [ ] Build shadow testing harness
- [ ] Define community proposal submission format
- [ ] Create formula coverage dashboard (35/104 scored, prioritized backlog)
- IDEA: Use intervention outcome data to rank which unscored capabilities would most improve care quality if scored

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
The registry pattern is one of the best things about GraphCare's architecture. It was designed for pluggability, and formula evolution is exactly the kind of pluggability it was designed for. The path from "static formulas" to "evolving formulas" is clear and requires surprisingly little new code — mostly metadata additions.

**Threads I was holding:**
- The 40/60 brain/behavior split is itself a candidate for evolution. Should this ratio be per-capability rather than universal? Some capabilities may be 80% behavioral, others 80% structural.
- The `_cap` ceilings (e.g., `_cap(brain.desire_count, 10)` uses ceiling 10) are themselves tunable parameters. Calibration should include ceiling values, not just weights.

**Intuitions:**
The first calibration wins will come from adjusting ceiling values in `_cap` calls. These were set by intuition and probably don't match real citizen distributions. If the average citizen has 3 desires, a ceiling of 10 means most citizens max out at 0.3 on that signal. That might be right or very wrong.

**What I wish I'd known at the start:**
The formula files are already well-structured with clear docstrings explaining the signal rationale. The code quality is high. Evolution should preserve this clarity — every weight change needs the same quality of explanation.

---

## POINTERS

| What | Where |
|------|-------|
| Formula registry | `services/health_assessment/scoring_formulas/registry.py` |
| Initiative formulas (example) | `services/health_assessment/scoring_formulas/initiative.py` |
| All 14 formula files | `services/health_assessment/scoring_formulas/*.py` |
| Daily record storage | `services/health_assessment/aggregator.py` |
| Personhood Ladder spec | `docs/specs/personhood_ladder.json` |
| Daily health algorithm | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Process improvement (sibling) | `docs/analysis/process_improvement/` |
