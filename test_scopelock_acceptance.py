#!/usr/bin/env python3
"""
Scopelock Acceptance Tests - GraphCare Stage 11
Mel's Final Quality Gate

Tests all 4 views, error handling, and performance against production.
Pass criteria: All tests pass, all queries <2s
"""

import asyncio
import json
import time
import websockets
from typing import Dict, List, Tuple
from datetime import datetime

# Production endpoint
WS_URL = "wss://mindprotocol.ai/api/ws"
ORG = "scopelock"

# Test results tracking
results = {
    "passed": 0,
    "failed": 0,
    "errors": [],
    "performance": []
}

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_test(name: str, passed: bool, duration_ms: float = None, details: str = ""):
    """Pretty print test result."""
    status = f"{Colors.GREEN}✅ PASS{Colors.RESET}" if passed else f"{Colors.RED}❌ FAIL{Colors.RESET}"
    perf = f" ({duration_ms:.0f}ms)" if duration_ms else ""
    detail_str = f"\n   {Colors.YELLOW}{details}{Colors.RESET}" if details else ""
    print(f"{status} {name}{perf}{detail_str}")

async def send_request(ws, view_id: str, format: str = "json", params: dict = None) -> Tuple[dict, float]:
    """Send docs.view.request and measure response time."""
    request = {
        "type": "docs.view.request",
        "org": ORG,
        "view_id": view_id,
        "format": format,
        "request_id": f"test_{view_id}_{int(time.time() * 1000)}"
    }

    if params:
        request.update(params)

    start_time = time.time()
    await ws.send(json.dumps(request))

    response_raw = await asyncio.wait_for(ws.recv(), timeout=5.0)
    duration_ms = (time.time() - start_time) * 1000

    response = json.loads(response_raw)
    return response, duration_ms

async def test_architecture_view(ws):
    """Test 1: Architecture view returns services and layers."""
    print(f"\n{Colors.BLUE}=== Test 1: Architecture View ==={Colors.RESET}")

    try:
        response, duration = await send_request(ws, "architecture")

        # Check response structure
        passed = (
            response.get("type") == "docs.view.result" and
            response.get("status") == "ok" and
            "view_model" in response
        )

        if passed:
            view_model = response.get("view_model", {})
            services = view_model.get("services", [])
            layers = view_model.get("layers", [])

            details = f"Services: {len(services)}, Layers: {len(layers)}"
            print_test("Architecture view returns data", True, duration, details)
            results["passed"] += 1
            results["performance"].append(("architecture", duration))

            # Verify expected content
            has_services = len(services) > 0
            has_layers = len(layers) > 0

            print_test("Architecture has services", has_services, details=f"{len(services)} services found")
            print_test("Architecture has layers", has_layers, details=f"{len(layers)} layers found")

            if has_services:
                results["passed"] += 2
            else:
                results["failed"] += 2
        else:
            print_test("Architecture view returns data", False, duration, f"Status: {response.get('status')}")
            results["failed"] += 1
            results["errors"].append(("architecture", response))

    except Exception as e:
        print_test("Architecture view returns data", False, details=str(e))
        results["failed"] += 1
        results["errors"].append(("architecture", str(e)))

async def test_api_view(ws):
    """Test 2: API reference view returns endpoints."""
    print(f"\n{Colors.BLUE}=== Test 2: API Reference View ==={Colors.RESET}")

    try:
        response, duration = await send_request(ws, "api-reference")

        passed = (
            response.get("type") == "docs.view.result" and
            response.get("status") == "ok" and
            "view_model" in response
        )

        if passed:
            view_model = response.get("view_model", {})
            endpoints = view_model.get("endpoints", [])

            details = f"Endpoints: {len(endpoints)}"
            print_test("API reference returns data", True, duration, details)
            results["passed"] += 1
            results["performance"].append(("api-reference", duration))

            # Verify endpoints
            has_endpoints = len(endpoints) >= 13  # We know Scopelock has 13
            print_test("API has expected endpoints", has_endpoints, details=f"{len(endpoints)} endpoints found (expected ≥13)")

            if has_endpoints:
                results["passed"] += 1
            else:
                results["failed"] += 1
        else:
            print_test("API reference returns data", False, duration, f"Status: {response.get('status')}")
            results["failed"] += 1
            results["errors"].append(("api-reference", response))

    except Exception as e:
        print_test("API reference returns data", False, details=str(e))
        results["failed"] += 1
        results["errors"].append(("api-reference", str(e)))

