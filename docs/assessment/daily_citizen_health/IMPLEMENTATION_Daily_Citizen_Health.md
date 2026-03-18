# Daily Citizen Health — Implementation: Code Architecture and Structure

```
STATUS: DRAFT
CREATED: 2026-03-13
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Daily_Citizen_Health.md
BEHAVIORS:       ./BEHAVIORS_Daily_Citizen_Health.md
PATTERNS:        ./PATTERNS_Daily_Citizen_Health.md
ALGORITHM:       ./ALGORITHM_Daily_Citizen_Health.md
VALIDATION:      ./VALIDATION_Daily_Citizen_Health.md
THIS:            IMPLEMENTATION_Daily_Citizen_Health.md (you are here)
HEALTH:          ./HEALTH_Daily_Citizen_Health.md
SYNC:            ./SYNC_Daily_Citizen_Health.md

IMPL:            @mind:TODO (not yet built)
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## CODE STRUCTURE

@mind:TODO — Code structure to be defined when implementation begins.

Proposed layout:

```
services/
├── health_assessment/
│   ├── daily_check_runner.py             # Cron entry point, iterates citizens
│   ├── brain_topology_reader.py          # Fetch + decrypt brain topology
│   ├── universe_moment_reader.py         # Query universe graph for public moments
│   ├── capability_scorer.py              # Apply scoring formulas per capability
│   ├── scoring_formulas/                 # One file per aspect
│   │   ├── execution.py                  # Scoring formulas for execution aspect
│   │   ├── initiative.py                 # Scoring formulas for initiative aspect
│   │   ├── context.py                    # ...
│   │   └── registry.py                   # Formula registry (capability_id → function)
│   ├── aggregator.py                     # Aggregate scores, compute delta
│   ├── intervention_composer.py          # Compose intervention messages
│   └── stress_stimulus_sender.py         # Send stress feedback to brain
```

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Pipeline — sequential stages, each producing data for the next.

**Why this pattern:** The daily check is a linear flow: fetch → compute → score → aggregate → intervene → feedback. No complex branching or event-driven behavior needed.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Registry | `scoring_formulas/registry.py` | Capability ID → formula function lookup |
| Pipeline | `daily_check_runner.py` | Sequential stages with clear data handoff |
| Strategy | `scoring_formulas/*.py` | Each formula is a strategy implementing the same interface |

### Anti-Patterns to Avoid

- **Content access**: No function may access `content` or `synthesis` fields. The topology reader physically strips them.
- **Custom queries**: No formula may run its own Cypher query. All data comes from the 7 primitives + universe observables.
- **Direct brain writes**: Never write to brain graph. Only send stimuli through the designated URL.

---

## SCHEMA

### Key Infrastructure

```yaml
GraphCareKeyPair:
  private_key: AES-256 private key (stored securely in GraphCare infrastructure)
  public_key: AES-256 public key (distributed via mind init)

CitizenBrainAccess:
  brain_url: string              # URL to access brain graph (from L4 registry)
  topology_key: bytes            # Symmetric key encrypted with GraphCare public key
  content_key: bytes             # Symmetric key encrypted with citizen public key

MindInitKeyFile:
  created_at: timestamp
  graphcare_public_key: bytes    # Public key of GraphCare health service
  topology_symmetric_key: bytes  # Encrypted with graphcare_public_key
```

### Scoring Formula Interface

```yaml
ScoringFormula:
  capability_id: string                    # Must match personhood_ladder.json
  primitives_used:
    brain: [list of primitive names]       # From the 7 primitives
    universe: [list of observable names]   # From universe graph observables
  weights: dict[string, float]             # Sub-component weights
  caps: dict[string, float]                # Normalization caps
  function: callable(brain_stats, behavior_stats) → CapabilityScore

CapabilityScore:
  brain_component: float   # 0-40
  behavior_component: float # 0-60
  total: float             # 0-100
```

### Health History Record

```yaml
DailyRecord:
  citizen_id: string
  date: date
  aggregate_score: float
  capability_scores: dict[capability_id, float]
  intervention_sent: bool
  stress_stimulus: float
  brain_reachable: bool
```

---

## ENTRY POINTS

| Entry Point | File | Triggered By |
|-------------|------|--------------|
| Daily cron | `daily_check_runner.py` | Cron job, once per 24 hours |

---

## KEY INFRASTRUCTURE SETUP

### Step 1: Generate GraphCare Key Pair

```
GraphCare generates an asymmetric key pair (RSA-4096 or Ed25519).
Private key: stored in GraphCare's secure infrastructure (never in repo, never in logs).
Public key: distributed to all projects via mind init.
```

### Step 2: Integrate Into mind init

When a citizen runs `mind init`:
1. The GraphCare public key is included in the init template
2. A symmetric topology key is generated for the brain graph
3. The topology key is encrypted with GraphCare's public key → stored in core graph config
4. A separate symmetric content key is generated
5. The content key is encrypted with the citizen's own public key → stored in core graph config

### Step 3: Register Brain URL in L4

The citizen's brain graph URL is registered in the Protocol layer registry.
GraphCare's daily check queries this registry to get the list of citizens + brain URLs.

### Step 4: Mind Protocol Repo Changes

```
mind-protocol/
├── templates/
│   └── keys/
│       └── graphcare_public.key    # GraphCare's public key for topology access
├── mind/init.py                    # Modified: generates topology_key + content_key
└── docs/
    └── KEY_INFRASTRUCTURE.md       # Documents the key model
```

---

## BIDIRECTIONAL LINKS

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM Step 1 (fetch) | @mind:TODO `brain_topology_reader.py` |
| ALGORITHM Step 2-3 (compute) | @mind:TODO `capability_scorer.py` |
| ALGORITHM Step 4-5 (aggregate) | @mind:TODO `aggregator.py` |
| ALGORITHM Step 6 (intervene) | @mind:TODO `intervention_composer.py` |
| ALGORITHM Step 7 (stimulus) | @mind:TODO `stress_stimulus_sender.py` |
| VALIDATION V1 (no content) | @mind:TODO `brain_topology_reader.py` (strips content) |

---

## MARKERS

<!-- @mind:todo Generate GraphCare key pair and add public key to mind-protocol templates -->
<!-- @mind:todo Modify mind init to generate topology_key + content_key -->
<!-- @mind:todo Build first scoring formula (exec_dehallucinate or init_propose_improvements) -->
<!-- @mind:todo Define health history storage (FalkorDB time series? flat files? separate DB?) -->
