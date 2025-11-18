#!/usr/bin/env python3
"""
GraphCare Ask - Graph-Aware Semantic Question Answering

Adapted from Mind Protocol's beam search implementation for L2 organizational graphs.

Algorithm:
0. Build contextual query embedding
1. Candidate discovery via vector similarity (K=5 per label)
2. Beam search exploration (B=4, T=9 steps, alternating node→edges→node)
3. Path scoring: geometric_mean(node_scores + edge_scores)
   - Node score = cos_similarity × confidence × base_weight
   - Edge score = confidence × energy
4. Return best path with full context

Usage:
  python ask.py "How does Telegram bot work?"
  python ask.py "What validates proposals?" scopelock

Author: Mel (Chief Care Coordinator, GraphCare)
Date: 2025-11-05
Adapted from: Mind Protocol tools/doc_ingestion/ask.py
"""

import sys
import json
import math
import requests
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.embedding.embedding_service import get_embedding_service

# API Configuration
API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"

# Search Parameters (tunable)
K_PER_LABEL = 5         # Top-K candidates per node type
N_INITIAL = 6           # Initial nodes for beam
BEAM_WIDTH = 4          # Beam width for search
MAX_STEPS = 12          # Maximum traversal steps
MARGINAL_GAIN_THRESHOLD = 0.001  # Stop if improvement < 0.1% (was 0.01)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class PathState:
    """Represents a partial path in beam search."""
    nodes: List[str]                    # node IDs in path order
    edges: List[Tuple[str, str, str]]   # (source_id, edge_type, target_id)
    score: float                        # geometric mean path score
    last_step_type: str                 # 'node' or 'links'
    depth: int                          # number of steps taken


# ============================================================================
# QUERY EXECUTION
# ============================================================================

def execute_query(graph_name: str, cypher: str, params: Dict = None) -> Dict[str, Any]:
    """Execute Cypher query via REST API."""
    # FalkorDB REST doesn't support parameterized queries well, so we embed params
    if params:
        for key, value in params.items():
            if isinstance(value, list):
                # Convert list to Cypher array format
                if all(isinstance(x, str) for x in value):
                    value_str = "[" + ",".join(f"'{x}'" for x in value) + "]"
                else:
                    value_str = "[" + ",".join(str(x) for x in value) + "]"
                cypher = cypher.replace(f"${key}", value_str)
            elif isinstance(value, str):
                cypher = cypher.replace(f"${key}", f"'{value}'")
            else:
                cypher = cypher.replace(f"${key}", str(value))

    payload = {"graph_name": graph_name, "query": cypher}
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# ============================================================================
# CANDIDATE DISCOVERY
# ============================================================================

