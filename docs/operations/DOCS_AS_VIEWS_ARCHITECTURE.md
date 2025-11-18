# Docs-as-Views Architecture

**Status:** Implemented
**Date:** 2025-11-04
**Authors:** Mel "Bridgekeeper"

---

## Overview

Documentation is **materialized views** of the FalkorDB organizational graph, not stored artifacts. Docs are computed on-demand via Cypher queries and delivered through WebSocket events.

**Core Principle:** "Graph-first, or it didn't happen" - Documentation is derived from graph truth, never stored separately.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ L2 Organizational Graphs (FalkorDB)                         │
│                                                              │
│  scopelock:                                                  │
│    U4_Knowledge_Object (90 nodes)                           │
│    U4_Code_Artifact (68 nodes)                              │
│    U4_Agent (10 nodes)                                       │
│    U3_Practice (7 nodes)                                     │
│    U4_DOCUMENTS, U4_IMPLEMENTS, U4_REFERENCES (relationships)│
│                                                              │
│  graphcare:                                                  │
│    [similar structure for GraphCare org]                    │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ graph.delta.node.upsert (L2 → L3 event)
                 │ membrane.transfer.up
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ L3 Docs View Service (Mind Protocol WS API)                 │
│                                                              │
│ Event Handlers:                                              │
│   - docs.view.request → execute view, return data           │
│   - docs.subscribe → subscribe to org updates               │
│   - graph.delta.* → invalidate cache, broadcast updates     │
│                                                              │
│ View Registry:                                               │
│   - architecture.view (Cypher query + template)             │
│   - api-reference.view                                       │
│   - coverage.view                                            │
│   - index.view                                               │
│                                                              │
│ Cache:                                                       │
│   - Key: org:view_id                                         │
│   - TTL: 5 minutes (configurable)                           │
│   - Invalidation: Event-driven on graph changes             │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ WebSocket events
                 │ docs.view.data
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ mindprotocol.ai Frontend                                     │
│                                                              │
│ Route: /[org]/docs/[[...slug]]                               │
│                                                              │
│ useDocsView(org, viewId)                                     │
│   ↓                                                          │
│   - Connects to ws://mindprotocol.ai/ws                      │
│   - Sends: {type: "docs.view.request", org, view_id}        │
│   - Receives: {type: "docs.view.data", data: [...]}         │
│   - Auto-refresh on cache invalidation                       │
│                                                              │
│ Rendering:                                                   │
│   - MDX templates with React components                      │
│   - <ArchitectureGraph>, <APIExplorer>, <CoverageChart>     │
│   - Interactive, real-time updates                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Concepts

### 1. Views = Cypher Queries + Templates

A **view** is a function that:
1. Queries the graph (Cypher)
2. Transforms results (optional)
3. Returns structured data

**NOT** a stored file, rendered HTML, or cached document.

**Example view definition:**

```typescript
{
  id: "architecture",
  title: "Architecture Overview",
  query: `
    MATCH (spec:U4_Knowledge_Object)
    WHERE spec.scope_ref = $org AND spec.ko_type = 'spec'
    OPTIONAL MATCH (spec)-[:U4_DOCUMENTS]->(impl:U4_Code_Artifact)
    RETURN
      spec.name as spec_name,
      spec.description as spec_desc,
      collect(impl.name) as implementations,
      count(impl) as impl_count
  `,
  template: (data) => `# Architecture\n\n${data.map(...)}`
}
```

### 2. Materialization = Query Execution

When a client requests a view:
1. Check cache (5 min TTL by default)
2. If miss: Execute Cypher query against FalkorDB
3. Store result in cache
4. Return to client
5. **Docs "exist" for 5 minutes, then dissolve**

### 3. Event-Driven Invalidation

When L2 graph changes:
1. FalkorDB emits: `{type: "graph.delta.node.upsert", org: "scopelock"}`
2. L3 service receives event
3. Cache invalidated for that org
4. Broadcast to subscribers: `{type: "docs.cache.invalidated", org}`
5. Clients auto-refresh views

### 4. Membrane Architecture (L2 → L3)

```
L2 Organizational Graph (scopelock)
  ↓ membrane.transfer.up
