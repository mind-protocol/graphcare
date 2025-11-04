# Architecture Narrative - {{client_name}}

**For:** Technical Leads, Architects, Senior Developers
**Prepared By:** Sage (Chief Documenter) + Nora (Chief Architect)
**Date:** {{preparation_date}}

---

## The Story of This System

[**SAGE WRITES:** Opening narrative - how did this system evolve?]

[Template guidance:
- Tell the architectural story, not just list facts
- How did this architecture emerge?
- What problems was it solving?
- What constraints shaped it?
- What trade-offs were made?
- Use narrative structure: setup → conflict → resolution]

**Example opening:**
> This system began as [ORIGIN_STORY]. Over time, it evolved to handle [NEW_REQUIREMENTS] which led to [ARCHITECTURAL_DECISIONS]. The current architecture reflects [PRIORITIES] while balancing [TRADEOFFS].

---

## Core Architectural Principles

[**NORA IDENTIFIES, SAGE ARTICULATES:** What principles guide this design?]

[Template guidance:
- What are the non-negotiable principles?
- Why these principles? What do they enable?
- How do they manifest in the code?
- What happens when they're violated?]

{{#each architectural_principles}}
### {{principle_number}}. {{principle_name}}

**What it means:** {{principle_description}}

**Why it matters:** {{rationale}}

**How it's enforced:** {{enforcement_mechanism}}

**Evidence in code:**
{{#each code_evidence}}
- {{evidence_description}} (see `{{file_path}}`)
{{/each}}

**Violations detected:**
{{#if violations}}
{{#each violations}}
- {{violation_description}} in `{{location}}`
  - Impact: {{impact}}
  - Recommendation: {{recommendation}}
{{/each}}
{{else}}
✅ No violations detected
{{/if}}

---

{{/each}}

## The Big Picture: How It All Fits Together

[**SAGE WRITES:** System-level narrative]

[Template guidance:
- Start with the user's journey
- Follow the data flow
- Explain how components collaborate
- Use concrete examples, not abstractions
- "When a user does X, here's what happens..."]

**Example flow:**
> When a {{user_type}} performs {{action}}, the request flows through {{component_flow}}. At each step, {{what_happens}}. The system maintains {{guarantees}} by {{mechanisms}}.

### Request Flow (Typical Use Case)

```mermaid
sequenceDiagram
    {{#each sequence_diagram_steps}}
    {{step}}
    {{/each}}
```

**Step-by-step explanation:**

{{#each flow_steps}}
{{step_number}}. **{{step_name}}**

   **Component:** {{component_name}}

   **What happens:** {{detailed_explanation}}

   **Why this design:** {{rationale}}

   **Alternatives considered:** {{alternatives}}

   **Files involved:** {{#each files}}`{{path}}`{{#unless @last}}, {{/unless}}{{/each}}

{{/each}}

---

## The Layers: Vertical Structure

[**NORA IDENTIFIES, SAGE EXPLAINS:** How is the system organized vertically?]

[Template guidance:
- Describe each layer's responsibility
- Explain dependencies between layers
- What crosses layer boundaries? How?
- What CANNOT cross layer boundaries? Why?]

{{#each layers}}
### {{layer_name}} Layer

**Responsibility:** {{responsibility_description}}

**Key Components:**
{{#each components}}
- **{{component_name}}** - {{component_description}}
{{/each}}

**Dependencies:**
- **Depends on:** {{#each dependencies}}{{layer_name}}{{#unless @last}}, {{/unless}}{{/each}}
- **Used by:** {{#each dependents}}{{layer_name}}{{#unless @last}}, {{/unless}}{{/each}}

**Communication Patterns:**
{{#each communication_patterns}}
- {{pattern_description}}
{{/each}}

**Design Rules:**
{{#each design_rules}}
- {{rule_description}}
{{/each}}

**Example Code:**
```{{language}}
{{example_code}}
```

---

{{/each}}

## The Boundaries: Horizontal Structure

[**NORA IDENTIFIES, SAGE EXPLAINS:** How is the system divided horizontally?]

[Template guidance:
- What are the major service/module boundaries?
- Why these boundaries? (Conway's law? Team structure? Domain?)
- How do they communicate?
- What are the interfaces?
- What happens at the boundaries?]

{{#each service_boundaries}}
### {{service_name}} Service

**Purpose:** {{purpose_description}}

**Responsibilities:**
{{#each responsibilities}}
- {{responsibility}}
{{/each}}

**Exposed Interface:**
{{#each api_endpoints}}
- `{{method}} {{path}}` - {{description}}
{{/each}}

**Dependencies:**
{{#if upstream_services}}
**Upstream (calls):**
{{#each upstream_services}}
- {{service_name}} - {{relationship_description}}
{{/each}}
{{/if}}

{{#if downstream_services}}
**Downstream (called by):**
{{#each downstream_services}}
- {{service_name}} - {{relationship_description}}
{{/each}}
{{/if}}

**Data Ownership:**
{{#each owned_data}}
- {{data_entity}} - {{ownership_description}}
{{/each}}

**Why this boundary exists:** {{boundary_rationale}}

---

{{/each}}

## Key Design Decisions

[**SAGE + NORA SYNTHESIZE:** What were the pivotal decisions?]

[Template guidance:
- Identify 5-7 most important architectural decisions
- For each: What was decided? Why? What alternatives existed? What are the consequences?
- Link to ADRs if they exist]

{{#each key_decisions}}
### Decision {{decision_number}}: {{decision_title}}

**Context:** {{context_description}}

**Decision:** {{what_was_decided}}

**Rationale:** {{why_this_decision}}

**Alternatives Considered:**
{{#each alternatives}}
- **{{alternative_name}}** - {{why_not_chosen}}
{{/each}}

**Consequences:**
{{#each consequences}}
- {{consequence_type}}: {{consequence_description}}
{{/each}}

**Current Status:** {{current_status}}

{{#if adr_link}}
**Full ADR:** [{{adr_title}}]({{adr_link}})
{{/if}}

---

{{/each}}

## Patterns in Action

[**SAGE EXPLAINS:** What design patterns are used and why?]

[Template guidance:
- Identify significant design patterns
- Show concrete examples from the code
- Explain why the pattern was chosen
- Show what happens when pattern is violated]

{{#each design_patterns}}
### {{pattern_name}}

**Intent:** {{pattern_intent}}

**Where it's used:**
{{#each usage_locations}}
- {{location_description}}
{{/each}}

**Example Implementation:**
```{{language}}
{{example_code}}
```

**Why this pattern here?** {{rationale}}

**Benefits realized:**
{{#each benefits}}
- {{benefit}}
{{/each}}

**Costs incurred:**
{{#each costs}}
- {{cost}}
{{/each}}

---

{{/each}}

## The Data Story

[**SAGE + NORA:** How does data flow and transform?]

[Template guidance:
- What are the core data entities?
- Where does data originate?
- How does it transform as it moves through the system?
- Where is it persisted?
- What are the consistency guarantees?]

### Core Data Entities

{{#each data_entities}}
#### {{entity_name}}

**Definition:** {{entity_description}}

**Lifecycle:**
{{#each lifecycle_stages}}
{{stage_number}}. {{stage_description}}
{{/each}}

**Transformations:**
{{#each transformations}}
- **{{from_representation}} → {{to_representation}}** at {{transformation_point}}
{{/each}}

**Persistence:**
- **Storage:** {{storage_location}}
- **Schema:** {{schema_description}}
- **Guarantees:** {{consistency_guarantees}}

---

{{/each}}

### Data Flow Diagram

```mermaid
{{data_flow_diagram}}
```

**Key Observations:**
{{#each data_flow_observations}}
- {{observation}}
{{/each}}

---

## Evolution and Technical Debt

[**SAGE HONEST ASSESSMENT:** What's the history? What's the debt?]

[Template guidance:
- How has architecture evolved?
- What decisions made sense then but not now?
- What is the technical debt?
- What are the risks of NOT paying it down?
- What would modernization look like?]

### Architectural Evolution

**Phase 1 ({{phase_1_timeline}}):** {{phase_1_description}}
- Architecture: {{phase_1_architecture}}
- Drivers: {{phase_1_drivers}}

**Phase 2 ({{phase_2_timeline}}):** {{phase_2_description}}
- Architecture: {{phase_2_architecture}}
- Drivers: {{phase_2_drivers}}

**Current Phase ({{current_timeline}}):** {{current_description}}
- Architecture: {{current_architecture}}
- Drivers: {{current_drivers}}

### Technical Debt Inventory

{{#each technical_debt}}
#### {{debt_title}}

**What is it?** {{debt_description}}

**How did it happen?** {{debt_origin}}

**Current impact:** {{current_impact}}

**Paydown strategy:** {{paydown_strategy}}

**Estimated effort:** {{effort_estimate}}

**Risk if not addressed:** {{risk_description}}

---

{{/each}}

---

## Future Architecture Vision

[**NORA PROPOSES, SAGE ARTICULATES:** Where should this go?]

[Template guidance:
- If we were starting fresh today, what would we do differently?
- What modernization paths exist?
- What are the incremental steps vs. rewrites?
- What are the risks and benefits of each path?]

### Modernization Paths

{{#each modernization_paths}}
#### Path {{path_number}}: {{path_name}}

**Vision:** {{vision_description}}

**Key Changes:**
{{#each key_changes}}
- {{change_description}}
{{/each}}

**Migration Strategy:** {{migration_strategy}}

**Estimated Timeline:** {{timeline}}

**Investment Required:** {{investment_estimate}}

**Risks:**
{{#each risks}}
- {{risk_description}}
{{/each}}

**Benefits:**
{{#each benefits}}
- {{benefit_description}}
{{/each}}

---

{{/each}}

---

## For New Architects: What You Need to Know

[**SAGE DIRECT ADVICE:** What should someone new understand?]

[Template guidance:
- What are the non-obvious things?
- What will surprise new people?
- What are the gotchas?
- What should they NOT change without understanding first?]

### Critical Knowledge

{{#each critical_knowledge}}
- **{{topic}}:** {{explanation}}
{{/each}}

### Common Misconceptions

{{#each misconceptions}}
- **Misconception:** {{wrong_belief}}
- **Reality:** {{actual_truth}}
- **Why it matters:** {{importance}}
{{/each}}

### Sacred Cows (Don't Touch Without Understanding)

{{#each sacred_cows}}
- **{{component_or_pattern}}:** {{why_sacred}} (see {{rationale_location}})
{{/each}}

---

## For More Detail

- [Auto-Generated Architecture Diagram](./tier1_architecture_overview.md)
- [Component Code Reference](./tier1_code_reference.md)
- [ADR Index](./adr_index.md)
- [Interactive Graph Explorer](https://docs.{{client_domain}}.mindprotocol.ai/graph)

---

**Authors:**
- **Nora** (Chief Architect, GraphCare) - Architecture analysis
- **Sage** (Chief Documenter, GraphCare) - Narrative synthesis

**Last Updated:** {{last_updated}}
