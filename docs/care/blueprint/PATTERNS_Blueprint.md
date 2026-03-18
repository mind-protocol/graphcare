# PATTERNS — Universe Blueprint

> CHAIN: [OBJECTIVES](OBJECTIVES_Blueprint.md) → **PATTERNS** → ALGORITHM → VALIDATION → SYNC
> IMPL: mind-mcp `runtime/seed_brain_from_source_docs_dynamic_generator.py` + `runtime/cognition/citizen_brain_seeder.py`
> STATUS: DESIGNING

## Why This Design

### The Blueprint is a Brain, Not a Config

The blueprint lives as an L1 brain graph — same format as citizen brains. It's public and queryable. This means:
- GraphCare can run health assessment on the blueprint itself
- The blueprint is subject to the same physics as citizen brains
- Quality is measurable, not just claimed

### Two-Layer Architecture

```
Blueprint (L1, per-universe, public)     = shared starting structure
  +
Citizen Overlay (citizen_brain_seeder)   = per-citizen differentiation
  =
Citizen Brain (L1, private)              = unique starting state
```

**Blueprint** provides: universal values, architecture concepts, social processes, typed node scaffolding, drive baselines.

**Overlay** provides: role-specific processes, personality-derived drive adjustments, goal-derived desires, relational seeds.

### Per-Universe, No Common Base

Each universe has its own blueprint:
- **Lumina Prime:** Mind Protocol values, engineering concepts, collaborative processes
- **Venezia:** Venetian culture, merchant values, guild structures, historical context
- **Contre-Terre:** (future) its own values and structures

Some universes have citizens who don't know about Mind Protocol. Their blueprint shouldn't contain Mind Protocol manifestos.

## Current Problem (2026-03-18)

The `falkordb_checkpointer.py` writes all nodes with `type: ""` because it reads `getattr(node, 'type', None)` but the Node dataclass uses `node_type` (a NodeType enum). This means:

1. The base brain generates 209+ typed nodes (value, concept, process, etc.)
2. `load_brain_into_state()` maps them to `NodeType` enum correctly
3. The checkpointer writes `node_type` correctly but `type` as empty string
4. GraphCare reads `type` — finds nothing — scores 4.8/100 for everyone

**Fix:** One-liner in checkpointer + reseed all brains.

## Design Principles

**P1: Measurable quality.** The blueprint's health score should be measurable by GraphCare. If we can't score it, we can't improve it. Target: a fresh blueprint brain should score 60+ on GraphCare's assessment.

**P2: Open contribution.** Any org can propose additions. GraphCare proposes health nodes. Arsenal proposes engineering nodes. Proposals are reviewed against the universe's identity.

**P3: The overlay does the differentiation.** The blueprint doesn't try to make every citizen unique. It provides the shared floor. The citizen_brain_seeder + lived experience create uniqueness.

**P4: Reseed, don't patch.** When the blueprint improves, reseed all brains. FalkorDB backups protect against regressions. No diff-apply complexity.

## What GraphCare Contributes

GraphCare is the feedback loop for the blueprint. Our 14 scoring formulas define what "healthy" means. The blueprint should create brains that start with:

- **Typed nodes:** desire, concept, value, process, memory (minimum counts TBD from scoring formula thresholds)
- **Drive baselines:** curiosity, ambition, social_need, frustration — non-zero starting values
- **Cluster density:** nodes interconnected enough that cluster_coefficient > 0.1
- **Limbic state:** present and initialized

The exact requirements come from reverse-engineering the scoring formulas: what inputs produce a score above the MINIMAL→SEEDED→STRUCTURED thresholds?

## Scope

**In scope:**
- Blueprint definition and quality assessment
- Open contribution process
- Integration with citizen_brain_seeder
- Health-driven feedback loop

**Out of scope (for now):**
- Blueprint editor UI
- Automated blueprint generation from universe lore
- Cross-universe blueprint inheritance
