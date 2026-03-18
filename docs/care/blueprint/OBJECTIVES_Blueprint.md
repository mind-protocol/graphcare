# OBJECTIVES — Universe Blueprint

> CHAIN: → [PATTERNS](PATTERNS_Blueprint.md) → ALGORITHM → VALIDATION → SYNC
> IMPL: mind-mcp `runtime/seed_brain_from_source_docs_dynamic_generator.py` + `runtime/cognition/citizen_brain_seeder.py`
> STATUS: DESIGNING

## What This Module Optimizes For

**O1: Starting health.** Every new citizen should start with a brain that scores above MINIMAL — with typed nodes (desire, concept, value, process), initialized drives, and enough structure for the scoring formulas to measure real capabilities. Today: 4.8/100 uniform. Target: differentiated scores from day 1.

**O2: Per-universe identity.** A Venetian merchant and a Lumina Primer engineer should NOT start with the same brain. Each universe has its own blueprint that reflects its culture, values, and norms. There is no common base across universes — some universes don't share Mind Protocol values.

**O3: Continuous improvement.** The blueprint is not a frozen snapshot. It's a living artifact that improves as we learn what makes healthy brains. GraphCare's health data feeds back into blueprint quality. Better blueprint → better starting health → less intervention needed.

**O4: Open process.** Any citizen or org can propose additions to the blueprint. GraphCare proposes health-related nodes. Arsenal proposes engineering nodes. The process is open, proposals are reviewed, and improvements are merged.

## Non-Objectives

- **Per-citizen customization at blueprint level.** The blueprint is the shared starting point. Per-citizen differentiation comes from the overlay (citizen_brain_seeder) and from lived experience. The blueprint defines the floor, not the ceiling.
- **Backward compatibility.** When the blueprint improves, we reseed. Old brains get the new structure. No maintaining deprecated node types.
- **Explicit versioning.** FalkorDB backups handle snapshots. We don't maintain a v1/v2/v3 registry.

## Tradeoffs

| Decision | Chosen | Over | Why |
|----------|--------|------|-----|
| Blueprint scope | Per-universe (L1) | Global (L4) | Universes have different cultures and values. No common base. |
| Storage | L1 brain graph (public) | JSON file | Must be queryable, not just readable. Same format as citizen brains. |
| Update strategy | Reseed all | Diff-apply | Simpler, more reliable. FalkorDB is fast enough. |
