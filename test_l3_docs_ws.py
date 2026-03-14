import json
import sys
import types
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

if "websockets" not in sys.modules:
    ws_module = types.ModuleType("websockets")
    ws_module.connect = None
    ws_module.exceptions = types.SimpleNamespace(ConnectionClosed=Exception)
    ws_server_module = types.ModuleType("websockets.server")
    ws_server_module.WebSocketServerProtocol = object
    ws_module.server = ws_server_module
    sys.modules["websockets"] = ws_module
    sys.modules["websockets.server"] = ws_server_module

from services import l3_docs_ws




class FakeWs:
    def __init__(self):
        self.messages = []

    async def send(self, payload: str):
        self.messages.append(json.loads(payload))

class FakeSubscriber:
    def __init__(self):
        self.messages = []

    async def send(self, payload: str):
        self.messages.append(json.loads(payload))


class TestL3DocsWs(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        l3_docs_ws.VIEW_CACHE.clear()
        l3_docs_ws.SUBSCRIBERS.clear()

    def test_parse_graph_event(self):
        self.assertIsNone(l3_docs_ws.parse_graph_event("not-json"))
        self.assertIsNone(l3_docs_ws.parse_graph_event(json.dumps({"type": "docs.view.result"})))

        event = l3_docs_ws.parse_graph_event(json.dumps({"type": "graph.delta.node.upsert", "org": "acme"}))
        self.assertEqual(event["org"], "acme")



    def test_emit_query_audit_payload(self):
        with patch("builtins.print") as mocked_print:
            l3_docs_ws.emit_query_audit("acme", "MATCH (n) RETURN n", "ok", "rows=1")

        payload = json.loads(mocked_print.call_args.args[0])
        self.assertEqual(payload["type"], "graph.query.audit")
        self.assertEqual(payload["org"], "acme")
        self.assertEqual(payload["status"], "ok")
        self.assertIn("query_digest", payload)

    def test_is_quote_expired(self):
        future = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()
        past = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()

        self.assertFalse(l3_docs_ws.is_quote_expired({"quote_expires_at": future}))
        self.assertTrue(l3_docs_ws.is_quote_expired({"quote_expires_at": past}))
        self.assertTrue(l3_docs_ws.is_quote_expired({"quote_expires_at": "invalid"}))

    async def test_handle_view_request_rejects_expired_quote(self):
        ws = FakeWs()
        past = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()

        with patch("services.l3_docs_ws.compute_view") as mocked_compute:
            await l3_docs_ws.handle_view_request(
                ws,
                {"type": "docs.view.request", "org": "acme", "request_id": "r1", "quote_expires_at": past},
            )
            mocked_compute.assert_not_called()

        self.assertEqual(ws.messages[0]["type"], "error")
        self.assertEqual(ws.messages[0]["message"], "Quote expired")

    async def test_handle_graph_update_invalidates_cache_and_broadcasts(self):
        l3_docs_ws.VIEW_CACHE["acme:index"] = (datetime.now(), {"x": 1})
        l3_docs_ws.VIEW_CACHE["other:index"] = (datetime.now(), {"x": 2})

        ws = FakeSubscriber()
        l3_docs_ws.SUBSCRIBERS["acme"] = {ws}

        await l3_docs_ws.handle_graph_update({"type": "graph.delta.node.upsert", "org": "acme"})

        self.assertNotIn("acme:index", l3_docs_ws.VIEW_CACHE)
        self.assertIn("other:index", l3_docs_ws.VIEW_CACHE)
        self.assertEqual(ws.messages[0]["type"], "docs.cache.invalidated")
        self.assertEqual(ws.messages[0]["event_type"], "graph.delta.node.upsert")

    async def test_subscribe_loop_stops_after_max_retries(self):
        async def immediate_sleep(_):
            return None

        with patch("services.l3_docs_ws.websockets.connect", side_effect=RuntimeError("boom")), \
             patch("services.l3_docs_ws.asyncio.sleep", side_effect=immediate_sleep):
            await l3_docs_ws.subscribe_to_falkordb_events(
                ws_url="ws://invalid",
                reconnect_delay_seconds=0,
                max_retries=1,
            )


if __name__ == "__main__":
    unittest.main()
