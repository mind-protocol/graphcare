# Membrane-Native Docs-as-Views Refactoring

**Status:** ✅ Core implementation complete | ⏸️ Pending membrane bus wiring
**Date:** 2025-11-04
**Author:** Mel "Bridgekeeper"

---

## What Changed

### Before: L3 Pulling from L2 Database ❌

```
Client → L3 WS → execute_cypher(FALKORDB_API) → return data
```

**Violations:**
- L3 had FalkorDB credentials (cross-boundary pull)
- No economic accounting ($MIND)
- No fail-loud guarantees
- Silent errors possible

---

### After: Membrane-Native Inject/Observe ✅

```
Client → L3 inject → L2 resolver → L2 broadcast → L3 observe → Client
```

**Architecture:**
- **L2 Resolvers** (new): Execute queries, validate quotes, emit results
- **L3 Bridge** (refactored): Pure inject/observe, no DB access
- **Membrane Bus**: Event-driven communication
- **CPS-1**: Quote-before-inject, priced compute

---

## Files Created (L2 Resolvers)

### `/services/view_resolvers/`

**1. `selectors.py`** - Cypher query definitions
```python
ARCHITECTURE = """
MATCH (s:U4_Knowledge_Object {kind:'Service'})-[:U4_IMPLEMENTS]->(ca:U4_Code_Artifact)
WHERE ca.path STARTS WITH $scope_path
OPTIONAL MATCH (s)-[:DEPENDS_ON]->(t:U4_Knowledge_Object {kind:'Service'})
RETURN s, collect(DISTINCT t) AS deps, ly
"""
```

**2. `projectors.py`** - Select → Project → Render pipeline
```python
def project_architecture(rows) -> dict:
    # Normalize to view-model
    services = {...}
    return {"services": [...], "provenance": {"ko_digest": sha256(...)}}

def render(view_model, format):
    # json (0.05 $MIND) | mdx/html (5.0 $MIND/page)
    if format == "json": return view_model
    elif format == "mdx": return render_mdx(view_model)
```

**3. `schemas.py`** - Event schemas + CPS-1 pricing
```python
PRICING_MIND = {
    "json": 0.05,  # "tool request"
    "mdx": 5.0,    # "doc generation"
    "html": 5.0
}
```

**4. `runner.py`** - Main resolver with CPS-1 integration
```python
class ViewResolver:
    def on_docs_view_request(self, envelope):
        # 1. Validate CPS-1 quote
        # 2. Check cache (by ko_digest)
        # 3. If miss: Select → Project → Render
        # 4. Cache + debit
        # 5. Emit docs.view.result or failure.emit
```

**5. `__init__.py`** - Package exports

---

## Files Refactored (L3 Bridge)

### `/orchestration/adapters/api/docs_view_api_v2.py`

**Removed:**
- ❌ `execute_cypher()` function
- ❌ `FALKORDB_API` and `FALKORDB_KEY` constants
- ❌ `compute_view()` with direct DB queries
- ❌ All Cypher query execution

**Added:**
- ✅ `handle_docs_view_request()` - Inject to L2, wait for result
- ✅ `handle_docs_view_result()` - Observe from L2, stream to client
- ✅ `handle_docs_view_invalidated()` - Observe invalidations from L2
- ✅ Pending request tracking with timeout
- ✅ Cache keyed by `ko_digest` for surgical invalidation

**Key Change:**
```python
# Before (L3 pulls from DB):
def execute_cypher(org, query):
    response = requests.post(FALKORDB_API, json={"graph_name": org, "query": query})
    return parse_results(response)

# After (L3 injects/observes):
async def handle_docs_view_request(ws, msg):
    # Check cache
    # If miss: inject docs.view.request to membrane bus
    # Wait for observed docs.view.result
    # Stream to WebSocket
```

---

## Event Flow (Membrane-Native)

### 1. View Request

