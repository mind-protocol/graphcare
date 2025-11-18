#!/usr/bin/env python3
"""
Systematic Embedding for All Graph Nodes
Embeds U4_Knowledge_Object and U4_Code_Artifact nodes with relevant field combinations.
"""

import requests
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.embedding.embedding_service import get_embedding_service

# FalkorDB configuration
API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"
GRAPH_NAME = "scopelock"

def execute_cypher(cypher: str) -> dict:
    """Execute Cypher query."""
    payload = {"graph_name": GRAPH_NAME, "query": cypher}
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        raw = response.json()

        result_data = raw.get("result", [])
        if len(result_data) >= 2:
            columns = result_data[0]
            rows = result_data[1]
            return {"success": True, "data": [
                {col: row[i] for i, col in enumerate(columns)}
                for row in rows
            ]}
        return {"success": True, "data": []}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_nodes_to_embed() -> Dict[str, List[Dict]]:
    """Get all nodes that need embeddings, organized by label."""
    nodes = {}

    # Known node types in Scopelock graph
    KNOWN_LABELS = [
        'U4_Knowledge_Object',
        'U4_Code_Artifact',
        'Layer',
        'GraphCare_Schema'
    ]

    print("Fetching nodes by type...")
    print()

    # For each known label, fetch nodes with specific properties
    for label in KNOWN_LABELS:
        print(f"Fetching {label} nodes...")

        # Query specific properties based on label
        if label == 'U4_Knowledge_Object':
            cypher = f"""
            MATCH (n:{label})
            RETURN ID(n) as id, n.name as name, n.description as description,
                   n.markdown_content as markdown_content, n.ko_type as ko_type,
                   n.section_type as section_type, n.path as path
            """
        elif label == 'U4_Code_Artifact':
            cypher = f"""
            MATCH (n:{label})
            RETURN ID(n) as id, n.name as name, n.description as description,
                   n.path as path, n.lang as lang
            """
        elif label == 'Layer':
            cypher = f"""
            MATCH (n:{label})
            RETURN ID(n) as id, n.name as name, n.description as description,
                   n.purpose as purpose
            """
        else:
            cypher = f"""
            MATCH (n:{label})
            RETURN ID(n) as id, n.name as name, n.description as description
            """

        result = execute_cypher(cypher)

        if result['success']:
            node_list = []
            for row in result['data']:
                # Build properties dict from returned columns
                properties = {k: v for k, v in row.items() if k != 'id'}

                node_data = {
                    'id': row['id'],
                    'labels': [label],
                    'properties': properties
                }
                node_list.append(node_data)

            nodes[label] = node_list
            print(f"  Found {len(node_list)} {label} nodes")
        else:
            print(f"  Error fetching {label}: {result['error']}")
            nodes[label] = []

    # Get unlabeled or other nodes
    print(f"Fetching unlabeled/other nodes...")
    where_clause = " AND ".join([f"NOT n:{label}" for label in KNOWN_LABELS])
    cypher = f"""
    MATCH (n)
    WHERE {where_clause}
    RETURN ID(n) as id, n.name as name, n.description as description,
           n.kind as kind, n.type as type
    """

    result = execute_cypher(cypher)

    if result['success']:
        node_list = []
        for row in result['data']:
            properties = {k: v for k, v in row.items() if k != 'id'}

            node_data = {
                'id': row['id'],
                'labels': ['Other'],
                'properties': properties
            }
            node_list.append(node_data)

        if node_list:
            nodes['Other'] = node_list
            print(f"  Found {len(node_list)} other nodes")
    else:
        print(f"  Error fetching other nodes: {result['error']}")

    return nodes

