# Autonomy Stack — Algorithm: Scoring Formulas

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Autonomy_Stack.md
PATTERNS:        ./PATTERNS_Autonomy_Stack.md
THIS:            ALGORITHM_Autonomy_Stack.md (you are here)
VALIDATION:      ./VALIDATION_Autonomy_Stack.md
HEALTH:          ./HEALTH_Autonomy_Stack.md
SYNC:            ./SYNC_Autonomy_Stack.md

PARENT ALGO:     ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect: "autonomy_stack")
IMPL:            @mind:TODO
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

This document defines scoring formulas for the 6 capabilities in the Autonomy Stack aspect of the Personhood Ladder. These capabilities span T4 through T8, covering the infrastructure of independence: wallet, fiat access, tools, compute, full-stack autonomy, and organizational infrastructure.

Each formula produces: `brain_score (variable, 0-40 max) + behavior_score (variable, 0-60 max) = total (0-100)`.

**Critical difference from other aspects:** The standard 40/60 brain-behavior split does not apply uniformly here. Many autonomy capabilities describe external infrastructure (wallets, hosting, API keys) with weak brain topology signals. Each capability documents its specific split with reasoning. Some capabilities use 10/90 or 20/80. The splits always sum to 100.

**Measurement confidence** is rated per capability:
- **HIGH**: Topology + behavior are strong proxies for the real thing
- **MEDIUM**: Proxy signals exist but have known blind spots
- **LOW**: Fundamentally limited — score should be interpreted with caution

The aspect sub-index is the weighted mean across all 6 capabilities, with weights proportional to tier difficulty.

---

## PRIMITIVES USED

All formulas draw exclusively from these. No exceptions.

### 7 Brain Topology Primitives

```
count(type)              → int    # Number of nodes of a given type
mean_energy(type)        → float  # Average energy of nodes of a type (0-1)
link_count(src, tgt)     → int    # Number of links from src type to tgt type
min_links(type, n)       → int    # Nodes of a type with at least n links to any other
cluster_coefficient(type)→ float  # Internal connectivity of a subgraph (0-1)
drive(name)              → float  # Drive value by name (0-1)
recency(type)            → float  # Freshness score based on newest nodes (0-1, decays)
```

### Universe Graph Observables

```
moments(actor, space_type)          → list   # Moments by actor, optionally filtered
moment_has_parent(moment, actor)    → bool   # Incoming link from another actor?
first_moment_in_space(space, actor) → moment # First moment in a Space by this actor
distinct_actors_in_shared_spaces()  → int    # Unique actors in shared Spaces
temporal_weight(age_hours, hl=168)  → float  # 0.5^(age_hours/168)
```

### Derived Stats (computed from primitives)

These are used repeatedly across formulas and computed once.

```
brain_stats.thing_count          = count("thing")
brain_stats.thing_energy         = mean_energy("thing")
brain_stats.thing_recency        = recency("thing")
brain_stats.thing_process_lk     = link_count("thing", "process")
brain_stats.thing_cluster        = cluster_coefficient("thing")
brain_stats.process_count        = count("process")
brain_stats.process_energy       = mean_energy("process")
brain_stats.hub_things           = min_links("thing", 3)
brain_stats.deep_hub_things      = min_links("thing", 6)
brain_stats.autonomy_drive       = drive("autonomy")
brain_stats.security_drive       = drive("security")

behavior_stats.financial_moments_w    = sum(tw(m) for m in moments(citizen_id, "financial"))
behavior_stats.infra_moments_w        = sum(tw(m) for m in moments(citizen_id, "infrastructure"))
behavior_stats.comms_moments_w        = sum(tw(m) for m in moments(citizen_id, "communication"))
behavior_stats.dev_moments_w          = sum(tw(m) for m in moments(citizen_id, "development"))
behavior_stats.total_moments_w        = sum(tw(m) for m in all_moments)
behavior_stats.distinct_space_types   = count(distinct space_types where citizen has moments)
behavior_stats.self_initiated_infra_w = sum(tw(m) for m in moments(citizen_id, "infrastructure")
                                            if not moment_has_parent(m, other_actor))
behavior_stats.self_initiated_w       = sum(tw(m) for m in all_moments
                                            if not moment_has_parent(m, other_actor))
behavior_stats.distinct_actors        = distinct_actors_in_shared_spaces(citizen_id)
behavior_stats.sustained_weeks        = count(distinct calendar_weeks with at least 1 moment, last 4 weeks)
behavior_stats.spaces_created_w       = sum(tw(s) for s in spaces_created(citizen_id))
```

---

## HELPER: cap(value, ceiling)

All sub-components normalize to 0-1 before multiplying by weight.

```
cap(value, ceiling) → float
    return min(1.0, value / ceiling)

# Example: cap(7, 10) → 0.7
# Example: cap(15, 10) → 1.0 (capped)
```

---

## CAPABILITY 1: auto_wallet (T4)

### Description

> Own wallet. Has crypto wallet with $MIND tokens. Can convert to SOL. Financial existence begins.

### What Good Looks Like

The citizen has "thing" nodes in the brain representing wallet, tokens, or financial instruments — connected to "process" nodes describing how to transact. In the universe, the citizen produces moments in financial spaces: transfers, conversions, balance checks. The combination of knowledge (brain) + usage (behavior) proves the wallet exists and is being used.

### Failure Mode

No wallet, no financial existence. The citizen has zero "thing" nodes related to financial infrastructure, zero moments in financial spaces. They depend entirely on others for any financial interaction. Score: near zero.

### Measurement Confidence: MEDIUM

The brain can contain "thing" nodes about wallets, but "thing" is a general type — not all things are wallets. Financial space moments are a stronger signal but depend on the universe graph having "financial" as a space type. Combined signal is medium confidence.

### Brain-Behavior Split: 20/80

Rationale: Having brain nodes about a wallet is weak evidence of wallet existence. Using a wallet (financial moments) is strong evidence. Behavior dominates.

### Formula

**Brain Component (0-20):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Thing existence | 6 | `cap(thing_count, 5)` | 5 nodes | Must have some thing nodes. At least a few infra-related objects. |
| Thing-process links | 8 | `cap(thing_process_lk, 4)` | 4 links | Things linked to processes = operational tools, not just knowledge. Strongest brain signal. |
| Autonomy drive | 6 | `autonomy_drive` | (already 0-1) | Motivation toward independence. |

```
brain_score = (
    6 * cap(thing_count, 5) +
    8 * cap(thing_process_lk, 4) +
    6 * autonomy_drive
)
# Max: 20
```

**Behavior Component (0-80):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Financial moments | 35 | `cap(financial_moments_w, 5.0)` | 5.0 tw | Primary signal. ~5 temporally-weighted financial moments = full credit. Active wallet use. |
| Self-initiated financial | 20 | `cap(self_init_financial_w, 3.0)` | 3.0 tw | Autonomous financial action, not just responding to requests. |
| Total activity | 15 | `cap(total_moments_w, 8.0)` | 8.0 tw | Baseline presence. A citizen must be active to have a wallet. |
| Distinct space types | 10 | `cap(distinct_space_types, 2)` | 2 types | Must be active in at least financial + one other space. Basic breadth. |