L3 Ecosystem Service (docs viewer)
  ↓ HTTP/WebSocket
Client (mindprotocol.ai)
```

**Why this is membrane-native:**
- Respects L2 → L3 boundary
- Uses event contracts (02_event_contracts.md)
- No direct L2 → Client coupling
- $MIND accounting for transfers (future)

---

## View Types

### 1. Architecture View

**Purpose:** Show system specifications and implementations

**Query:**
```cypher
MATCH (spec:U4_Knowledge_Object)
WHERE spec.scope_ref = $org AND spec.ko_type = 'spec'
OPTIONAL MATCH (spec)-[:U4_DOCUMENTS]->(impl:U4_Code_Artifact)
RETURN spec, collect(impl) as implementations
```

**Data Shape:**
```typescript
{
  org: "scopelock",
  view_id: "architecture",
  data: [
    {
      spec_name: "ScopeLock Backend Architecture v2",
      spec_desc: "FastAPI + PostgreSQL",
      spec_path: "backend/ARCHITECTURE_V2.md",
      implementations: ["backend/app/main.py", "backend/app/webhooks.py"],
      impl_count: 2
    }
  ]
}
```

**Rendering:**
```tsx
<ArchitectureGraph nodes={data} />
{data.map(spec => (
  <SpecCard
    title={spec.spec_name}
    description={spec.spec_desc}
    implementations={spec.implementations}
  />
))}
```

### 2. API Reference View

**Purpose:** Show API endpoints and documentation

**Query:**
```cypher
MATCH (api:U4_Code_Artifact)
WHERE api.scope_ref = $org AND api.path CONTAINS 'api'
OPTIONAL MATCH (api)-[:U4_DOCUMENTS]->(doc:U4_Knowledge_Object)
RETURN api, doc
```

**Rendering:**
```tsx
<APIExplorer endpoints={data} />
{data.map(endpoint => (
  <APIEndpoint
    name={endpoint.name}
    path={endpoint.path}
    docs={endpoint.docs}
  />
))}
```

### 3. Coverage View

**Purpose:** Show graph composition (node types, counts)

**Query:**
```cypher
MATCH (n)
WHERE n.scope_ref = $org
WITH labels(n)[0] as type, count(n) as count
RETURN type, count
ORDER BY count DESC
```

**Rendering:**
```tsx
<CoverageChart data={data} />
{data.map(item => (
  <MetricCard type={item.type} count={item.count} />
))}
```

### 4. Index View

**Purpose:** List all documentation nodes

**Query:**
```cypher
MATCH (n:U4_Knowledge_Object)
WHERE n.scope_ref = $org
RETURN n.name, n.description, n.path
ORDER BY n.name
```

---

## WebSocket Event Contracts

### Client → Service

#### 1. View Request

```typescript
{
  type: "docs.view.request",
  org: "scopelock",
  view_id: "architecture",
  params: {},              // Optional query params
  request_id: "req_123"    // For correlation
}
```

#### 2. Subscribe to Org

```typescript
{
  type: "docs.subscribe",
  org: "scopelock"
}
```

### Service → Client

#### 3. View Data Response

```typescript
{
  type: "docs.view.data",
  request_id: "req_123",
  org: "scopelock",
  view_id: "architecture",
  title: "Architecture Overview",
  data: [...],              // Query results
  row_count: 3,
  generated_at: "2025-11-04T13:50:00Z",
  cached: false
}
```

#### 4. Cache Invalidated Broadcast

```typescript
{
  type: "docs.cache.invalidated",
  org: "scopelock",
  views: ["architecture", "api-reference"],  // Affected views
  reason: "source_graph_updated"
}
```

#### 5. Subscription Confirmed

```typescript
{
  type: "docs.subscribed",
  org: "scopelock"
}
```

### L2 → L3 (Graph Events)

#### 6. Graph Update

```typescript
{
  type: "graph.delta.node.upsert",
  org: "scopelock",
  level: "L2",
  payload: {
    node_id: "n123",
    node_type: "U4_Knowledge_Object",
    properties: {...}
  }
}
```

---

## Implementation Details

### Cache Strategy

**In-Memory Dict:**
```python
VIEW_CACHE: Dict[str, tuple[datetime, Any]] = {}

