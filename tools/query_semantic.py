#!/usr/bin/env python3
"""
Semantic Query Tool for Scopelock Graph
Query the graph using natural language questions.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
import numpy as np
from services.embedding.embedding_service import get_embedding_service

API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"
GRAPH_NAME = "scopelock"

def semantic_search(question: str, limit: int = 10, node_type: str = None):
    """
    Search graph using natural language question.

    Args:
        question: Natural language query
        limit: Number of results to return
        node_type: Filter by node type (U4_Code_Artifact, U4_Knowledge_Object, Layer)

    Returns:
        List of (similarity, node_data) tuples
    """
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

    # Generate query embedding
    print(f"🔍 Searching for: '{question}'")
    print()

    embedding_service = get_embedding_service()
    query_embedding = embedding_service.embed(question)

    # Build Cypher query
    if node_type:
        cypher = f"""
        MATCH (n:{node_type})
        WHERE n.embedding IS NOT NULL
        RETURN ID(n) as id, n.name as name, n.path as path, n.description as description,
               n.embedding as embedding, labels(n) as labels, n.ko_type as ko_type,
               n.section_type as section_type, n.lang as lang
        """
    else:
        cypher = """
        MATCH (n)
        WHERE n.embedding IS NOT NULL
        RETURN ID(n) as id, n.name as name, n.path as path, n.description as description,
               n.embedding as embedding, labels(n) as labels, n.ko_type as ko_type,
               n.section_type as section_type, n.lang as lang
        """

    payload = {"graph_name": GRAPH_NAME, "query": cypher}
    response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    result = response.json()

    if 'result' not in result or len(result['result']) < 2:
        print("❌ No results found (graph may be empty)")
        return []

    columns = result['result'][0]
    rows = result['result'][1]

    # Compute similarities
    similarities = []
    for row in rows:
        try:
            node_id = row[0]
            name = row[1]
            path = row[2]
            description = row[3]
            embedding_raw = row[4]
            labels = row[5]
            ko_type = row[6] if len(row) > 6 else None
            section_type = row[7] if len(row) > 7 else None
            lang = row[8] if len(row) > 8 else None

            # Parse embedding
            if isinstance(embedding_raw, str):
                embedding_raw = embedding_raw.strip('[]')
                node_embedding = [float(x.strip()) for x in embedding_raw.split(',')]
            elif isinstance(embedding_raw, list):
                node_embedding = [float(x) for x in embedding_raw]
            else:
                node_embedding = list(embedding_raw)

            # Cosine similarity
            similarity = np.dot(query_embedding, node_embedding)

            node_data = {
                'id': node_id,
                'name': name,
                'path': path,
                'description': description,
                'labels': labels,
                'ko_type': ko_type,
                'section_type': section_type,
                'lang': lang
            }

            similarities.append((similarity, node_data))

        except Exception as e:
            continue

    # Sort by similarity
    similarities.sort(reverse=True)

    return similarities[:limit]

def format_result(rank: int, similarity: float, node: dict):
    """Pretty print a search result."""
    name = node['name'] or f"node_{node['id']}"
    labels = node['labels']

    if isinstance(labels, list):
        label_str = labels[0] if labels else 'Unknown'
    else:
        label_str = str(labels)

    # Build context string
    context_parts = []
    if node['ko_type']:
        context_parts.append(f"type: {node['ko_type']}")
    if node['lang']:
        context_parts.append(f"lang: {node['lang']}")
    if node['path']:
        path_short = node['path'][:50] + "..." if len(node['path']) > 50 else node['path']
        context_parts.append(f"path: {path_short}")

    context_str = " | ".join(context_parts) if context_parts else ""

    print(f"{rank:2}. [{similarity:.3f}] {name[:60]}")
    print(f"    └─ {label_str}")
    if context_str:
        print(f"    └─ {context_str}")
    if node['description']:
        desc = node['description'][:100] + "..." if len(node['description']) > 100 else node['description']
        print(f"    └─ {desc}")
    print()

def main():
    if len(sys.argv) < 2:
        print("Usage: python query_semantic.py <question> [limit] [node_type]")
        print()
        print("Examples:")
        print("  python query_semantic.py 'How does Telegram bot work?'")
        print("  python query_semantic.py 'upwork proposal submission' 20")
        print("  python query_semantic.py 'validation pattern' 10 U4_Knowledge_Object")
        print()
        print("Node types: U4_Code_Artifact, U4_Knowledge_Object, Layer")
        sys.exit(1)

    question = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    node_type = sys.argv[3] if len(sys.argv) > 3 else None

    results = semantic_search(question, limit, node_type)

    if not results:
        print("No results found.")
        return

    print(f"📊 Top {len(results)} results:")
    print("=" * 80)
    print()

    for i, (similarity, node) in enumerate(results, 1):
        format_result(i, similarity, node)

if __name__ == "__main__":
    main()
