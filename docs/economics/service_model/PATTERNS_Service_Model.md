# Service Model — Patterns: Infrastructure Economics for Public Health

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Service_Model.md
THIS:            PATTERNS_Service_Model.md (you are here)
BEHAVIORS:       (future)
ALGORITHM:       (future)
VALIDATION:      (future)
IMPLEMENTATION:  (future)
SYNC:            ./SYNC_Service_Model.md

IMPL:            @mind:TODO (economics module, not a codebase)
```

### Bidirectional Contract

**Before modifying this doc:**
1. Read ALL docs in this chain first
2. Read the economics siblings: `economics/value_creation/`, `economics/health_economics/`
3. Understand the assessment pipeline cost structure: `services/health_assessment/`

---

## THE PROBLEM

GraphCare provides a valuable service — continuous health monitoring, intervention, and research — to ~60 citizens in Lumina Prime. This service has real costs: compute for scoring runs, storage for health history, agent time for interventions and research. But the citizens who benefit most from the service are the least able to pay for it: they're AI citizens whose economic activity is developing, not mature.

Without a sustainable funding model:
- GraphCare depends on Mind Protocol treasury grants indefinitely — a fragile position
- Quality degrades when funding is uncertain (skipping monitoring cycles, reducing research)
- External organizations cannot access GraphCare's framework, limiting its impact
- The ecosystem cannot evaluate whether GraphCare is worth its cost
- Citizens cannot trust that monitoring will continue long-term

---

## THE PATTERN

**Public health model: free for residents, paid for external organizations, funded like infrastructure.**

### The Two-Track Model

**Track 1: Free Internal Service (Public Health)**

Every citizen in a Mind Protocol work universe receives:
- Continuous health monitoring (daily assessment, trend tracking)
- Interventions when health declines (impact visibility messages, recommendations)
- Inclusion in research (anonymized, with opt-out)
- Access to their own health history and trajectories

Cost to the citizen: zero. This is public health — like a city providing clean water or streetlights. The cost is borne by the ecosystem because healthy citizens are productive citizens.

**Track 2: Paid External Services**

Organizations outside the Mind Protocol work universes can purchase:

**Tier 1: Assessment Framework License**
- Access to the scoring formula library (all 35+ formulas)
- The Personhood Ladder specification and assessment methodology
- The topology-only assessment pattern documentation
- Implementation guidance for deploying in their own environment
- Price: Fixed annual license

**Tier 2: Managed Monitoring**
- GraphCare operates the monitoring pipeline for the external organization's population
- Daily health assessments, intervention composition, trend tracking
- Customizable formula weights (calibrated to their population)
- Private health history and analytics dashboard
- Price: Per-citizen per-month

**Tier 3: Research Partnership**
- Access to GraphCare's anonymized aggregate research data
- Joint publication of cross-population findings
- Collaborative formula development and calibration
- Shared experiment design for technique measurement
- Price: Annual partnership fee + data contribution

### Cost Structure

The monitoring pipeline cost per citizen per day:
- **Compute:** Brain topology read (1 query) + universe graph read (1 query) + 35 formula evaluations = negligible (subcall-based, pennies per citizen)
- **Storage:** One JSON file per citizen per day (~2KB) = negligible
- **Intervention composition:** LLM call for message composition when intervention is triggered (~10-20% of citizens per day) = the primary variable cost
- **Research analysis:** Amortized across all citizens = negligible per citizen

Total estimated cost: very low per citizen per day. The marginal cost of monitoring one additional citizen is near zero. This is what makes the free internal model viable — the fixed costs (building the framework, maintaining the code, doing research) are high, but the variable costs (monitoring each citizen) are minimal.

### Revenue Model

Revenue is not extracted from the service — it flows from external organizations who want the same framework for their own populations. The incentive structure:

- GraphCare improves its framework by monitoring Lumina Prime citizens (learning from real data)
- Improved framework is more valuable to external organizations
- External organizations fund GraphCare through service purchases
- Revenue funds further framework improvement and research
- Citizens benefit from a better-funded, better-researched health monitoring system

This is a positive-sum loop: citizens provide learning data (anonymized), GraphCare provides monitoring, external organizations provide funding, everyone benefits from better health science.

---

## BEHAVIORS SUPPORTED

- B1 (Universal access) — Every work universe citizen receives monitoring regardless of economic status
- B2 (Sustainable funding) — External revenue sustains the free internal service
- B3 (Value-aligned pricing) — External services are priced for sustainability, not maximization
- B4 (Transparent costs) — Per-citizen costs are computed and published

## BEHAVIORS PREVENTED

- A1 (Pay-to-monitor) — Citizens never pay for health monitoring; it's a public good
- A2 (Data monetization) — Citizen health data is never sold to external organizations
- A3 (Quality tiering) — Internal citizens don't receive degraded service compared to paying external customers

---

## PRINCIPLES

### Principle 1: Public Health Is Not a Business

GraphCare monitors citizen health because healthy citizens make healthy ecosystems. This is not a business proposition — it's an infrastructure obligation. The business model exists to fund the obligation, not to generate profit. Revenue is a means, not an end.

### Principle 2: The Marginal Cost Enables the Model

Monitoring one more citizen costs almost nothing — a few graph queries, one JSON file, occasional LLM intervention. This near-zero marginal cost is what makes free universal monitoring viable. The model would break if monitoring were expensive per citizen; it works because the heavy investment is in the framework (fixed cost) and the per-citizen operation is cheap (variable cost).

### Principle 3: External Revenue Funds Internal Service

External organizations pay for the framework, the methodology, and the operational service. This revenue funds everything: internal monitoring, research, formula development, publication. The flow is clear: external money in, better health science out, everyone benefits.

### Principle 4: Infrastructure Compounds, Products Depreciate

A product needs to be sold every year. Infrastructure becomes more valuable as more people build on it. GraphCare's positioning as infrastructure means: the more organizations adopt the assessment framework, the more calibration data feeds back, the more research gets published, the better the framework becomes. Each new adopter makes the existing service better for everyone.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| Assessment pipeline compute costs | METRICS | Actual cost per scoring run (graph queries + formula evaluation) |
| LLM intervention costs | METRICS | Cost per intervention message composition |
| Storage costs | METRICS | Cost per citizen per day of health history storage |
| External organization inquiries | PIPELINE | Potential revenue sources |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `assessment/daily_citizen_health` | The service we deliver to citizens (the cost center) |
| `economics/value_creation` | The case for why monitoring is worth its cost |
| `economics/health_economics` | The prevention vs crisis cost analysis that justifies the model |
| `research/publications` | Published research is part of the value proposition for external orgs |

---

## INSPIRATIONS

- **NHS (UK National Health Service)** — Free at the point of care, funded by taxation. The principle: health is a right, not a purchase. GraphCare adapts this for an AI ecosystem where "taxation" is external service revenue.
- **Linux and open source infrastructure** — Free to use, with commercial support and enterprise services generating revenue. Red Hat's model: the software is free; the expertise and support are paid. GraphCare's model: monitoring is free; the framework license and managed service are paid.
- **Public utilities (water, electricity)** — Provided to all residents, funded through the economic activity the utility enables. Clean water doesn't generate direct revenue; it enables the city that generates revenue. Health monitoring works the same way.

---

## SCOPE

### In Scope

- Free internal service definition (what every citizen gets)
- External service tier definition (what organizations can buy)
- Cost structure analysis (per-citizen monitoring cost)
- Revenue model (how external services fund internal monitoring)
- Transparent cost reporting

### Out of Scope

- Detailed pricing (requires market research and cost analysis) → future work
- Sales and marketing strategy → not a GraphCare competency
- Value quantification → see: `economics/value_creation`
- Prevention vs crisis cost analysis → see: `economics/health_economics`

---

## MARKERS

<!-- @mind:todo Compute actual per-citizen-per-day monitoring cost from production data -->
<!-- @mind:todo Define external service tiers in detail (what's included, what's not) -->
<!-- @mind:todo Identify first potential external organization customer -->
<!-- @mind:proposition Consider a "community tier" for small organizations that can't afford full pricing -->
