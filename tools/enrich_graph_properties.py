#!/usr/bin/env python3
"""
Enrich Graph with Beam Search Properties

Adds properties required for Mind Protocol-style beam search:
- id: Unique identifier (uses FalkorDB ID + prefix)
- confidence: Quality score [0,1]
- base_weight: Node importance [0,1]
- energy: Edge strength [0,1]

Author: Mel (Chief Care Coordinator, GraphCare)
Date: 2025-11-05
"""

import requests
import sys

API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"


def execute_query(graph_name: str, cypher: str) -> dict:
    """Execute Cypher query."""
    payload = {"graph_name": graph_name, "query": cypher}
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def enrich_nodes(graph_name: str):
    """Add id, confidence, base_weight to all nodes."""

    print("Enriching nodes with beam search properties...")

    # Add id property (node_<FalkorDB_ID>)
    cypher = """
    MATCH (n)
    WHERE n.id IS NULL
    SET n.id = 'node_' + toString(ID(n))
    RETURN count(n) as updated
    """

    result = execute_query(graph_name, cypher)

    if 'error' in result:
        print(f"  ❌ Error adding id: {result['error']}")
        return False

    if 'result' in result and len(result['result']) >= 2 and result['result'][1]:
        count = result['result'][1][0][0]
        print(f"  ✅ Added id to {count} nodes")

    # Add confidence (default 0.7 for all nodes)
    cypher = """
    MATCH (n)
    WHERE n.confidence IS NULL
    SET n.confidence = 0.7
    RETURN count(n) as updated
    """

    result = execute_query(graph_name, cypher)

    if 'result' in result and len(result['result']) >= 2 and result['result'][1]:
        count = result['result'][1][0][0]
        print(f"  ✅ Added confidence to {count} nodes")

    # Add base_weight (intelligent defaults)
    # - Knowledge objects: 0.8 (documentation is valuable)
    # - Code artifacts: 0.6 (implementation details)
    # - Layers: 0.9 (architectural nodes are high-level)

    # Knowledge objects
    cypher = """
    MATCH (n:U4_Knowledge_Object)
    WHERE n.base_weight IS NULL
    SET n.base_weight = 0.8
    RETURN count(n) as updated
    """

    result = execute_query(graph_name, cypher)
    if 'result' in result and len(result['result']) >= 2 and result['result'][1]:
        count = result['result'][1][0][0]
        print(f"  ✅ Set base_weight=0.8 for {count} U4_Knowledge_Object nodes")

    # Code artifacts
    cypher = """
    MATCH (n:U4_Code_Artifact)
    WHERE n.base_weight IS NULL
    SET n.base_weight = 0.6
    RETURN count(n) as updated
    """

    result = execute_query(graph_name, cypher)
    if 'result' in result and len(result['result']) >= 2 and result['result'][1]:
        count = result['result'][1][0][0]
        print(f"  ✅ Set base_weight=0.6 for {count} U4_Code_Artifact nodes")

    # Layers
    cypher = """
    MATCH (n:Layer)
    WHERE n.base_weight IS NULL
    SET n.base_weight = 0.9
    RETURN count(n) as updated
    """

    result = execute_query(graph_name, cypher)
    if 'result' in result and len(result['result']) >= 2 and result['result'][1]:
        count = result['result'][1][0][0]
        print(f"  ✅ Set base_weight=0.9 for {count} Layer nodes")

    # Others
    cypher = """
    MATCH (n)
    WHERE n.base_weight IS NULL
    SET n.base_weight = 0.5
    RETURN count(n) as updated
    """

    result = execute_query(graph_name, cypher)
    if 'result' in result and len(result['result']) >= 2 and result['result'][1]:
        count = result['result'][1][0][0]
        print(f"  ✅ Set base_weight=0.5 for {count} other nodes")

    return True


