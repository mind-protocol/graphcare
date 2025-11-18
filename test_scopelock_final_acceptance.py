#!/usr/bin/env python3
"""
Scopelock Final Acceptance Tests
Tests for consciousness design pattern extraction (PATTERN → BEHAVIOR_SPEC → ... → GUIDE)
"""

import requests
from typing import Dict

API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"
GRAPH_NAME = "scopelock"

results = {"passed": 0, "failed": 0, "errors": []}

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def query_graph(cypher: str) -> Dict:
    """Execute Cypher and parse results."""
    payload = {"graph_name": GRAPH_NAME, "query": cypher}
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

    response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    raw = response.json()

    result_data = raw.get("result", [])
    if len(result_data) >= 2:
        columns = result_data[0]
        rows = result_data[1]
        return {"data": [{col: row[i] for i, col in enumerate(columns)} for row in rows]}
    return {"data": []}

def print_test(name: str, passed: bool, details: str = ""):
    """Print test result."""
    status = f"{Colors.GREEN}✅{Colors.RESET}" if passed else f"{Colors.RED}❌{Colors.RESET}"
    detail_str = f"\n   {Colors.YELLOW}{details}{Colors.RESET}" if details else ""
    print(f"{status} {name}{detail_str}")

    if passed:
        results["passed"] += 1
    else:
        results["failed"] += 1
        results["errors"].append(name)

