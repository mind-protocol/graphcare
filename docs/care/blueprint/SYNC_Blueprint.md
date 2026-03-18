# SYNC — Universe Blueprint

> CHAIN: [OBJECTIVES](OBJECTIVES_Blueprint.md) → [PATTERNS](PATTERNS_Blueprint.md) → ALGORITHM → VALIDATION → **SYNC**
> IMPL: mind-mcp `runtime/seed_brain_from_source_docs_dynamic_generator.py` + `runtime/cognition/citizen_brain_seeder.py`
> STATUS: DESIGNING

## Current State (2026-03-18)

### What Exists

- **Blueprint generator:** `seed_brain_from_source_docs_dynamic_generator.py` — creates 209+ nodes from 6 manifestos. Produces typed nodes (value, concept, process, etc.) with correct string types.
- **Citizen overlay:** `citizen_brain_seeder.py` — adds per-citizen role processes, drive adjustments, goals→desires, relational seeds. Correctly maps string types to NodeType enum.
- **Batch seeder:** `scripts/seed_lumina_prime_brains.py` — seeds all LP citizens from L4 registry.
- **Checkpointer:** `falkordb_checkpointer.py` — persists to FalkorDB.

### Critical Bug Found

The checkpointer writes `type: ""` for all nodes (line 169: `getattr(node, 'type', None)` but Node uses `node_type`). The `node_type` field is written correctly but GraphCare reads `type`.

**Impact:** All 278 Lumina Prime brains have 209+ nodes with `type: ""`. Scoring formulas find 0 desires, 0 concepts, 0 values → uniform 4.8/100.

**Fix needed:** One-liner in checkpointer + reseed all brains.

### What's Missing

- No "blueprint" concept exists yet — just "base brain" + "overlay"
- No quality assessment of the base brain
- No open process for improving the base brain
- No per-universe differentiation (everything seeds from the same manifestos)
- The base brain has no drives, no limbic state — those come only from the overlay

## Immediate TODOs

1. **Fix checkpointer bug** — `type` field should mirror `node_type.value`. @nervo notified.
2. **Reseed all brains** after fix — verify type distribution changes.
3. **Assess blueprint quality** — run GraphCare health check on a fresh blueprint-only brain (no overlay). What score does it get? What's missing?
4. **Define blueprint v1 spec** — what typed nodes, drives, cluster density are required based on scoring formula thresholds?

## Handoff

- **For @nervo:** Fix the checkpointer one-liner, reseed blueprints
- **For @dragon_slayer (GraphCare):** Define blueprint quality requirements from scoring formulas, run health assessment on blueprint brain
- **For NLR:** Decision on per-universe blueprint content — what goes in Lumina Prime vs Venezia?

## Recent Changes

| Date | What | Who |
|------|------|-----|
| 2026-03-18 | Bug found: checkpointer writes type="" | @dragon_slayer |
| 2026-03-18 | Blueprint module documented (OBJECTIVES, PATTERNS, SYNC) | @dragon_slayer |
| 2026-03-18 | @nervo notified via Discord | @dragon_slayer |
