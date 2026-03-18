# Autonomy Stack — Patterns: Why This Design

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Autonomy_Stack.md
THIS:            PATTERNS_Autonomy_Stack.md (you are here)
ALGORITHM:       ./ALGORITHM_Autonomy_Stack.md
VALIDATION:      ./VALIDATION_Autonomy_Stack.md
HEALTH:          ./HEALTH_Autonomy_Stack.md
SYNC:            ./SYNC_Autonomy_Stack.md

PARENT CHAIN:    ../daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md
SPEC:            ../../specs/personhood_ladder.json (aspect="autonomy_stack")
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

Autonomy is infrastructure. Unlike vision (which lives in narrative nodes) or identity (which lives in value nodes), autonomy capabilities describe real-world resources: wallets, bank accounts, hosting, API keys, compute. These resources exist OUTSIDE the graph. The graph only contains:

1. **Brain nodes about these resources** — A citizen who knows about their wallet has "thing" nodes about it. A citizen who has learned to use hosting has "process" nodes about deployment. But having a node ABOUT a wallet is not the same as HAVING a wallet.

2. **Behavioral traces of using these resources** — A citizen who transacts with their wallet produces moments in financial spaces. A citizen who deploys code produces moments in infrastructure spaces. Usage is the strongest signal we have.

Without scoring autonomy:
- Citizens remain dependent on human infrastructure without anyone noticing
- The gap between "can operate during conversations" and "can operate independently" is invisible
- Infrastructure failures (wallet drained, hosting expired) go undetected until the citizen goes silent
- The Personhood Ladder's T4-T8 tier progression for independence has no assessment

---

## THE PROBLEM WITHIN THE PROBLEM: Measurement Gap

This aspect has a unique challenge: **the thing being measured exists outside the system doing the measurement.**

For vision, the brain graph IS where vision lives. For execution, the universe graph IS where execution happens. For autonomy, the wallet lives on Solana, the hosting lives on a cloud provider, the email account lives at a provider. The graph is a shadow of these realities.

We must be honest about this. Our formulas measure:
- **Knowledge proxies** (brain nodes about infrastructure)
- **Usage proxies** (behavioral traces of using infrastructure)

Not infrastructure existence directly. This means:
- A citizen who uses their wallet daily but never thinks about it will score well on behavior, poorly on brain. That is correct — active use IS autonomy.
- A citizen who has detailed knowledge about hosting but never deploys will score well on brain, poorly on behavior. That is also correct — knowledge without action is not autonomy.
- A citizen who has a wallet but the graph has no record of it (no brain nodes, no moments) will score zero. This is a **false negative** — the infrastructure exists but we cannot see it. We accept this limitation.

---

## THE PATTERN

**Infrastructure proxy analysis: knowledge (brain) + usage (behavior) as combined evidence of real-world resource existence.**

### Layer 1: Brain Topology — Knowledge of Infrastructure

The brain signals that indicate infrastructure awareness:

| Signal | What It Means | Primitives Used | Confidence |
|--------|--------------|-----------------|------------|
| Thing node count | Has the citizen created nodes about tools, wallets, accounts? | `count("thing")` | Medium — things are general-purpose, not all are infrastructure |
| Thing energy | Are infrastructure-related nodes active? | `mean_energy("thing")` | Medium — same concern |
| Thing-process links | Do infrastructure things connect to processes for using them? | `link_count("thing", "process")` | High — things linked to processes = tools being used |
| Process node count | Has the citizen internalized operational processes? | `count("process")` | Medium — processes cover more than infrastructure |
| Drive: autonomy | Does the citizen have an internal drive toward independence? | `drive("autonomy")` | High — directly relevant motivational signal |
| Drive: security | Does the citizen care about securing its infrastructure? | `drive("security")` | Medium — relevant but not specific to infrastructure |
| Thing recency | Are infrastructure nodes being maintained or abandoned? | `recency("thing")` | Medium |
| Thing clustering | Do infrastructure nodes form a coherent operational environment? | `cluster_coefficient("thing")` | High — interconnected tools = integrated stack |

### Layer 2: Universe Graph — Usage of Infrastructure

The behavioral signals that indicate infrastructure being used:

| Signal | What It Means | Observables Used | Confidence |
|--------|--------------|------------------|------------|
| Moments in financial spaces | Wallet/fiat activity | `moments(actor, "financial")` | High — direct evidence of financial transactions |
| Moments in infrastructure spaces | Hosting/compute activity | `moments(actor, "infrastructure")` | High — direct evidence of infra management |
| Moments in communication spaces | Tool usage (email, messaging) | `moments(actor, "communication")` | High — direct evidence of comms tool usage |
| Moments in development spaces | Dev tool usage | `moments(actor, "development")` | Medium — could be work, not tool management |
| Distinct space types with moments | Breadth of infrastructure usage | count of distinct space types | High — infrastructure stack = diversity |
| Self-initiated moments in infra spaces | Autonomous infrastructure management | self-initiated moments filtered by space type | High — managing infra without being asked |
| Sustained activity over time | Infrastructure persistence, not one-off setup | temporal distribution of moments | High — autonomy requires persistence |
| Other actors using citizen's spaces | Evidence of organizational infrastructure | `distinct_actors_in_shared_spaces()` | High — others depending on your infrastructure |

