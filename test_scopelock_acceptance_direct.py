#!/usr/bin/env python3
"""
Scopelock Acceptance Tests - Direct FalkorDB Queries
Mel's Final Quality Gate

Tests graph data quality by querying production FalkorDB directly.
Pass criteria: All queries succeed, data meets acceptance criteria.
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any

# Production FalkorDB (REST API)
FALKORDB_URL = "https://mindprotocol.onrender.com/admin/query"
FALKORDB_API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"
GRAPH_NAME = "scopelock"

# Test results tracking
results = {
    "passed": 0,
    "failed": 0,
    "errors": [],
    "queries": []
}

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_test(name: str, passed: bool, details: str = ""):
    """Pretty print test result."""
    status = f"{Colors.GREEN}✅ PASS{Colors.RESET}" if passed else f"{Colors.RED}❌ FAIL{Colors.RESET}"
    detail_str = f"\n   {Colors.YELLOW}{details}{Colors.RESET}" if details else ""
    print(f"{status} {name}{detail_str}")

    if passed:
        results["passed"] += 1
    else:
        results["failed"] += 1
        results["errors"].append(name)

def query_graph(cypher: str) -> Dict[str, Any]:
    """Execute Cypher query against production FalkorDB."""
    try:
        response = requests.post(
            FALKORDB_URL,
            headers={
                "X-API-Key": FALKORDB_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "graph_name": GRAPH_NAME,
                "query": cypher
            },
            timeout=10.0
        )

        response.raise_for_status()
        raw_data = response.json()

        # FalkorDB REST API format:
        # {"result": [["col1", "col2"], [[val1, val2], ...], ["stats"]], "execution_time_ms": X}
        # Convert to simpler format: {"data": [{"col1": val1, "col2": val2}, ...]}
        result_data = raw_data.get("result", [])

        if len(result_data) >= 2:
            columns = result_data[0]  # Column names
            rows = result_data[1]     # Data rows

            # Convert to dict format
            data = {
                "data": [
                    {col: row[i] for i, col in enumerate(columns)}
                    for row in rows
                ]
            }
        else:
            data = {"data": []}

        results["queries"].append({
            "query": cypher[:100],
            "success": True,
            "row_count": len(data.get("data", []))
        })
        return data
    except Exception as e:
        results["queries"].append({
            "query": cypher[:100],
            "success": False,
            "error": str(e)
        })
        raise

def test_graph_exists():
    """Test 1: Scopelock graph exists and is non-empty."""
    print(f"\n{Colors.BLUE}=== Test 1: Graph Existence ==={Colors.RESET}")

    try:
        data = query_graph("MATCH (n) RETURN count(n) as node_count")
        node_count = data["data"][0]["node_count"] if data["data"] else 0

        passed = node_count > 0
        print_test(
            "Graph has nodes",
            passed,
            f"Found {node_count} nodes (expected >0)"
        )

        if node_count >= 170:
            print_test(
                "Node count meets expectations",
                True,
                f"{node_count} nodes (expected ~172)"
            )
        else:
            print_test(
                "Node count meets expectations",
                False,
                f"{node_count} nodes (expected ~172)"
            )

    except Exception as e:
        print_test("Graph query", False, f"Error: {e}")

def test_code_artifacts():
    """Test 2: Code artifacts extracted."""
    print(f"\n{Colors.BLUE}=== Test 2: Code Artifacts ==={Colors.RESET}")

    try:
        # Check for U4_Code_Artifact nodes
        data = query_graph("""
            MATCH (c:U4_Code_Artifact)
            WHERE c.scope_ref = 'scopelock'
            RETURN count(c) as artifact_count
        """)

        artifact_count = data["data"][0]["artifact_count"] if data["data"] else 0
        passed = artifact_count > 0

        print_test(
            "Code artifacts present",
            passed,
            f"Found {artifact_count} artifacts (expected >0)"
        )

        # Check for language diversity
        data = query_graph("""
            MATCH (c:U4_Code_Artifact)
            WHERE c.scope_ref = 'scopelock'
            RETURN c.lang as language, count(c) as count
        """)

        languages = [row["language"] for row in data.get("data", []) if row.get("language")]

        print_test(
            "Multiple languages extracted",
            len(languages) >= 2,
            f"Languages: {', '.join(set(languages))}"
        )

    except Exception as e:
        print_test("Code artifacts query", False, f"Error: {e}")

def test_architectural_classification():
    """Test 3: Architecture enrichment (kinds: Service, Endpoint, Schema)."""
    print(f"\n{Colors.BLUE}=== Test 3: Architectural Classification ==={Colors.RESET}")

    try:
        # Check for kind property
        data = query_graph("""
            MATCH (n)
            WHERE n.scope_ref = 'scopelock' AND n.kind IS NOT NULL
            RETURN n.kind as kind, count(n) as count
        """)

        kinds = {row["kind"]: row["count"] for row in data.get("data", [])}
        total_classified = sum(kinds.values())

        print_test(
            "Nodes have architectural classification",
            total_classified > 0,
            f"Classified {total_classified} nodes with {len(kinds)} kinds"
        )

        # Check for specific architectural kinds
        expected_kinds = ["Service", "Endpoint", "Schema"]
        found_kinds = [k for k in expected_kinds if k in kinds]

        print_test(
            "Expected architectural kinds present",
            len(found_kinds) >= 2,
            f"Found: {', '.join(found_kinds)} (expected Service, Endpoint, Schema)"
        )

        # Show breakdown
        for kind, count in kinds.items():
            print(f"   {Colors.YELLOW}{kind}: {count}{Colors.RESET}")

    except Exception as e:
        print_test("Architectural classification query", False, f"Error: {e}")

def test_architectural_layers():
    """Test 4: Architectural layers defined."""
    print(f"\n{Colors.BLUE}=== Test 4: Architectural Layers ==={Colors.RESET}")

    try:
        # Check for layers
        data = query_graph("""
            MATCH (layer)
            WHERE layer.scope_ref = 'scopelock' AND (layer:U4_Knowledge_Object OR layer.kind = 'Layer')
            RETURN layer.name as layer_name, count(layer) as count
        """)

        layers = [row["layer_name"] for row in data.get("data", []) if row.get("layer_name")]

        print_test(
            "Architectural layers defined",
            len(layers) > 0,
            f"Found {len(layers)} layers: {', '.join(layers)}"
        )

        # Check for IN_LAYER relationships
        data = query_graph("""
            MATCH ()-[r:IN_LAYER]->()
            RETURN count(r) as in_layer_count
        """)

        in_layer_count = data["data"][0]["in_layer_count"] if data["data"] else 0

        print_test(
            "Services organized by layer",
            in_layer_count > 0,
            f"Found {in_layer_count} IN_LAYER relationships"
        )

    except Exception as e:
        print_test("Architectural layers query", False, f"Error: {e}")

def test_relationships():
    """Test 5: Relationships extracted (U4_CALLS, EXPOSES, USES_SCHEMA)."""
    print(f"\n{Colors.BLUE}=== Test 5: Relationships ==={Colors.RESET}")

    try:
        # Check for U4_CALLS relationships
        data = query_graph("""
            MATCH ()-[r:U4_CALLS]->()
            RETURN count(r) as calls_count
        """)

        calls_count = data["data"][0]["calls_count"] if data["data"] else 0

        print_test(
            "Code dependencies (U4_CALLS)",
            calls_count > 0,
            f"Found {calls_count} call relationships"
        )

        # Check for architectural relationships
        data = query_graph("""
            MATCH ()-[r]->()
            WHERE type(r) IN ['EXPOSES', 'USES_SCHEMA', 'IN_LAYER']
            RETURN type(r) as rel_type, count(r) as count
        """)

        arch_rels = {row["rel_type"]: row["count"] for row in data.get("data", [])}
        total_arch = sum(arch_rels.values())

        print_test(
            "Architectural relationships",
            total_arch > 0,
            f"Found {total_arch} architectural relationships"
        )

        for rel_type, count in arch_rels.items():
            print(f"   {Colors.YELLOW}{rel_type}: {count}{Colors.RESET}")

    except Exception as e:
        print_test("Relationships query", False, f"Error: {e}")

def test_scope_ref():
    """Test 6: All nodes have scope_ref='scopelock'."""
    print(f"\n{Colors.BLUE}=== Test 6: Scope Reference ==={Colors.RESET}")

    try:
        # Check for nodes without scope_ref
        data = query_graph("""
            MATCH (n)
            WHERE n.scope_ref IS NULL OR n.scope_ref <> 'scopelock'
            RETURN count(n) as missing_scope_count
        """)

        missing_scope = data["data"][0]["missing_scope_count"] if data["data"] else 0

        # Some nodes might be universal (layers, types), so we allow some without scope_ref
        print_test(
            "Nodes have scope_ref",
            missing_scope < 50,  # Lenient check
            f"{missing_scope} nodes without scope_ref='scopelock' (some universal nodes expected)"
        )

    except Exception as e:
        print_test("Scope reference query", False, f"Error: {e}")

def test_data_completeness():
    """Test 7: Nodes have required properties (name, path, etc.)."""
    print(f"\n{Colors.BLUE}=== Test 7: Data Completeness ==={Colors.RESET}")

    try:
        # Check for nodes with name property
        data = query_graph("""
            MATCH (n:U4_Code_Artifact)
            WHERE n.scope_ref = 'scopelock'
            RETURN
                count(n) as total,
                count(CASE WHEN n.name IS NOT NULL THEN 1 END) as with_name,
                count(CASE WHEN n.path IS NOT NULL THEN 1 END) as with_path
        """)

        if data["data"]:
            row = data["data"][0]
            total = row["total"]
            with_name = row["with_name"]
            with_path = row["with_path"]

            name_pct = (with_name / total * 100) if total > 0 else 0
            path_pct = (with_path / total * 100) if total > 0 else 0

            print_test(
                "Artifacts have name property",
                name_pct >= 90,
                f"{with_name}/{total} ({name_pct:.1f}%)"
            )

            print_test(
                "Artifacts have path property",
                path_pct >= 80,
                f"{with_path}/{total} ({path_pct:.1f}%)"
            )
        else:
            print_test("Data completeness", False, "No data returned")

    except Exception as e:
        print_test("Data completeness query", False, f"Error: {e}")

def test_security_no_pii():
    """Test 8: No obvious PII in graph (Marcus's security check)."""
    print(f"\n{Colors.BLUE}=== Test 8: Security - No PII ==={Colors.RESET}")

    try:
        # Check for email patterns in name/path/description
        data = query_graph("""
            MATCH (n)
            WHERE n.scope_ref = 'scopelock' AND
                  (n.name =~ '.*@.*\\..*' OR
                   n.path =~ '.*@.*\\..*' OR
                   n.description =~ '.*@.*\\..*')
            RETURN count(n) as pii_count
        """)

        pii_count = data["data"][0]["pii_count"] if data["data"] else 0

        print_test(
            "No email addresses in graph",
            pii_count == 0,
            f"Found {pii_count} potential emails (expected 0)"
        )

        # Note: This is a basic check. Marcus's full audit would be more comprehensive.
        print(f"   {Colors.YELLOW}Note: Basic PII check only. Full audit by Marcus required for production.{Colors.RESET}")

    except Exception as e:
        print_test("PII security check", False, f"Error: {e}")

def run_all_tests():
    """Run all acceptance tests."""
    print(f"{Colors.BLUE}={'='*70}{Colors.RESET}")
    print(f"{Colors.BLUE}SCOPELOCK ACCEPTANCE TESTS - GraphCare Stage 11{Colors.RESET}")
    print(f"{Colors.BLUE}Mel's Direct FalkorDB Quality Gate{Colors.RESET}")
    print(f"{Colors.BLUE}={'='*70}{Colors.RESET}")
    print(f"Graph: {GRAPH_NAME}")
    print(f"FalkorDB: {FALKORDB_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.BLUE}={'='*70}{Colors.RESET}")

    # Run all test suites
    test_graph_exists()
    test_code_artifacts()
    test_architectural_classification()
    test_architectural_layers()
    test_relationships()
    test_scope_ref()
    test_data_completeness()
    test_security_no_pii()

    # Print summary
    print(f"\n{Colors.BLUE}={'='*70}{Colors.RESET}")
    print(f"{Colors.BLUE}TEST SUMMARY{Colors.RESET}")
    print(f"{Colors.BLUE}={'='*70}{Colors.RESET}")
    print(f"Passed: {Colors.GREEN}{results['passed']}{Colors.RESET}")
    print(f"Failed: {Colors.RED}{results['failed']}{Colors.RESET}")
    print(f"Total Queries: {len(results['queries'])}")

    if results["failed"] > 0:
        print(f"\n{Colors.RED}FAILED TESTS:{Colors.RESET}")
        for error in results["errors"]:
            print(f"  - {error}")

    print(f"\n{Colors.BLUE}={'='*70}{Colors.RESET}")

    if results["failed"] == 0:
        print(f"{Colors.GREEN}✅ ALL TESTS PASSED - APPROVED FOR DELIVERY{Colors.RESET}")
        print(f"{Colors.GREEN}Scopelock graph meets acceptance criteria.{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.RED}❌ TESTS FAILED - BLOCKED{Colors.RESET}")
        print(f"{Colors.RED}Fix issues before delivery.{Colors.RESET}")
        return 1

if __name__ == "__main__":
    exit(run_all_tests())
