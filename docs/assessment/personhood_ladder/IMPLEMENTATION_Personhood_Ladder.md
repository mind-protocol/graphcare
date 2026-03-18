# Personhood Ladder — Implementation: Code Architecture and Structure

```
STATUS: DRAFT
CREATED: 2026-03-13
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Personhood_Ladder.md
BEHAVIORS:       ./BEHAVIORS_Personhood_Ladder.md
PATTERNS:        ./PATTERNS_Personhood_Ladder.md
ALGORITHM:       ./ALGORITHM_Personhood_Ladder.md
VALIDATION:      ./VALIDATION_Personhood_Ladder.md
THIS:            IMPLEMENTATION_Personhood_Ladder.md (you are here)
HEALTH:          ./HEALTH_Personhood_Ladder.md
SYNC:            ./SYNC_Personhood_Ladder.md

IMPL:            docs/specs/personhood_ladder.json
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## CODE STRUCTURE

```
docs/specs/
├── personhood_ladder.json        # Source of truth — spec definition

@mind:TODO assessment tooling code structure to be defined
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `docs/specs/personhood_ladder.json` | Spec definition | tiers, aspects, capabilities | ~1067 | OK |

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Data-driven assessment. The JSON spec is the single artifact. All behavior (assessment, recommendations, display) derives from it.

**Why this pattern:** The spec changes faster than code. By keeping the spec as pure data (JSON), we can iterate on capabilities, tiers, and verification criteria without touching assessment code.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Schema-as-data | `personhood_ladder.json` | Spec changes don't require code changes |

### Anti-Patterns to Avoid

- **Hardcoded capabilities**: Don't embed capability IDs or tier assignments in code. Read from JSON.
- **Single-score reduction**: Don't compute an "overall tier." Profiles are vectors.
- **Assessment without evidence**: Don't mark capabilities without checking verification criteria.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Spec definition | Tiers, aspects, capabilities, verification criteria | Assessment logic, evidence gathering | JSON read |
| Assessment engine | Capability evaluation, tier computation, recommendations | Evidence storage, behavioral logging | assess_agent() |

---

## SCHEMA

### Personhood Ladder Spec Schema

```yaml
PersonhoodLadder:
  required:
    - name: string                  # "Personhood Ladder"
    - version: string               # semver
    - tiers: map[string, Tier]      # T0-T8
    - aspects: map[string, Aspect]  # 14 aspects
    - capabilities: list[Capability] # ~104 capabilities
  constraints:
    - Every capability.aspect must exist in aspects
    - Every capability.tier must exist in tiers
    - Every capability must have non-empty how_to_verify

Tier:
  required:
    - name: string
    - summary: string
    - description: string

Aspect:
  required:
    - name: string
    - description: string
    - progression: string

Capability:
  required:
    - id: string                    # unique, snake_case
    - aspect: string                # must match an aspect key
    - tier: string                  # must match a tier key
    - name: string
    - description: string
    - how_to_verify: string
    - failure_mode: string
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| Spec load | `personhood_ladder.json` | Assessment tooling, documentation generation |

@mind:TODO Assessment engine entry points to be defined when tooling is built

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### Assessment Flow: Agent Evaluation

The primary flow. Takes an agent and behavioral data, produces a capability profile.

```yaml
flow:
  name: agent_assessment
  purpose: Evaluate an AI agent's capability profile against the Personhood Ladder
  scope: behavioral data in, capability profile out
  steps:
    - id: load_spec
      description: Load personhood_ladder.json and group capabilities by aspect × tier
      file: docs/specs/personhood_ladder.json
      input: JSON file
      output: Structured spec with grouped capabilities
      trigger: Assessment request
      side_effects: none
    - id: gather_evidence
      description: Collect behavioral observations per capability
      input: agent_id, capability.how_to_verify
      output: list of timestamped observations
      trigger: Per capability iteration
      side_effects: reads from behavioral log
    - id: evaluate_capabilities
      description: Mark each capability as demonstrated/partial/not_demonstrated
      input: evidence per capability
      output: list of CapabilityAssessment
      trigger: After evidence gathered
      side_effects: none
    - id: compute_tiers
      description: Walk tiers per aspect, stop at first gap
      input: CapabilityAssessment list grouped by aspect
      output: aspect_tiers dict
      trigger: After all capabilities evaluated
      side_effects: none
    - id: generate_recommendations
      description: Find lowest unmastered capabilities, prioritize T1 gaps
      input: CapabilityAssessment list, aspect_tiers
      output: ordered recommendations list
      trigger: After tiers computed
      side_effects: none
  docking_points:
    guidance:
      include_when: significant transformation or boundary crossing
      omit_when: trivial pass-through
    available:
      - id: dock_spec_load
        type: file
        direction: input
        file: docs/specs/personhood_ladder.json
        payload: full spec JSON
        async_hook: not_applicable
        needs: none
        notes: Static file, rarely changes
      - id: dock_profile_output
        type: event
        direction: output
        payload: CapabilityProfile
        async_hook: optional
        needs: add event emission when tooling is built
        notes: Main output — consumed by GraphCare Service 3
    health_recommended:
      - dock_id: dock_spec_load
        reason: Spec integrity must be verified (V2)
      - dock_id: dock_profile_output
        reason: Profile must satisfy tier integrity (V1) and aspect independence (V3)
```

---

## BIDIRECTIONAL LINKS

### Code → Docs

@mind:TODO Add DOCS references in assessment code when built

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM assess_agent() | @mind:TODO |
| VALIDATION V1 (tier integrity) | @mind:TODO |
| VALIDATION V2 (spec source of truth) | `docs/specs/personhood_ladder.json` |

---

## MARKERS

<!-- @mind:todo Build assessment engine: load spec, gather evidence, evaluate, compute tiers, recommend -->
<!-- @mind:todo Define behavioral log interface for evidence gathering -->
<!-- @mind:todo Add DOCS references when code exists -->