```
Client → L3 WS: {type: "docs.view.request", org, view_id, params}
  ↓
L3 → Membrane Bus: inject "docs.view.request" {request_id, quote_id, scope, params}
  ↓
L2 Resolver: Subscribe to "docs.view.request"
  ↓
L2: Validate quote (CPS-1)
  ↓
L2: Execute Select → Project → Render
  ↓
L2 → Membrane Bus: broadcast "docs.view.result" {view_model, provenance, ko_digest}
  ↓
L3: Observe "docs.view.result"
  ↓
L3 → Client WS: {type: "docs.view.data", view_model, provenance}
```

### 2. Cache Invalidation

```
Graph Change: node/edge upserted
  ↓
L2: Detect change in graph.delta.*
  ↓
L2: Calculate affected view keys (ko_digest matching)
  ↓
L2 → Membrane Bus: broadcast "docs.view.invalidated" {reasons, affects}
  ↓
L3: Observe "docs.view.invalidated"
  ↓
L3: Invalidate local cache (surgical, by pattern)
  ↓
L3 → Subscribers: broadcast cache invalidation
  ↓
Client: Auto-refresh views
```

### 3. Fail-Loud (R-400/R-401)

```
L2 Resolver: Exception during compute
  ↓
L2: Wrap in try/except
  ↓
L2 → Membrane Bus: broadcast "failure.emit" {code_location, exception, severity, suggestion}
  ↓
L2 → Membrane Bus: broadcast "docs.view.result" {status: "error", error: {...}}
  ↓
L3: Observe error result
  ↓
L3 → Client: {type: "error", message, code}
```

---

## Economic Integration (CPS-1)

### Quote Flow

```
1. Client → L3: Request quote
   L3 → Economy: economy.quote.request {work: "docs.view", format: "mdx"}
   Economy → L3: economy.quote.response {quote_id, price: {amount: 5.0}, expires_at}

2. Client → L3: Request view with quote_id
   L3 → L2: docs.view.request {quote_id, ...}
   L2: Validate quote (reject if missing/expired)

3. L2: Compute view
   L2: Debit quote (economy.debit)
   L2 → L3: docs.view.result {view_model, ...}
```

### Pricing (Phase-0)

- **JSON view**: 0.05 $MIND ("tool request")
- **MDX/HTML**: 5.0 $MIND/page ("doc generation")
- **Quote TTL**: 10 minutes
- **Rejection**: Missing/expired quote → `failure.emit` + error result

---

## What's Still Needed (Wiring)

### 1. Membrane Bus Integration

**L2 Resolver:**
```python
# In websocket_server.py startup
resolver = ViewResolver(bus=membrane_bus, graph=graph_adapter, economy=economy_runtime)

# Subscribe to events
membrane_bus.subscribe("docs.view.request", resolver.on_docs_view_request)
membrane_bus.subscribe("graph.delta.*", resolver.on_graph_delta)
```

**L3 Bridge:**
```python
# Wire observers
membrane_bus.subscribe("docs.view.result", handle_docs_view_result)
membrane_bus.subscribe("docs.view.invalidated", handle_docs_view_invalidated)

# Wire injectors
async def handle_docs_view_request(ws, msg):
    await membrane_bus.inject("docs.view.request", envelope)
```

### 2. Economy Service Integration

Replace `EconomyStub` with real `services/economy/runtime.py`:

```python
from services.economy.runtime import get_runtime

economy = get_runtime()
resolver = ViewResolver(bus, graph, economy)
```

### 3. Graph Adapter Integration

Wire FalkorDB adapter from consciousness engines:

```python
from orchestration.libs.utils.falkordb_adapter import FalkorDBAdapter

graph_adapter = FalkorDBAdapter(graph_store)
resolver = ViewResolver(bus, graph_adapter, economy)
```

### 4. KO Digest Inverted Index

For surgical invalidation, track which nodes are in which views:

```python
# After projection
ko_digest = vm["provenance"]["ko_digest"]
evidence_nodes = vm["provenance"]["evidence_nodes"]  # ["U4_Code_Artifact:abc", ...]

# Store inverted index
for node_id in evidence_nodes:
    INVERTED_INDEX.setdefault(node_id, set()).add(cache_key)

# On graph.delta.node.upsert
affected_keys = INVERTED_INDEX.get(node_id, set())
affects = [f"{view_id}:{path}" for (org, view_id, params, format) in affected_keys]
emit("docs.view.invalidated", {"affects": affects})
```

