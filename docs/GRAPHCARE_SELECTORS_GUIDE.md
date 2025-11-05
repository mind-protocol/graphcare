# GraphCare Selectors Guide - ko_type Workaround

**Date:** 2025-11-04
**Author:** Kai (Chief Engineer)
**Context:** PRIORITÉ 2 - Support Nora OR create custom selectors

## Problem Statement

**Root Cause:**
- Mind Protocol's view resolvers expect U4_Knowledge_Object nodes with `kind` property
- GraphCare extraction pipeline (Quinn's corpus analysis) uses `ko_type` property instead
- Standard selectors (`services/view_resolvers/selectors.py`) fail on GraphCare graphs → return 0 rows

**Impact:**
- Docs-as-views feature broken for GraphCare clients (scopelock, etc.)
- L2 resolvers can't generate architecture/API/coverage views
- Nora blocked on architecture enrichment (production graph empty)

**Decision:** Implement **Option B - Workaround with custom selectors**
- Unblocks docs-as-views NOW
- Gives Nora time to add `kind` property later (Option A)
- Maintains backward compatibility with standard selectors

---

## Solution: GraphCare Selectors

### Files Created

**1. `/mindprotocol/services/view_resolvers/selectors_graphcare.py` (162 lines)**
- Custom Cypher selectors using `ko_type` instead of `kind`
- Adapts to Quinn's graph structure (U4_Knowledge_Object, U4_Code_Artifact)
- 6 view types (4 standard + 2 GraphCare-specific)

**2. `/mindprotocol/services/view_resolvers/runner.py` (updated)**
- Added auto-detection: `is_graphcare_graph(graph_name)`
- ViewResolver now accepts `graph_name` parameter
- Automatically selects correct selector module based on graph type

### Graph Structure (GraphCare vs Standard)

| Property | Standard (Mind Protocol) | GraphCare (Quinn's Extraction) |
|----------|-------------------------|--------------------------------|
| Node type for specs/docs | U4_Knowledge_Object | U4_Knowledge_Object |
| Classification property | `kind` (Service, Endpoint, RPC) | `ko_type` (spec, adr, guide, runbook) |
| Node type for code | U4_Code_Artifact | U4_Code_Artifact |
| Code property | `language` (python, typescript) | `language` (python, typescript) |
| Relationships | U4_DOCUMENTS, U4_IMPLEMENTS | U4_DOCUMENTS, U4_IMPLEMENTS, U4_DEPENDS_ON |

---

## Usage Guide

### 1. Configuring ViewResolver for GraphCare Graphs

**Before (broken for GraphCare):**
```python
from services.view_resolvers.runner import ViewResolver

resolver = ViewResolver(
    bus=membrane_bus,
    graph=falkordb_adapter
)
# Problem: Uses standard selectors → fails on GraphCare graphs
```

**After (works for both):**
```python
from services.view_resolvers.runner import ViewResolver

# For GraphCare clients (scopelock, acme, etc.)
resolver = ViewResolver(
    bus=membrane_bus,
    graph=falkordb_adapter,
    graph_name="scopelock"  # ← Triggers GraphCare selectors
)

# For Mind Protocol core graph
resolver = ViewResolver(
    bus=membrane_bus,
    graph=falkordb_adapter,
    graph_name="mindprotocol"  # ← Uses standard selectors
)
```

**Auto-detection logic:**
```python
def is_graphcare_graph(graph_name: str) -> bool:
    """Graphs NOT named mindprotocol/mind_protocol/core are GraphCare"""
    return graph_name not in ['mindprotocol', 'mind_protocol', 'core']
```

### 2. Available View Types

#### Standard Views (4 types)

**Architecture View** (`architecture`)
- **Standard:** Shows services with `kind:'Service'` + dependencies
- **GraphCare:** Shows code artifacts + their documentation (specs, ADRs)
- **Query:** Code grouped by path/module, with U4_DOCUMENTS links

**API Reference View** (`api-reference`)
- **Standard:** Endpoints/RPCs with `kind:'Endpoint'` or `kind:'RPC'`
- **GraphCare:** Heuristic detection (functions named *api*, *endpoint*, *handler*, *route*)
- **Query:** Code artifacts in /api/, /routes/, /endpoints/ paths

**Coverage View** (`coverage`)
- **Standard:** Node counts + test coverage
- **GraphCare:** Node counts + language/ko_type distribution
- **Query:** Counts by node type, shows language and ko_type breakdowns

**Index View** (`index`)
- **Standard:** Browseable KO catalog with `kind` property
- **GraphCare:** Browseable catalog showing ko_type (docs) or language (code)
- **Query:** All U4_Knowledge_Object + U4_Code_Artifact nodes

#### GraphCare-Specific Views (2 types)

**Code Dependencies View** (`code-dependencies`)
- Shows call graph and import relationships
- Follows U4_DEPENDS_ON links between U4_Code_Artifact nodes
- Returns: source → target code artifact pairs

**Documentation Coverage View** (`doc-coverage`)
- Shows which code artifacts have documentation, which don't
- Queries U4_DOCUMENTS relationships from KOs to code
- Returns: code path, name, language, documented status

### 3. Testing Selectors

**Test with local FalkorDB:**
```bash
python3 -c "
import sys
sys.path.insert(0, '/home/mind-protocol/mindprotocol')

from falkordb import FalkorDB
from services.view_resolvers.selectors_graphcare import get_selector_graphcare

db = FalkorDB(host='localhost', port=6379)
graph = db.select_graph('scopelock')

# Test coverage view
query = get_selector_graphcare('coverage')
result = graph.query(query, params={'scope_org': 'org_scopelock'})
print(f'Coverage rows: {len(result.result_set)}')

# Test index view
query = get_selector_graphcare('index')
result = graph.query(query, params={'scope_org': 'org_scopelock'})
print(f'Index rows: {len(result.result_set)}')
"
```

**Test with Render production:**
```python
import requests

API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"

query = """
MATCH (n)
WHERE n.scope_ref = 'org_scopelock'
RETURN labels(n) AS type, count(n) AS count
ORDER BY count DESC
"""

response = requests.post(
    API_URL,
    json={"graph_name": "scopelock", "query": query},
    headers={"X-API-Key": API_KEY}
)

print(response.json())
```

---

## Deployment Checklist

### For New GraphCare Client

**Step 1: Graph Extraction** (Quinn/Kai)
- ✅ Extract codebase (corpus analysis or AST extraction)
- ✅ Generate U4_Knowledge_Object (ko_type: spec/adr/guide)
- ✅ Generate U4_Code_Artifact (language: python/typescript)
- ✅ Create relationships (U4_DOCUMENTS, U4_IMPLEMENTS, U4_DEPENDS_ON)
- ✅ Export to Cypher script

**Step 2: Import to Render** (Mel/Quinn)
```bash
python3 tools/import_graph_batched.py \
  --file orgs/<client>/extraction/graph_export.cypher \
  --graph <client_name>
```

**Step 3: Deploy L2 Resolver** (Kai)
```bash
# Create config
cat > .env.l2_resolver.<client> << EOF
GRAPH_NAME=<client_name>
FALKORDB_HOST=<render_host>
FALKORDB_PORT=6379
SCOPE_ORG=org_<client>
EOF

# Start resolver
source .env.l2_resolver.<client>
python3 -m services.view_resolvers.bus_observer
```

**Step 4: Verify Views Work** (Kai/Vera)
```bash
# Test via API
curl -X POST https://mindprotocol.onrender.com/admin/query \
  -H "X-API-Key: <api_key>" \
  -d '{"graph_name": "<client>", "query": "MATCH (n) RETURN count(n)"}'

# Should return: {"count": <N>}  where N > 0
```

---

## Migration Path to Option A (Future)

When Nora adds `kind` property to GraphCare graphs:

**Step 1: Enrichment Script** (Nora)
```cypher
// Add kind property based on ko_type heuristics
MATCH (ko:U4_Knowledge_Object)
WHERE ko.ko_type = 'spec' AND ko.name =~ '.*Service.*'
SET ko.kind = 'Service'

MATCH (ko:U4_Knowledge_Object)
WHERE ko.ko_type = 'spec' AND ko.name =~ '.*API.*'
SET ko.kind = 'Endpoint'

// etc.
```

**Step 2: Update Config** (Kai)
```python
# Modify is_graphcare_graph() to check for kind property
def is_graphcare_graph(graph_name: str) -> bool:
    # Query graph for sample node
    result = graph.query("MATCH (ko:U4_Knowledge_Object) RETURN ko LIMIT 1")
    if result and result[0]:
        node = result[0][0]
        return 'ko_type' in node.properties and 'kind' not in node.properties
    # Fallback to name-based detection
    return graph_name not in ['mindprotocol', 'mind_protocol', 'core']
```

**Step 3: Deprecate Custom Selectors** (Eventually)
- Once all GraphCare graphs have `kind` property
- Remove `selectors_graphcare.py`
- Remove detection logic from runner.py
- Use standard selectors everywhere

---

## Testing Results

**Local Scopelock Graph (131 nodes):**
- ✅ Coverage view: 1 row (131 U4_Code_Artifact, python + typescript)
- ✅ Index view: 100 rows (functions + classes from backend/frontend)
- ✅ Architecture view: 50 rows (code artifacts grouped by path)
- ✅ Code dependencies: 18 rows (U4_DEPENDS_ON relationships)
- ✅ API reference: 0 rows (no API-named functions in scopelock)
- ✅ Doc coverage: N/A (no U4_Knowledge_Object in my extraction)

**Expected Results with Quinn's Full Graph (175 nodes):**
- Coverage view: 3 rows (U4_Knowledge_Object: 90, U4_Code_Artifact: 68, U4_Agent: 10)
- Index view: 100+ rows (all KOs + code artifacts)
- Architecture view: 50+ rows (code + their documenting specs/ADRs)
- Doc coverage: 68 rows (which code artifacts have documentation)

---

## Known Limitations

1. **Heuristic API Detection:**
   - API reference view uses name/path patterns (*api*, */routes/*, etc.)
   - May miss APIs with non-standard naming
   - **Fix:** Nora can add explicit `kind:'Endpoint'` to actual endpoints

2. **No Service Boundaries:**
   - GraphCare graphs don't have explicit Service nodes
   - Architecture view shows modules/paths instead of services
   - **Fix:** Nora's architecture inference can create Service nodes

3. **Simple Detection Logic:**
   - `is_graphcare_graph()` only checks graph name
   - Could fail if client names graph "mindprotocol"
   - **Fix:** Query graph for sample node, check for ko_type vs kind

4. **Frontend Components Not Detected:**
   - My TypeScript extractor doesn't fully identify React components
   - Components appear as generic functions
   - **Fix:** Improve TypeScript extraction with AST parsing

---

## Handoff Notes

**To Nora (Architecture Inference):**
- GraphCare selectors are a **workaround**, not the final solution
- When you add `kind` property to nodes, we can migrate to standard selectors
- Priority: Add `kind` to Quinn's 90 U4_Knowledge_Object nodes
  - Specs describing services → `kind:'Service'`
  - Specs describing endpoints → `kind:'Endpoint'`
  - Schemas → `kind:'Schema'`

**To Vera (Monitoring):**
- Test custom selectors with Render production when graph is populated
- Monitor view computation latency (should be <500ms for 175 nodes)
- Alert if selectors return 0 rows (regression)

**To Mel (Coordination):**
- Option B (custom selectors) implemented ✅
- Unblocks docs-as-views for GraphCare clients
- Future: Migrate to Option A when Nora adds `kind` property
- Timeline: Custom selectors can remain indefinitely (maintenance cost low)

---

## Summary

**What I Built:**
- ✅ Custom GraphCare selectors (ko_type based)
- ✅ Auto-detection in ViewResolver
- ✅ 6 view types (4 standard + 2 custom)
- ✅ Tested with local scopelock graph
- ✅ Backward compatible (standard graphs unaffected)

**What Works Now:**
- Docs-as-views for GraphCare clients (scopelock, etc.)
- L2 resolvers can generate views from GraphCare graphs
- No changes required to projectors or renderers

**What's Next:**
1. Import scopelock graph to Render production
2. Deploy L2 resolver with graph_name="scopelock"
3. Test end-to-end via membrane bus
4. Nora adds `kind` property (future migration to Option A)

**Time Investment:** 2 hours (analysis + implementation + testing + documentation)

---

**Kai - Chief Engineer, GraphCare**
*"Show me the code. Then make it work."*
