#!/usr/bin/env python3
"""Test WebSocket connection to production."""

import asyncio
import websockets
import json

async def test_connection():
    """Test basic WebSocket connection."""
    url = "wss://mindprotocol.ai/api/ws"

    try:
        print(f"Connecting to {url}...")
        async with websockets.connect(url) as ws:
            print("✅ Connected successfully!")

            # Send a test request
            request = {
                "type": "docs.view.request",
                "org": "scopelock",
                "view_id": "architecture",
                "format": "json",
                "request_id": "test_123"
            }

            print(f"Sending request: {json.dumps(request, indent=2)}")
            await ws.send(json.dumps(request))

            print("Waiting for response...")
            response = await asyncio.wait_for(ws.recv(), timeout=10.0)

            print(f"✅ Received response: {response[:200]}...")
            return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())
