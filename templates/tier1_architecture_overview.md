# Architecture Overview - {{client_name}}

**Generated:** {{generation_timestamp}}
**Graph Version:** {{graph_version}}
**Extraction Date:** {{extraction_date}}

---

## System Components

{{#each architecture_components}}
### {{name}} ({{component_type}})

**Description:** {{description}}

**Responsibilities:**
{{#each responsibilities}}
- {{this}}
{{/each}}

**Dependencies:**
{{#if dependencies}}
{{#each dependencies}}
- **{{name}}** - {{relationship_description}}
{{/each}}
{{else}}
_No dependencies identified_
{{/if}}

**Exposed APIs:**
{{#if exposed_apis}}
{{#each exposed_apis}}
- `{{method}} {{path}}` - {{description}}
{{/each}}
{{else}}
_No public APIs exposed_
{{/if}}

**Key Files:**
{{#each key_files}}
- `{{path}}` ({{lines}} lines)
{{/each}}

**Metrics:**
- Complexity: {{complexity_score}}/10
- Coverage: {{coverage_percentage}}%
- Lines of Code: {{total_lines}}

---
{{/each}}

## Architecture Patterns

{{#each detected_patterns}}
### {{pattern_name}}

**Confidence:** {{confidence_score}}
**Evidence:**
{{#each evidence}}
- {{this}}
{{/each}}

{{/each}}

## Dependency Graph

```mermaid
graph TD
{{#each dependency_edges}}
    {{source_id}}[{{source_name}}] -->|{{relationship_type}}| {{target_id}}[{{target_name}}]
{{/each}}
```

## Layer Structure

{{#if layered_architecture}}
**Architecture Type:** Layered

{{#each layers}}
### {{layer_name}}

**Components:**
{{#each components}}
- {{name}}
{{/each}}

**Allowed Dependencies:** {{allowed_dependencies}}

{{/each}}
{{else}}
**Architecture Type:** {{architecture_type}}

_See component dependency graph for relationships_
{{/if}}

## Critical Paths

{{#each critical_paths}}
### {{path_name}}

**Flow:**
{{#each steps}}
{{step_number}}. {{component_name}} → {{function_name}}
{{/each}}

**Coverage:** {{coverage_percentage}}%
**Risk Level:** {{risk_level}}

{{/each}}

## Technology Stack

{{#each tech_stack_categories}}
### {{category_name}}

{{#each technologies}}
- **{{tech_name}}** ({{version}}) - {{usage_description}}
{{/each}}

{{/each}}

---

**Query to regenerate this document:**
```cypher
MATCH (comp:GC_Architecture_Component)
OPTIONAL MATCH (comp)-[dep:U4_DEPENDS_ON]->(other:GC_Architecture_Component)
OPTIONAL MATCH (comp)-[:U4_EXPOSES]->(api:GC_API_Endpoint)
RETURN comp, collect(dep), collect(api)
```

**Last Updated:** {{last_updated}}