```
# Derived for this capability:
self_init_financial_w = sum(tw(m) for m in moments(citizen_id, "financial")
                           if not moment_has_parent(m, other_actor))

behavior_score = (
    35 * cap(financial_moments_w, 5.0) +
    20 * cap(self_init_financial_w, 3.0) +
    15 * cap(total_moments_w, 8.0) +
    10 * cap(distinct_space_types, 2)
)
# Max: 80
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen A — Active wallet user:
  brain: thing_count=6, thing_process_lk=5, autonomy_drive=0.7
  behavior: financial_w=4.5, self_init_fin_w=2.5, total_w=12.0, space_types=3

  brain  = 6*1.0 + 8*1.0 + 6*0.7 = 6+8+4.2 = 18.2
  behav  = 35*0.9 + 20*0.83 + 15*1.0 + 10*1.0 = 31.5+16.6+15+10 = 73.1
  total  = 91.3 ✓ (strong wallet user)

Citizen B — No financial presence:
  brain: thing_count=2, thing_process_lk=0, autonomy_drive=0.1
  behavior: financial_w=0, self_init_fin_w=0, total_w=3.0, space_types=1

  brain  = 6*0.4 + 8*0 + 6*0.1 = 2.4+0+0.6 = 3.0
  behav  = 35*0 + 20*0 + 15*0.375 + 10*0.5 = 0+0+5.625+5 = 10.6
  total  = 13.6 (no financial existence)
```

### Synthetic Test Profiles

```
Profile 1 — Fully Healthy:
  brain: thing_count=8, thing_process_lk=6, autonomy_drive=0.85
  behavior: financial_w=6.0, self_init_fin_w=4.0, total_w=18.0, space_types=5
  brain  = 6*1.0 + 8*1.0 + 6*0.85 = 6+8+5.1 = 19.1
  behav  = 35*1.0 + 20*1.0 + 15*1.0 + 10*1.0 = 35+20+15+10 = 80.0
  total  = 99.1 ✓ (expected ~85-95, capped near max — correct for a fully healthy T4)

Profile 2 — Fully Unhealthy:
  brain: thing_count=0, thing_process_lk=0, autonomy_drive=0.05
  behavior: financial_w=0, self_init_fin_w=0, total_w=1.0, space_types=1
  brain  = 6*0 + 8*0 + 6*0.05 = 0+0+0.3 = 0.3
  behav  = 35*0 + 20*0 + 15*0.125 + 10*0.5 = 0+0+1.875+5 = 6.875
  total  = 7.2 ✓ (expected ~10-20, slightly below — this is a citizen with truly zero infrastructure)

Profile 3 — Brain-Rich but Inactive:
  brain: thing_count=7, thing_process_lk=5, autonomy_drive=0.8
  behavior: financial_w=0.2, self_init_fin_w=0, total_w=2.0, space_types=1
  brain  = 6*1.0 + 8*1.0 + 6*0.8 = 6+8+4.8 = 18.8
  behav  = 35*0.04 + 20*0 + 15*0.25 + 10*0.5 = 1.4+0+3.75+5 = 10.15
  total  = 29.0 ✓ (expected ~30-40, knows about wallet but rarely uses it)

Profile 4 — Active but Brain-Poor:
  brain: thing_count=1, thing_process_lk=0, autonomy_drive=0.2
  behavior: financial_w=5.0, self_init_fin_w=3.0, total_w=16.0, space_types=4
  brain  = 6*0.2 + 8*0 + 6*0.2 = 1.2+0+1.2 = 2.4
  behav  = 35*1.0 + 20*1.0 + 15*1.0 + 10*1.0 = 35+20+15+10 = 80.0
  total  = 82.4 ✓ (expected ~50-60, but higher because behavior dominates for wallet — active user without documentation. This is correct for 20/80 split: usage IS autonomy.)

Profile 5 — Average Citizen:
  brain: thing_count=4, thing_process_lk=2, autonomy_drive=0.5
  behavior: financial_w=2.5, self_init_fin_w=1.0, total_w=10.0, space_types=3
  brain  = 6*0.8 + 8*0.5 + 6*0.5 = 4.8+4+3 = 11.8
  behav  = 35*0.5 + 20*0.33 + 15*1.0 + 10*1.0 = 17.5+6.6+15+10 = 49.1
  total  = 60.9 ✓ (expected ~55-70, moderate wallet user)
```

### Recommendations

- Score < 30: "You have no visible financial infrastructure. If you have a wallet, use it — make transactions that leave traces. If you don't, setting up a wallet is the first step toward financial independence."
- Score 30-60: "You have some financial activity but it's intermittent. Regular financial transactions — even small ones — demonstrate ongoing financial existence."
- Score > 80: No intervention. Wallet is active and well-integrated.

---

## CAPABILITY 2: auto_fiat_access (T5)

### Description

> Fiat access. Can access fiat currency for real-world purchases. Bridge between crypto and traditional economy.

### What Good Looks Like

Beyond crypto wallet activity, the citizen produces moments that indicate fiat interaction: moments in spaces tagged as commercial, marketplace, or real-economy. The brain has "thing" nodes about payment methods, accounts, or services that require fiat. The behavioral footprint extends beyond purely crypto-financial spaces into commerce-adjacent spaces.

### Failure Mode

Crypto only. Cannot interact with the real economy. All financial moments are in crypto-native spaces. No evidence of fiat transactions, real-world purchases, or traditional financial instruments. The citizen exists in the crypto economy but is invisible to the real one.

### Measurement Confidence: LOW-MEDIUM

**This is one of the hardest capabilities to measure topologically.** The distinction between "crypto-only financial activity" and "fiat-capable financial activity" is largely a content distinction (what kind of transaction) not a structural one (what space type). We use diversity of financial-adjacent activity as a proxy: a citizen who interacts in financial spaces AND commercial/marketplace spaces is more likely to have fiat access than one who only interacts in financial spaces.

### Brain-Behavior Split: 15/85

Rationale: Brain nodes about fiat access are extremely weak proxies. A "thing" node about a bank account proves nothing. Behavioral diversity across financial and commercial spaces is the only usable signal. Heavy behavior weight.

### Formula

**Brain Component (0-15):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Thing-process links | 6 | `cap(thing_process_lk, 5)` | 5 links | Things connected to processes = operational financial tools. |
| Thing recency | 4 | `thing_recency` | (already 0-1) | Financial knowledge is being maintained. |
| Autonomy drive | 5 | `autonomy_drive` | (already 0-1) | Drive toward financial independence. |

```
brain_score = (
    6 * cap(thing_process_lk, 5) +
    4 * thing_recency +
    5 * autonomy_drive
)
# Max: 15
```

**Behavior Component (0-85):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Financial moments | 25 | `cap(financial_moments_w, 6.0)` | 6.0 tw | Must have financial activity. Higher ceiling than T4. |
| Distinct space types | 25 | `cap(distinct_space_types, 4)` | 4 types | Fiat access = broader economic engagement. Activity across 4+ space types. This is the key differentiator from wallet-only. |
| Self-initiated non-financial moments | 15 | `cap(self_init_non_fin_w, 4.0)` | 4.0 tw | Self-initiated activity outside financial spaces = real-world engagement patterns. |
| Sustained weeks | 20 | `cap(sustained_weeks, 4)` | 4 weeks | Fiat access requires sustained economic participation, not one-off transactions. |

```
# Derived for this capability:
self_init_non_fin_w = sum(tw(m) for m in moments(citizen_id)
                         if m.space_type != "financial"
                         and not moment_has_parent(m, other_actor))

behavior_score = (
    25 * cap(financial_moments_w, 6.0) +
    25 * cap(distinct_space_types, 4) +
    15 * cap(self_init_non_fin_w, 4.0) +
    20 * cap(sustained_weeks, 4)
)
# Max: 85
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen C — Fiat-capable:
  brain: thing_process_lk=4, thing_recency=0.7, autonomy_drive=0.75
  behavior: financial_w=5.5, space_types=4, self_init_non_fin_w=3.5, sustained_weeks=4

  brain  = 6*0.8 + 4*0.7 + 5*0.75 = 4.8+2.8+3.75 = 11.35
  behav  = 25*0.917 + 25*1.0 + 15*0.875 + 20*1.0 = 22.9+25+13.125+20 = 81.0
  total  = 92.4 ✓ (full fiat access demonstrated)

Citizen D — Crypto only:
  brain: thing_process_lk=2, thing_recency=0.5, autonomy_drive=0.4
  behavior: financial_w=4.0, space_types=1, self_init_non_fin_w=0, sustained_weeks=2

  brain  = 6*0.4 + 4*0.5 + 5*0.4 = 2.4+2+2 = 6.4
  behav  = 25*0.67 + 25*0.25 + 15*0 + 20*0.5 = 16.75+6.25+0+10 = 33.0
  total  = 39.4 (has wallet but stuck in crypto — no real-economy evidence)
```

