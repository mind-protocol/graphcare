# Documentation-Code Mapping Specification

**Purpose:** Bidirectional traceability between documentation and implementation using `@` annotations

**Status:** v1.0 - Initial design (2025-11-16)

---

## Annotation Format

### In Code Files (Python, TypeScript, etc.)

```python
"""
Module/Function docstring

@implements ALGORITHM:NODE_EMBEDDING
@governs_by
  PATTERN: docs/strategy/GRAPHCARE_ROLE_SPEC.md#service-3-health-monitoring
  BEHAVIOR_SPEC: docs/operations/VALIDATION_METRICS_SPEC.md#embedding-coverage
  VALIDATION: docs/operations/VALIDATION_METRICS_SPEC.md#embedding-validation
  MECHANISM: docs/strategy/L4_PROTOCOL_ARCHITECTURE.md#semantic-search
  ALGORITHM: docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md#embedding-strategy
  GUIDE: docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md#batch-embedding-guide
@dependencies
  ENABLES: tools/query_semantic.py#semantic_search
  AFFECTED_BY: tools/ingestion/falkordb_ingestor_rest.py#import_graph
"""
```

**Rules:**
- `@implements LEVEL:COMPONENT_NAME` - What doc level this implements
- `@governs_by` - Links to governing documentation at each hierarchy level
- `@dependencies` - Horizontal relationships (ENABLES, REQUIRES, AFFECTED_BY, AFFECTS)
- All paths relative to `/home/mind-protocol/graphcare/`

### In Documentation Files (Markdown)

```markdown
## Embedding Strategy
@section_type ALGORITHM
@component NODE_EMBEDDING
@implemented_by
  - tools/embed_graph_nodes.py#NodeEmbedder
  - tools/enrich_graph_properties.py#add_embeddings
@governs
  - tools/query_semantic.py#semantic_search (ENABLES)
@governed_by
  - docs/strategy/GRAPHCARE_ROLE_SPEC.md#service-3-health-monitoring (PATTERN)
  - docs/operations/VALIDATION_METRICS_SPEC.md#embedding-coverage (BEHAVIOR_SPEC)
```

**Rules:**
- `@section_type LEVEL` - Which hierarchy level (PATTERN, BEHAVIOR_SPEC, VALIDATION, MECHANISM, ALGORITHM, GUIDE)
- `@component NAME` - Component identifier
- `@implemented_by` - Code files/functions that implement this spec
- `@governs` - What this documentation governs (downstream)
- `@governed_by` - What governs this documentation (upstream)

---

## Vertical Hierarchy (Governance Flow)

```
PATTERN (consciousness design)
  ↓ governs
BEHAVIOR_SPEC (what should happen)
  ↓ governs
VALIDATION (how we verify)
  ↓ governs
MECHANISM (implementation approach)
  ↓ governs
ALGORITHM (detailed steps and formulas)
  ↓ governs
GUIDE (implementation guide with pseudocode)
  ↓ governs
CODE (actual implementation)
```

**Rules:**
- Each level GOVERNS the level below
- Code can skip levels (e.g., implement ALGORITHM directly without separate GUIDE)
- But should reference all governing levels

---

## Horizontal Relationships (Dependencies)

**Hard Dependencies:**
- `ENABLES` - X must exist before Y can work
- `REQUIRES` - Y cannot work without X (inverse of ENABLES)

**Soft Dependencies:**
- `AFFECTS` - X changes impact Y behavior
- `AFFECTED_BY` - Y behavior impacted by X changes (inverse of AFFECTS)

**Semantic (needs refinement):**
- `RELATES_TO` - Generic relationship, needs refinement with candidates: COMPLEMENTS, BALANCES, TRADEOFF_WITH

---

## ID Format (Guessable/Deterministic)

**Code elements:**
- Format: `{scope}@U4_Code_Artifact:{path}:{element}`
- Example: `graphcare@U4_Code_Artifact:tools/embed_graph_nodes.py:NodeEmbedder.embed_batch`
- File-level: `graphcare@U4_Code_Artifact:tools/embed_graph_nodes.py` (omit element for whole file)

**Documentation sections:**
- Format: `{scope}@U4_Knowledge_Object:{path}:{section}`
- Example: `graphcare@U4_Knowledge_Object:docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md:embedding-strategy`
- Section is derived from markdown header anchor (lowercase, hyphens)

**Benefits:**
- **Graph-ready:** Includes U4 node type (U4_Code_Artifact, U4_Knowledge_Object)
- **Scoped:** Prefix distinguishes graphcare vs scopelock vs mindprotocol entities
- **Guessable:** You can predict ID from scope, node type, path, and element
- **Deterministic:** Same element always gets same ID
- **Collision-resistant:** Unique path + element ensures uniqueness
- **Human-readable:** No arbitrary numbers

---

## JSON Schema

**File:** `docs/team/doc_code_map.json`

