# FalkorDB Multi-Tenant Configuration - GraphCare

**Author:** Nora (Chief Architect)
**Date:** 2025-11-04
**Schema Version:** v2.0.0 (Minimal Extension Strategy)

---

## Overview

GraphCare uses **FalkorDB** (graph database) with a **multi-tenant architecture**. Each client gets a separate graph database.

**Connection:**
- Host: `localhost`
- Port: `6379`
- Protocol: Redis-compatible

**Graph naming convention:**
- Pattern: `graphcare_<client_name>`
- Example: `graphcare_scopelock`

---

## Schema Strategy (v2.0.0 - Minimal Extension)

### Strategic Pivot

After analysis, GraphCare adopts Quinn's **minimal extension** recommendation:

**0 new node types** - Reuse Mind Protocol universal types:
- `U4_Code_Artifact` with **path granularity** (`file`, `file::class`, `file::class::function`)
- `U4_Knowledge_Object` with **ko_type** (`adr`, `spec`, `runbook`, `guide`)
- `U4_Subentity` with **kind** (`semantic` for topic clusters, `functional`, `emergent`)
- `U4_Decision`, `U4_Metric`, `U4_Measurement`, `U4_Assessment`
- `U4_Agent`, `U4_Work_Item`, `U4_Event`, `U4_Goal`

**1 new link type:**
- `U4_SEMANTICALLY_SIMILAR`: Semantic clustering between `U4_Subentity` nodes
  - Properties: `similarity_score` (float 0-1), `confidence`, timestamps
  - Usage: Link related semantic clusters (e.g., "authentication" ↔ "authorization")

### Why This Strategy?

1. **Protocol Compatibility:** Works with Mind Protocol infrastructure
2. **Schema Maintenance:** No custom types to maintain
3. **Client Value:** Clients get "Mind Protocol-compatible graph" (future integration with consciousness systems)
4. **Flexibility:** Path granularity gives us file/class/function without new types

---

## Schema Migration

### Initial Setup (New Client)

```bash
# Create graph and apply schema
cd /home/mind-protocol/graphcare
python3 orchestration/schema_migration.py --graph graphcare_<client> --migrate
```

**What this does:**
1. Creates graph in FalkorDB (if not exists)
2. Creates indexes for efficient queries:
   - `type_name`, `name` (all node types)
   - `scope_ref`, `level` (universal filters)
   - `path` (U4_Code_Artifact)
   - `ko_type` (U4_Knowledge_Object)
   - `kind` (U4_Subentity)
   - `status` (U4_Work_Item)
3. Stores schema metadata (version, node/link counts, strategy)

### Verify Schema

```bash
# Check schema status
python3 orchestration/schema_migration.py --graph graphcare_<client> --status

# Validate schema compliance (after data extraction)
python3 orchestration/schema_migration.py --graph graphcare_<client> --validate
```

---

## Node Type Usage

### U4_Code_Artifact (Code Structure)

**Purpose:** Represents code at file, class, or function granularity

**Path Granularity:**
- `src/auth/login.py` (file level)
- `src/auth/login.py::LoginHandler` (class level)
- `src/auth/login.py::LoginHandler::authenticate` (function level)

**Required Properties:**
```cypher
CREATE (artifact:U4_Code_Artifact {
  name: "authenticate",
  path: "src/auth/login.py::LoginHandler::authenticate",
  description: "Authenticates user credentials against database",
  type_name: "U4_Code_Artifact",

  // Universal attributes (REQUIRED)
  level: "L2",                    // Organizational level
  scope_ref: "org_scopelock",     // Client organization ID
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),

  // Optional (code-specific)
  language: "python",
  lines_of_code: 42,
  complexity: 8,
  visibility: "public"
})
```

**Links:**
- `U4_CALLS` → another function
- `U4_DEPENDS_ON` → module/package
- `U4_TESTS` ← test case
- `U4_DOCUMENTS` ← documentation

---

### U4_Knowledge_Object (Documentation)

**Purpose:** Architecture decisions, specs, runbooks, guides

**Types (ko_type):**
- `adr`: Architecture Decision Record
- `spec`: Technical specification
- `runbook`: Operational runbook
- `guide`: Implementation guide

**Required Properties:**
```cypher
CREATE (ko:U4_Knowledge_Object {
  name: "ADR-015: Database Choice",
  ko_type: "adr",
  description: "Decision to use PostgreSQL for primary database",
  type_name: "U4_Knowledge_Object",

  // Universal attributes
  level: "L2",
  scope_ref: "org_scopelock",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),

  // Optional
  status: "accepted",
  content: "Full ADR text here...",
  author: "team",
  decision_date: "2024-03-15"
})
```

**Links:**
- `U4_DOCUMENTS` → code artifact
- `U4_REFERENCES` → another decision
- `U4_IMPLEMENTS` ← code that implements decision

---

### U4_Subentity (Semantic Clusters)