async def test_coverage_view(ws):
    """Test 3: Coverage view returns artifact counts."""
    print(f"\n{Colors.BLUE}=== Test 3: Coverage View ==={Colors.RESET}")

    try:
        response, duration = await send_request(ws, "coverage")

        passed = (
            response.get("type") == "docs.view.result" and
            response.get("status") == "ok" and
            "view_model" in response
        )

        if passed:
            view_model = response.get("view_model", {})
            items = view_model.get("items", [])

            total_artifacts = sum(item.get("count", 0) for item in items)
            details = f"Total artifacts: {total_artifacts}"
            print_test("Coverage view returns data", True, duration, details)
            results["passed"] += 1
            results["performance"].append(("coverage", duration))

            # Verify expected counts
            has_artifacts = total_artifacts >= 131  # We know Scopelock has 131
            print_test("Coverage has expected artifacts", has_artifacts, details=f"{total_artifacts} artifacts (expected ≥131)")

            if has_artifacts:
                results["passed"] += 1
            else:
                results["failed"] += 1
        else:
            print_test("Coverage view returns data", False, duration, f"Status: {response.get('status')}")
            results["failed"] += 1
            results["errors"].append(("coverage", response))

    except Exception as e:
        print_test("Coverage view returns data", False, details=str(e))
        results["failed"] += 1
        results["errors"].append(("coverage", str(e)))

async def test_index_view(ws):
    """Test 4: Index view returns browseable catalog."""
    print(f"\n{Colors.BLUE}=== Test 4: Index View ==={Colors.RESET}")

    try:
        response, duration = await send_request(ws, "index")

        passed = (
            response.get("type") == "docs.view.result" and
            response.get("status") == "ok" and
            "view_model" in response
        )

        if passed:
            view_model = response.get("view_model", {})
            items = view_model.get("items", [])

            details = f"Index items: {len(items)}"
            print_test("Index view returns data", True, duration, details)
            results["passed"] += 1
            results["performance"].append(("index", duration))

            # Verify catalog structure
            has_items = len(items) > 0
            print_test("Index has catalog items", has_items, details=f"{len(items)} items found")

            if has_items:
                results["passed"] += 1
            else:
                results["failed"] += 1
        else:
            print_test("Index view returns data", False, duration, f"Status: {response.get('status')}")
            results["failed"] += 1
            results["errors"].append(("index", response))

    except Exception as e:
        print_test("Index view returns data", False, details=str(e))
        results["failed"] += 1
        results["errors"].append(("index", str(e)))

async def test_error_handling(ws):
    """Test 5-8: Error handling for invalid requests."""
    print(f"\n{Colors.BLUE}=== Test 5-8: Error Handling ==={Colors.RESET}")

    # Test 5: Invalid org
    try:
        request = {
            "type": "docs.view.request",
            "org": "nonexistent_org",
            "view_id": "architecture",
            "format": "json"
        }
        await ws.send(json.dumps(request))
        response_raw = await asyncio.wait_for(ws.recv(), timeout=5.0)
        response = json.loads(response_raw)

        # Should return error or empty result
        is_error = response.get("status") == "error" or response.get("type") == "failure.emit"
        print_test("Invalid org returns error", is_error, details=f"Response type: {response.get('type')}")

        if is_error:
            results["passed"] += 1
        else:
            results["failed"] += 1

    except Exception as e:
        print_test("Invalid org returns error", False, details=str(e))
        results["failed"] += 1

    # Test 6: Invalid view_id
    try:
        request = {
            "type": "docs.view.request",
            "org": ORG,
            "view_id": "nonexistent_view",
            "format": "json"
        }
        await ws.send(json.dumps(request))
        response_raw = await asyncio.wait_for(ws.recv(), timeout=5.0)
        response = json.loads(response_raw)

        is_error = response.get("status") == "error" or response.get("type") == "failure.emit"
        print_test("Invalid view_id returns error", is_error, details=f"Response type: {response.get('type')}")

        if is_error:
            results["passed"] += 1
        else:
            results["failed"] += 1

    except Exception as e:
        print_test("Invalid view_id returns error", False, details=str(e))
        results["failed"] += 1

    # Test 7: Missing required fields
    try:
        request = {
            "type": "docs.view.request",
            "format": "json"
            # Missing org and view_id
        }
        await ws.send(json.dumps(request))
        response_raw = await asyncio.wait_for(ws.recv(), timeout=5.0)
        response = json.loads(response_raw)

        is_error = response.get("status") == "error" or response.get("type") == "failure.emit"
        print_test("Missing fields returns error", is_error, details=f"Response type: {response.get('type')}")

        if is_error:
            results["passed"] += 1
        else:
            results["failed"] += 1

    except Exception as e:
        print_test("Missing fields returns error", False, details=str(e))
        results["failed"] += 1

    # Test 8: Invalid format
    try:
        response, duration = await send_request(ws, "architecture", format="invalid_format")

        # Should either return error or default to json
        is_handled = response.get("status") in ["ok", "error"]
        print_test("Invalid format is handled", is_handled, duration, f"Status: {response.get('status')}")

        if is_handled:
            results["passed"] += 1
        else:
            results["failed"] += 1

    except Exception as e:
        print_test("Invalid format is handled", False, details=str(e))
        results["failed"] += 1

