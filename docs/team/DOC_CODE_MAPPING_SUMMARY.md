# Documentation-Code Mapping System: Complete

**Status:** ✅ Ready for use
**Created:** 2025-11-16
**Author:** Mel "Bridgekeeper"

---

## What We Built

A **bidirectional traceability system** between documentation and implementation using `@` annotations.

### Key Components

1. **Annotation Format Spec** (`DOC_CODE_MAPPING_SPEC.md`)
   - How to annotate code files
   - How to annotate documentation sections
   - Vertical hierarchy (PATTERN → BEHAVIOR_SPEC → VALIDATION → MECHANISM → ALGORITHM → GUIDE → CODE)
   - Horizontal dependencies (ENABLES, REQUIRES, AFFECTS, AFFECTED_BY)

2. **Extraction Tool** (`tools/mapping/build_doc_code_map.py`)
   - Scans Python files for `@` annotations
   - Scans Markdown files for `@` annotations
   - Builds JSON map: `docs/team/doc_code_map.json`
   - Validates bidirectional consistency

3. **JSON Mapping File** (`docs/team/doc_code_map.json`)
   - Complete map of all doc-code relationships
   - Graph-ready with U4 node types
   - Guessable IDs: `{scope}@{node_type}:{path}:{element}`

---

## ID Format (Guessable!)

**Code:**
```
graphcare@U4_Code_Artifact:tools/embed_graph_nodes.py:NodeEmbedder.embed_batch
│         │                  │                          │
scope     node_type          path                       element
```

**Documentation:**
```
graphcare@U4_Knowledge_Object:docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md:embedding-strategy
│         │                    │                                              │
scope     node_type            path                                           section_anchor
```

**Benefits:**
- ✅ Predictable - you can guess the ID from file/section
- ✅ Graph-ready - includes U4 node type
- ✅ Scoped - distinguishes graphcare vs scopelock vs mindprotocol
- ✅ Human-readable - no arbitrary UUIDs

---

## How to Use

### 1. Annotate Code Files

```python
#!/usr/bin/env python3
"""
Node embedding implementation

@implements ALGORITHM:NODE_EMBEDDING
@governs_by
  PATTERN: docs/strategy/GRAPHCARE_ROLE_SPEC.md#service-3-health-monitoring
  BEHAVIOR_SPEC: docs/operations/VALIDATION_METRICS_SPEC.md#embedding-coverage
  ALGORITHM: docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md#embedding-strategy
@dependencies
  ENABLES: tools/query_semantic.py#semantic_search
  AFFECTED_BY: tools/ingestion/falkordb_ingestor_rest.py#import_graph

Author: Quinn + Kai
"""

class NodeEmbedder:
    """
    Embeds graph nodes with semantic vectors.

    @implements GUIDE:BATCH_EMBEDDING
    @governs_by
      ALGORITHM: docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md#batch-embedding
    """

    def embed_batch(self, nodes):
        pass
```

### 2. Annotate Documentation Sections

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

The embedding strategy uses...
```

### 3. Run Extraction Tool

```bash
python3 tools/mapping/build_doc_code_map.py
```

**Output:**
```
Building documentation-code map...

Scanning code files...
✓ tools/embed_graph_nodes.py: 2 mappings
Found 2 code mappings

Scanning documentation files...
✓ docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md: 1 mappings
Found 1 documentation sections

Validating map...
✓ No validation warnings

✓ Wrote map to docs/team/doc_code_map.json

Summary:
  Code mappings: 2
  Doc sections: 1
  Validation warnings: 0
```

### 4. Query Mappings

**Find what governs a code file:**
```bash
jq '.mappings[] | select(.implementation.path == "tools/embed_graph_nodes.py")' docs/team/doc_code_map.json
```

**Find what implements a doc section:**
```bash
jq '.documentation_sections[] | select(.section == "embedding-strategy")' docs/team/doc_code_map.json
```

**Detect orphan code (no governing docs):**
```bash
jq '.mappings[] | select(.governs_by | length == 0) | .id' docs/team/doc_code_map.json
```

**Detect orphan docs (no implementations):**
```bash
jq '.documentation_sections[] | select(.section_type == "ALGORITHM" or .section_type == "GUIDE") | select(.implemented_by | length == 0) | .id' docs/team/doc_code_map.json
```

---

## Validation

The tool automatically validates:

**Path existence:**
- ⚠️ References to non-existent files
- ⚠️ Broken doc paths

**Orphan detection:**
- ⚠️ Code without governing docs
- ⚠️ ALGORITHM/GUIDE docs without implementations

**Example validation output:**
```
Validation warnings (2):
⚠️  Orphan code (no governing docs): graphcare@U4_Code_Artifact:tools/legacy_tool.py
⚠️  graphcare@U4_Knowledge_Object:docs/operations/FUTURE_FEATURE.md:widget-algorithm references non-existent code: tools/widget_builder.py#WidgetBuilder
```

---

## Migration to Graph

**Current:** JSON file (`docs/team/doc_code_map.json`)

**Future:** Extract into FalkorDB graph:

```cypher
// Create documentation node
CREATE (doc:U4_Knowledge_Object {
  id: 'graphcare@U4_Knowledge_Object:docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md:embedding-strategy',
  path: 'docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md',
  section: 'embedding-strategy',
  section_type: 'ALGORITHM',
  component: 'NODE_EMBEDDING',
  scope_ref: 'graphcare'
})