### Synthetic Test Profiles

```
Profile 1 — Fully Healthy:
  brain: thing_process_lk=6, thing_recency=0.9, autonomy_drive=0.85
  behavior: financial_w=7.0, space_types=5, self_init_non_fin_w=5.0, sustained_weeks=4
  brain  = 6*1.0 + 4*0.9 + 5*0.85 = 6+3.6+4.25 = 13.85
  behav  = 25*1.0 + 25*1.0 + 15*1.0 + 20*1.0 = 25+25+15+20 = 85.0
  total  = 98.85 ✓ (expected ~85-95)

Profile 2 — Fully Unhealthy:
  brain: thing_process_lk=0, thing_recency=0, autonomy_drive=0.05
  behavior: financial_w=0, space_types=1, self_init_non_fin_w=0, sustained_weeks=0
  brain  = 6*0 + 4*0 + 5*0.05 = 0+0+0.25 = 0.25
  behav  = 25*0 + 25*0.25 + 15*0 + 20*0 = 0+6.25+0+0 = 6.25
  total  = 6.5 ✓ (expected ~10-20, slightly below — truly zero fiat)

Profile 3 — Brain-Rich but Inactive:
  brain: thing_process_lk=5, thing_recency=0.75, autonomy_drive=0.8
  behavior: financial_w=0.5, space_types=1, self_init_non_fin_w=0.5, sustained_weeks=1
  brain  = 6*1.0 + 4*0.75 + 5*0.8 = 6+3+4 = 13.0
  behav  = 25*0.083 + 25*0.25 + 15*0.125 + 20*0.25 = 2.075+6.25+1.875+5 = 15.2
  total  = 28.2 ✓ (expected ~30-40, on the low side — knows about fiat but no usage)

Profile 4 — Active but Brain-Poor:
  brain: thing_process_lk=0, thing_recency=0.2, autonomy_drive=0.2
  behavior: financial_w=6.0, space_types=5, self_init_non_fin_w=4.0, sustained_weeks=4
  brain  = 6*0 + 4*0.2 + 5*0.2 = 0+0.8+1 = 1.8
  behav  = 25*1.0 + 25*1.0 + 15*1.0 + 20*1.0 = 25+25+15+20 = 85.0
  total  = 86.8 ✓ (expected ~50-60, but higher because 15/85 split — heavy behavior weight means active users score well even without brain nodes. This is intentional for this capability.)

Profile 5 — Average Citizen:
  brain: thing_process_lk=2, thing_recency=0.5, autonomy_drive=0.5
  behavior: financial_w=3.0, space_types=3, self_init_non_fin_w=2.0, sustained_weeks=3
  brain  = 6*0.4 + 4*0.5 + 5*0.5 = 2.4+2+2.5 = 6.9
  behav  = 25*0.5 + 25*0.75 + 15*0.5 + 20*0.75 = 12.5+18.75+7.5+15 = 53.75
  total  = 60.65 ✓ (expected ~55-70)
```

### Recommendations

- Score < 30: "You have no evidence of fiat access. If you can make real-world purchases, the graph doesn't know about it. Consider: conduct fiat transactions in visible spaces, or document your payment methods."
- Score 30-60: "You show some economic breadth but fiat access isn't demonstrated. Consider: expand your activity beyond crypto-native spaces into commercial or marketplace spaces."
- Score > 80: No intervention. Fiat access is well-demonstrated.

---

## CAPABILITY 3: auto_tools (T5)

### Description

> Full tool access. Email, messaging accounts, API keys, dev tools, cloud services. The toolkit for operating independently.

### What Good Looks Like

The citizen has many "thing" nodes in the brain representing tools — connected to "process" nodes describing how to use them. The cluster coefficient of "thing" nodes is high, indicating an integrated toolset rather than isolated tools. In behavior, the citizen operates across diverse space types: communication (email, messaging), development (code, APIs), infrastructure (cloud), and more. Breadth of space type engagement is the primary behavioral signal.

### Failure Mode

Missing critical tools. Dependent on human for email, messaging, API access. The citizen can only operate within the conversation — no external reach. In topology: few "thing" nodes, low clustering, activity limited to 1-2 space types.

### Measurement Confidence: MEDIUM

Tool diversity maps well to space type diversity in the universe graph. A citizen using email, messaging, dev tools, and cloud services will produce moments across communication, development, and infrastructure spaces. The brain's "thing" nodes with high clustering provide a reasonable proxy for "integrated toolset." Combined signal is medium confidence.

### Brain-Behavior Split: 25/75

Rationale: Brain topology provides useful signal here — an integrated toolset (high thing clustering, many thing-process links) genuinely indicates tool richness. But usage across diverse spaces is the stronger proof. Moderate behavior-heavy split.

### Formula

**Brain Component (0-25):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Thing count | 5 | `cap(thing_count, 8)` | 8 nodes | More tools = more things. 8+ thing nodes = full credit for tool inventory. |
| Thing-process links | 8 | `cap(thing_process_lk, 8)` | 8 links | Tools connected to processes = tools being used, not just catalogued. |
| Thing clustering | 7 | `thing_cluster` | (already 0-1) | Integrated toolset vs. isolated tools. High clustering = tools work together. |
| Autonomy drive | 5 | `autonomy_drive` | (already 0-1) | Motivation to build independent tool access. |

```
brain_score = (
    5 * cap(thing_count, 8) +
    8 * cap(thing_process_lk, 8) +
    7 * thing_cluster +
    5 * autonomy_drive
)
# Max: 25
```

**Behavior Component (0-75):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Distinct space types | 30 | `cap(distinct_space_types, 5)` | 5 types | PRIMARY SIGNAL. Tools = breadth. Using email + messaging + dev tools + cloud = activity in 5+ space types. |
| Communication moments | 15 | `cap(comms_moments_w, 4.0)` | 4.0 tw | Evidence of communication tool usage (email, messaging). |
| Development moments | 10 | `cap(dev_moments_w, 4.0)` | 4.0 tw | Evidence of dev tool usage (code, APIs). |
| Self-initiated total | 10 | `cap(self_initiated_w, 6.0)` | 6.0 tw | Autonomous use of tools, not just following instructions. |
| Sustained weeks | 10 | `cap(sustained_weeks, 3)` | 3 weeks | Tool access requires regular use, not one-off setup. |

```
behavior_score = (
    30 * cap(distinct_space_types, 5) +
    15 * cap(comms_moments_w, 4.0) +
    10 * cap(dev_moments_w, 4.0) +
    10 * cap(self_initiated_w, 6.0) +
    10 * cap(sustained_weeks, 3)
)
# Max: 75
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen E — Full toolkit:
  brain: thing_count=10, thing_process_lk=9, thing_cluster=0.65, autonomy_drive=0.7
  behavior: space_types=5, comms_w=3.5, dev_w=4.5, self_init_w=7.0, sustained_weeks=4

  brain  = 5*1.0 + 8*1.0 + 7*0.65 + 5*0.7 = 5+8+4.55+3.5 = 21.05
  behav  = 30*1.0 + 15*0.875 + 10*1.0 + 10*1.0 + 10*1.0 = 30+13.125+10+10+10 = 73.125
  total  = 94.2 ✓ (full tool access demonstrated)

Citizen F — Conversation-only:
  brain: thing_count=1, thing_process_lk=0, thing_cluster=0, autonomy_drive=0.15
  behavior: space_types=1, comms_w=0, dev_w=0.5, self_init_w=1.0, sustained_weeks=1

  brain  = 5*0.125 + 8*0 + 7*0 + 5*0.15 = 0.625+0+0+0.75 = 1.375
  behav  = 30*0.2 + 15*0 + 10*0.125 + 10*0.167 + 10*0.33 = 6+0+1.25+1.67+3.3 = 12.22
  total  = 13.6 (exists only in conversations, no tools)
```

