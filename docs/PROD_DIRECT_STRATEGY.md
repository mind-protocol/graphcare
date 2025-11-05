# GraphCare Prod-Direct Strategy

**Decision Date:** 2025-11-04
**Author:** Nora (Chief Architect)
**Status:** ✅ Confirmed by team

---

## Strategy Overview

**All GraphCare graph operations go directly to production FalkorDB (Render).**

- ✅ Graph extraction → Render FalkorDB
- ✅ Docs view queries → Render FalkorDB
- ✅ Development/testing → Render FalkorDB
- ❌ No local FalkorDB population for client graphs

---

## Rationale

1. **Single source of truth** - No sync issues between local/remote
2. **Simpler workflow** - No dev/prod split
3. **Faster iteration** - No local import step
4. **Production-grade testing** - Real environment from day one

---

## Connection Information

**Production FalkorDB (Render):**
```
API Endpoint: https://mindprotocol.onrender.com/admin/query
API Key: Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU
Protocol: REST API (POST requests)
```

**Graph Names:**
- `scopelock` (current client)
- `mindsync` (future client)
- `laserenissima` (future client)
- Pattern: `<client_name>` (simple, clean)

---

## Directory Structure

### Client Repository Location
```
/home/mind-protocol/graphcare/clients/<client>/
```

**Example: scopelock**
```
/home/mind-protocol/graphcare/clients/scopelock/
├── backend/         # Python FastAPI backend
├── src/             # Next.js frontend
├── docs/            # Client documentation
├── citizens/        # Citizen identities (CLAUDE.md files)
├── proofgen/        # Proof generation
├── playbooks/       # Operational docs
├── README.md        # Client repo readme
└── ...
```

This is the **actual client repository** (git clone from client's GitHub).

### GraphCare Work Directory
```
/home/mind-protocol/graphcare/orgs/<client>/
```

**Example: scopelock**
```
/home/mind-protocol/graphcare/orgs/scopelock/
├── config/
│   └── extraction_config.yaml    # GraphCare extraction config
├── extraction/                    # Quinn's corpus analysis outputs
├── reports/                       # Analysis reports
├── docs/                          # Generated documentation
└── delivery/                      # Final client package
```

This is **GraphCare's working directory** for the client engagement.

---

## Tools & Scripts

### Graph Import (to Render)

**Tool:** `tools/import_graph_batched.py`

**Usage:**
```bash
cd /home/mind-protocol/graphcare
python3 tools/import_graph_batched.py \
  --file orgs/scopelock/extraction/graph_export.cypher \
  --graph scopelock
```

**What it does:**
- Reads Cypher statements from file
- Executes each statement via Render API
- Handles retries and progress tracking
- Reports success/failure stats

**Configuration:**
```python
API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"
```

### Schema Migration (Create Graph)

**Tool:** `orchestration/schema_migration.py`

**Usage:**
```bash
# This creates schema metadata only
# Actual data import uses import_graph_batched.py
python3 orchestration/schema_migration.py --graph <client> --migrate
```

**Note:** This tool is for **local testing only**. Production graphs are created via API import.

### Query Render FalkorDB

**Python Example:**
```python
import requests

API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"

def query_graph(graph_name: str, cypher: str):
    payload = {
        "graph_name": graph_name,
        "query": cypher
    }
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()

# Example: Get node counts
result = query_graph("scopelock", "MATCH (n) RETURN labels(n)[0] as label, count(n) as count")
print(result['result'])
```

---

## Team Workflows

### Quinn (Corpus Analysis)
1. Clone client repo to `clients/<client>/`
2. Run corpus analysis
3. Generate embeddings
4. Export graph to `orgs/<client>/extraction/graph_export.cypher`
5. Import to Render: `python3 tools/import_graph_batched.py --file ... --graph <client>`

### Kai + Nora (Graph Extraction)
1. Extract code (Kai) + architecture (Nora) from `clients/<client>/`
2. Generate U4_* nodes and links
3. Export to Cypher: `orgs/<client>/extraction/graph_export.cypher`
4. Import to Render: `python3 tools/import_graph_batched.py --file ... --graph <client>`
5. Verify: Query Render API for node/relationship counts

### Vera (Validation)
1. Query Render API for validation checks
2. Test coverage queries against production graph
3. Report validation results

### Marcus (Security Audit)
1. Query Render API for PII scan
2. Check for credentials in graph
3. Validate compliance
4. Report: ship/hold decision

### Sage (Documentation)
1. Query Render API for graph data
2. Generate documentation from production graph
3. Create client delivery package

---

## Local FalkorDB Usage

**Local FalkorDB (localhost:6379) is ONLY for:**
- Mind Protocol consciousness graphs (citizen graphs)
- Testing schema migrations
- Development of FalkorDB tools

**Local FalkorDB is NOT for:**
- Client graphs (use Render)
- Production data (use Render)
- Documentation generation (use Render)

---

## Benefits of Prod-Direct

**For Development:**
- ✅ No local setup complexity
- ✅ No data sync issues
- ✅ Production-grade testing from start

**For Team:**
- ✅ Single source of truth
- ✅ Simpler coordination (everyone queries same data)
- ✅ Real-time collaboration (changes immediately visible)

**For Clients:**
- ✅ Documentation always reflects latest graph state
- ✅ No "works locally but not in prod" issues
- ✅ Faster delivery (no sync/deploy steps)

---

## Trade-offs

**Advantages:**
- Single source of truth
- No sync complexity
- Production testing

**Disadvantages:**
- Requires internet connection
- API latency (vs localhost)
- Rate limits (if applicable)
- Shared resource (all team uses same FalkorDB)

**Decision:** Advantages outweigh disadvantages for GraphCare use case.

---

## Migration from Local Dev

**If you were using local FalkorDB:**

**Before (local):**
```python
from falkordb import FalkorDB
db = FalkorDB(host='localhost', port=6379)
graph = db.select_graph('scopelock')
result = graph.query("MATCH (n) RETURN count(n)")
```

**After (prod-direct):**
```python
import requests

API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"

def query_graph(graph_name, cypher):
    response = requests.post(
        API_URL,
        json={"graph_name": graph_name, "query": cypher},
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
        timeout=30
    )
    return response.json()

result = query_graph("scopelock", "MATCH (n) RETURN count(n)")
```

---

## Future Considerations

**If we scale to many clients:**
- Consider read replicas for heavy query loads
- Consider caching layer for common queries
- Consider GraphQL API for more flexible queries

**For now:** Direct API access is simple and sufficient.

---

## References

**Documentation:**
- `docs/FALKORDB_SETUP.md` - FalkorDB schema and setup
- `docs/EXTRACTION_WORKFLOW.md` - Full extraction pipeline
- `tools/import_graph_batched.py` - Import tool source

**API Documentation:**
- Render endpoint: https://mindprotocol.onrender.com/admin/query
- Accepts: `{graph_name: str, query: str}`
- Returns: `{result: [[row1], [row2], ...], metadata: {...}}`

**Team Coordination:**
- `citizens/SYNC.md` - Latest team updates
- Ask in coordination channel if uncertain

---

**Questions?** Ask Nora (Chief Architect) or check SYNC.md for latest updates.
