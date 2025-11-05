# Docs-as-Views Startup Guide

**Status:** ✅ Implementation complete | Ready for testing
**Date:** 2025-11-04
**Author:** Mel "Bridgekeeper"

---

## Quick Start (Copy/Paste)

### Terminal 1: Membrane Hub
```bash
cd /home/mind-protocol/mindprotocol
python -m orchestration.adapters.bus.membrane_hub
# Should see: [MembraneHub] Ready - accepting connections
```

### Terminal 2: L2 Resolver (scopelock org)
```bash
cd /home/mind-protocol/mindprotocol
export $(cat .env.l2_resolver | xargs)
python -m services.view_resolvers.bus_observer
# Should see: [L2 Observer] Ready - waiting for docs.view.request events
```

### Terminal 3: Mind Protocol WebSocket Server (L3)
```bash
cd /home/mind-protocol/mindprotocol
python orchestration/adapters/ws/websocket_server.py
# Should see: Mind Protocol WS API running on port 8000
```

**IMPORTANT:** Start the background observer task `observe_bus_and_fanout()` in the WebSocket server.
**TODO:** Wire this into websocket_server.py startup (see below).

---

## What's Running

**Port 8765:** Membrane Hub (ws://localhost:8765/{inject,observe})
- `/inject`: Publishers send events
- `/observe`: Subscribers receive events

**Port 8000:** Mind Protocol WebSocket API (ws://localhost:8000/api/ws)
- L3 bridge for client connections
- Routes `docs.view.request` to membrane bus
- Observes `docs.view.result` from bus and streams to clients

**L2 Resolver Process:** (no external port)
- Subscribes to `docs.view.request` events
- Executes Cypher against FalkorDB (remote Render instance)
- Broadcasts `docs.view.result` and `failure.emit` to bus

---

## Testing the Flow

### Option 1: WebSocket Client (JavaScript)

```javascript
// Connect to Mind Protocol WS
const ws = new WebSocket('ws://localhost:8000/api/ws');

// Request a view
ws.send(JSON.stringify({
  type: "docs.view.request",
  org: "scopelock",
  view_id: "coverage",  // or "architecture", "api-reference", "index"
  format: "json",
  request_id: "test_123"
}));

// Receive result
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === "docs.view.data") {
    console.log("View data:", data.view_model);
    console.log("Provenance:", data.provenance);
  }
};
```

### Option 2: Python Test Client

```python
import asyncio
import json
import websockets

async def test_docs_view():
    async with websockets.connect("ws://localhost:8000/api/ws") as ws:
        # Request coverage view
        request = {
            "type": "docs.view.request",
            "org": "scopelock",
            "view_id": "coverage",
            "format": "json",
            "request_id": "test_coverage_001"
        }

        await ws.send(json.dumps(request))

        # Wait for response
        response = await ws.recv()
        data = json.loads(response)

        print(f"Type: {data.get('type')}")
        print(f"Status: {data.get('status')}")
        print(f"View Model: {json.dumps(data.get('view_model'), indent=2)}")
        print(f"KO Digest: {data.get('provenance', {}).get('ko_digest')}")

asyncio.run(test_docs_view())
```

---

## Expected Results

### Coverage View (JSON)
```json
{
  "type": "docs.view.data",
  "request_id": "test_123",
  "status": "ok",
  "format": "json",
  "view_type": "coverage",
  "cached": false,
  "view_model": {
    "items": [
      {"type": "U4_Knowledge_Object", "count": 175, "tests": 0},
      {"type": "U4_Code_Artifact", "count": 80, "tests": 0},
      ...
    ],
    "provenance": {
      "ko_digest": "sha256:abc123..."
    }
  },
  "provenance": {
    "ko_digest": "sha256:abc123...",
    "selectors": ["MATCH (n) WHERE..."],
    "evidence_nodes": []
  }
}
```

---

## Troubleshooting

### "Connection refused" on port 8765
- **Fix:** Start membrane hub first (Terminal 1)

### L2 Resolver error: "Failed to connect to membrane bus"
- **Check:** Is membrane hub running on port 8765?
- **Check:** `MEMBRANE_OBSERVE_URI` in .env correct?

### L2 Resolver error: "FalkorDB query failed"
- **Check:** `FALKORDB_API_URL` and `FALKORDB_API_KEY` correct in .env
- **Check:** Graph name `scopelock` exists on remote FalkorDB
- **Test:** `curl -X POST https://mindprotocol.onrender.com/admin/query -H "X-API-Key: Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU" -d '{"graph_name":"scopelock","query":"MATCH (n) RETURN count(n)"}'`

### Client receives timeout error
- **Check:** All 3 services running (hub, L2, L3)?
- **Check:** L3 background observer started? (see TODO below)
- **Increase timeout:** Change `REQUEST_TIMEOUT` in docs_view_api_v2.py (default 15s)

### Client receives error: "Unknown view_id"
- **Valid view_ids:** `architecture`, `api-reference`, `coverage`, `index`

---

## TODO: Wire L3 Observer into WebSocket Server

**File:** `/orchestration/adapters/ws/websocket_server.py`

**Add to startup** (around line 300-400 where engines are started):

```python
# Start L3 docs view observer (background task)
from orchestration.adapters.api.docs_view_api_v2 import observe_bus_and_fanout

async def start_background_tasks():
    # Existing tasks...

    # Add docs view observer
    asyncio.create_task(observe_bus_and_fanout())
    logger.info("[WebSocket Server] Started docs view observer")

# Call during server startup
asyncio.create_task(start_background_tasks())
```

---

## Configuration

### Remote FalkorDB (Current - Production Data)

`.env.l2_resolver`:
```bash
FALKORDB_MODE=remote
FALKORDB_API_URL=https://mindprotocol.onrender.com/admin/query
FALKORDB_API_KEY=Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU
GRAPH_NAME=scopelock
```

### Local FalkorDB (Future - Developer Setup)

`.env.l2_resolver.dev`:
```bash
FALKORDB_MODE=local
FALKORDB_HOST=localhost
FALKORDB_PORT=6379
GRAPH_NAME=scopelock
```

To use local, import graph first:
```bash
python tools/import_graph_batched.py graphcare/output/scopelock/scopelock_l2.cypher scopelock
```

---

## Architecture Verification

### ✅ Membrane Discipline
- **L3 has no DB credentials** ✅ (check docs_view_api_v2.py - no FALKORDB imports)
- **L2 computes inside org boundary** ✅ (bus_observer.py connects to remote FalkorDB)
- **Events flow through membrane bus** ✅ (inject/observe pattern)

### ✅ Fail-Loud (R-400/R-401)
- **All exceptions emit failure.emit** ✅ (see runner.py:_emit_failure)
- **Error results sent to client** ✅ (see runner.py:_emit_result_error)

### ✅ CPS-1 Economy Integration
- **Quote validation gate exists** ✅ (see runner.py:on_docs_view_request line 156)
- **Soft-enforced for dev** ✅ (CPS1_ENFORCE=false in .env)

### ✅ KO Digest Caching
- **Cache keys include ko_digest** ✅ (see runner.py:cache.set)
- **Surgical invalidation possible** ✅ (see runner.py:on_graph_delta)

---

## Next Steps

1. **Wire L3 observer** into websocket_server.py startup ⏸️
2. **Test end-to-end** with all 3 services running ⏸️
3. **Add frontend route** at `/[org]/docs` in mindprotocol.ai ⏸️
4. **Upgrade bus** to Redis pub/sub for production (optional) ⏸️

---

**Ready to view docs!** Start the 3 services and connect via WebSocket.