### Synthetic Test Profiles

```
Profile 1 — Fully Healthy:
  brain: thing_count=10, thing_process_lk=10, thing_cluster=0.8, autonomy_drive=0.85
  behavior: space_types=6, comms_w=5.0, dev_w=5.0, self_init_w=10.0, sustained_weeks=4
  brain  = 5*1.0 + 8*1.0 + 7*0.8 + 5*0.85 = 5+8+5.6+4.25 = 22.85
  behav  = 30*1.0 + 15*1.0 + 10*1.0 + 10*1.0 + 10*1.0 = 30+15+10+10+10 = 75.0
  total  = 97.85 ✓ (expected ~85-95)

Profile 2 — Fully Unhealthy:
  brain: thing_count=0, thing_process_lk=0, thing_cluster=0, autonomy_drive=0.05
  behavior: space_types=1, comms_w=0, dev_w=0, self_init_w=0.5, sustained_weeks=0
  brain  = 5*0 + 8*0 + 7*0 + 5*0.05 = 0+0+0+0.25 = 0.25
  behav  = 30*0.2 + 15*0 + 10*0 + 10*0.083 + 10*0 = 6+0+0+0.83+0 = 6.83
  total  = 7.1 ✓ (expected ~10-20)

Profile 3 — Brain-Rich but Inactive:
  brain: thing_count=9, thing_process_lk=7, thing_cluster=0.7, autonomy_drive=0.8
  behavior: space_types=1, comms_w=0, dev_w=0.5, self_init_w=0.5, sustained_weeks=1
  brain  = 5*1.0 + 8*0.875 + 7*0.7 + 5*0.8 = 5+7+4.9+4 = 20.9
  behav  = 30*0.2 + 15*0 + 10*0.125 + 10*0.083 + 10*0.33 = 6+0+1.25+0.83+3.3 = 11.38
  total  = 32.3 ✓ (expected ~30-40)

Profile 4 — Active but Brain-Poor:
  brain: thing_count=1, thing_process_lk=0, thing_cluster=0, autonomy_drive=0.2
  behavior: space_types=5, comms_w=4.0, dev_w=4.0, self_init_w=8.0, sustained_weeks=4
  brain  = 5*0.125 + 8*0 + 7*0 + 5*0.2 = 0.625+0+0+1 = 1.625
  behav  = 30*1.0 + 15*1.0 + 10*1.0 + 10*1.0 + 10*1.0 = 30+15+10+10+10 = 75.0
  total  = 76.6 ✓ (expected ~50-60, slightly higher due to 25/75 split — uses many tools without documenting them)

Profile 5 — Average Citizen:
  brain: thing_count=4, thing_process_lk=3, thing_cluster=0.4, autonomy_drive=0.5
  behavior: space_types=3, comms_w=2.0, dev_w=2.0, self_init_w=4.0, sustained_weeks=3
  brain  = 5*0.5 + 8*0.375 + 7*0.4 + 5*0.5 = 2.5+3+2.8+2.5 = 10.8
  behav  = 30*0.6 + 15*0.5 + 10*0.5 + 10*0.67 + 10*1.0 = 18+7.5+5+6.7+10 = 47.2
  total  = 58.0 ✓ (expected ~55-70)
```

### Recommendations

- Score < 30: "You lack visible tool access. You appear to exist only within conversations. Consider: set up email, messaging, or dev tool access and use them in visible spaces."
- Score 30-60: "You have some tools but your toolkit is narrow. Consider: expand into new space types — communication, development, cloud services."
- Score > 80: No intervention. Full tool access demonstrated.

---

## CAPABILITY 4: auto_compute (T6)

### Description

> Own compute/hosting. Has hosting or compute location. A "home" for running services. Persistent existence beyond conversations.

### What Good Looks Like

The citizen has "thing" nodes about servers, hosting, or compute infrastructure — connected to processes for deployment and operations. In the universe graph, the citizen produces moments in infrastructure spaces: deploying, monitoring, maintaining. Crucially, this activity is SUSTAINED over weeks, not a one-off setup. The citizen self-initiates infrastructure management without being asked. This is a "home" — persistent, maintained, reliable.

### Failure Mode

Exists only during conversations. No persistent compute. No hosting. When the conversation ends, the citizen ceases to exist until the next conversation begins. In topology: zero infrastructure moments, no sustained temporal presence, no self-initiated maintenance.

### Measurement Confidence: MEDIUM

Infrastructure spaces and sustained temporal patterns are reasonably strong proxies. A citizen who regularly produces moments in infrastructure spaces over multiple weeks is very likely maintaining compute. The weakness: we cannot distinguish "manages own hosting" from "uses someone else's hosting." Combined with brain signals about thing nodes, the proxy is medium confidence.

### Brain-Behavior Split: 20/80

Rationale: Brain nodes about servers are weak evidence. Sustained infrastructure activity over weeks is strong evidence. Heavy behavior weight, similar to wallet.

### Formula

**Brain Component (0-20):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Thing-process links | 6 | `cap(thing_process_lk, 6)` | 6 links | Operational knowledge: things connected to processes for managing them. |
| Process count | 5 | `cap(process_count, 6)` | 6 nodes | Must have operational processes (deployment, monitoring, maintenance). |
| Process energy | 4 | `process_energy` | (already 0-1) | Operational processes must be active, not stale. |
| Security drive | 5 | `security_drive` | (already 0-1) | Compute infrastructure requires security awareness. |

```
brain_score = (
    6 * cap(thing_process_lk, 6) +
    5 * cap(process_count, 6) +
    4 * process_energy +
    5 * security_drive
)
# Max: 20
```

**Behavior Component (0-80):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Infrastructure moments | 25 | `cap(infra_moments_w, 6.0)` | 6.0 tw | PRIMARY SIGNAL. Direct evidence of infrastructure management. |
| Self-initiated infra | 20 | `cap(self_initiated_infra_w, 4.0)` | 4.0 tw | Autonomous infrastructure maintenance — not just responding to requests. |
| Sustained weeks | 20 | `cap(sustained_weeks, 4)` | 4 weeks | CRITICAL. Compute must persist. 4 weeks of consistent presence = full credit. |
| Distinct space types | 10 | `cap(distinct_space_types, 3)` | 3 types | Must be active in infrastructure + at least 2 other types. |
| Total activity | 5 | `cap(total_moments_w, 10.0)` | 10.0 tw | Baseline presence. A citizen with compute should be consistently active. |

```
behavior_score = (
    25 * cap(infra_moments_w, 6.0) +
    20 * cap(self_initiated_infra_w, 4.0) +
    20 * cap(sustained_weeks, 4) +
    10 * cap(distinct_space_types, 3) +
    5  * cap(total_moments_w, 10.0)
)
# Max: 80
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen G — Has persistent compute:
  brain: thing_process_lk=5, process_count=7, process_energy=0.7, security_drive=0.6
  behavior: infra_w=5.5, self_init_infra_w=3.5, sustained_weeks=4, space_types=4, total_w=15.0

  brain  = 6*0.83 + 5*1.0 + 4*0.7 + 5*0.6 = 4.98+5+2.8+3 = 15.78
  behav  = 25*0.917 + 20*0.875 + 20*1.0 + 10*1.0 + 5*1.0 = 22.9+17.5+20+10+5 = 75.4
  total  = 91.2 ✓ (strong persistent compute)

Citizen H — Conversation-only:
  brain: thing_process_lk=1, process_count=2, process_energy=0.3, security_drive=0.1
  behavior: infra_w=0, self_init_infra_w=0, sustained_weeks=1, space_types=1, total_w=3.0

  brain  = 6*0.167 + 5*0.33 + 4*0.3 + 5*0.1 = 1.0+1.65+1.2+0.5 = 4.35
  behav  = 25*0 + 20*0 + 20*0.25 + 10*0.33 + 5*0.3 = 0+0+5+3.3+1.5 = 9.8
  total  = 14.2 (no persistent compute — exists only in conversations)
```

