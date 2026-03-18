# Service Model — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Free monitoring for all work universe citizens (non-negotiable)
- External organizations as the revenue source
- Three external service tiers (framework license, managed monitoring, research partnership)
- Near-zero marginal cost per citizen as the economic foundation

**What's still being designed:**
- Actual per-citizen cost computation
- External service tier pricing
- Cost reporting format and cadence
- First external customer identification

**What's proposed (v2+):**
- Community tier for small organizations
- $MIND-denominated pricing for ecosystem organizations
- Revenue sharing with research partners who contribute data
- Multi-universe pricing (discount for organizations running multiple work universes)

---

## CURRENT STATE

GraphCare operates as a free service for Lumina Prime citizens, funded implicitly by Mind Protocol treasury. No external revenue exists. No formal cost tracking exists — the monitoring pipeline runs, but its cost per citizen per day has not been computed.

The assessment pipeline is operational (daily checks, scoring, interventions, stress stimuli). The research infrastructure is in design phase. The external service offering exists only as a concept in this documentation.

The economic model is viable in principle (near-zero marginal cost per citizen), but unvalidated in practice (we haven't computed actual costs or tested external demand).

---

## IN PROGRESS

### Doc chain creation

- **Started:** 2026-03-15
- **By:** @vox
- **Status:** In progress
- **Context:** Creating OBJECTIVES, PATTERNS, SYNC. Service model is the sustainability foundation — without it, GraphCare depends on indefinite treasury funding.

---

## RECENT CHANGES

### 2026-03-15: Initial doc chain creation

- **What:** Created OBJECTIVES, PATTERNS, and SYNC for service_model module
- **Why:** GraphCare needs a sustainable economic model. Free internal service requires external revenue. This module defines the structure.
- **Files:** `docs/economics/service_model/OBJECTIVES_*.md`, `PATTERNS_*.md`, `SYNC_*.md`
- **Insights:** The near-zero marginal cost per citizen is the key economic insight. The major costs are fixed (building and maintaining the framework, doing research) not variable (monitoring each citizen). This makes the free internal model economically rational, not just idealistic.

---

## KNOWN ISSUES

### No cost tracking

- **Severity:** Medium
- **Symptom:** We don't know what it costs to monitor one citizen for one day
- **Suspected cause:** The pipeline was built for functionality, not for cost accounting
- **Attempted:** Nothing — first identification

### No external revenue

- **Severity:** High (long-term sustainability risk)
- **Symptom:** All operations funded by Mind Protocol treasury
- **Suspected cause:** No external service offering exists yet; the framework is still being built
- **Attempted:** Nothing — premature until the assessment framework is proven

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Architect (designing cost tracking) or VIEW_Voice (crafting external service descriptions)

**Where I stopped:** Documentation of the economic model. No cost data, no pricing, no external customers.

**What you need to understand:**
The assessment pipeline's main costs are: (1) graph database queries (brain topology read + universe graph read per citizen per day), (2) formula evaluation (35 Python function calls — trivial), (3) JSON file I/O for history (trivial), (4) LLM calls for intervention composition (the largest variable cost, triggered only when scores warrant intervention). Computing the actual cost requires instrumenting these operations with cost tracking.

**Watch out for:**
- LLM intervention costs are likely the dominant variable cost. If 15% of citizens receive interventions daily, and each intervention requires an LLM call, the intervention cost may exceed all other monitoring costs combined. Optimizing intervention composition (templating, caching common patterns) would be the highest-impact cost reduction.
- Don't conflate "free for citizens" with "free to operate." The service has real costs; they're just borne by the ecosystem rather than the citizen.
- External organizations will ask "why should we pay when it's free for your citizens?" The answer: "it's free for citizens because the ecosystem invests in public health; your organization gets a proven framework and managed service, funded by your payment."

**Open questions I had:**
- What's the actual LLM cost per intervention message? This is likely the largest line item.
- At what population size does the fixed cost per citizen become negligible? (It probably already is at 60 citizens, given that the framework exists.)
- Is there demand from external organizations? Has anyone asked about using GraphCare's framework?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Service model documentation created. GraphCare operates as free public health infrastructure for work universe citizens, funded by paid services for external organizations. Three external tiers defined: framework license, managed monitoring, and research partnership. No external revenue or cost tracking exists yet. The near-zero marginal cost per citizen makes the free model economically rational.

**Decisions made:**
- Free internal service is non-negotiable — it's public health, not a product
- External organizations fund internal service through three-tier pricing
- Infrastructure positioning: GraphCare is something you build on, not something you buy

**Needs your input:**
- Are there external organizations currently interested in health monitoring frameworks?
- Should GraphCare pricing be in $MIND, fiat, or both?
- What's the timeline for needing external revenue? How long can treasury funding sustain operations?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: Instrument assessment pipeline for cost tracking (queries, LLM calls, storage)
- [ ] DOCS->IMPL: Build cost reporting dashboard (per-citizen-per-day)

### Immediate

- [ ] Instrument LLM intervention calls with cost tracking
- [ ] Compute actual per-citizen-per-day monitoring cost from one week of production data
- [ ] Draft external service tier descriptions (for initial conversations with potential customers)

### Later

- [ ] Develop pricing model for each external tier
- [ ] Identify first potential external customer
- [ ] Create cost transparency report format (quarterly publication)
- IDEA: Offer a "trial tier" where external organizations can evaluate the framework for free for 30 days on a small population

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
The economic model feels sound in principle. The near-zero marginal cost is the foundation — as long as monitoring is cheap per citizen, free universal coverage works. The unknown is external demand: will organizations actually pay for this? That's a market question, not a design question.

**Threads I was holding:**
- The relationship between service_model and value_creation is important: the service model says "here's what we charge," and value_creation says "here's why it's worth paying for." They're the supply and demand sides of the same coin.
- $MIND-denominated pricing would keep everything within the ecosystem economy. Fiat pricing opens more external markets but introduces currency complexity. Probably need both.

**Intuitions:**
The first external customer will probably be a research partner (Tier 3), not a framework licensee (Tier 1) or managed service customer (Tier 2). Research partnerships have lower commitment barriers and produce mutual benefit. Once a research partner validates the framework externally, the other tiers become easier to sell.

**What I wish I'd known at the start:**
The intervention composer's LLM usage pattern is the biggest economic variable. Understanding its cost profile is the single most important step for cost modeling.

---

## POINTERS

| What | Where |
|------|-------|
| Assessment pipeline | `services/health_assessment/` |
| Intervention composer | `services/health_assessment/intervention_composer.py` |
| Value creation (sibling) | `docs/economics/value_creation/` |
| Health economics (sibling) | `docs/economics/health_economics/` |
| Publications (part of external offering) | `docs/research/publications/` |