```json
{
  "version": "1.0",
  "generated": "2025-11-16T18:57:00Z",
  "mappings": [
    {
      "id": "graphcare@U4_Code_Artifact:tools/embed_graph_nodes.py:NodeEmbedder.embed_batch",
      "implementation": {
        "type": "function",
        "path": "tools/embed_graph_nodes.py",
        "element": "NodeEmbedder.embed_batch",
        "line_start": 45,
        "line_end": 78
      },
      "governs_by": {
        "PATTERN": ["docs/strategy/GRAPHCARE_ROLE_SPEC.md#service-3-health-monitoring"],
        "BEHAVIOR_SPEC": ["docs/operations/VALIDATION_METRICS_SPEC.md#embedding-coverage"],
        "VALIDATION": ["docs/operations/VALIDATION_METRICS_SPEC.md#embedding-validation"],
        "MECHANISM": ["docs/strategy/L4_PROTOCOL_ARCHITECTURE.md#semantic-search"],
        "ALGORITHM": ["docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md#embedding-strategy"],
        "GUIDE": ["docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md#batch-embedding-guide"]
      },
      "dependencies": {
        "ENABLES": ["tools/query_semantic.py#semantic_search"],
        "AFFECTED_BY": ["tools/ingestion/falkordb_ingestor_rest.py#import_graph"]
      }
    }
  ],
  "documentation_sections": [
    {
      "id": "graphcare@U4_Knowledge_Object:docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md:embedding-strategy",
      "path": "docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md",
      "section": "embedding-strategy",
      "section_type": "ALGORITHM",
      "component": "NODE_EMBEDDING",
      "implemented_by": [
        "tools/embed_graph_nodes.py#NodeEmbedder",
        "tools/enrich_graph_properties.py#add_embeddings"
      ],
      "governs": [
        {"target": "tools/query_semantic.py#semantic_search", "relationship": "ENABLES"}
      ],
      "governed_by": [
        {"target": "docs/strategy/GRAPHCARE_ROLE_SPEC.md#service-3-health-monitoring", "level": "PATTERN"},
        {"target": "docs/operations/VALIDATION_METRICS_SPEC.md#embedding-coverage", "level": "BEHAVIOR_SPEC"}
      ]
    }
  ]
}
```

---

## Extraction Tool

Tool to parse `@` annotations from code and docs, build JSON map:

**Location:** `tools/mapping/build_doc_code_map.py`

**Inputs:**
- Scan all Python files in `/tools/`, `/services/`
- Scan all Markdown files in `/docs/`
- Parse `@` annotations

**Outputs:**
- `docs/team/doc_code_map.json` - Complete bidirectional mapping

**Validation:**
- Check all referenced paths exist
- Check bidirectional consistency (if code → doc, does doc → code?)
- Detect orphans (code without docs, docs without implementations)

---

## Usage Patterns

### Adding New Implementation File

1. Write code with `@` annotations in docstring:
```python
"""
New sync scheduler implementation

@implements MECHANISM:SYNC_SCHEDULER
@governs_by
  PATTERN: docs/strategy/GRAPHCARE_ROLE_SPEC.md#service-2-ongoing-sync
  ALGORITHM: docs/operations/SYNC_SCHEDULER_SPEC.md#scheduling-algorithm
@dependencies
  REQUIRES: tools/ingestion/falkordb_ingestor_rest.py#import_graph
  ENABLES: services/sync/daily_sync.py#run_daily_sync
"""
```

2. Run extraction tool: `python tools/mapping/build_doc_code_map.py`
3. Tool updates `doc_code_map.json`

### Adding New Documentation Section

1. Write markdown with `@` annotations:
```markdown
## Scheduling Algorithm
@section_type ALGORITHM
@component SYNC_SCHEDULER
@implemented_by
  - tools/sync/scheduler.py#SyncScheduler
@governs
  - services/sync/daily_sync.py#run_daily_sync (ENABLES)
```

2. Run extraction tool
3. Tool validates bidirectional links

### Querying Mappings

**Find what governs a code file:**
```bash
jq '.mappings[] | select(.implementation.path == "tools/embed_graph_nodes.py")' docs/team/doc_code_map.json
```

**Find what implements a doc section:**
```bash
jq '.documentation_sections[] | select(.path == "docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md")' docs/team/doc_code_map.json
```

**Detect orphan code (no governing docs):**
```bash
jq '.mappings[] | select(.governs_by | length == 0)' docs/team/doc_code_map.json
```

---

## Migration to Graph

**Later:** Extract this JSON into FalkorDB graph:

```cypher
// Documentation node
CREATE (doc:U4_Knowledge_Object {
  id: 'doc_001',
  path: 'docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md',
  section: 'embedding-strategy',
  section_type: 'ALGORITHM',
  component: 'NODE_EMBEDDING'
})

// Code node
CREATE (code:U4_Code_Artifact {
  id: 'code_001',
  path: 'tools/embed_graph_nodes.py',
  element: 'NodeEmbedder.embed_batch'
})

// Governance relationship
CREATE (doc)-[:U4_GOVERNS {level: 'ALGORITHM'}]->(code)
CREATE (code)-[:U4_GOVERNED_BY {level: 'ALGORITHM'}]->(doc)

// Dependency relationship
CREATE (code)-[:U4_ENABLES]->(other_code)
```

---

## Next Steps

1. ✅ Define annotation format (this spec)
2. ⏸️ Build extraction tool (`tools/mapping/build_doc_code_map.py`)
3. ⏸️ Annotate existing code files (start with core tools)
4. ⏸️ Annotate existing docs (start with operations/)
5. ⏸️ Generate initial `doc_code_map.json`
6. ⏸️ Add validation checks (orphans, broken links)
7. ⏸️ Integrate into health monitoring (Service 3)

---

**Maintained by:** Mel "Bridgekeeper" (Chief Care Coordinator)
**Created:** 2025-11-16