def build_embedding_text(node: Dict, node_type: str) -> str:
    """Build text to embed based on node type and available fields."""

    # Extract properties from nested structure
    props = node.get('properties', {})
    labels = node.get('labels', [])

    # Priority fields for embedding (in order of importance)
    PRIORITY_FIELDS = [
        'name', 'title', 'description', 'summary',
        'markdown_content', 'content', 'text', 'body',
        'ko_type', 'kind', 'type', 'category',
        'path', 'file_path', 'location',
        'lang', 'language',
        'role', 'purpose', 'definition'
    ]

    # Build embedding text based on node type
    parts = []

    # Add node type/label information
    if labels:
        parts.append(f"Type: {', '.join(labels)}")

    # Type-specific handling for rich nodes
    if node_type == 'U4_Knowledge_Object' or 'U4_Knowledge_Object' in labels:
        # Knowledge objects: prioritize semantic content
        if props.get('name'):
            parts.append(f"Section: {props['name']}")

        if props.get('ko_type'):
            parts.append(f"Knowledge Type: {props['ko_type']}")

        if props.get('section_type'):
            parts.append(f"Section Type: {props['section_type']}")

        if props.get('description'):
            parts.append(f"Description: {props['description']}")

        if props.get('markdown_content'):
            # Limit to 2000 chars for embedding
            content = str(props['markdown_content'])[:2000]
            parts.append(f"Content: {content}")

    elif node_type == 'U4_Code_Artifact' or 'U4_Code_Artifact' in labels:
        # Code artifacts: name + path + context
        if props.get('name'):
            parts.append(f"Code: {props['name']}")

        if props.get('lang'):
            parts.append(f"Language: {props['lang']}")

        if props.get('path'):
            path = str(props['path'])
            parts.append(f"Path: {path}")

            # Infer context from path
            path_lower = path.lower()
            contexts = []
            if 'webhook' in path_lower:
                contexts.append("webhook handler")
            if 'telegram' in path_lower:
                contexts.append("Telegram integration")
            if 'automation' in path_lower or 'browser' in path_lower:
                contexts.append("browser automation")
            if 'runner' in path_lower:
                contexts.append("AI runner")
            if 'database' in path_lower or 'model' in path_lower:
                contexts.append("database model")

            if contexts:
                parts.append(f"Context: {', '.join(contexts)}")

        if props.get('description'):
            parts.append(f"Description: {props['description']}")

    elif node_type == 'Layer' or 'Layer' in labels:
        # Architectural layers
        if props.get('name'):
            parts.append(f"Layer: {props['name']}")

        if props.get('description'):
            parts.append(f"Description: {props['description']}")

        if props.get('purpose'):
            parts.append(f"Purpose: {props['purpose']}")

    else:
        # Generic node: extract all priority fields
        for field in PRIORITY_FIELDS:
            value = props.get(field)
            if value:
                # Convert to string and limit length
                value_str = str(value)
                if len(value_str) > 2000:
                    value_str = value_str[:2000]
                parts.append(f"{field.title()}: {value_str}")

                # Stop after we have enough content
                if len(parts) >= 5:
                    break

    # If we still have no content, extract ALL text fields
    if len(parts) <= 1:  # Only has type info
        for key, value in props.items():
            if isinstance(value, str) and len(value) > 0:
                value_str = str(value)[:500]  # Limit each field
                parts.append(f"{key}: {value_str}")

                if len(parts) >= 5:
                    break

    embedding_text = "\n\n".join(parts)

    # Fallback: if still empty, use just the node type
    if not embedding_text.strip():
        embedding_text = f"Node type: {node_type}"

    return embedding_text

def embed_node(node_id: int, embedding: List[float]) -> bool:
    """Update node with embedding vector."""
    # Convert embedding to Cypher array format
    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"

    cypher = f"""
    MATCH (n)
    WHERE ID(n) = {node_id}
    SET n.embedding = {embedding_str}
    """

    result = execute_cypher(cypher)
    return result['success']

def main():
    print("="*80)
    print("Systematic Graph Node Embedding")
    print("="*80)
    print()

    # Initialize embedding service
    print("Initializing embedding service...")
    embedding_service = get_embedding_service()
    print(f"  Using model: {embedding_service.__class__.__name__}")
    print()

    # Get all nodes to embed
    nodes_by_type = get_nodes_to_embed()

    total_nodes = sum(len(nodes) for nodes in nodes_by_type.values())
    print(f"\nTotal nodes to embed: {total_nodes}")
    print()

    # Process each node type
    embedded_count = 0
    error_count = 0

    for node_type, nodes in nodes_by_type.items():
        if not nodes:
            continue

        print(f"Processing {node_type} ({len(nodes)} nodes)...")
        print()

        for i, node in enumerate(nodes):
            try:
                # Build embedding text
                text = build_embedding_text(node, node_type)

                if not text.strip():
                    print(f"  ⚠️  Skipping node {node['id']} (no text to embed)")
                    continue

                # Generate embedding
                embedding = embedding_service.embed(text)

                # Update node
                success = embed_node(node['id'], embedding)

                if success:
                    embedded_count += 1
                    node_name = node.get('name', 'unknown')[:50]
                    if (i + 1) % 10 == 0:
                        print(f"  Progress: {i + 1}/{len(nodes)} embedded")
                else:
                    error_count += 1
                    print(f"  ❌ Failed to embed node {node['id']}")

            except Exception as e:
                error_count += 1
                print(f"  ❌ Error embedding node {node.get('id', 'unknown')}: {e}")

        print(f"  ✅ {node_type}: {embedded_count} embedded")
        print()

    print()
    print("="*80)
    print("Embedding Summary")
    print("="*80)
    print(f"Total nodes embedded: {embedded_count}/{total_nodes}")
    print(f"Errors: {error_count}")

    # Breakdown by type
    print("\nBreakdown by type:")
    for node_type, nodes in nodes_by_type.items():
        if nodes:
            print(f"  {node_type}: {len(nodes)} nodes")

    if error_count == 0:
        print("\n✅ All nodes embedded successfully!")
    else:
        print(f"\n⚠️  Completed with {error_count} errors")

    # Verify embeddings
    print("\nVerifying embeddings...")

    for node_type in nodes_by_type.keys():
        if node_type == 'U4_Knowledge_Object':
            result = execute_cypher("""
                MATCH (k:U4_Knowledge_Object)
                WHERE k.scope_ref = 'scopelock' AND k.embedding IS NOT NULL
                RETURN count(k) as count
            """)
        elif node_type == 'U4_Code_Artifact':
            result = execute_cypher("""
                MATCH (c:U4_Code_Artifact)
                WHERE c.embedding IS NOT NULL
                RETURN count(c) as count
            """)
        else:
            continue

        if result['success'] and result['data']:
            count = result['data'][0]['count']
            print(f"  {node_type}: {count} nodes with embeddings")

    print()

if __name__ == "__main__":
    main()