// Create code node
CREATE (code:U4_Code_Artifact {
  id: 'graphcare@U4_Code_Artifact:tools/embed_graph_nodes.py:NodeEmbedder.embed_batch',
  path: 'tools/embed_graph_nodes.py',
  element: 'NodeEmbedder.embed_batch',
  scope_ref: 'graphcare'
})

// Governance relationship (doc → code)
CREATE (doc)-[:U4_GOVERNS {level: 'ALGORITHM'}]->(code)

// Dependency relationship (code → code)
MATCH (code1:U4_Code_Artifact {id: 'graphcare@U4_Code_Artifact:tools/embed_graph_nodes.py'})
MATCH (code2:U4_Code_Artifact {id: 'graphcare@U4_Code_Artifact:tools/query_semantic.py'})
CREATE (code1)-[:U4_ENABLES]->(code2)
```

---

## Integration with Health Monitoring

**This is Service 3 infrastructure:**

### Health Metrics

**Coverage:**
- % of code files with governing docs
- % of ALGORITHM/GUIDE docs with implementations

**Drift:**
- Code changes without doc updates
- Broken references (files moved/deleted)

**Coherence:**
- Bidirectional consistency (code ↔ doc both directions)
- Orphan detection

**Dashboard query:**
```bash
# Coverage score
jq '[.mappings[] | select(.governs_by | length > 0)] | length' doc_code_map.json
jq '.mappings | length' doc_code_map.json
# (annotated / total) * 100 = coverage %
```

---

## Next Steps

### Phase 1: Bootstrap (Current)
- ✅ Spec defined (`DOC_CODE_MAPPING_SPEC.md`)
- ✅ Extraction tool built (`build_doc_code_map.py`)
- ✅ JSON output working (`doc_code_map.json`)
- ✅ Validation working (path checks, orphan detection)

### Phase 2: Annotate Core Files (Next)
- ⏸️ Annotate top 10 implementation files:
  - `tools/embed_graph_nodes.py`
  - `tools/enrich_graph_properties.py`
  - `tools/query_semantic.py`
  - `tools/ingestion/falkordb_ingestor_rest.py`
  - `tools/link_code_to_docs.py`
  - (5 more core tools)

- ⏸️ Annotate corresponding doc sections:
  - `docs/operations/DOCS_AS_VIEWS_ARCHITECTURE.md`
  - `docs/operations/VALIDATION_METRICS_SPEC.md`
  - `docs/strategy/L4_PROTOCOL_ARCHITECTURE.md`

### Phase 3: Health Monitoring Integration
- ⏸️ Add coverage metric to health dashboard
- ⏸️ Add drift detection (files changed without doc updates)
- ⏸️ Add orphan alerts

### Phase 4: Graph Migration
- ⏸️ Build importer: JSON → FalkorDB graph
- ⏸️ Query mappings via Cypher
- ⏸️ Visualize doc-code relationships

---

## Files Created

| File | Purpose |
|------|---------|
| `docs/team/DOC_CODE_MAPPING_SPEC.md` | Complete annotation format specification |
| `tools/mapping/build_doc_code_map.py` | Extraction tool (parses `@` annotations) |
| `docs/team/doc_code_map.json` | Generated mapping (run tool to update) |
| `docs/team/DOC_CODE_MAPPING_SUMMARY.md` | This summary document |

---

**This system enables:**
- **Traceability:** Code → governing docs (why does this exist?)
- **Validation:** Docs → implementations (is this actually built?)
- **Drift detection:** Files change without doc updates (health degradation)
- **Onboarding:** New citizens trace from code to design rationale
- **Health monitoring:** Coverage, coherence, orphan detection metrics

**Part of GraphCare's kidney care model - infrastructure for ongoing health monitoring and drift detection.**