def discover_candidates(
    graph_name: str,
    query_vector: np.ndarray,
    k_per_label: int = K_PER_LABEL
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Discover top-K candidates per node type via semantic similarity.

    Returns: {label: [{id, labels, props, score_cos}, ...]}
    """
    # Known node types in graph
    node_types = ['U4_Code_Artifact', 'U4_Knowledge_Object', 'Layer']

    candidates = {}

    for label in node_types:
        # Fetch nodes with embeddings
        cypher = f"""
        MATCH (n:{label})
        WHERE n.embedding IS NOT NULL
        RETURN n.id AS id, labels(n) AS labels,
               n.name AS name, n.description AS description,
               n.confidence AS confidence, n.base_weight AS base_weight,
               n.embedding AS embedding
        LIMIT 100
        """

        result = execute_query(graph_name, cypher)

        if 'error' in result or 'result' not in result:
            continue

        if len(result['result']) < 2:
            continue

        columns = result['result'][0]
        rows = result['result'][1]

        label_candidates = []

        for row in rows:
            node_id = row[0]
            labels = row[1]
            name = row[2]
            description = row[3]
            confidence = row[4] if len(row) > 4 else 0.7
            base_weight = row[5] if len(row) > 5 else 0.5
            embedding_raw = row[6] if len(row) > 6 else None

            if not embedding_raw:
                continue

            # Parse embedding
            try:
                if isinstance(embedding_raw, str):
                    embedding_raw = embedding_raw.strip('[]')
                    node_embedding = np.array([float(x.strip()) for x in embedding_raw.split(',')])
                elif isinstance(embedding_raw, list):
                    node_embedding = np.array([float(x) for x in embedding_raw])
                else:
                    node_embedding = np.array(list(embedding_raw))

                # Compute cosine similarity
                cos_sim = float(np.dot(query_vector, node_embedding))

                label_candidates.append({
                    'id': node_id,
                    'labels': labels,
                    'props': {
                        'name': name,
                        'description': description,
                        'confidence': confidence,
                        'base_weight': base_weight
                    },
                    'score_cos': cos_sim
                })

            except Exception as e:
                continue

        # Sort by cosine similarity and take top-K
        label_candidates.sort(key=lambda c: c['score_cos'], reverse=True)
        candidates[label] = label_candidates[:k_per_label]

    return candidates


# ============================================================================
# SCORING
# ============================================================================

def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Clamp value to range."""
    if isinstance(value, str):
        try:
            value = float(value)
        except (ValueError, TypeError):
            value = 0.5
    return max(min_val, min(max_val, float(value)))


def node_score(node_props: Dict[str, Any], cosine_score: float) -> float:
    """
    Node score = cos(v_q, v_n) × confidence × base_weight
    """
    cos_clamped = clamp(cosine_score)
    confidence = clamp(node_props.get('confidence', 0.7))
    base_weight = clamp(node_props.get('base_weight', 0.5))

    return cos_clamped * confidence * base_weight


def edge_score(edge_props: Dict[str, Any]) -> float:
    """
    Edge score = confidence × energy
    """
    confidence = clamp(edge_props.get('confidence', 0.7))
    energy = clamp(edge_props.get('energy', 0.5))

    return confidence * energy


def path_score(node_scores: List[float], edge_scores: List[float]) -> float:
    """
    Path score = geometric mean of all node + edge scores
    S_path = exp( (Σ ln s_node + Σ ln s_edge) / (N + E) )
    """
    all_scores = node_scores + edge_scores
    if not all_scores:
        return 0.0

    epsilon = 1e-10
    log_sum = sum(math.log(max(s, epsilon)) for s in all_scores)

    return math.exp(log_sum / len(all_scores))


# ============================================================================
# BEAM SEARCH
# ============================================================================

def beam_search(
    graph_name: str,
    initial_nodes: List[Dict[str, Any]],
    query_vector: np.ndarray,
    beam_width: int = BEAM_WIDTH,
    max_steps: int = MAX_STEPS
) -> PathState:
    """
    Generic beam search exploration.

    Algorithm:
    - Start with top N nodes by relevance
    - Alternate: node → outgoing/incoming edges → nodes those edges touch
    - Score paths using geometric mean
    - De-dup nodes within path (no cycles)
    - Stop when reaching max steps or marginal gain < 1%

    Returns: Best path found
    """
    # Initialize beam with top N initial nodes
    beam: List[PathState] = []

    for node_data in initial_nodes[:N_INITIAL]:
        node_id = node_data['id']
        score = node_score(node_data['props'], node_data['score_cos'])

        beam.append(PathState(
            nodes=[node_id],
            edges=[],
            score=score,
            last_step_type='node',
            depth=1
        ))

    # Sort beam by score
    beam.sort(key=lambda s: s.score, reverse=True)
    beam = beam[:beam_width]

    if not beam:
        return PathState([], [], 0.0, 'node', 0)

    best_score = beam[0].score

    # Beam search loop
    for step in range(max_steps):
        new_beam = []

        for state in beam:
            if state.last_step_type == 'node':
                # Expand from node to edges
                last_node = state.nodes[-1]

                # Query outgoing AND incoming edges
                edge_query = f"""
                MATCH (n {{id: '{last_node}'}})-[r]-(m)
                WHERE m.id IS NOT NULL
                RETURN type(r) AS rel_type, startNode(r).id AS source_id,
                       endNode(r).id AS target_id,
                       r.confidence AS confidence, r.energy AS energy,
                       m.id AS target_id_check
                LIMIT 20
                """

                result = execute_query(graph_name, edge_query)

                if 'error' in result or 'result' not in result or len(result['result']) < 2:
                    continue

                for row in result['result'][1]:
                    rel_type = row[0]
                    source_id = row[1]
                    target_id = row[2]
                    confidence = row[3] if len(row) > 3 else 0.7
                    energy = row[4] if len(row) > 4 else 0.5

                    # Determine which end is the "other" node (not current node)
                    # For undirected edges, could be either source or target
                    if source_id == last_node:
                        other_node = target_id
                    elif target_id == last_node:
                        other_node = source_id
                    else:
                        # Edge doesn't touch current node (shouldn't happen)
                        continue

                    # Skip if other node already in path (avoid cycles)
                    if other_node in state.nodes:
                        continue

                    # Create new state with edge added
                    # Store edge with correct direction for this traversal
                    new_edges = state.edges + [(last_node, rel_type, other_node)]

                    edge_props = {'confidence': confidence, 'energy': energy}
                    e_score = edge_score(edge_props)

                    # Recompute path score with new edge
                    new_score = state.score * (e_score ** (1.0 / (len(state.nodes) + len(new_edges))))

                    new_beam.append(PathState(
                        nodes=state.nodes.copy(),
                        edges=new_edges,
                        score=new_score,
                        last_step_type='links',
                        depth=state.depth + 1
                    ))

            else:  # last_step_type == 'links'
                # Expand from links to target node (the "other" end of the edge)
                if not state.edges:
                    continue

                last_edge = state.edges[-1]
                # last_edge is (last_node, rel_type, other_node)
                # We want the other_node (the node we're traversing TO)
                target_id = last_edge[2]

                # Query target node properties
                node_query = f"""
                MATCH (n {{id: '{target_id}'}})
                RETURN n.id AS id, n.name AS name, n.confidence AS confidence,
                       n.base_weight AS base_weight, n.embedding AS embedding
                """
                result = execute_query(graph_name, node_query)

                if 'error' in result or 'result' not in result or len(result['result']) < 2:
                    continue

                if not result['result'][1]:
                    continue

                row = result['result'][1][0]
                node_id = row[0]
                confidence = row[2] if len(row) > 2 else 0.7
                base_weight = row[3] if len(row) > 3 else 0.5
                node_embedding_raw = row[4] if len(row) > 4 else None

                # Calculate cosine similarity
                cos_sim = 0.5  # fallback
                if node_embedding_raw:
                    try:
                        if isinstance(node_embedding_raw, str):
                            node_embedding_raw = node_embedding_raw.strip('[]')
                            node_embedding = np.array([float(x.strip()) for x in node_embedding_raw.split(',')])
                        else:
                            node_embedding = np.array(list(node_embedding_raw))
                        cos_sim = float(np.dot(query_vector, node_embedding))
                    except:
                        pass

                # Add node to path
                new_nodes = state.nodes + [target_id]
                node_props = {'confidence': confidence, 'base_weight': base_weight}
                n_score = node_score(node_props, cos_sim)

                # Recompute path score
                new_score = state.score * (n_score ** (1.0 / len(new_nodes)))

                new_beam.append(PathState(
                    nodes=new_nodes,
                    edges=state.edges.copy(),
                    score=new_score,
                    last_step_type='node',
                    depth=state.depth + 1
                ))

        if not new_beam:
            break

        # Sort and keep top beam_width
        new_beam.sort(key=lambda s: s.score, reverse=True)
        beam = new_beam[:beam_width]

        # Check marginal gain
        new_best_score = beam[0].score
        marginal_gain = (new_best_score - best_score) / (best_score + 1e-10)

        if marginal_gain < MARGINAL_GAIN_THRESHOLD:
            break

        best_score = new_best_score

    best = beam[0] if beam else PathState([], [], 0.0, 'node', 0)

    # DEBUG
    import os
    if os.environ.get('DEBUG_BEAM'):
        print(f"\n=== BEAM SEARCH DEBUG ===", file=sys.stderr)
        print(f"Best path: {len(best.nodes)} nodes, {len(best.edges)} edges", file=sys.stderr)
        print(f"Nodes: {best.nodes}", file=sys.stderr)
        print(f"Edges: {best.edges}", file=sys.stderr)

    return best


# ============================================================================
# HYDRATION & SERIALIZATION
# ============================================================================

def hydrate_and_serialize(graph_name: str, path: PathState) -> List[Dict[str, Any]]:
    """
    Hydrate full path and serialize as: node → links → node → ...
    """
    if not path.nodes:
        return []

    # Batch query to get all nodes in path
    node_ids_str = "'" + "','".join(path.nodes) + "'"
    nodes_query = f"""
    MATCH (n)
    WHERE n.id IN [{node_ids_str}]
    RETURN n.id AS id, labels(n) AS labels,
           n.name AS name, n.description AS description, n.path AS path,
           n.ko_type AS ko_type, n.lang AS lang
    """

    result = execute_query(graph_name, nodes_query)

    nodes_by_id = {}
    if 'result' in result and len(result['result']) >= 2:
        for row in result['result'][1]:
            node_id = row[0]
            labels = row[1]
            name = row[2]
            description = row[3]
            node_path = row[4] if len(row) > 4 else None
            ko_type = row[5] if len(row) > 5 else None
            lang = row[6] if len(row) > 6 else None

            nodes_by_id[node_id] = {
                'type': 'node',
                'id': node_id,
                'labels': labels,
                'name': name,
                'description': description,
                'path': node_path,
                'ko_type': ko_type,
                'lang': lang
            }

    # Get all edges in path - organize by position in path, not by source
    edges_between_nodes = []
    for i in range(len(path.nodes) - 1):
        current_node = path.nodes[i]
        next_node = path.nodes[i + 1]

        # Find the edge(s) that connect these two nodes
        for source_id, rel_type, target_id in path.edges:
            if (source_id == current_node and target_id == next_node) or \
               (source_id == next_node and target_id == current_node):
                # Query this specific edge
                edge_query = f"""
                MATCH (s {{id: '{source_id}'}})-[r:`{rel_type}`]-(t {{id: '{target_id}'}})
                RETURN type(r) AS rel_type, r.confidence AS confidence, r.energy AS energy,
                       s.id AS source, t.id AS target
                LIMIT 1
                """

                result = execute_query(graph_name, edge_query)

                if 'result' in result and len(result['result']) >= 2 and result['result'][1]:
                    row = result['result'][1][0]
                    rel_type_actual = row[0]
                    confidence = row[1] if len(row) > 1 else None
                    energy = row[2] if len(row) > 2 else None
                    actual_source = row[3] if len(row) > 3 else source_id
                    actual_target = row[4] if len(row) > 4 else target_id

                    edges_between_nodes.append({
                        'rel_type': rel_type_actual,
                        'source': actual_source,
                        'target': actual_target,
                        'confidence': confidence,
                        'energy': energy
                    })
                    break  # Found the edge for this position

    # Serialize as sequence: node → links → node → links → node → ...
    cluster = []
    for i, node_id in enumerate(path.nodes):
        # Add node
        if node_id in nodes_by_id:
            cluster.append(nodes_by_id[node_id])
        else:
            # Node not hydrated - add placeholder
            cluster.append({
                'type': 'node',
                'id': node_id,
                'labels': [],
                'name': f'(node {node_id})',
                'description': None
            })

        # Add links to next node (if not last node)
        if i < len(path.nodes) - 1 and i < len(edges_between_nodes):
            cluster.append({
                'type': 'links',
                'items': [edges_between_nodes[i]]
            })

    return cluster


# ============================================================================
# MAIN
# ============================================================================

def ask(question: str, graph_name: str = "scopelock") -> Dict[str, Any]:
    """
    Execute the ask algorithm.

    Returns: JSON-serializable result dict
    """
    # Initialize embedding service
    embedding_service = get_embedding_service()

    # Build query embedding
    query_vector = embedding_service.embed(question)

    # Candidate discovery
    candidates = discover_candidates(graph_name, query_vector)

    # Flatten candidates for initial beam (top N globally by score)
    all_candidates = []
    for label, label_cands in candidates.items():
        all_candidates.extend(label_cands)

    # Sort by cosine score (relevance)
    all_candidates.sort(key=lambda c: c['score_cos'], reverse=True)

    if not all_candidates:
        return {
            'query': question,
            'graph': graph_name,
            'cluster': [],
            'notes': 'No candidates found (graph may be empty or have no embeddings)'
        }

    # Beam search exploration
    best_path = beam_search(graph_name, all_candidates, query_vector)

    # Hydrate and serialize
    cluster = hydrate_and_serialize(graph_name, best_path)

    # Emit result
    return {
        'query': question,
        'graph': graph_name,
        'cluster': cluster,
        'path_score': round(best_path.score, 4),
        'path_depth': best_path.depth,
        'notes': f'Beam search found {len(cluster)} elements in path'
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python ask.py \"<question>\" [graph_name]")
        print("\nExamples:")
        print("  python ask.py \"How does Telegram bot work?\"")
        print("  python ask.py \"What validates proposals?\" scopelock")
        print("\nReturns: JSON with query, cluster (path), path_score, notes")
        sys.exit(1)

    question = sys.argv[1]
    graph_name = sys.argv[2] if len(sys.argv) > 2 else "scopelock"

    try:
        result = ask(question, graph_name)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({
            'error': str(e),
            'query': question,
            'graph': graph_name
        }, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
