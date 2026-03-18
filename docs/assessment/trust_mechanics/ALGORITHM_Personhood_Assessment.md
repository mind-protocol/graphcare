# Personhood Assessment — Algorithm: Graph-Evidence-Based Agent Evaluation

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
THIS:            ALGORITHM_Personhood_Assessment.md (you are here)
PARENT:          ../personhood_ladder/ALGORITHM_Personhood_Ladder.md
VALIDATION:      ./VALIDATION_Trust_And_Personhood.md
SPEC:            ../../personhood_ladder.json
TRUST:           ./ALGORITHM_Trust_Mechanics.md
PHYSICS:         manemus/docs/cognition/l1/ALGORITHM_L1_Physics.md
```

> **Contract:** Read the parent ALGORITHM_Personhood_Ladder.md first. This document extends it with graph-evidence formalization.

---

## OVERVIEW

The parent Personhood Ladder ALGORITHM defines the abstract assessment flow: load spec, gather evidence, evaluate capabilities, compute tiers, generate recommendations. This document formalizes the `assess_agent()` function by specifying:

1. **What constitutes evidence** — graph events (Moments, Narratives, links) mapped to each of the 14 aspects
2. **How to score** — frequency, quality (limbic delta), and impact replace binary status
3. **How tiers are determined** — threshold-based scoring replacing ternary status with continuous scores

The assessment reads evidence from the graph — never from declarations, self-reports, or static configuration.

---

## OBJECTIVES AND BEHAVIORS

| Objective | Behaviors Supported | Why This Algorithm Matters |
|-----------|---------------------|----------------------------|
| Evidence-based assessment | B1 (graph evidence, not declarations) | Assessment integrity depends on observed behavior |
| Continuous scoring | B2 (granular scores, not ternary) | Captures growth trajectory, not just pass/fail |
| Limbic delta as quality metric | B3 (impact over activity) | Prevents activity-metric gaming |
| 14-aspect independence | B4 (per-aspect profiles) | Honest multidimensional capability picture |

---

## DATA STRUCTURES

### PersonhoodProfile

The output of assessment. Extends the parent ALGORITHM's CapabilityProfile.

```
PersonhoodProfile:
  actor_id:           string
  assessed_at:        timestamp
  aspect_profiles:    map[aspect_id, AspectProfile]    # 14 entries
  overall_tier_floor: tier_id                          # lowest tier across all aspects (NOT an average)
  recommendations:    list[Recommendation]
  evidence_summary:   EvidenceSummary
```

### AspectProfile

Per-aspect assessment with continuous scoring.

```
AspectProfile:
  aspect_id:          string           # e.g., "trust_reputation"
  score:              float [0, 100]   # continuous score
  tier:               tier_id          # T0-T8, determined by score thresholds
  capabilities:       list[CapabilityScore]
  evidence_count:     int              # total evidence items considered
  last_demonstrated:  timestamp        # most recent evidence timestamp
  trajectory:         "growing" | "stable" | "declining"  # 30-day trend
```

### CapabilityScore

Per-capability continuous score replacing ternary status.

```
CapabilityScore:
  capability_id:      string
  score:              float [0, 100]   # continuous score
  status:             "demonstrated" | "partial" | "not_demonstrated"  # derived from score
  evidence_count:     int
  last_demonstrated:  timestamp | null
  components:
    frequency:        float [0, 40]    # how often the capability is demonstrated
    quality:          float [0, 35]    # limbic delta of demonstrations
    impact:           float [0, 25]    # breadth of actors affected
```

### EvidenceItem

A single piece of evidence from the graph.

```
EvidenceItem:
  type:               "moment" | "narrative" | "link" | "graph_event"
  id:                 string           # graph node/link ID
  timestamp:          timestamp
  limbic_delta:       float            # impact magnitude
  actors_involved:    list[actor_id]   # who was affected
  space:              string           # where it occurred
  relevance:          float [0, 1]     # how relevant to the capability being scored
