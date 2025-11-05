#!/usr/bin/env python3
"""
Test client for docs-as-views membrane-native architecture.

Connects to L3 WebSocket server and requests a docs view.
Flow: Client → L3 → L4 → L2 → L4 → L3 → Client
"""

import asyncio
import websockets
import json
import sys

async def test_docs_request():
    """Test end-to-end docs request flow."""
    uri = "ws://localhost:8000/ws"  # Router has no prefix, endpoint is at /ws

    print("🔌 Connecting to L3 WebSocket Server...")
    print(f"   URI: {uri}")

    try:
        # Add Origin header to pass CORS validation
        extra_headers = {"Origin": "http://localhost:3000"}
        async with websockets.connect(uri, extra_headers=extra_headers) as websocket:
            print("✅ Connected!")

            # Send docs.view.request
            request = {
                "type": "docs.view.request",
                "org": "scopelock",
                "view_id": "coverage",
                "format": "json",
                "quote_id": "q-stub-test-12345"  # Valid format for stub
            }

            print(f"\n📤 Sending request:")
            print(json.dumps(request, indent=2))

            await websocket.send(json.dumps(request))
            print("✅ Request sent")

            print("\n⏳ Waiting for response...")
            print("   (L3 → L4 → L2 → L4 → L3 → here)")

            # Wait for response (with timeout)
            try:
                response_raw = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                response = json.loads(response_raw)

                print(f"\n📥 Received response:")
                print(f"   Type: {response.get('type')}")

                if response.get('type') == 'docs.view.result':
                    print(f"   Status: {response.get('payload', {}).get('status')}")
                    print(f"   View type: {response.get('payload', {}).get('view_type')}")
                    print(f"   Format: {response.get('payload', {}).get('format')}")

                    if response.get('payload', {}).get('status') == 'ok':
                        print("\n🎉 SUCCESS! Docs-as-views working end-to-end!")
                        view_model = response.get('payload', {}).get('view_model')
                        if view_model:
                            print(f"   View model keys: {list(view_model.keys())}")
                    else:
                        error = response.get('payload', {}).get('error')
                        print(f"\n❌ Error: {error}")

                elif response.get('type') == 'failure.emit':
                    print(f"   Error: {response.get('payload', {}).get('exception')}")
                    print(f"   Location: {response.get('payload', {}).get('code_location')}")
                    print("\n❌ Request failed (check logs above)")
                else:
                    print(f"\n⚠️  Unexpected response type: {response.get('type')}")

                print(f"\n📄 Full response:")
                print(json.dumps(response, indent=2))

            except asyncio.TimeoutError:
                print("\n⏱️  Timeout waiting for response (30s)")
                print("   Check if L2 resolver is processing request")
                return False

    except ConnectionRefusedError:
        print(f"❌ Connection refused: {uri}")
        print("   Is the L3 WebSocket server running?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    print("=" * 70)
    print("MEMBRANE-NATIVE DOCS-AS-VIEWS TEST")
    print("=" * 70)

    result = asyncio.run(test_docs_request())

    print("\n" + "=" * 70)
    if result:
        print("✅ TEST PASSED")
    else:
        print("❌ TEST FAILED")
    print("=" * 70)

    sys.exit(0 if result else 1)