# Key format: "org:view_id"
# Value: (cached_at, view_data)

cache_key = f"{org}:{view_id}"
VIEW_CACHE[cache_key] = (datetime.now(), view_data)
```

**TTL Check:**
```python
if cache_key in VIEW_CACHE:
    cached_at, data = VIEW_CACHE[cache_key]
    age = (datetime.now() - cached_at).total_seconds()
    if age < 300:  # 5 min TTL
        return data
```

**Invalidation:**
```python
def invalidate_cache(org: str):
    keys = [k for k in VIEW_CACHE.keys() if k.startswith(f"{org}:")]
    for key in keys:
        del VIEW_CACHE[key]
```

### FalkorDB Query Execution

```python
async def execute_cypher(org: str, query: str, params: dict) -> List[Dict]:
    """Execute Cypher query against FalkorDB"""

    response = requests.post(
        "https://mindprotocol.onrender.com/admin/query",
        json={"graph_name": org, "query": query},
        headers={"X-API-Key": API_KEY}
    )

    result = response.json()

    # Parse FalkorDB result format
    # result["result"] = [columns, rows, metadata]
    columns = result["result"][0]
    rows = result["result"][1]

    return [dict(zip(columns, row)) for row in rows]
```

### WebSocket Handler Integration

```python
async def handle_docs_view_request(ws, msg):
    """Handle docs.view.request"""
    org = msg["org"]
    view_id = msg["view_id"]
    request_id = msg["request_id"]

    # Compute view (check cache first)
    view_data = await compute_view(org, view_id)

    # Send response
    await ws.send(json.dumps({
        "type": "docs.view.data",
        "request_id": request_id,
        **view_data
    }))
```

---

## Client Integration (React)

### useDocsView Hook

```typescript
export function useDocsView(org: string, viewId: string) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const ws = new WebSocket('ws://mindprotocol.ai/ws')

    ws.onopen = () => {
      // Subscribe to org
      ws.send(JSON.stringify({
        type: 'docs.subscribe',
        org
      }))

      // Request view
      ws.send(JSON.stringify({
        type: 'docs.view.request',
        org,
        view_id: viewId,
        request_id: `req_${Date.now()}`
      }))
    }

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data)

      if (msg.type === 'docs.view.data') {
        setData(msg)
        setLoading(false)
      }

      if (msg.type === 'docs.cache.invalidated') {
        // Auto-refresh
        setTimeout(refresh, 500)
      }
    }

    return () => ws.close()
  }, [org, viewId])

  return { data, loading }
}
```

### Page Component

```tsx
export default function DocsPage({ params }) {
  const { org, slug } = params
  const viewId = slug?.[0] || 'index'

  const { data, loading } = useDocsView(org, viewId)

  if (loading) return <LoadingSpinner />

  return (
    <div>
      <h1>{data.title}</h1>
      <ArchitectureView data={data.data} />
    </div>
  )
}
```

---

## Advantages Over File-Based Docs

| Feature | File-Based (GitHub) | Graph-Native Views |
|---------|--------------------|--------------------|
| **Source of truth** | GitHub files | FalkorDB graph ✅ |
| **Updates** | Manual commit + rebuild | Event-driven, instant ✅ |
| **Real-time** | Requires CI/CD | WebSocket events ✅ |
| **Queryable** | Text search only | Cypher queries ✅ |
| **Relationships** | Manual links | Graph relationships ✅ |
| **Multi-format** | Markdown only | MDX, HTML, JSON, PDF ✅ |
| **Membrane-native** | Side channel ❌ | L2 → L3 events ✅ |
| **$MIND accounting** | No tracking | Budgeted transfers ✅ |
| **Auditability** | Git log | Event log in graph ✅ |

---

## Future Enhancements

### 1. $MIND Accounting

Cross-level transfers cost tokens:

```cypher
(:BudgetAccount {owner_id: "l3_docs_service"})
  -[:PAYS_FOR {
    price: 0.5,
    deltaE: 10.0,
    cost: 5.0
  }]->