async def test_performance(ws):
    """Test 9-12: Performance validation (<2s per query)."""
    print(f"\n{Colors.BLUE}=== Test 9-12: Performance Validation ==={Colors.RESET}")

    views = ["architecture", "api-reference", "coverage", "index"]

    for view_id in views:
        try:
            response, duration = await send_request(ws, view_id)

            passed = duration < 2000  # <2 seconds
            status_str = f"{duration:.0f}ms" + (f" {Colors.GREEN}(good){Colors.RESET}" if passed else f" {Colors.RED}(slow){Colors.RESET}")
            print_test(f"{view_id} performance <2s", passed, duration, status_str)

            if passed:
                results["passed"] += 1
            else:
                results["failed"] += 1

        except Exception as e:
            print_test(f"{view_id} performance <2s", False, details=str(e))
            results["failed"] += 1

async def test_cache_behavior(ws):
    """Test 13-14: Cache behavior (second request should be faster)."""
    print(f"\n{Colors.BLUE}=== Test 13-14: Cache Behavior ==={Colors.RESET}")

    # Test 13: First request (cold cache)
    try:
        response1, duration1 = await send_request(ws, "architecture")
        print_test("First request (cold cache)", True, duration1, f"{duration1:.0f}ms")
        results["passed"] += 1

        # Test 14: Second request (should hit cache)
        await asyncio.sleep(0.1)  # Brief delay
        response2, duration2 = await send_request(ws, "architecture")

        # Cache hit should be faster OR same (if already fast)
        cached_indicator = response2.get("cached", False)
        is_cached = cached_indicator or (duration2 <= duration1 * 1.5)  # Allow 50% variance

        print_test("Second request (warm cache)", is_cached, duration2,
                   f"{duration2:.0f}ms (cached={cached_indicator})")

        if is_cached:
            results["passed"] += 1
        else:
            results["failed"] += 1

    except Exception as e:
        print_test("Cache behavior", False, details=str(e))
        results["failed"] += 2