def enrich_edges(graph_name: str):
    """Add confidence, energy to all edges."""

    print("\nEnriching edges with beam search properties...")

    # Add confidence (default 0.7)
    cypher = """
    MATCH ()-[r]->()
    WHERE r.confidence IS NULL
    SET r.confidence = 0.7
    RETURN count(r) as updated
    """

    result = execute_query(graph_name, cypher)

    if 'error' in result:
        print(f"  ❌ Error adding confidence: {result['error']}")
        return False

    if 'result' in result and len(result['result']) >= 2 and result['result'][1]:
        count = result['result'][1][0][0]
        print(f"  ✅ Added confidence to {count} edges")

    # Add energy (intelligent defaults based on relationship type)
    # - U4_IMPLEMENTS: 0.9 (strong code→doc link)
    # - U4_MEMBER_OF: 0.8 (hierarchical structure)
    # - U4_CALLS: 0.6 (code dependencies)
    # - IN_LAYER: 0.7 (architectural organization)
    # - Others: 0.5

    relationships = [
        ("U4_IMPLEMENTS", 0.9),
        ("U4_MEMBER_OF", 0.8),
        ("U4_CALLS", 0.6),
        ("IN_LAYER", 0.7),
        ("U4_DOCUMENTS", 0.8),
        ("U4_VALIDATES", 0.7),
        ("USES_SCHEMA", 0.6),
        ("EXPOSES", 0.6),
    ]

    for rel_type, energy_value in relationships:
        cypher = f"""
        MATCH ()-[r:{rel_type}]->()
        WHERE r.energy IS NULL
        SET r.energy = {energy_value}
        RETURN count(r) as updated
        """

        result = execute_query(graph_name, cypher)
        if 'result' in result and len(result['result']) >= 2 and result['result'][1]:
            count = result['result'][1][0][0]
            if count > 0:
                print(f"  ✅ Set energy={energy_value} for {count} {rel_type} edges")

    # Others
    cypher = """
    MATCH ()-[r]->()
    WHERE r.energy IS NULL
    SET r.energy = 0.5
    RETURN count(r) as updated
    """

    result = execute_query(graph_name, cypher)
    if 'result' in result and len(result['result']) >= 2 and result['result'][1]:
        count = result['result'][1][0][0]
        if count > 0:
            print(f"  ✅ Set energy=0.5 for {count} other edges")

    return True


def verify_enrichment(graph_name: str):
    """Verify all properties are set."""

    print("\nVerifying enrichment...")

    queries = [
        ("Nodes with id", "MATCH (n) WHERE n.id IS NOT NULL RETURN count(n)"),
        ("Nodes with confidence", "MATCH (n) WHERE n.confidence IS NOT NULL RETURN count(n)"),
        ("Nodes with base_weight", "MATCH (n) WHERE n.base_weight IS NOT NULL RETURN count(n)"),
        ("Edges with confidence", "MATCH ()-[r]->() WHERE r.confidence IS NOT NULL RETURN count(r)"),
        ("Edges with energy", "MATCH ()-[r]->() WHERE r.energy IS NOT NULL RETURN count(r)"),
    ]

    for label, cypher in queries:
        result = execute_query(graph_name, cypher)

        if 'result' in result and len(result['result']) >= 2 and result['result'][1]:
            count = result['result'][1][0][0]
            print(f"  {label}: {count}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python enrich_graph_properties.py <graph_name>")
        print("\nExample:")
        print("  python enrich_graph_properties.py scopelock")
        sys.exit(1)

    graph_name = sys.argv[1]

    print(f"Enriching graph: {graph_name}")
    print("=" * 80)
    print()

    # Enrich nodes
    if not enrich_nodes(graph_name):
        print("\n❌ Node enrichment failed")
        sys.exit(1)

    # Enrich edges
    if not enrich_edges(graph_name):
        print("\n❌ Edge enrichment failed")
        sys.exit(1)

    # Verify
    verify_enrichment(graph_name)

    print()
    print("=" * 80)
    print("✅ Graph enrichment complete!")
    print("\nNext steps:")
    print("  1. Run linter: python tools/lint_graph.py scopelock")
    print("  2. Test beam search: python tools/ask.py \"<question>\"")


if __name__ == "__main__":
    main()
