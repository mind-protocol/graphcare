#!/usr/bin/env python3
"""
Test client for integrated L3 Docs WebSocket (Mind Protocol WS API port 8000)
"""

import asyncio
import json
import websockets

async def test_docs_view_integrated():
    """Test requesting a view from integrated Mind Protocol WebSocket API"""

    uri = "ws://localhost:8000/api/ws"

    async with websockets.connect(uri) as websocket:
        print(f"✅ Connected to {uri}")

        # Subscribe to scopelock docs
        await websocket.send(json.dumps({
            "type": "docs.subscribe",
            "org": "scopelock"
        }))
        print("📤 Sent docs.subscribe for scopelock")

        # Request architecture view
        await websocket.send(json.dumps({
            "type": "docs.view.request",
            "org": "scopelock",
            "view_id": "architecture",
            "request_id": "test_integrated_123"
        }))
        print("📤 Sent docs.view.request for scopelock/architecture")

        # Receive responses
        for i in range(5):  # Wait for up to 5 messages
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=15.0)
                msg = json.loads(response)

                print(f"\n📥 Received: {msg.get('type')}")

                # Handle subscribe ack from main WS API
                if msg.get('type') == 'subscribe.ack@1.0':
                    print(f"   Connection ID: {msg.get('payload', {}).get('connection_id')}")
                    print(f"   Topics: {msg.get('payload', {}).get('topics', [])[:3]}")  # First 3

                # Handle docs.subscribed from docs view handlers
                elif msg.get('type') == 'docs.subscribed':
                    print(f"   Org: {msg.get('org')}")

                # Handle docs.view.data from docs view handlers
                elif msg.get('type') == 'docs.view.data':
                    print(f"   Title: {msg.get('title')}")
                    print(f"   Rows: {msg.get('row_count')}")
                    print(f"   Generated: {msg.get('generated_at')}")
                    print(f"   Cached: {msg.get('cached')}")

                    if msg.get('data'):
                        print(f"\n   Sample data (first 2 rows):")
                        for row in msg['data'][:2]:
                            print(f"   - {row}")

                elif msg.get('type') == 'error':
                    print(f"   ❌ Error: {msg.get('message')}")

            except asyncio.TimeoutError:
                print("\n⏰ Timeout waiting for response")
                break

if __name__ == "__main__":
    asyncio.run(test_docs_view_integrated())