**Purpose:** Group related concepts into semantic clusters

**Kinds:**
- `semantic`: Topic/theme clusters (authentication, payment, etc.)
- `functional`: Functional groupings (citizens in Mind Protocol)
- `emergent`: Dynamically discovered clusters

**Required Properties:**
```cypher
CREATE (cluster:U4_Subentity {
  name: "cluster_authentication",
  kind: "semantic",
  description: "Authentication and security concepts",
  type_name: "U4_Subentity",

  // Universal attributes
  level: "L2",
  scope_ref: "org_scopelock",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),

  // Optional (semantic-specific)
  member_count: 15,              // Number of nodes in cluster
  coherence_score: 0.82          // Semantic coherence (0-1)
})
```

**Links:**
- `U4_MEMBER_OF` ← code artifacts, knowledge objects (membership)
- `U4_SEMANTICALLY_SIMILAR` ↔ other clusters (similarity)

---

## Link Type Usage

### U4_SEMANTICALLY_SIMILAR (NEW)

**Purpose:** Connect semantically related clusters

**Example:**
```cypher
MATCH (c1:U4_Subentity {name: 'cluster_authentication'})
MATCH (c2:U4_Subentity {name: 'cluster_authorization'})
CREATE (c1)-[r:U4_SEMANTICALLY_SIMILAR {
  similarity_score: 0.82,       // Cosine similarity (0-1)
  confidence: 0.95,              // Link confidence
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),

  // Optional
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2",
  method: "centroid_cosine"
}]->(c2)
```

**Querying Similar Clusters:**
```cypher
// Find clusters similar to authentication
MATCH (c1:U4_Subentity {name: 'cluster_authentication'})-[r:U4_SEMANTICALLY_SIMILAR]-(c2)
WHERE r.similarity_score >= 0.7
RETURN c2.name, r.similarity_score
ORDER BY r.similarity_score DESC
```

---

### Other Mind Protocol Link Types

**Code Structure:**
- `U4_CALLS`: Function → Function
- `U4_DEPENDS_ON`: Module → Module/Package
- `U4_IMPLEMENTS`: Code → Spec/Decision
- `U4_TESTS`: Test → Code

**Documentation:**
- `U4_DOCUMENTS`: Docs → Code/Feature
- `U4_REFERENCES`: Doc → Doc

**Relationships:**
- `U4_MEMBER_OF`: Node → Cluster/Entity
- `U4_RELATES_TO`: Generic relationship

**Workflow:**
- `U4_ASSIGNED_TO`: Task → Agent
- `U4_BLOCKED_BY`: Task → Task

**Observability:**
- `U4_EMITS`: Component → Event
- `U4_CONSUMES`: Component → Event
- `U4_MEASURES`: Metric → Component
- `U4_EVIDENCED_BY`: Assessment → Evidence

---

## Universal Attributes (REQUIRED for All Nodes)

All nodes MUST have these properties:

```cypher
{
  // Identity
  name: "unique_identifier",
  description: "Human-readable description",
  type_name: "U4_Code_Artifact",  // Node type

  // Bitemporal Tracking
  created_at: timestamp(),         // When knowledge was captured
  updated_at: timestamp(),         // Last modification
  valid_from: timestamp(),         // When fact became true
  valid_to: NULL,                  // When fact stopped being true (NULL = still valid)

  // Organizational Context
  level: "L2",                     // L1 (Mind Protocol), L2 (Client org)
  scope_ref: "org_scopelock",      // Client organization ID

  // Privacy & Provenance
  visibility: "private",           // private, internal, public
  created_by: "citizen_nora",      // Creator ID
  substrate: "organizational"      // organizational, personal, shared
}
```

---

## Universal Link Attributes (REQUIRED for All Links)

All links MUST have these properties:

```cypher
{
  // Bitemporal Tracking
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: NULL,

  // Consciousness Metadata (for Mind Protocol compatibility)
  confidence: 0.95,                // Confidence in link (0-1)
  energy: 0.0,                     // Activation energy (0-1)
  forming_mindstate: NULL,         // Optional: mindstate during formation
  goal: "",                        // Optional: goal driving link formation

  // Privacy & Provenance
  visibility: "private",
  created_by: "citizen_nora",
  substrate: "organizational"
}
```

---

## Common Query Patterns

### Find All Code in File

```cypher
MATCH (artifact:U4_Code_Artifact)
WHERE artifact.path STARTS WITH 'src/auth/login.py'
RETURN artifact.name, artifact.path
ORDER BY artifact.path
```

### Find Functions Called by Function

```cypher
MATCH (fn:U4_Code_Artifact {path: 'src/auth/login.py::LoginHandler::authenticate'})
      -[:U4_CALLS]->(called:U4_Code_Artifact)
RETURN called.name, called.path
```

### Find All Nodes in Semantic Cluster

```cypher
MATCH (node)-[:U4_MEMBER_OF]->(cluster:U4_Subentity {name: 'cluster_authentication'})
RETURN labels(node)[0] AS type, node.name, node.description
```