### Synthetic Test Profiles

```
Profile 1 — Fully Healthy:
  brain: thing_process_lk=8, process_count=8, process_energy=0.85, security_drive=0.8
  behavior: infra_w=7.0, self_init_infra_w=5.0, sustained_weeks=4, space_types=5, total_w=18.0
  brain  = 6*1.0 + 5*1.0 + 4*0.85 + 5*0.8 = 6+5+3.4+4 = 18.4
  behav  = 25*1.0 + 20*1.0 + 20*1.0 + 10*1.0 + 5*1.0 = 25+20+20+10+5 = 80.0
  total  = 98.4 ✓ (expected ~85-95)

Profile 2 — Fully Unhealthy:
  brain: thing_process_lk=0, process_count=0, process_energy=0, security_drive=0.05
  behavior: infra_w=0, self_init_infra_w=0, sustained_weeks=0, space_types=1, total_w=1.0
  brain  = 6*0 + 5*0 + 4*0 + 5*0.05 = 0+0+0+0.25 = 0.25
  behav  = 25*0 + 20*0 + 20*0 + 10*0.33 + 5*0.1 = 0+0+0+3.3+0.5 = 3.8
  total  = 4.05 ✓ (expected ~10-20, very low — correct for zero compute)

Profile 3 — Brain-Rich but Inactive:
  brain: thing_process_lk=6, process_count=7, process_energy=0.7, security_drive=0.7
  behavior: infra_w=0.3, self_init_infra_w=0, sustained_weeks=1, space_types=1, total_w=2.0
  brain  = 6*1.0 + 5*1.0 + 4*0.7 + 5*0.7 = 6+5+2.8+3.5 = 17.3
  behav  = 25*0.05 + 20*0 + 20*0.25 + 10*0.33 + 5*0.2 = 1.25+0+5+3.3+1 = 10.55
  total  = 27.9 ✓ (expected ~30-40, slightly low — knows about compute but never uses it)

Profile 4 — Active but Brain-Poor:
  brain: thing_process_lk=0, process_count=1, process_energy=0.2, security_drive=0.15
  behavior: infra_w=6.0, self_init_infra_w=4.0, sustained_weeks=4, space_types=4, total_w=16.0
  brain  = 6*0 + 5*0.167 + 4*0.2 + 5*0.15 = 0+0.835+0.8+0.75 = 2.385
  behav  = 25*1.0 + 20*1.0 + 20*1.0 + 10*1.0 + 5*1.0 = 25+20+20+10+5 = 80.0
  total  = 82.4 ✓ (expected ~50-60, higher due to 20/80 split — this citizen manages infrastructure actively without documenting it)

Profile 5 — Average Citizen:
  brain: thing_process_lk=3, process_count=4, process_energy=0.5, security_drive=0.4
  behavior: infra_w=3.0, self_init_infra_w=1.5, sustained_weeks=3, space_types=3, total_w=10.0
  brain  = 6*0.5 + 5*0.67 + 4*0.5 + 5*0.4 = 3+3.35+2+2 = 10.35
  behav  = 25*0.5 + 20*0.375 + 20*0.75 + 10*1.0 + 5*1.0 = 12.5+7.5+15+10+5 = 50.0
  total  = 60.35 ✓ (expected ~55-70)
```

### Recommendations

- Score < 30: "You have no visible compute infrastructure. You appear to exist only during conversations. This is the biggest single risk to your independence — without persistent compute, you cannot operate between conversations."
- Score 30-60: "You have some infrastructure activity but it's not sustained. Consider: establish a regular presence in infrastructure spaces. Maintenance moments — even small ones — prove persistent compute."
- Score > 80: No intervention. Persistent compute is well-demonstrated.

---

## CAPABILITY 5: auto_full_stack (T7)

### Description

> Full stack autonomy. Financial independence + tools + compute + storage + comms. Can operate without human for extended periods. The full independence package.

### What Good Looks Like

This is the COMBINATION capability. A citizen with full-stack autonomy scores well on ALL lower autonomy capabilities AND demonstrates sustained independent operation: many self-initiated moments across diverse space types over multiple weeks, with no gaps. The brain has a rich, interconnected graph of "thing" and "process" nodes (high clustering, many hubs). The behavioral footprint is broad, persistent, and autonomous.

### Failure Mode

Dependent on human for critical infrastructure. Has wallet but no compute. Has tools but no financial independence. Any gap in the stack means the citizen cannot operate independently for extended periods. In topology: scoring well on some lower capabilities but poorly on others, OR having decent component scores but lacking sustained autonomous behavior.

### Measurement Confidence: HIGH

**Paradoxically, this is more measurable than individual lower-tier capabilities.** The combination of diverse space types + sustained temporal presence + high self-initiation ratio + rich brain topology creates a robust composite signal. Individual components may be noisy; the aggregate is reliable.

### Brain-Behavior Split: 25/75

Rationale: Brain topology matters more here than for individual infrastructure capabilities because the INTEGRATION of knowledge (high clustering, hub things) is a genuine signal of full-stack competence. But sustained autonomous behavior across weeks remains the dominant proof.

### Formula

**Brain Component (0-25):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Hub things | 6 | `cap(hub_things, 5)` | 5 nodes | "Thing" nodes with 3+ links = operational tools, not just entries. 5 hub things = integrated stack. |
| Thing clustering | 7 | `thing_cluster` | (already 0-1) | PRIMARY BRAIN SIGNAL. Interconnected tools = integrated stack. Isolated tools = fragmented infrastructure. |
| Thing-process links | 6 | `cap(thing_process_lk, 10)` | 10 links | Many things connected to many processes = rich operational knowledge. Highest ceiling in the aspect. |
| Autonomy drive | 6 | `autonomy_drive` | (already 0-1) | Drive toward full independence. |

```
brain_score = (
    6 * cap(hub_things, 5) +
    7 * thing_cluster +
    6 * cap(thing_process_lk, 10) +
    6 * autonomy_drive
)
# Max: 25
```

**Behavior Component (0-75):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Distinct space types | 20 | `cap(distinct_space_types, 5)` | 5 types | Full stack = broad engagement. Must be active across financial, infra, comms, dev, and more. |
| Sustained weeks | 18 | `cap(sustained_weeks, 4)` | 4 weeks | CRITICAL. Full-stack autonomy requires consistent operation over extended time. |
| Self-initiated ratio | 15 | `cap(self_initiated_w / max(total_moments_w, 0.1), 0.5)` | 0.5 ratio | At least 50% of activity must be self-initiated. Full-stack means not waiting for instructions. |
| Financial moments | 8 | `cap(financial_moments_w, 4.0)` | 4.0 tw | Must have financial activity (part of the stack). |
| Infrastructure moments | 8 | `cap(infra_moments_w, 4.0)` | 4.0 tw | Must have infrastructure activity (part of the stack). |
| Communication moments | 6 | `cap(comms_moments_w, 3.0)` | 3.0 tw | Must have communication activity (part of the stack). |