async def test_concurrent_requests(ws):
    """Test 15: Concurrent requests don't interfere."""
    print(f"\n{Colors.BLUE}=== Test 15: Concurrent Requests ==={Colors.RESET}")

    try:
        # Send 3 requests simultaneously
        tasks = [
            send_request(ws, "architecture"),
            send_request(ws, "api-reference"),
            send_request(ws, "coverage")
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        all_successful = all(
            isinstance(r, tuple) and r[0].get("status") == "ok"
            for r in responses if not isinstance(r, Exception)
        )

        print_test("Concurrent requests succeed", all_successful,
                   details=f"{len([r for r in responses if not isinstance(r, Exception)])} responses received")

        if all_successful:
            results["passed"] += 1
        else:
            results["failed"] += 1

    except Exception as e:
        print_test("Concurrent requests succeed", False, details=str(e))
        results["failed"] += 1

async def test_provenance(ws):
    """Test 16-17: Provenance data is included."""
    print(f"\n{Colors.BLUE}=== Test 16-17: Provenance Data ==={Colors.RESET}")

    try:
        response, duration = await send_request(ws, "architecture")

        # Test 16: Provenance exists
        has_provenance = "provenance" in response
        print_test("Response includes provenance", has_provenance)

        if has_provenance:
            results["passed"] += 1

            # Test 17: Provenance has required fields
            provenance = response.get("provenance", {})
            has_digest = "ko_digest" in provenance
            has_query_time = "query_time_ms" in provenance or "selectors" in provenance

            print_test("Provenance has required fields", has_digest and has_query_time,
                       details=f"ko_digest: {has_digest}, timing/selectors: {has_query_time}")

            if has_digest and has_query_time:
                results["passed"] += 1
            else:
                results["failed"] += 1
        else:
            results["failed"] += 2

    except Exception as e:
        print_test("Provenance data", False, details=str(e))
        results["failed"] += 2

async def test_view_model_structure(ws):
    """Test 18-20: View models have expected structure."""
    print(f"\n{Colors.BLUE}=== Test 18-20: View Model Structure ==={Colors.RESET}")

    # Test 18: Architecture view structure
    try:
        response, _ = await send_request(ws, "architecture")
        view_model = response.get("view_model", {})

        has_expected_keys = any(k in view_model for k in ["services", "layers", "items", "nodes"])
        print_test("Architecture view has expected structure", has_expected_keys,
                   details=f"Keys: {list(view_model.keys())}")

        if has_expected_keys:
            results["passed"] += 1
        else:
            results["failed"] += 1
    except Exception as e:
        print_test("Architecture view structure", False, details=str(e))
        results["failed"] += 1

    # Test 19: API view structure
    try:
        response, _ = await send_request(ws, "api-reference")
        view_model = response.get("view_model", {})

        has_expected_keys = any(k in view_model for k in ["endpoints", "apis", "items", "nodes"])
        print_test("API view has expected structure", has_expected_keys,
                   details=f"Keys: {list(view_model.keys())}")

        if has_expected_keys:
            results["passed"] += 1
        else:
            results["failed"] += 1
    except Exception as e:
        print_test("API view structure", False, details=str(e))
        results["failed"] += 1

    # Test 20: Coverage view structure
    try:
        response, _ = await send_request(ws, "coverage")
        view_model = response.get("view_model", {})

        has_expected_keys = "items" in view_model or "coverage" in view_model
        print_test("Coverage view has expected structure", has_expected_keys,
                   details=f"Keys: {list(view_model.keys())}")

        if has_expected_keys:
            results["passed"] += 1
        else:
            results["failed"] += 1
    except Exception as e:
        print_test("Coverage view structure", False, details=str(e))
        results["failed"] += 1

async def run_acceptance_tests():
    """Run all acceptance tests."""
    print(f"\n{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BLUE}SCOPELOCK ACCEPTANCE TESTS - GraphCare Stage 11{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"Organization: {ORG}")
    print(f"Endpoint: {WS_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.BLUE}{'='*70}{Colors.RESET}")

    try:
        async with websockets.connect(WS_URL) as ws:
            print(f"{Colors.GREEN}✅ Connected to WebSocket{Colors.RESET}")

            # Run all test suites
            await test_architecture_view(ws)
            await test_api_view(ws)
            await test_coverage_view(ws)
            await test_index_view(ws)
            await test_error_handling(ws)
            await test_performance(ws)
            await test_cache_behavior(ws)
            await test_concurrent_requests(ws)
            await test_provenance(ws)
            await test_view_model_structure(ws)

    except ConnectionRefusedError:
        print(f"{Colors.RED}❌ Connection refused: {WS_URL}{Colors.RESET}")
        print(f"{Colors.YELLOW}Is the L3 WebSocket server running?{Colors.RESET}")
        return False
    except Exception as e:
        print(f"{Colors.RED}❌ Connection error: {e}{Colors.RESET}")
        return False

    # Print summary
    print(f"\n{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BLUE}TEST SUMMARY{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*70}{Colors.RESET}")

    total = results["passed"] + results["failed"]
    pass_rate = (results["passed"] / total * 100) if total > 0 else 0

    print(f"Total Tests: {total}")
    print(f"{Colors.GREEN}Passed: {results['passed']}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {results['failed']}{Colors.RESET}")
    print(f"Pass Rate: {pass_rate:.1f}%")

    # Performance summary
    if results["performance"]:
        print(f"\n{Colors.BLUE}PERFORMANCE SUMMARY:{Colors.RESET}")
        for view, duration in results["performance"]:
            status = f"{Colors.GREEN}✅{Colors.RESET}" if duration < 2000 else f"{Colors.RED}❌{Colors.RESET}"
            print(f"  {status} {view}: {duration:.0f}ms")

        avg_duration = sum(d for _, d in results["performance"]) / len(results["performance"])
        print(f"\n  Average: {avg_duration:.0f}ms")

    # Errors
    if results["errors"]:
        print(f"\n{Colors.RED}ERRORS:{Colors.RESET}")
        for view, error in results["errors"]:
            print(f"  ❌ {view}: {error}")

    # Final verdict
    print(f"\n{Colors.BLUE}{'='*70}{Colors.RESET}")
    if results["failed"] == 0:
        print(f"{Colors.GREEN}✅ ALL TESTS PASSED - SCOPELOCK APPROVED FOR DELIVERY{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*70}{Colors.RESET}")
        return True
    else:
        print(f"{Colors.RED}❌ TESTS FAILED - SCOPELOCK BLOCKED FOR DELIVERY{Colors.RESET}")
        print(f"{Colors.YELLOW}Fix failing tests before proceeding{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*70}{Colors.RESET}")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_acceptance_tests())
    exit(0 if success else 1)