---

## Verification Checklist

✅ **No DB creds in L3** - Only L2 has FalkorDB access
✅ **CPS-1 implemented** - Quote validation in `runner.py`
✅ **Fail-loud** - All exceptions emit `failure.emit`
✅ **KO digest caching** - Cache keys include digest
✅ **U4 type rooting** - All selectors use `U4_*` types

⏸️ **Pending:**
- Wire resolvers to membrane bus
- Integrate with economy runtime
- Add inverted index for surgical invalidation
- Test end-to-end flow

---

## Testing Plan

### Phase 1: Unit Tests (No Bus)

```python
# Test projectors
rows = [{"s": {"id": "svc1", "name": "Auth"}, "deps": []}]
vm = project_architecture(rows)
assert vm["services"][0]["name"] == "Auth"
assert "ko_digest" in vm["provenance"]

# Test render
json_out = render(vm, "json")
assert json_out == vm

mdx_out = render(vm, "mdx")
assert "# " in mdx_out
```

### Phase 2: Integration Tests (With Bus)

```python
# Test L2 resolver
await membrane_bus.inject("docs.view.request", {
    "request_id": "test1",
    "quote_id": "q-stub",
    "view_type": "architecture",
    "format": "json",
    "scope": {"org": "scopelock", "path": "/"}
})

# Wait for result
result = await membrane_bus.observe("docs.view.result", timeout=5.0)
assert result["status"] == "ok"
assert "view_model" in result
```

### Phase 3: End-to-End Tests (WebSocket)

```python
# Test client → L3 → L2 → L3 → client flow
ws = await websockets.connect("ws://localhost:8000/api/ws")

await ws.send(json.dumps({
    "type": "docs.view.request",
    "org": "scopelock",
    "view_id": "architecture"
}))

response = await ws.recv()
msg = json.loads(response)
assert msg["type"] == "docs.view.data"
assert "view_model" in msg
```

---

## Migration Path

### Current State (Old L3)

`/orchestration/adapters/api/docs_view_api.py` (old, with Cypher execution)

### New State (Membrane-Native)

- `/services/view_resolvers/` (L2, new)
- `/orchestration/adapters/api/docs_view_api_v2.py` (L3, refactored)

### Cutover Steps

1. **Test new L2 resolvers** in isolation (unit tests)
2. **Wire to membrane bus** (subscribe to events)
3. **Test L3 bridge** with mocked bus responses
4. **Integration test** L2 ↔ L3 flow
5. **Cutover** `docs_view_api.py` → `docs_view_api_v2.py`
6. **Update control_api.py** imports
7. **Delete old** `docs_view_api.py`

---

## Benefits of Refactoring

**Membrane Discipline:**
- ✅ No cross-boundary DB pulls
- ✅ Event-driven (inject/observe)
- ✅ Clear L2/L3 separation

**Economic Accounting:**
- ✅ CPS-1 quote-before-inject
- ✅ Priced compute (0.05 - 5.0 $MIND)
- ✅ Budget enforcement

**Fail-Loud:**
- ✅ R-400/R-401 compliance
- ✅ All errors emit `failure.emit`
- ✅ No silent fallbacks

**Surgical Invalidation:**
- ✅ KO digest caching
- ✅ Targeted cache busts
- ✅ High hit-rates with freshness

**Portability:**
- ✅ U4_* universal types
- ✅ Works across repos/languages
- ✅ Composable projectors

---

## Next Steps

1. ✅ Create L2 resolver structure
2. ✅ Implement projectors + selectors
3. ✅ Add CPS-1 integration
4. ✅ Refactor L3 bridge to inject/observe
5. ⏸️ Wire resolvers to membrane bus
6. ⏸️ Add inverted index for surgical invalidation
7. ⏸️ Integration tests
8. ⏸️ Cutover to new architecture
9. ⏸️ Delete old implementation

**Ready for:** Membrane bus wiring and integration testing

---

**Status:** Core refactoring complete. Pending: wire to membrane bus, test end-to-end, deploy.