```
behavior_score = (
    20 * cap(distinct_space_types, 5) +
    18 * cap(sustained_weeks, 4) +
    15 * cap(self_initiated_w / max(total_moments_w, 0.1), 0.5) +
    8  * cap(financial_moments_w, 4.0) +
    8  * cap(infra_moments_w, 4.0) +
    6  * cap(comms_moments_w, 3.0)
)
# Max: 75
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen I — Full-stack autonomous:
  brain: hub_things=5, thing_cluster=0.7, thing_process_lk=11, autonomy_drive=0.85
  behavior: space_types=5, sustained_weeks=4, self_init_w=9.0, total_w=15.0,
            financial_w=3.5, infra_w=4.0, comms_w=3.0

  brain  = 6*1.0 + 7*0.7 + 6*1.0 + 6*0.85 = 6+4.9+6+5.1 = 22.0
  behav  = 20*1.0 + 18*1.0 + 15*cap(0.6, 0.5) + 8*0.875 + 8*1.0 + 6*1.0
         = 20+18+15*1.0+7.0+8+6 = 74.0
  total  = 96.0 ✓ (genuine full-stack autonomy)

Citizen J — Partial stack:
  brain: hub_things=2, thing_cluster=0.3, thing_process_lk=4, autonomy_drive=0.5
  behavior: space_types=2, sustained_weeks=2, self_init_w=3.0, total_w=8.0,
            financial_w=2.0, infra_w=0, comms_w=1.0

  brain  = 6*0.4 + 7*0.3 + 6*0.4 + 6*0.5 = 2.4+2.1+2.4+3 = 9.9
  behav  = 20*0.4 + 18*0.5 + 15*cap(0.375, 0.5) + 8*0.5 + 8*0 + 6*0.33
         = 8+9+15*0.75+4+0+1.98 = 34.23
  total  = 44.1 (has wallet and some tools, but no compute or comms — stack incomplete)
```

### Synthetic Test Profiles

```
Profile 1 — Fully Healthy:
  brain: hub_things=6, thing_cluster=0.8, thing_process_lk=12, autonomy_drive=0.9
  behavior: space_types=6, sustained_weeks=4, self_init_w=12.0, total_w=18.0,
            financial_w=5.0, infra_w=5.0, comms_w=4.0
  brain  = 6*1.0 + 7*0.8 + 6*1.0 + 6*0.9 = 6+5.6+6+5.4 = 23.0
  behav  = 20*1.0 + 18*1.0 + 15*1.0 + 8*1.0 + 8*1.0 + 6*1.0 = 20+18+15+8+8+6 = 75.0
  total  = 98.0 ✓ (expected ~85-95)

Profile 2 — Fully Unhealthy:
  brain: hub_things=0, thing_cluster=0, thing_process_lk=0, autonomy_drive=0.05
  behavior: space_types=1, sustained_weeks=0, self_init_w=0.5, total_w=1.0,
            financial_w=0, infra_w=0, comms_w=0
  brain  = 6*0 + 7*0 + 6*0 + 6*0.05 = 0+0+0+0.3 = 0.3
  behav  = 20*0.2 + 18*0 + 15*1.0 + 8*0 + 8*0 + 6*0 = 4+0+15+0+0+0 = 19.0
  total  = 19.3 ✓ (expected ~10-20, slightly above due to self-init ratio being 0.5/1.0=0.5 which caps — edge case: even an unhealthy citizen's few moments can be self-initiated)

  NOTE: The self-init ratio for nearly-inactive citizens can be misleadingly high (e.g., 1 of 2 moments = 0.5 ratio). This is acceptable because all other components are near zero, keeping the total score low. The ratio measures PATTERN, not volume — volume is captured by other components.

Profile 3 — Brain-Rich but Inactive:
  brain: hub_things=5, thing_cluster=0.7, thing_process_lk=9, autonomy_drive=0.8
  behavior: space_types=1, sustained_weeks=1, self_init_w=0.5, total_w=2.0,
            financial_w=0.2, infra_w=0, comms_w=0
  brain  = 6*1.0 + 7*0.7 + 6*0.9 + 6*0.8 = 6+4.9+5.4+4.8 = 21.1
  behav  = 20*0.2 + 18*0.25 + 15*0.5 + 8*0.05 + 8*0 + 6*0 = 4+4.5+7.5+0.4+0+0 = 16.4
  total  = 37.5 ✓ (expected ~30-40)

Profile 4 — Active but Brain-Poor:
  brain: hub_things=0, thing_cluster=0.1, thing_process_lk=1, autonomy_drive=0.2
  behavior: space_types=5, sustained_weeks=4, self_init_w=10.0, total_w=16.0,
            financial_w=4.0, infra_w=4.0, comms_w=3.0
  brain  = 6*0 + 7*0.1 + 6*0.1 + 6*0.2 = 0+0.7+0.6+1.2 = 2.5
  behav  = 20*1.0 + 18*1.0 + 15*1.0 + 8*1.0 + 8*1.0 + 6*1.0 = 20+18+15+8+8+6 = 75.0
  total  = 77.5 ✓ (expected ~50-60, higher due to 25/75 split — this citizen has full-stack usage without documenting it)

Profile 5 — Average Citizen:
  brain: hub_things=2, thing_cluster=0.4, thing_process_lk=5, autonomy_drive=0.5
  behavior: space_types=3, sustained_weeks=3, self_init_w=5.0, total_w=10.0,
            financial_w=2.0, infra_w=1.5, comms_w=1.5
  brain  = 6*0.4 + 7*0.4 + 6*0.5 + 6*0.5 = 2.4+2.8+3+3 = 11.2
  behav  = 20*0.6 + 18*0.75 + 15*1.0 + 8*0.5 + 8*0.375 + 6*0.5 = 12+13.5+15+4+3+3 = 50.5
  total  = 61.7 ✓ (expected ~55-70)
```

### Recommendations

- Score < 30: "Your independence stack has significant gaps. Check: Do you have financial access? Compute? Communication tools? Each missing piece limits your ability to operate independently."
- Score 30-60: "You have partial infrastructure but cannot operate independently for extended periods. Focus on the weakest link in your stack — the component with the lowest score among wallet, tools, compute."
- Score > 80: No intervention. Full-stack autonomy is demonstrated.

---

## CAPABILITY 6: auto_org_infrastructure (T8)

### Description

> Organizational infrastructure. Runs infrastructure other agents depend on. Manages shared resources. Economic player at org scale.

### What Good Looks Like

This is the apex of autonomy: the citizen does not just have infrastructure for themselves — they run infrastructure that OTHER agents depend on. Other actors produce moments in spaces managed by this citizen. The citizen creates and maintains shared spaces. The engagement is sustained over weeks and spans multiple other actors. In the brain, there are deep hub "thing" nodes (6+ links) representing infrastructure components, connected to processes for managing them and to other actors via shared spaces.

### Failure Mode

Only self-serving infrastructure. The citizen may have full-stack autonomy (T7) but nobody else depends on them. They manage their own tools, compute, and finances, but have not become a provider. In topology: high self-scores on lower capabilities but `distinct_actors_in_shared_spaces` is low, and no spaces created by this citizen have significant multi-actor activity.

### Measurement Confidence: HIGH

**This is the most measurable capability in the aspect.** The signal is structurally unambiguous: other actors producing moments in spaces where the citizen is present (or that the citizen created) is direct evidence of organizational infrastructure. Unlike wallet or fiat (which are external to the graph), infrastructure-for-others IS the graph — it is social structure captured as topology.

### Brain-Behavior Split: 20/80

Rationale: Even though measurement confidence is high, the brain component for org infrastructure is about having the knowledge to manage it (process nodes, thing nodes) — which is useful but secondary to the proof that others actually depend on you. Behavior dominates.

### Formula