def main():
    print(f"{Colors.BLUE}{'='*80}{Colors.RESET}")
    print(f"{Colors.BLUE}SCOPELOCK FINAL ACCEPTANCE TESTS{Colors.RESET}")
    print(f"{Colors.BLUE}Consciousness Design Pattern Extraction{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*80}{Colors.RESET}\n")

    # Test 1: Total nodes
    print(f"{Colors.BLUE}=== Test 1: Graph Completeness ==={Colors.RESET}")
    data = query_graph("MATCH (n) RETURN count(n) as total")
    total_nodes = data["data"][0]["total"] if data["data"] else 0

    print_test(
        "Total nodes in graph",
        total_nodes > 200,
        f"{total_nodes} nodes (expected >200)"
    )

    # Test 2: Code artifacts
    data = query_graph("MATCH (c:U4_Code_Artifact) RETURN count(c) as count")
    code_count = data["data"][0]["count"] if data["data"] else 0

    print_test(
        "Code artifacts present",
        code_count == 131,
        f"{code_count} artifacts (expected 131)"
    )

    # Test 3: Documentation knowledge objects
    print(f"\n{Colors.BLUE}=== Test 2: Documentation Structure ==={Colors.RESET}")

    data = query_graph("""
        MATCH (k:U4_Knowledge_Object)
        WHERE k.scope_ref = 'scopelock'
        RETURN count(k) as total
    """)
    ko_count = data["data"][0]["total"] if data["data"] else 0

    print_test(
        "Knowledge objects extracted",
        ko_count == 86,
        f"{ko_count} knowledge objects (expected 86)"
    )

    # Test 4: Breakdown by ko_type
    data = query_graph("""
        MATCH (k:U4_Knowledge_Object)
        WHERE k.scope_ref = 'scopelock'
        RETURN k.ko_type as ko_type, count(k) as count
        ORDER BY ko_type
    """)

    ko_types = {row["ko_type"]: row["count"] for row in data["data"]}

    expected_types = {"pattern": 15, "spec": 15, "validation": 14, "mechanism": 14, "algorithm": 14, "guide": 14}

    for ko_type, expected_count in expected_types.items():
        actual_count = ko_types.get(ko_type, 0)
        print_test(
            f"ko_type='{ko_type}' count",
            actual_count >= expected_count - 2,  # Allow small variance
            f"{actual_count} (expected ~{expected_count})"
        )

    # Test 5: Hierarchical relationships
    print(f"\n{Colors.BLUE}=== Test 3: Consciousness Design Hierarchy ==={Colors.RESET}")

    data = query_graph("""
        MATCH ()-[r:U4_MEMBER_OF]->()
        WHERE r.scope_ref = 'scopelock'
        RETURN count(r) as count
    """)
    member_of_count = data["data"][0]["count"] if data["data"] else 0

    print_test(
        "U4_MEMBER_OF relationships (hierarchy)",
        member_of_count == 71,
        f"{member_of_count} relationships (expected 71)"
    )

    # Test 6: Sample hierarchy path
    data = query_graph("""
        MATCH (pattern:U4_Knowledge_Object {ko_type: 'pattern'})
        MATCH (spec:U4_Knowledge_Object {ko_type: 'spec'})
        MATCH (spec)-[:U4_MEMBER_OF]->(pattern)
        RETURN count(*) as count
    """)
    pattern_spec_links = data["data"][0]["count"] if data["data"] else 0

    print_test(
        "BEHAVIOR_SPEC → PATTERN links",
        pattern_spec_links > 0,
        f"{pattern_spec_links} links found"
    )

    # Test 7: Code to documentation links
    print(f"\n{Colors.BLUE}=== Test 4: Code → Documentation Links ==={Colors.RESET}")

    data = query_graph("""
        MATCH ()-[r:U4_IMPLEMENTS]->()
        RETURN count(r) as count
    """)
    implements_count = data["data"][0]["count"] if data["data"] else 0

    print_test(
        "U4_IMPLEMENTS relationships",
        implements_count == 92,
        f"{implements_count} code→doc links (expected 92)"
    )

    # Test 8: Sample code→guide link
    data = query_graph("""
        MATCH (code:U4_Code_Artifact)-[:U4_IMPLEMENTS]->(guide:U4_Knowledge_Object {ko_type: 'guide'})
        RETURN count(*) as count
    """)
    code_guide_links = data["data"][0]["count"] if data["data"] else 0

    print_test(
        "Code artifacts implement GUIDE sections",
        code_guide_links > 0,
        f"{code_guide_links} code→GUIDE links"
    )

    # Test 9: Architectural layers
    print(f"\n{Colors.BLUE}=== Test 5: Architectural Layers ==={Colors.RESET}")

    data = query_graph("""
        MATCH (layer)
        WHERE (layer:Layer OR layer.kind = 'Layer')
        RETURN count(layer) as count
    """)
    layer_count = data["data"][0]["count"] if data["data"] else 0

    print_test(
        "Architectural layers defined",
        layer_count >= 4,
        f"{layer_count} layers (expected ≥4)"
    )

    # Test 10: IN_LAYER relationships
    data = query_graph("""
        MATCH ()-[r:IN_LAYER]->()
        RETURN count(r) as count
    """)
    in_layer_count = data["data"][0]["count"] if data["data"] else 0

    print_test(
        "IN_LAYER relationships",
        in_layer_count >= 30,
        f"{in_layer_count} relationships (expected ≥30)"
    )

    # Summary
    print(f"\n{Colors.BLUE}{'='*80}{Colors.RESET}")
    print(f"{Colors.BLUE}SUMMARY{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*80}{Colors.RESET}")
    print(f"Passed: {Colors.GREEN}{results['passed']}{Colors.RESET}")
    print(f"Failed: {Colors.RED}{results['failed']}{Colors.RESET}")

    if results["failed"] > 0:
        print(f"\n{Colors.RED}Failed tests:{Colors.RESET}")
        for error in results["errors"]:
            print(f"  - {error}")

    print(f"\n{Colors.BLUE}{'='*80}{Colors.RESET}")

    if results["failed"] == 0:
        print(f"{Colors.GREEN}✅ ALL TESTS PASSED - APPROVED FOR DELIVERY{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.RED}❌ {results['failed']} TESTS FAILED{Colors.RESET}")
        return 1

if __name__ == "__main__":
    exit(main())
