#!/usr/bin/env python3
"""
Import documentation structure to FalkorDB.
Handles U4_Knowledge_Object nodes and U4_MEMBER_OF relationships.
"""

import json
import sys
import requests
from pathlib import Path

# FalkorDB configuration
API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"
GRAPH_NAME = "scopelock"

def execute_cypher(cypher: str) -> dict:
    """Execute Cypher query via REST API."""
    payload = {
        "graph_name": GRAPH_NAME,
        "query": cypher
    }

    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def escape_string(s: str) -> str:
    """Escape string for Cypher."""
    if s is None:
        return ""
    return s.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", "\\n")

def create_knowledge_object_node(node: dict) -> str:
    """Generate Cypher for U4_Knowledge_Object node."""
    props = node['properties']

    # Build property string
    prop_parts = []
    prop_parts.append(f"name: '{escape_string(props['name'])}'")
    prop_parts.append(f"description: '{escape_string(props.get('description', ''))}'")
    prop_parts.append(f"ko_type: '{props['ko_type']}'")
    prop_parts.append(f"path: '{escape_string(props['path'])}'")
    prop_parts.append(f"scope_ref: '{props['scope_ref']}'")
    prop_parts.append(f"level: '{props['level']}'")
    prop_parts.append(f"section_type: '{props['section_type']}'")
    prop_parts.append(f"line_start: {props['line_start']}")
    prop_parts.append(f"line_end: {props['line_end']}")
    prop_parts.append(f"content_length: {props['content_length']}")

    if props.get('markdown_content'):
        content = escape_string(props['markdown_content'][:500])  # Limit size
        prop_parts.append(f"markdown_content: '{content}'")

    props_str = ", ".join(prop_parts)

    cypher = f"""
    MERGE (n:U4_Knowledge_Object {{id: '{node['id']}'}})
    ON CREATE SET n += {{{props_str}}}
    ON MATCH SET n += {{{props_str}}}
    """

    return cypher

def create_relationship(rel: dict) -> str:
    """Generate Cypher for U4_MEMBER_OF relationship."""
    props = rel['properties']

    prop_parts = []
    prop_parts.append(f"membership_type: '{props['membership_type']}'")
    prop_parts.append(f"role: '{escape_string(props['role'])}'")
    prop_parts.append(f"scope_ref: '{props['scope_ref']}'")

    props_str = ", ".join(prop_parts)

    cypher = f"""
    MATCH (source {{id: '{rel['source']}'}})
    MATCH (target {{id: '{rel['target']}'}})
    MERGE (source)-[r:U4_MEMBER_OF {{{props_str}}}]->(target)
    """

    return cypher

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 import_docs_structure.py <extraction_json>")
        sys.exit(1)

    extraction_path = Path(sys.argv[1])

    if not extraction_path.exists():
        print(f"Error: {extraction_path} not found")
        sys.exit(1)

    print(f"Loading: {extraction_path}")
    data = json.loads(extraction_path.read_text())

    nodes = data['nodes']
    relationships = data['relationships']

    print(f"\nImporting to FalkorDB:")
    print(f"  Graph: {GRAPH_NAME}")
    print(f"  Endpoint: {API_URL}")
    print(f"  Nodes: {len(nodes)}")
    print(f"  Relationships: {len(relationships)}")
    print()

    # Import nodes
    print("Creating U4_Knowledge_Object nodes...")
    nodes_created = 0
    errors = 0

    for i, node in enumerate(nodes):
        cypher = create_knowledge_object_node(node)
        result = execute_cypher(cypher)

        if result['success']:
            nodes_created += 1
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i + 1}/{len(nodes)}")
        else:
            errors += 1
            print(f"  ❌ Error creating node {node['id']}: {result['error']}")

    print(f"✅ Nodes created: {nodes_created}/{len(nodes)}")

    # Import relationships
    print("\nCreating U4_MEMBER_OF relationships...")
    rels_created = 0

    for i, rel in enumerate(relationships):
        cypher = create_relationship(rel)
        result = execute_cypher(cypher)

        if result['success']:
            rels_created += 1
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i + 1}/{len(relationships)}")
        else:
            errors += 1
            print(f"  ❌ Error creating relationship {rel['source']} → {rel['target']}: {result['error']}")

    print(f"✅ Relationships created: {rels_created}/{len(relationships)}")

    print()
    print("="*80)
    print("Import Summary")
    print("="*80)
    print(f"Nodes: {nodes_created}/{len(nodes)}")
    print(f"Relationships: {rels_created}/{len(relationships)}")
    print(f"Errors: {errors}")

    if errors == 0:
        print("\n✅ Import complete!")
    else:
        print(f"\n⚠️  Import complete with {errors} errors")

if __name__ == "__main__":
    main()