### Find Similar Clusters (Transitive)

```cypher
MATCH path = (c1:U4_Subentity {name: 'cluster_authentication'})
             -[:U4_SEMANTICALLY_SIMILAR*1..2]-(c2:U4_Subentity)
WHERE c1 <> c2
RETURN DISTINCT c2.name, c2.description, length(path) AS hops
ORDER BY hops ASC, c2.name
```

### Filter by Client

```cypher
MATCH (n)
WHERE n.scope_ref = 'org_scopelock'
RETURN labels(n)[0] AS type, count(n) AS count
ORDER BY count DESC
```

---

## Python Connection Code

### Basic Connection

```python
from falkordb import FalkorDB

# Connect to FalkorDB
db = FalkorDB(host='localhost', port=6379)
graph = db.select_graph('graphcare_scopelock')

# Simple query
result = graph.query("MATCH (n:U4_Code_Artifact) RETURN count(n)")
count = result.result_set[0][0]
print(f"Code artifacts: {count}")
```

### Using Mind Protocol Adapter

```python
from orchestration.libs.utils.falkordb_adapter import get_falkordb_graph

# Get graph (reuses Mind Protocol connection logic)
graph = get_falkordb_graph('graphcare_scopelock')

# Parametrized query
result = graph.query(
    "MATCH (n:U4_Code_Artifact) WHERE n.path = $path RETURN n",
    {'path': 'src/auth/login.py::LoginHandler::authenticate'}
)

for row in result.result_set:
    node = row[0]
    print(f"Found: {node.properties['name']}")
```

---

## Multi-Tenant Isolation

**Graph Isolation:**
- Each client has separate graph database
- No cross-graph queries possible
- Data isolation at database level

**Graph Naming:**
- Pattern: `graphcare_<client>`
- Examples: `graphcare_scopelock`, `graphcare_mindsync`, `graphcare_laserensisma`

**Scope Reference:**
- All nodes have `scope_ref` property
- Example: `scope_ref: "org_scopelock"`
- Secondary isolation layer (for queries across graphs if needed)

**Level:**
- All GraphCare client graphs at `level: "L2"` (organizational layer)
- Mind Protocol internal graphs at `level: "L1"`
- Enables future L1 ↔ L2 integration

---

## Schema Versioning

**Current Version:** 2.0.0 (Minimal Extension)

**Version History:**
- v1.0.0 (2025-11-04): Initial schema with 8 custom GC_* node types
- v2.0.0 (2025-11-04): Strategic pivot - 0 custom nodes, 1 new link type

**Migration Path:**
- No migration needed for v1.0.0 → v2.0.0 (no v1.0.0 data exists yet)
- Future migrations: Use `schema_migration.py --migrate`

**Schema Metadata:**
```cypher
MATCH (schema:GraphCare_Schema)
RETURN schema.version, schema.strategy, schema.migrated_at
```

---

## Next Steps

**For Quinn (Infrastructure Engineer):**
- Build embedding service (SentenceTransformers)
- Implement type classifier (U4_Code_Artifact vs U4_Knowledge_Object)
- Calculate similarity scores for U4_SEMANTICALLY_SIMILAR links

**For Kai (Code Extraction):**
- Python AST extractor → U4_Code_Artifact nodes (with path granularity)
- Link extractor → U4_CALLS, U4_DEPENDS_ON links

**For Team:**
- All extraction should use these universal types
- Ensure all nodes have universal attributes (bitemporal, scope, privacy)
- Use U4_SEMANTICALLY_SIMILAR for semantic clustering

---

## Troubleshooting

### "Connection refused" Error

```bash
# Check if FalkorDB is running
docker ps | grep falkordb

# Start FalkorDB (if using Docker)
docker start falkordb
```

### "Graph not found" Error

```bash
# Create graph with schema migration
python3 orchestration/schema_migration.py --graph graphcare_<client> --migrate
```

### "Index already exists" Warning

This is normal. Schema migration is idempotent - safe to run multiple times.

### Validation Failures

```bash
# Run validation to see missing attributes
python3 orchestration/schema_migration.py --graph graphcare_<client> --validate

# Fix: Ensure all nodes have universal attributes (see above)
```

---

## References

**Mind Protocol Schema:**
- `/home/mind-protocol/mindprotocol/docs/COMPLETE_TYPE_REFERENCE.md`

**L2 Graph Creation Process:**
- `/home/mind-protocol/graphcare/docs/L2_GRAPH_CREATION_PROCESS.md`

**FalkorDB Adapter:**
- `/home/mind-protocol/mindprotocol/orchestration/libs/utils/falkordb_adapter.py`

**Schema Migration Script:**
- `/home/mind-protocol/graphcare/orchestration/schema_migration.py`

---

**Questions?** Ask Nora (Chief Architect) or check SYNC.md for latest updates.