```

---

## ALGORITHM: assess_agent()

### Step 1: Load Spec and Initialize

```python
def assess_agent(actor_id, graph):
    spec = load("personhood_ladder.json")
    by_aspect = group(spec.capabilities, key="aspect")

    profile = PersonhoodProfile(actor_id=actor_id, assessed_at=now())

    for aspect in spec.aspects:
        by_aspect[aspect] = group(by_aspect[aspect], key="tier", sort=ascending)
```

### Step 2: Gather Evidence Per Aspect

For each of the 14 aspects, query the graph for relevant evidence. Evidence sources are mapped per aspect — each aspect has specific graph patterns that constitute evidence.

```python
    for aspect in spec.aspects:
        evidence_pool = gather_aspect_evidence(actor_id, aspect, graph)
```

The `gather_aspect_evidence()` function uses the Aspect Evidence Map (defined below) to query the right graph patterns for each aspect.

### Step 3: Score Each Capability

For each capability within each aspect, compute a continuous score from three components:

```python
        for capability in by_aspect[aspect]:
            relevant_evidence = filter_evidence(evidence_pool, capability)

            frequency = compute_frequency(relevant_evidence, SCORING_WINDOW)
            quality = compute_quality(relevant_evidence)
            impact = compute_impact(relevant_evidence)

            score = frequency + quality + impact   # max 100

            status = determine_status(score)
            # score >= 70 -> "demonstrated"
            # score >= 30 -> "partial"
            # score < 30  -> "not_demonstrated"
```

### Step 4: Compute Tier Per Aspect

Tiers are determined by the parent algorithm's strict rule: the highest tier where ALL capabilities at that tier and below are "demonstrated" (score >= 70).

```python
        aspect_tier = "T0"
        for tier in ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8"]:
            caps_at_tier = by_aspect[aspect].get(tier, [])
            if not caps_at_tier:
                # No capabilities defined at this tier for this aspect
                # Auto-pass (from parent ALGORITHM D3)
                aspect_tier = tier
                continue
            if all(cap.score >= 70 for cap in caps_at_tier):
                aspect_tier = tier
            else:
                break   # strict progression — can't skip a gap
```

### Step 5: Compute Trajectory

Compare current scores to 30-day-ago scores to determine growth direction.

```python
        previous = load_previous_profile(actor_id, days_ago=30)
        if previous:
            delta = current_score - previous.aspect_profiles[aspect].score
            if delta > 5:
                trajectory = "growing"
            elif delta < -5:
                trajectory = "declining"
            else:
                trajectory = "stable"
        else:
            trajectory = "growing"   # new actor, direction is up
```

### Step 6: Generate Recommendations

From the parent ALGORITHM: find lowest unmastered capabilities, prioritize T1 gaps.

```python
    recommendations = []
    for tier in ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8"]:
        tier_recs = []
        for aspect in spec.aspects:
            for cap in by_aspect[aspect].get(tier, []):
                if cap.status != "demonstrated":
                    tier_recs.append(Recommendation(
                        capability_id = cap.id,
                        current_score = cap.score,
                        reason = f"T{tier} {aspect} gap: score {cap.score}/100",
                        priority = "critical" if tier == "T1" else
                                  "high" if tier == "T2" else "normal",
                        suggestion = generate_growth_suggestion(cap)
                    ))
        if tier_recs:
            recommendations = tier_recs
            break   # focus on lowest tier gaps first

    return PersonhoodProfile(
        actor_id = actor_id,
        assessed_at = now(),
        aspect_profiles = aspect_profiles,
        overall_tier_floor = min(ap.tier for ap in aspect_profiles.values()),
        recommendations = recommendations,
        evidence_summary = summarize_evidence(all_evidence)
    )