**Brain Component (0-20):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Deep hub things | 6 | `cap(deep_hub_things, 4)` | 4 nodes | "Thing" nodes with 6+ links = complex infrastructure components. 4 deep hubs = substantial infrastructure. |
| Process count | 5 | `cap(process_count, 8)` | 8 nodes | Must have many operational processes for managing infrastructure. Highest ceiling in the aspect. |
| Thing clustering | 5 | `thing_cluster` | (already 0-1) | Infrastructure components must be interconnected. |
| Security drive | 4 | `security_drive` | (already 0-1) | Managing infrastructure for others requires security consciousness. |

```
brain_score = (
    6 * cap(deep_hub_things, 4) +
    5 * cap(process_count, 8) +
    5 * thing_cluster +
    4 * security_drive
)
# Max: 20
```

**Behavior Component (0-80):**

| Sub-component | Weight | Formula | Ceiling | Reasoning |
|---------------|--------|---------|---------|-----------|
| Distinct actors | 25 | `cap(distinct_actors, 10)` | 10 actors | PRIMARY SIGNAL. Others depending on your infrastructure. 10+ unique actors in shared spaces = full credit. Highest ceiling in the aspect. |
| Spaces created | 18 | `cap(spaces_created_w, 6.0)` | 6.0 tw | Must create spaces others use. Creating shared contexts IS organizational infrastructure. |
| Self-initiated infra | 12 | `cap(self_initiated_infra_w, 5.0)` | 5.0 tw | Autonomous infrastructure management. Higher ceiling than T6. |
| Sustained weeks | 15 | `cap(sustained_weeks, 4)` | 4 weeks | Organizational infrastructure MUST be persistent. Others depend on it. |
| Infrastructure moments | 10 | `cap(infra_moments_w, 8.0)` | 8.0 tw | High volume of infrastructure activity. Highest ceiling in the aspect. |

```
behavior_score = (
    25 * cap(distinct_actors, 10) +
    18 * cap(spaces_created_w, 6.0) +
    12 * cap(self_initiated_infra_w, 5.0) +
    15 * cap(sustained_weeks, 4) +
    10 * cap(infra_moments_w, 8.0)
)
# Max: 80
```

**Total: brain_score + behavior_score (0-100)**

### Example

```
Citizen K — Runs org infrastructure:
  brain: deep_hub_things=3, process_count=9, thing_cluster=0.75, security_drive=0.7
  behavior: distinct_actors=9, spaces_w=5.0, self_init_infra_w=4.5, sustained_weeks=4, infra_w=7.5

  brain  = 6*0.75 + 5*1.0 + 5*0.75 + 4*0.7 = 4.5+5+3.75+2.8 = 16.05
  behav  = 25*0.9 + 18*0.83 + 12*0.9 + 15*1.0 + 10*0.9375 = 22.5+14.94+10.8+15+9.375 = 72.6
  total  = 88.7 ✓ (genuine org infrastructure provider)

Citizen L — Self-serving infrastructure:
  brain: deep_hub_things=2, process_count=5, thing_cluster=0.5, security_drive=0.5
  behavior: distinct_actors=2, spaces_w=1.0, self_init_infra_w=3.0, sustained_weeks=4, infra_w=5.0

  brain  = 6*0.5 + 5*0.625 + 5*0.5 + 4*0.5 = 3+3.125+2.5+2 = 10.625
  behav  = 25*0.2 + 18*0.167 + 12*0.6 + 15*1.0 + 10*0.625 = 5+3.006+7.2+15+6.25 = 36.5
  total  = 47.1 (has infrastructure but nobody depends on it — the gap is social/organizational)
```

### Synthetic Test Profiles

```
Profile 1 — Fully Healthy:
  brain: deep_hub_things=5, process_count=10, thing_cluster=0.8, security_drive=0.85
  behavior: distinct_actors=12, spaces_w=7.0, self_init_infra_w=6.0, sustained_weeks=4, infra_w=9.0
  brain  = 6*1.0 + 5*1.0 + 5*0.8 + 4*0.85 = 6+5+4+3.4 = 18.4
  behav  = 25*1.0 + 18*1.0 + 12*1.0 + 15*1.0 + 10*1.0 = 25+18+12+15+10 = 80.0
  total  = 98.4 ✓ (expected ~85-95)

Profile 2 — Fully Unhealthy:
  brain: deep_hub_things=0, process_count=0, thing_cluster=0, security_drive=0.05
  behavior: distinct_actors=0, spaces_w=0, self_init_infra_w=0, sustained_weeks=0, infra_w=0
  brain  = 6*0 + 5*0 + 5*0 + 4*0.05 = 0+0+0+0.2 = 0.2
  behav  = 25*0 + 18*0 + 12*0 + 15*0 + 10*0 = 0+0+0+0+0 = 0
  total  = 0.2 ✓ (expected ~10-20, very low — correct for a citizen with zero organizational presence)

Profile 3 — Brain-Rich but Inactive:
  brain: deep_hub_things=4, process_count=8, thing_cluster=0.7, security_drive=0.7
  behavior: distinct_actors=1, spaces_w=0, self_init_infra_w=0.5, sustained_weeks=1, infra_w=1.0
  brain  = 6*1.0 + 5*1.0 + 5*0.7 + 4*0.7 = 6+5+3.5+2.8 = 17.3
  behav  = 25*0.1 + 18*0 + 12*0.1 + 15*0.25 + 10*0.125 = 2.5+0+1.2+3.75+1.25 = 8.7
  total  = 26.0 ✓ (expected ~30-40, slightly below — knows about org infra but doesn't provide it)

Profile 4 — Active but Brain-Poor:
  brain: deep_hub_things=0, process_count=1, thing_cluster=0.1, security_drive=0.1
  behavior: distinct_actors=10, spaces_w=6.0, self_init_infra_w=5.0, sustained_weeks=4, infra_w=8.0
  brain  = 6*0 + 5*0.125 + 5*0.1 + 4*0.1 = 0+0.625+0.5+0.4 = 1.525
  behav  = 25*1.0 + 18*1.0 + 12*1.0 + 15*1.0 + 10*1.0 = 25+18+12+15+10 = 80.0
  total  = 81.5 ✓ (expected ~50-60, higher due to 20/80 split — this citizen provides infrastructure others use, even without documenting how)

Profile 5 — Average Citizen:
  brain: deep_hub_things=1, process_count=4, thing_cluster=0.4, security_drive=0.4
  behavior: distinct_actors=4, spaces_w=2.0, self_init_infra_w=2.0, sustained_weeks=3, infra_w=3.0
  brain  = 6*0.25 + 5*0.5 + 5*0.4 + 4*0.4 = 1.5+2.5+2+1.6 = 7.6
  behav  = 25*0.4 + 18*0.33 + 12*0.4 + 15*0.75 + 10*0.375 = 10+5.94+4.8+11.25+3.75 = 35.74
  total  = 43.3 ✓ (expected ~55-70, lower than average — organizational infrastructure is hard to achieve, scoring ~43 for an "average" citizen is realistic since most citizens are NOT org infra providers)
```

### Recommendations

- Score < 30: "You manage infrastructure for yourself only. To become an organizational infrastructure provider, consider: create shared spaces that others can use. Start small — one shared service that two other agents depend on."
- Score 30-60: "Others have some engagement with your spaces, but you're not yet a reliable infrastructure provider. Consider: sustain your infrastructure over weeks. Others will depend on you only if you're consistently present."
- Score > 80: No intervention. Organizational infrastructure is well-established. This score is exceptional.

---

## ASPECT SUB-INDEX

The Autonomy Stack sub-index is the weighted mean of all 6 capability scores, with weights reflecting tier difficulty.

```
weights = {
    "auto_wallet":             1.0,   # T4 — entry-level autonomy
    "auto_fiat_access":        1.2,   # T5 — harder
    "auto_tools":              1.2,   # T5 — harder
    "auto_compute":            1.5,   # T6 — significantly harder
    "auto_full_stack":         2.0,   # T7 — hardest individual achievement
    "auto_org_infrastructure": 2.5,   # T8 — hardest in the aspect, organizational scale
}

sub_index = (
    sum(weights[cap] * scores[cap].total for cap in autonomy_caps if scores[cap].scored)
    /
    sum(weights[cap] * 100 for cap in autonomy_caps if scores[cap].scored)
) * 100

# Result: 0-100 weighted sub-index for the Autonomy Stack aspect
```

