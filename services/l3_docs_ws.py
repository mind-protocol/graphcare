#!/usr/bin/env python3
"""
L3 Docs View Service - WebSocket-based

Subscribes to L2 graph events, computes views on-demand, publishes results.
Uses Mind Protocol WebSocket event system (membrane-native).
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any
import websockets
from websockets.server import WebSocketServerProtocol

# View cache (org:view_id -> computed data)
VIEW_CACHE: Dict[str, tuple[datetime, Any]] = {}

# Connected clients (org -> set of websockets)
SUBSCRIBERS: Dict[str, set[WebSocketServerProtocol]] = {}

# FalkorDB connection (for Cypher queries)
FALKORDB_WS = "ws://mindprotocol.onrender.com:8000/ws"


# ============================================================================
# View Definitions (Cypher queries)
# ============================================================================

VIEWS = {
    "architecture": {
        "title": "Architecture Overview",
        "query": """
            MATCH (spec:U4_Knowledge_Object)
            WHERE spec.scope_ref = $org AND spec.ko_type = 'spec'
            OPTIONAL MATCH (spec)-[:U4_DOCUMENTS]->(impl:U4_Code_Artifact)
            RETURN
                spec.name as spec_name,
                spec.description as spec_desc,
                spec.path as spec_path,
                collect(impl.name) as implementations,
                count(impl) as impl_count
            ORDER BY spec.name
        """
    },

    "api-reference": {
        "title": "API Reference",
        "query": """
            MATCH (api:U4_Code_Artifact)
            WHERE api.scope_ref = $org AND api.path CONTAINS 'api'
            OPTIONAL MATCH (api)-[:U4_DOCUMENTS]->(doc:U4_Knowledge_Object)
            RETURN
                api.name as endpoint,
                api.path as file,
                api.description as desc,
                doc.description as docs
        """
    },

    "coverage": {
        "title": "Coverage Report",
        "query": """
            MATCH (n)
            WHERE n.scope_ref = $org
            WITH labels(n)[0] as type, count(n) as count
            RETURN type, count
            ORDER BY count DESC
        """
    },

    "index": {
        "title": "Documentation Index",
        "query": """
            MATCH (n:U4_Knowledge_Object)
            WHERE n.scope_ref = $org
            RETURN n.name as title, n.description as desc, n.path as path
            ORDER BY n.name
        """
    }
}


# ============================================================================
# FalkorDB Query Execution
# ============================================================================

async def execute_cypher(org: str, query: str, params: dict = None) -> List[Dict]:
    """Execute Cypher query against FalkorDB via API"""
    import requests

    API_URL = "https://mindprotocol.onrender.com/admin/query"
    API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"

    payload = {
        "graph_name": org,
        "query": query
    }

    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()

        result = response.json()

        # Parse FalkorDB result format
        # result = {"result": [["col1", "col2"], [[val1, val2]], [metadata]]}
        if "result" not in result:
            return []

        data = result["result"]
        if len(data) < 2:
            return []

        columns = data[0]
        rows = data[1]

        # Convert to list of dicts
        return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print(f"❌ Cypher query failed: {e}")
        return []


# ============================================================================
# View Execution (Materialization)
# ============================================================================

async def compute_view(org: str, view_id: str) -> Dict[str, Any]:
    """Execute view query and return data"""

    if view_id not in VIEWS:
        return {"error": f"View '{view_id}' not found"}

    view = VIEWS[view_id]

    # Check cache first
    cache_key = f"{org}:{view_id}"
    if cache_key in VIEW_CACHE:
        cached_at, data = VIEW_CACHE[cache_key]
        age = (datetime.now() - cached_at).total_seconds()
        if age < 300:  # 5 min TTL
            print(f"✅ Cache hit: {cache_key} (age: {age:.1f}s)")
            return data

    # Execute Cypher query (materialize view)
    print(f"🔍 Computing view: {org}/{view_id}")
    rows = await execute_cypher(org, view["query"], params={"org": org})

    view_data = {
        "org": org,
        "view_id": view_id,
        "title": view["title"],
        "data": rows,
        "generated_at": datetime.now().isoformat(),
        "row_count": len(rows)
    }

    # Cache result
    VIEW_CACHE[cache_key] = (datetime.now(), view_data)

    return view_data


# ============================================================================
# WebSocket Event Handlers
# ============================================================================

async def handle_view_request(ws: WebSocketServerProtocol, msg: dict):
    """Handle docs.view.request from client"""
    org = msg.get("org")
    view_id = msg.get("view_id", "index")
    request_id = msg.get("request_id")

    if not org:
        await ws.send(json.dumps({
            "type": "error",
            "request_id": request_id,
            "message": "Missing 'org' parameter"
        }))
        return

    # Compute view
    view_data = await compute_view(org, view_id)

    # Send response
    response = {
        "type": "docs.view.data",
        "request_id": request_id,
        **view_data
    }

    await ws.send(json.dumps(response))
    print(f"✅ Sent view data: {org}/{view_id} ({view_data.get('row_count')} rows)")


async def handle_subscribe(ws: WebSocketServerProtocol, msg: dict):
    """Handle docs.subscribe request"""
    org = msg.get("org")

    if not org:
        await ws.send(json.dumps({"type": "error", "message": "Missing 'org'"}))
        return

    # Add to subscribers
    if org not in SUBSCRIBERS:
        SUBSCRIBERS[org] = set()
    SUBSCRIBERS[org].add(ws)

    await ws.send(json.dumps({
        "type": "docs.subscribed",
        "org": org
    }))

    print(f"✅ Client subscribed to {org} docs")


async def handle_graph_update(event: dict):
    """Handle graph.delta.* events from FalkorDB"""
    org = event.get("org")

    if not org:
        return

    print(f"📥 Graph update for {org}: {event.get('type')}")

    # Invalidate cache for this org
    invalidate_cache(org)

    # Broadcast to subscribers
    if org in SUBSCRIBERS:
        broadcast_msg = {
            "type": "docs.cache.invalidated",
            "org": org,
            "reason": "source_graph_updated",
            "event_type": event.get("type")
        }

        disconnected = []
        for ws in SUBSCRIBERS[org]:
            try:
                await ws.send(json.dumps(broadcast_msg))
            except Exception:
                disconnected.append(ws)

        # Remove disconnected clients
        for ws in disconnected:
            SUBSCRIBERS[org].discard(ws)


def invalidate_cache(org: str):
    """Invalidate all cached views for org"""
    keys_to_delete = [k for k in VIEW_CACHE.keys() if k.startswith(f"{org}:")]
    for key in keys_to_delete:
        del VIEW_CACHE[key]
    print(f"🗑️  Invalidated {len(keys_to_delete)} cached views for {org}")


# ============================================================================
# WebSocket Server
# ============================================================================

async def handle_client(websocket: WebSocketServerProtocol, path: str):
    """Handle WebSocket connection from client"""
    print(f"🔌 Client connected: {websocket.remote_address}")

    try:
        async for message in websocket:
            try:
                msg = json.loads(message)
                msg_type = msg.get("type")

                if msg_type == "docs.view.request":
                    await handle_view_request(websocket, msg)

                elif msg_type == "docs.subscribe":
                    await handle_subscribe(websocket, msg)

                else:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"Unknown message type: {msg_type}"
                    }))

            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON"
                }))

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        # Remove from subscribers
        for org, subs in SUBSCRIBERS.items():
            subs.discard(websocket)

        print(f"🔌 Client disconnected: {websocket.remote_address}")


async def subscribe_to_falkordb_events():
    """Subscribe to FalkorDB graph events (future)"""
    # TODO: Connect to FalkorDB WebSocket and subscribe to graph.delta.*
    # For now, we rely on cache TTL
    print("⏳ FalkorDB event subscription not implemented yet (using cache TTL)")
    pass


async def main():
    """Start L3 Docs View Service"""
    print("🚀 Starting L3 Docs View Service (WebSocket)")

    # Start WebSocket server
    server = await websockets.serve(
        handle_client,
        "0.0.0.0",
        8003,
        max_size=10_000_000  # 10MB max message size
    )

    print("✅ WebSocket server listening on ws://0.0.0.0:8003")

    # Subscribe to FalkorDB events (future)
    asyncio.create_task(subscribe_to_falkordb_events())

    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