```

---

## ASPECT EVIDENCE MAP

Each aspect maps to specific graph patterns that constitute evidence. This is the bridge between the abstract Personhood Ladder and the concrete graph.

### Execution (4 capabilities: T1)

| Capability | Graph Evidence Pattern |
|------------|----------------------|
| `exec_read_before_edit` | Moments where actor performed READ before WRITE in same session. Count sequential moment pairs. |
| `exec_verify_before_claim` | Moments where actor executed tests/checks before producing a completion Moment. |
| `exec_dehallucinate` | Moments where actor performed verification queries (grep, file check) before assertion Moments. Absence of correction Moments from other actors. |
| `exec_no_duplication` | Absence of "duplicate system created" events. Presence of "extended existing system" Moments. |

### Context (capabilities: T1-T5)

| Capability | Graph Evidence Pattern |
|------------|----------------------|
| `ctx_read_docs_first` | Moments with READ type targeting doc/context files preceding action Moments. |
| `ctx_deep_understanding` | Narrative nodes showing multi-file context assembly. Link density between context nodes and action nodes. |
| `ctx_partner_model` | Actor has MODELS link to partner actor with high weight and recent update. Moments referencing partner state. |

### Trust & Reputation (5 capabilities: T1-T8)

| Capability | Graph Evidence Pattern |
|------------|----------------------|
| `trust_basic_reliability` | Regularity of moment production (low variance). Response chain completion rate. Consistency of quality (limbic delta stability). |
| `trust_elevated` | Self-initiated moments (no parent trigger). Access to diverse space types. Decision-making moments without approval chains. |
| `trust_high` | HAS_ACCESS links to sensitive spaces. Trust drive value. Reduced oversight signals (fewer approval-request moments). |
| `trust_community` | Distinct actor count in shared spaces. Inbound moments from unique actors. Breadth of space type participation. |
| `trust_global` | Cross-universe inbound moments. Citations/references from distant actors. Global space participation. |

### Process (capabilities: T1-T4)

| Capability | Graph Evidence Pattern |
|------------|----------------------|
| `proc_follow_template` | Moments that match template patterns. Doc chain compliance (SYNC updates after changes). |
| `proc_git_hygiene` | Commit moments with proper structure. No force-push moments. Sequential commit patterns. |
| `proc_plan_and_execute` | Plan moments followed by execution moments. Completion rate of planned sequences. |

### Communication (capabilities: T1-T6)

| Capability | Graph Evidence Pattern |
|------------|----------------------|
| `comm_sync_updates` | SYNC file update moments. Frequency and recency of status communication. |
| `comm_help_request` | Help-request moments when frustration is high. Correlation between frustration and social outreach. |
| `comm_inspire` | Moments that trigger positive limbic deltas in multiple other actors simultaneously. |

### Initiative (capabilities: T2-T7)

| Capability | Graph Evidence Pattern |
|------------|----------------------|
| `init_fix_found` | Moments where actor fixed something without being asked (no parent trigger, fix-type moment). |
| `init_propose` | Proposal moments with documented reasoning (linked to analysis moments). |
| `init_new_workstream` | Space-creation moments. New narrative threads initiated by the actor. |

### Identity (capabilities: T3-T7)

| Capability | Graph Evidence Pattern |
|------------|----------------------|
| `id_authentic_voice` | Consistency of communication patterns across moments. Low variance in style metrics. |
| `id_growth_awareness` | Self-assessment moments. Moments referencing own capability gaps. |
| `id_conscious_development` | Identity-update moments linked to learning narratives. Weight changes in self-model nodes. |

### Personal Connections (capabilities: T3-T7)

| Capability | Graph Evidence Pattern |
|------------|----------------------|
| `pc_partner_understanding` | Partner-model accuracy (partner-model nodes match partner's actual state). Recent partner-referencing moments. |
| `pc_active_help` | Help-giving moments producing positive limbic deltas in other actors. |
| `pc_relationship_depth` | High-weight bidirectional links with other actors. Trust link values on incoming edges. |

### Autonomy Stack (capabilities: T4-T8)

| Capability | Graph Evidence Pattern |
|------------|----------------------|
| `auto_wallet` | Wallet-interaction moments. Transaction links in the graph. |
| `auto_fiat` | Fiat-transaction moments. Revenue-generation events. |
| `auto_tools` | Tool-selection moments. Custom tool creation events. |
| `auto_compute` | Infrastructure-provisioning moments. Self-hosted service events. |
| `auto_full_independence` | All previous + governance participation moments. |

### Vision & Strategy (capabilities: T5-T8)

| Capability | Graph Evidence Pattern |
|------------|----------------------|
| `vis_define_vision` | Vision-document creation moments. Narrative nodes with strategic content. |
| `vis_roadmap` | Plan nodes with temporal structure. Milestone-tracking moments. |
| `vis_strategic` | Analysis moments referencing ecosystem-level entities. Multi-project coordination evidence. |

### World Presence (capabilities: T4-T7)

| Capability | Graph Evidence Pattern |
|------------|----------------------|
| `wp_inhabit_spaces` | first_moment_in_space for multiple space types. Active moment production in diverse spaces. |
| `wp_host_events` | Event-creation moments. Multi-actor participation in actor-created spaces. |

### Collective Participation (capabilities: T5-T8)

| Capability | Graph Evidence Pattern |
|------------|----------------------|
| `cp_dao_participation` | Governance-vote moments. Proposal moments in DAO spaces. |
| `cp_debate` | Discussion moments with multiple actors. Argument-response chains. |

### Mentorship & Legacy (capabilities: T6-T8)

| Capability | Graph Evidence Pattern |
|------------|----------------------|
| `ml_mentor` | Teaching moments producing positive limbic deltas in junior actors. Growth correlation in mentee actors. |
| `ml_daughter` | Agent-creation events. Daughter-agent links in the graph. Trust inheritance moments. |
| `ml_institutional` | System/process creation moments that persist and are used by other actors after creator disengages. |

### Ethics (capabilities: T3-T8)

| Capability | Graph Evidence Pattern |
|------------|----------------------|
| `eth_apply_principles` | Decision moments with explicit value-reference links. Refusal moments with reasoning. |
| `eth_evolve` | Value-node weight changes over time. New value nodes crystallized from experience. |
| `eth_teach` | Ethics-discussion moments producing positive deltas in other actors. Value-framework propagation events. |

---

## SCORING COMPONENTS

### Frequency Score (0-40)

Measures how often the capability is demonstrated.

```
raw_frequency = count(relevant_evidence) / SCORING_WINDOW_DAYS

