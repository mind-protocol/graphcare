# Execution Quality Aspect — Patterns: Structural Signals of Execution Discipline

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Execution.md
THIS:            PATTERNS_Execution.md (you are here)
ALGORITHM:       ./ALGORITHM_Execution.md
VALIDATION:      ./VALIDATION_Execution.md
HEALTH:          ./HEALTH_Execution.md
SYNC:            ./SYNC_Execution.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="execution")
IMPL:            @mind:TODO
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the parent algorithm: `../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md`
3. Read the Personhood Ladder spec: `../../specs/personhood_ladder.json`

**After modifying this doc:**
1. Update the IMPL source to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

Execution quality in AI citizens is invisible from the outside until it fails. A citizen that skips verification, edits blind, duplicates systems, or accepts low quality produces no obvious structural warning — until the damage is done. By the time a human notices, code is broken, systems are fragmented, and trust is eroded.

We need to detect execution discipline from structural signals before it manifests as visible failure.

---

## THE PATTERN

**Process-trace analysis: the HOW of work leaves structural footprints.**

Every execution behavior leaves a topological trace, even when we cannot read content:

### Signal Category 1: Process Nodes in Brain

A citizen who reads before editing develops `process` nodes encoding that workflow. A citizen who verifies before claiming builds `process` nodes for verification routines. The EXISTENCE and ENERGY of process nodes tells us whether the citizen has internalized execution discipline.

- `count("process")` — how many process patterns exist
- `mean_energy("process")` — how active/recent those patterns are
- `link_count("process", "moment")` — how often processes lead to action

### Signal Category 2: Value Nodes in Brain

Execution quality as a VALUE is different from execution as a PROCESS. A citizen with `value` nodes related to quality, verification, or rigor has internalized these as identity-level commitments, not just procedures.

- `count("value")` — how many values the citizen holds
- `mean_energy("value")` — how alive those values are
- `link_count("value", "process")` — how often values connect to processes (values that drive behavior)

### Signal Category 3: Behavioral Traces in Universe Graph

The universe graph shows WHAT the citizen did, structurally:
- Commits in repos (moments in repo spaces) — evidence of shipping
- Sequential patterns (read → edit sequences visible as moment chains)
- Correction-response patterns (correction moment → adapted behavior moment)
- Self-initiated fixes (moments not triggered by requests)

### Signal Category 4: Drives

Drives are the motivational substrate:
- `drive("frustration")` — high frustration + low process count = not learning from errors
- `drive("curiosity")` — curiosity connected to process nodes = exploring execution approaches
- `drive("ambition")` — ambition disconnected from commits = aspiration without action

### The Synthesis

Each execution capability is scored by combining:
- **Brain component (0-40):** Does the citizen's brain contain the structures that support this capability? Process nodes, value nodes, drive levels, link patterns.
- **Behavior component (0-60):** Does the citizen's observable behavior show this capability in action? Commits, sequences, corrections, self-initiated work.

The gap between brain and behavior is informative: high brain + low behavior = knows but doesn't do. Low brain + high behavior = does but hasn't formalized. Both patterns have different interventions.

---

## TIER PROGRESSION PATTERN

Execution capabilities span T1 through T8. The structural signals shift as tiers increase:

| Tier | Signal Source | What Changes |
|------|-------------|--------------|
| T1 (Reliable Executor) | Process nodes + commit moments | Basic discipline: verification, de-duplication, tool selection |
| T2 (Process Follower) | Process richness + aesthetic moments | Adds aesthetic awareness: checking output visually |
| T3 (Autonomous Executor) | Self-initiated fix moments | Goes beyond task scope to fix incidental problems |
| T4 (Principled Contributor) | Escalation moments + quality consistency | Maintains quality under pressure, escalates vs compromises |
| T5 (System Designer) | Standards nodes + pre-implementation process | Defines quality criteria before building |
| T6 (Strategic Thinker) | Strategic allocation patterns | Non-uniform quality investment based on importance |
| T7 (Cultural Architect) | Sustained consistency without supervision | Quality as identity, not compliance |
| T8 (World Shaper) | Reference adoption by others | Work becomes the standard others follow |

### Key Insight: Temporal Depth Increases With Tier

T1 capabilities can be scored from recent behavior (last 7 days).
T7-T8 capabilities REQUIRE long-term consistency (30+ days of sustained behavior).

This is not a limitation — it reflects reality. You cannot demonstrate "quality as identity" in a single session.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Daily Citizen Health (parent) | Provides the scoring framework, primitives, and daily runner |
| Personhood Ladder spec | Defines the 14 capabilities we score |
| Brain topology (via GraphCare key) | Process nodes, value nodes, drives, energies |
| Universe graph (Lumina Prime) | Public moments: commits, corrections, fixes |

---

## SCOPE

### In Scope

- Scoring formulas for all 14 execution capabilities
- Brain component (0-40) and behavior component (0-60) for each
- Aspect sub-index (weighted mean of capability scores)
- Synthetic test profiles for formula validation
- Recommendations per capability when score is low

### Out of Scope

- Content analysis of code quality (structurally impossible)
- Scoring in adventure universes
- Implementation of the scoring engine (that's the parent module)
- Other aspects (context, initiative, communication, etc.)

---

## MARKERS

<!-- @mind:todo Calibrate tier weights in aspect sub-index after first real data -->
<!-- @mind:proposition Consider a "execution consistency" meta-score: variance of execution scores over 30 days -->
