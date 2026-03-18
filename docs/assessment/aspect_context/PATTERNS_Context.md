# Context & Understanding — Patterns: Why This Shape

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Context.md
THIS:            PATTERNS_Context.md (you are here)
ALGORITHM:       ./ALGORITHM_Context.md
VALIDATION:      ./VALIDATION_Context.md
HEALTH:          ./HEALTH_Context.md
SYNC:            ./SYNC_Context.md

PARENT CHAIN:    ../daily_citizen_health/
SPEC:            ../../specs/personhood_ladder.json (aspect="context")
IMPL:            @mind:TODO
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the parent chain: `../daily_citizen_health/` (especially ALGORITHM for the 7 primitives)
3. Read the Personhood Ladder spec: `docs/specs/personhood_ladder.json`

**After modifying this doc:**
1. Update the IMPL source to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

---

## THE PROBLEM

Context & Understanding capabilities are the hardest to observe from topology because they describe internal cognitive processes: "did the citizen understand the stimulus?" is a mental event, not a graph structure.

Without good scoring:
- Citizens who act without reading context appear productive but produce misaligned work
- Citizens who ground in reality are indistinguishable from those who hallucinate state
- The most foundational capabilities (T1) go unmeasured while flashier ones get attention
- No feedback signal tells a citizen "you're not reading enough context before acting"

---

## THE PATTERN

**Structural proxy scoring: Brain structure reveals habits, behavior reveals practice.**

We cannot observe "did the citizen understand?" directly. But we CAN observe:

### Brain Signals (What It Has)

The brain graph reveals what context-related structures the citizen has built:

| Brain Signal | What It Reveals | Primitives Used |
|--------------|-----------------|-----------------|
| Process nodes | The citizen has internalized procedures | count("process"), mean_energy("process") |
| Memory nodes | The citizen retains session-to-session knowledge | count("memory"), recency("memory") |
| Concept nodes linked to processes | Understanding connects to action | link_count("concept", "process") |
| Curiosity drive | The citizen wants to learn/explore | drive("curiosity") |
| Cluster coefficient | Knowledge is interconnected, not fragmented | cluster_coefficient("concept") |

A citizen with many high-energy process nodes has internalized "how to do things." One with many memory nodes retains context across sessions. These are structural prerequisites for good context behavior.

### Behavior Signals (What It Does)

The universe graph reveals whether the citizen actually uses context:

| Behavior Signal | What It Reveals | Observables Used |
|-----------------|-----------------|------------------|
| Moments in doc/state spaces | Reads docs before acting | moments(actor, "doc_space") |
| First moment after stimulus is a read, not a write | Grounds before acting | temporal ordering of moments |
| Moments in multiple spaces before committing | Fetches diverse context | distinct spaces visited before commit |
| Self-initiated corrections | Notices own errors | moments with type "correction" |
| Response matches stimulus type | Understands what's being asked | moment link types relative to parent |

### The Gap

The gap between brain structure and behavior reveals context quality:

- **Brain-rich, behavior-poor:** Has process/memory nodes but never reads docs before acting. Knows HOW but doesn't DO.
- **Brain-poor, behavior-active:** Reads lots of docs but hasn't internalized structure. Depends on external context every time.
- **Both high:** Healthy — internalized knowledge AND consistently applies it.
- **Both low:** Does not understand context AND does not seek it. Foundational problem.

---

## DESIGN DECISIONS

### D1: Process Nodes as Context Readiness Proxy

```
WHY:    A citizen that has built process nodes has internalized procedures.
        This is the brain-side proxy for "knows how to operate."
        More process nodes + high energy = more internalized context habits.
RISK:   A citizen could have process nodes from another domain that don't
        help with current work. Acceptable — structure is still a signal.
```

### D2: Memory Nodes as State Continuity Proxy

```
WHY:    Memory nodes persist knowledge across sessions.
        A citizen with recent memory nodes is maintaining state.
        This maps directly to ctx_manage_own_state and ctx_read_journal_first.
RISK:   Memory nodes could be stale or irrelevant.
        recency("memory") addresses staleness.
```

### D3: Doc-Space Moments as Context Fetching Proxy

```
WHY:    When a citizen reads docs/SYNC/templates, it creates moments in
        doc-type spaces. Counting these (temporally weighted) reveals
        whether the citizen fetches context before acting.
RISK:   A citizen could "read" without understanding. Acceptable —
        we measure the habit, not the comprehension.
```

### D4: Curiosity Drive as Learning Proxy

```
WHY:    The curiosity drive in brain physics indicates desire to explore
        and learn. High curiosity = the citizen seeks context naturally.
        Low curiosity = the citizen acts from assumption.
ALTERNATIVE: Could use count("question") nodes — but questions are less
        universal than the curiosity drive.
```

### D5: Weighted Sub-Index (T1 > T2 > T3 > T4)

```
WHY:    T1 capabilities are foundational — a citizen that doesn't ground
        in reality is dangerous. T4 capabilities are advanced — missing
        them is a growth area, not a crisis.
WEIGHTS: T1 caps at 0.35 per capability (3 caps * 0.35 = 1.05, normalized)
         T2 caps at 0.25 per capability
         T3 caps at 0.20
         T4 caps at 0.15
```

---

## BEHAVIORS SUPPORTED

- B1 (Daily Assessment) — Each context capability gets a score daily
- B2 (Privacy Preservation) — All signals are structural: counts, energies, links, drives
- B3 (Actionable Intervention) — Low context scores produce specific recommendations ("read SYNC before starting")
- B4 (Self-Correction) — Context scores feed into aggregate, which feeds stress drive

## BEHAVIORS PREVENTED

- A1 (Content reading) — No formula reads what the citizen thought, only structure
- A2 (Rewarding theater) — A citizen that reads docs but never acts doesn't score high (behavior component dominates at 60%)
- A3 (Ignoring foundations) — T1 weighting ensures grounding failures are always visible

---

## DATA

| Source | Type | Purpose |
|--------|------|---------|
| Brain topology | GRAPH | Process, memory, concept nodes; curiosity drive; cluster coefficient |
| Universe graph | GRAPH | Doc-space moments, temporal ordering, stimulus-response patterns |
| Personhood Ladder spec | FILE | Exact capability definitions for aspect="context" |
| Parent ALGORITHM | FILE | 7 primitives, scoring pattern (40/60 split) |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Daily Citizen Health | Defines the 7 primitives, scoring framework, intervention pattern |
| Personhood Ladder | Defines the 7 capabilities we score |
| Brain topology reader | Provides process/memory/concept counts and drives |
| Universe graph reader | Provides moment data in doc-type spaces |

---

## SCOPE

### In Scope

- Scoring formulas for all 7 context capabilities
- Brain + behavior component for each
- Sub-index computation (weighted mean)
- Failure mode descriptions and recommendations
- Synthetic test profiles

### Out of Scope

- Other aspects (execution, process, initiative, etc.) — separate doc chains
- Content analysis — structurally impossible
- Quality-of-understanding measurement — we measure the habit, not the comprehension
- T5+ capabilities — none exist for this aspect

---

## MARKERS

<!-- @mind:todo Validate that doc-space moments are reliably created when citizens read docs -->
<!-- @mind:proposition Consider a "context diversity" signal: does the citizen read ONLY SYNC or also PATTERNS, ALGORITHM, etc.? -->