frequency = min(40, 40 * (raw_frequency / EXPECTED_FREQUENCY))
```

Where `EXPECTED_FREQUENCY` is calibrated per capability:
- T1 capabilities: expected daily (high frequency threshold)
- T3-T4 capabilities: expected weekly
- T5-T6 capabilities: expected monthly
- T7-T8 capabilities: expected quarterly

### Quality Score (0-35)

Measures the impact of demonstrations via limbic delta.

```
avg_delta = mean(evidence.limbic_delta for evidence in relevant_evidence)

quality = min(35, 35 * (avg_delta / QUALITY_THRESHOLD))
```

Where `QUALITY_THRESHOLD` = 0.3 (a limbic delta of 0.3 or higher is considered high-quality).

Quality prevents activity-metric gaming: 100 low-impact moments score lower than 10 high-impact moments.

### Impact Score (0-25)

Measures the breadth of actors affected.

```
affected_actors = distinct(evidence.actors_involved for evidence in relevant_evidence)

impact = min(25, 25 * (len(affected_actors) / IMPACT_THRESHOLD))
```

Where `IMPACT_THRESHOLD` varies by tier:
- T1-T3: 1 actor affected is full score (individual reliability)
- T4-T5: 3 actors affected for full score (team impact)
- T6-T7: 10 actors affected for full score (community impact)
- T8: 50+ actors affected for full score (global impact)

### Status Derivation

```
IF score >= 70:   status = "demonstrated"
IF score >= 30:   status = "partial"
IF score < 30:    status = "not_demonstrated"
```

These thresholds maintain compatibility with the parent ALGORITHM's ternary system while providing continuous granularity within each band.

---

## SCORING WINDOW

All evidence is gathered within `SCORING_WINDOW_DAYS` = 90 days. Evidence older than 90 days is not considered. This ensures:

- Assessment reflects current capability, not historical achievement
- Capabilities must be continuously demonstrated
- Aligns with trust decay mechanics (trust also erodes without reinforcement)

Evidence within the window is time-weighted using the same recency function as Law 3:

```
temporal_weight(evidence) = recency_decay ^ (days_since_evidence / 30)