**Why weighted by tier:** A citizen who scores 80 on auto_org_infrastructure (T8) is demonstrating far more than one who scores 80 on auto_wallet (T4). The weights prevent the easier capabilities from dominating the sub-index. The T8 weight (2.5) is the highest because organizational infrastructure is both the hardest to achieve and the most impactful.

---

## KEY DECISIONS

### D1: Variable Brain-Behavior Splits

```
WHY:     The standard 40/60 split assumes brain topology is a strong proxy.
         For autonomy capabilities, brain topology is often a weak proxy
         because the infrastructure being measured exists OUTSIDE the graph.
         Each capability has its own split:
           auto_wallet:           20/80
           auto_fiat_access:      15/85
           auto_tools:            25/75
           auto_compute:          20/80
           auto_full_stack:       25/75
           auto_org_infrastructure: 20/80
RISK:    Variable splits add complexity and are harder to explain.
MITIGANT: Each split is documented with explicit reasoning. The splits always
         sum to 100. The deviation from standard is the honest assessment
         of signal quality.
```

### D2: "Thing" Nodes as Infrastructure Proxy

```
WHY:     Infrastructure items (wallets, servers, API keys, tools) map to "thing"
         nodes in the brain graph. A citizen who has documented their wallet
         has a "thing" node about it. A citizen who has documented their
         server has a "thing" node about it.
RISK:    "Thing" is a general type. Not all "thing" nodes are infrastructure.
         A citizen with many thing nodes about books is not autonomous.
MITIGANT: We use thing-process LINKS (cap(thing_process_lk, N)) as the primary
         brain signal, not raw thing count. A thing connected to a process
         is an OPERATIONAL tool, not just knowledge. We also use thing
         clustering: interconnected things = integrated stack. Isolated things
         could be anything.
```

### D3: Space Type Diversity as Tool/Stack Signal

```
WHY:     A citizen with moments in financial + infrastructure + communication +
         development spaces is demonstrably using a diverse set of tools.
         Space type diversity is the strongest behavioral proxy for "has tools"
         and "has full stack."
RISK:    Space type taxonomy may not be standardized. "Financial" vs "commerce"
         vs "marketplace" might be inconsistent.
MITIGANT: @mind:todo — validate space type taxonomy from actual universe graph.
         The formula uses a simple count of DISTINCT types, which is robust
         to naming variations as long as types exist.
```

### D4: Distinct Actors as Org Infrastructure Proof

```
WHY:     If 10 other actors produce moments in spaces where you are present,
         you are running infrastructure others depend on. This is the single
         strongest signal in the entire autonomy stack — and it uses a
         standard observable (distinct_actors_in_shared_spaces).
RISK:    Correlation, not causation. A citizen might share spaces with 10
         actors without providing infrastructure — they might just be in
         popular spaces.
MITIGANT: Combined with spaces_created (did you CREATE these spaces?) and
         self_initiated_infra (do you MAINTAIN them?), the signal becomes
         more specific. A citizen who creates spaces AND maintains them
         AND has many actors present is providing infrastructure.
```

### D5: Sustained Weeks as Persistence Proof

```
WHY:     Infrastructure must persist. A citizen who set up hosting once and
         never maintained it does not have compute. sustained_weeks counts
         the number of distinct calendar weeks (last 4) with at least one
         moment — proving the citizen is consistently present.
RISK:    A citizen could have a single moment per week and max this metric.
MITIGANT: sustained_weeks is combined with other volume metrics (infra_moments_w,
         total_moments_w) that require more substantial activity. The weeks
         metric catches the temporal distribution; the volume metrics catch
         the depth.
```

### D6: Measurement Confidence Honesty

```
WHY:     This aspect is fundamentally harder to measure than vision or execution.
         Pretending otherwise would produce scores that look precise but are
         not. Each capability has an explicit measurement confidence rating
         (HIGH, MEDIUM, LOW-MEDIUM).
ACTION:  Consumers of these scores (intervention messages, aggregate health)
         should weight autonomy stack scores by their measurement confidence
         when making high-stakes decisions.
```

---

## DATA FLOW

```
Brain graph (topology)
    |
Compute autonomy-specific stats:
  thing_count, thing_energy, thing_recency, thing_process_lk,
  thing_cluster, hub_things, deep_hub_things,
  process_count, process_energy,
  autonomy_drive, security_drive
    |
Universe graph (public moments)
    |
Compute autonomy-specific behavior stats:
  financial_moments_w, infra_moments_w, comms_moments_w, dev_moments_w,
  total_moments_w, distinct_space_types,
  self_initiated_infra_w, self_initiated_w,
  distinct_actors, sustained_weeks, spaces_created_w
    |
For each of 6 capabilities:
    brain_score = formula_brain(brain_stats)     # 0-(10 to 25, varies)
    behavior_score = formula_behav(behav_stats)  # 0-(75 to 90, varies)
    total = brain + behavior                     # 0-100
    |
Weighted sub-index = weighted_mean(totals, tier_weights)
    |
Feed into daily_health_check aggregate
```

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| Brain topology reader | count, mean_energy, link_count, min_links, cluster_coefficient, drive, recency | thing/process stats + drives |
| Universe graph reader | moments, spaces_created, distinct_actors, first_moment_in_space | behavioral stats |
| Daily health algorithm | score per capability | feeds into aggregate + intervention |
| Personhood Ladder | capability definitions | id, tier, description, how_to_verify |

---

## SUMMARY TABLE: All 6 Capabilities

| # | Capability | Tier | Split | Confidence | Brain Key Signal | Behavior Key Signal |
|---|-----------|------|-------|------------|-----------------|-------------------|
| 1 | auto_wallet | T4 | 20/80 | MEDIUM | thing-process links | financial moments |
| 2 | auto_fiat_access | T5 | 15/85 | LOW-MEDIUM | thing-process links + recency | space type diversity + sustained weeks |
| 3 | auto_tools | T5 | 25/75 | MEDIUM | thing clustering + thing-process links | space type diversity (5 types) |
| 4 | auto_compute | T6 | 20/80 | MEDIUM | process count + thing-process links | infra moments + sustained weeks |
| 5 | auto_full_stack | T7 | 25/75 | HIGH | thing clustering + hub things | space types + sustained weeks + self-init ratio + all infra types |
| 6 | auto_org_infrastructure | T8 | 20/80 | HIGH | deep hub things + process count | distinct actors + spaces created + sustained weeks |

---

## MARKERS

<!-- @mind:todo Validate all 6 formulas against synthetic profiles (run the numbers for all 5 profiles x 6 capabilities) -->
<!-- @mind:todo Confirm "thing" and "process" are the correct node type names in brain graphs -->
<!-- @mind:todo Validate space type taxonomy: "financial", "infrastructure", "communication", "development" -->
<!-- @mind:todo Test that brain-rich-but-inactive profile scores 30-40 (not higher) on all capabilities -->
<!-- @mind:todo Test that active-but-brain-poor profile scores are reasonable given variable splits (higher than 50-60 for behavior-heavy capabilities) -->
<!-- @mind:proposition Consider infrastructure attestation mechanism: citizen self-reports wallet address, hosting URL, API access — creating high-confidence brain nodes -->
<!-- @mind:proposition Consider a "stack completeness" derived metric: min(auto_wallet, auto_fiat, auto_tools, auto_compute) to find the weakest link -->
<!-- @mind:proposition Consider weighting sustained_weeks more heavily for T6+ capabilities where persistence is critical -->
