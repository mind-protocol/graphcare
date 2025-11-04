#!/usr/bin/env python3
"""
Test client for L3 Docs WebSocket Service
"""

import asyncio
import json
import websockets

async def test_view_request():
    """Test requesting a view from L3 service"""

    uri = "ws://localhost:8003"

    async with websockets.connect(uri) as websocket:
        print(f"✅ Connected to {uri}")

        # Subscribe to scopelock
        await websocket.send(json.dumps({
            "type": "docs.subscribe",
            "org": "scopelock"
        }))

        # Request architecture view
        await websocket.send(json.dumps({
            "type": "docs.view.request",
            "org": "scopelock",
            "view_id": "architecture",
            "request_id": "test_123"
        }))

        print("📤 Sent view request for scopelock/architecture")

        # Receive responses
        for i in range(3):  # Wait for up to 3 messages
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                msg = json.loads(response)

                print(f"\n📥 Received: {msg.get('type')}")

                if msg.get('type') == 'docs.view.data':
                    print(f"   Title: {msg.get('title')}")
                    print(f"   Rows: {msg.get('row_count')}")
                    print(f"   Generated: {msg.get('generated_at')}")

                    if msg.get('data'):
                        print(f"\n   Sample data (first 2 rows):")
                        for row in msg['data'][:2]:
                            print(f"   - {row}")

                elif msg.get('type') == 'docs.subscribed':
                    print(f"   Org: {msg.get('org')}")

                elif msg.get('type') == 'error':
                    print(f"   ❌ Error: {msg.get('message')}")

            except asyncio.TimeoutError:
                print("\n⏰ Timeout waiting for response")
                break

if __name__ == "__main__":
    asyncio.run(test_view_request())