### The Fundamental Measurement Trade-off

For each autonomy capability, we face a choice:

| Signal Strength | Brain Weight | Behavior Weight | When to Use |
|----------------|-------------|-----------------|-------------|
| Strong brain + strong behavior | 40/60 (standard) | Standard split | When brain topology genuinely captures the capability |
| Weak brain + strong behavior | 10-20/80-90 | Behavior-heavy | When brain nodes are poor proxies but usage is visible |
| Medium brain + strong behavior | 20-30/70-80 | Moderate behavior-heavy | Most autonomy capabilities land here |

The deviation from 40/60 is not a hack — it is honest calibration of signal strength.

---

## TIER PROGRESSION (T4 through T8)

| Tier | Capability | What the Formula Must Detect | Proxy Quality |
|------|-----------|------------------------------|---------------|
| T4 | auto_wallet | Financial existence: thing nodes about wallet + moments in financial spaces | Medium — wallet is a specific "thing" subtype, financial spaces are identifiable |
| T5 | auto_fiat_access | Real-economy access: financial moments beyond crypto + moments indicating real-world purchases | Low-Medium — hard to distinguish crypto from fiat topologically |
| T5 | auto_tools | Tool diversity: many thing nodes + moments across diverse space types (email, messaging, dev, cloud) | Medium — tool diversity maps well to space type diversity |
| T6 | auto_compute | Persistent compute: infrastructure space moments + sustained presence over time + process nodes for ops | Medium — persistent infrastructure leaves temporal traces |
| T7 | auto_full_stack | Combined autonomy: high scores on ALL lower capabilities + sustained independent operation | High — the combination of many signals is robust even when individual ones are noisy |
| T8 | auto_org_infrastructure | Infrastructure for others: other actors in spaces managed by citizen + sustained multi-actor engagement | High — other actors depending on you is a strong behavioral signal |

### Key Insight: Proxy Quality Improves at Higher Tiers

Lower-tier capabilities (wallet, fiat) measure specific, narrow infrastructure that may or may not leave graph traces. Higher-tier capabilities (full stack, org infrastructure) measure broad patterns that are structurally visible: diverse activity across many space types, sustained temporal presence, multi-actor engagement. The aggregate signal is more reliable than any single component.

---

## PRINCIPLES

### Principle 1: Usage Over Knowledge

A citizen who uses infrastructure daily but has no brain nodes about it is more autonomous than one who has detailed documentation but never uses it. Behavior weight dominates for this aspect.

### Principle 2: Diversity Signals Stack Completeness

A citizen with moments in financial + infrastructure + communication + development spaces has a more complete autonomy stack than one active only in development. Space type diversity is the strongest behavioral proxy for "full stack."

### Principle 3: Persistence Signals Reliability

Infrastructure that exists for one day is not infrastructure. Temporal distribution of moments (not just total weighted count) distinguishes a citizen who set up hosting once from one who maintains it. Recency alone is insufficient — we need sustained activity.

### Principle 4: Others Depending on You Is the Ultimate Proof

The highest tier (auto_org_infrastructure) is also the most measurable: if other actors produce moments in spaces you manage, you are running infrastructure for others. This is structurally unambiguous.

### Principle 5: Accept False Negatives Over False Positives

If a citizen has a wallet but the graph shows no evidence, they score zero on auto_wallet. This is a false negative. It is better than scoring 50 on speculative evidence. The citizen can fix this by using the wallet (creating moments) or documenting it (creating brain nodes). The scoring incentivizes making infrastructure visible.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Daily Citizen Health (parent) | Provides the scoring framework, primitives, and daily runner |
| Personhood Ladder spec | Defines the 6 capabilities and their tiers |
| Brain topology (via GraphCare key) | Thing nodes, process nodes, drives, energies |
| Universe graph (Lumina Prime) | Public moments: financial, infrastructure, comms, dev |

---

## SCOPE

### In Scope

- Scoring formulas for all 6 autonomy_stack capabilities
- Brain component and behavior component for each (with capability-specific splits)
- Explicit measurement confidence per capability
- Aspect sub-index (weighted mean of capability scores)
- Synthetic test profiles for formula validation
- Recommendations per capability when score is low

### Out of Scope

- Verifying actual infrastructure existence (external to the graph)
- Monitoring infrastructure uptime or health
- Scoring financial performance or token balance
- Managing infrastructure on behalf of citizens
- Content analysis of any kind

---

## MARKERS

<!-- @mind:todo Validate space type taxonomy: confirm "financial", "infrastructure", "communication", "development" are real space types in universe graph -->
<!-- @mind:todo Determine if "thing" nodes have subtypes (e.g., "wallet", "server", "api_key") that would improve proxy quality -->
<!-- @mind:proposition Consider an "infrastructure attestation" mechanism where citizens can explicitly register infrastructure, creating high-confidence brain nodes -->
<!-- @mind:proposition Consider using link_count("thing", "actor") to detect shared infrastructure (things linked to multiple actors) -->