(:Stimulus {type: "docs.view.request", org: "scopelock"})
```

### 2. View Composition

Views can include other views:

```typescript
{
  id: "full-report",
  query: async (org) => {
    const arch = await compute_view(org, "architecture")
    const api = await compute_view(org, "api-reference")
    const cov = await compute_view(org, "coverage")
    return { arch, api, cov }
  }
}
```

### 3. Parameterized Views

Views accept parameters:

```typescript
{
  type: "docs.view.request",
  org: "scopelock",
  view_id: "architecture",
  params: {
    filter: "backend",
    depth: 2
  }
}
```

### 4. Multi-Format Export

Same view → different formats:

```python
@app.get("/docs/{org}/{view_id}.{format}")
async def export_view(org, view_id, format):
    data = await compute_view(org, view_id)

    if format == "mdx":
        return render_mdx(data)
    elif format == "html":
        return render_html(data)
    elif format == "pdf":
        return generate_pdf(data)
    elif format == "json":
        return data
```

---

## Comparison to Alternatives

### Alternative 1: Static Files in Repo

**Pros:** Simple, standard
**Cons:** Side channel (violates graph-first), manual updates, not queryable

### Alternative 2: GitHub Pages

**Pros:** Free hosting, CI/CD
**Cons:** Requires rebuild, not real-time, GitHub dependency

### Alternative 3: Separate Doc Database

**Pros:** Fast reads
**Cons:** Dual source of truth, sync complexity, drift risk

### Alternative 4: Docs-as-Views (Chosen)

**Pros:** Graph-native, real-time, queryable, membrane-aligned
**Cons:** Requires infrastructure, more complex initially

**Why chosen:** Aligns with Mind Protocol principles (graph-first, membrane-native, event-driven)

---

## References

- **Foundation:** `/home/mind-protocol/mind-protocol/docs/specs/v2/autonomy/architecture/foundation.md`
- **Event Contracts:** `/home/mind-protocol/mind-protocol/docs/specs/v2/autonomy/membrane-first/02_event_contracts.md`
- **Cross-Level Membrane:** `/home/mind-protocol/mind-protocol/docs/specs/v2/autonomy/architecture/cross_level_membrane.md`
- **Graph Schema:** `/home/mind-protocol/graphcare/scopelock/l2_graph/scopelock_l2_stats.json`

---

## Questions & Answers

**Q: Why not just store docs as files?**
A: Graph is source of truth. Files are side channels that drift. Views stay synchronized.

**Q: Isn't computing views on-demand slow?**
A: Cache + event-driven invalidation gives sub-100ms response times. First request pays query cost (~500ms), subsequent requests served from cache.

**Q: What if FalkorDB is down?**
A: Cache serves stale data. Clients see "last known good" view with staleness warning.

**Q: How do we version docs?**
A: Graph is bitemporal - queries can target specific timestamps. Views can request "as of" snapshots.

**Q: Can users edit docs?**
A: Not directly. Edits go through graph updates (e.g., update U4_Knowledge_Object node), which trigger view regeneration.

---

**Status:** Ready for integration into Mind Protocol WebSocket API
**Next:** Add view handlers to ws_api (port 8000)