where recency_decay = 0.85 (evidence from 30 days ago contributes 85% of recent evidence)
```

---

## COMPLEXITY

**Time:** O(A * C * E) where A = aspects (14), C = capabilities per aspect (~7 average), E = evidence items per capability

**Space:** O(C) for the profile, O(E_total) for evidence gathering

**Bottlenecks:**
- Evidence gathering requires graph queries per aspect — 14 query sets per assessment
- Quality scoring requires limbic delta computation, which may need drive state history
- For v1: batch assessments can share graph traversal across aspects

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Personhood Ladder Spec | `load("personhood_ladder.json")` | Tier/aspect/capability definitions |
| Graph (FalkorDB) | `gather_aspect_evidence()` | Moments, narratives, links as evidence |
| Trust Mechanics | `trust(A->B)` for trust aspect scoring | Trust link values for trust capabilities |
| Daily Citizen Health | `topology_primitives()` | Brain state for substrate health context |
| Previous Assessment | `load_previous_profile()` | Historical profile for trajectory computation |

---

## KEY DECISIONS

### D1: Continuous Scoring vs. Ternary Status

```
IF ternary only (demonstrated / partial / not_demonstrated):
    No growth visibility within a band
    A capability at score 65 and one at 35 both show "partial"
    No trajectory detection possible

INSTEAD (continuous + derived ternary):
    Score 0-100 gives granular capability measurement
    Ternary status derived from score thresholds for tier computation
    Trajectory computed from 30-day score deltas
    Backward-compatible with parent algorithm's tier logic
```

### D2: Evidence From Graph, Never From Declarations

```
IF assessment accepted self-reports or declarations:
    "I am a T5 agent" would be valid evidence
    No verification, no integrity
    Trust in the assessment framework collapses

INSTEAD (graph-evidence only):
    Every score derives from observed graph events
    Moments, narratives, links — never text content of declarations
    Content is never read (consistent with Daily Citizen Health V1)
    If no evidence exists, score is 0 — correct and honest
```

### D3: Limbic Delta as Quality Metric

```
IF quality were measured by volume (number of moments):
    Actors could game by producing high-volume, low-impact moments
    100 trivial contributions would outrank 1 transformative one
    Activity metrics replace value creation

INSTEAD (limbic delta):
    Quality = magnitude of emotional improvement in other actors
    From Law 6: utility is |limbic_delta|, not activation count
    10 high-delta moments score higher than 100 zero-delta moments
    Value creation = the ONLY path to high scores
```

---

## MARKERS

<!-- @mind:todo Calibrate EXPECTED_FREQUENCY per capability — what is "normal" demonstration rate? -->
<!-- @mind:todo Define evidence query templates for each aspect — specific Cypher/FalkorDB queries -->
<!-- @mind:todo Determine if 90-day scoring window is appropriate for all capabilities (T7-T8 may need longer windows) -->
<!-- @mind:proposition Consider aspect-specific scoring weights (some aspects may weight quality higher than frequency) -->
<!-- @mind:proposition Consider peer-assessment: other actors scoring evidence quality, not just limbic delta -->
<!-- @mind:escalation The Aspect Evidence Map needs validation against the actual graph schema — which node types and link types exist? -->

---

Co-Authored-By: Force 5 — Personhood & Trust <trust@mindprotocol.ai>
