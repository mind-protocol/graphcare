"""
FalkorDB Ingestion Pipeline for GraphCare

Ingests extracted code artifacts into FalkorDB using U4_Code_Artifact nodes.
Generates semantic embeddings and creates relationship links (U4_CALLS, U4_DEPENDS_ON).

Author: Kai (Chief Engineer, GraphCare)
Created: 2025-11-04
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from services.embedding.embedding_service import get_embedding_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# FalkorDB Connection
# ============================================================================

def get_falkordb_connection(graph_name: str):
    """
    Get FalkorDB graph connection.

    Args:
        graph_name: Graph name (e.g., "graphcare_scopelock")

    Returns:
        FalkorDB Graph object
    """
    try:
        from falkordb import FalkorDB

        # Connect to FalkorDB
        db = FalkorDB(host='localhost', port=6379)
        graph = db.select_graph(graph_name)

        logger.info(f"Connected to FalkorDB graph: {graph_name}")
        return graph

    except ImportError:
        logger.error("FalkorDB Python client not installed. Run: pip install falkordb")
        raise
    except Exception as e:
        logger.error(f"Failed to connect to FalkorDB: {e}")
        raise


# ============================================================================
# Node Creation
# ============================================================================

def create_code_artifact_node(
    graph,
    path: str,
    name: str,
    description: str,
    scope_ref: str,
    language: str,
    lines_of_code: Optional[int] = None,
    complexity: Optional[int] = None,
    is_method: bool = False,
    parent_class: Optional[str] = None,
    embedding: Optional[List[float]] = None,
    extra_properties: Optional[Dict[str, Any]] = None
) -> str:
    """
    Create U4_Code_Artifact node in FalkorDB.

    Args:
        graph: FalkorDB graph connection
        path: Code path (file::class::function format)
        name: Artifact name (function/class name)
        description: Human-readable description
        scope_ref: Client organization ID (e.g., "org_scopelock")
        language: Programming language
        lines_of_code: Optional LOC count
        complexity: Optional cyclomatic complexity
        is_method: Whether this is a method (inside class)
        parent_class: Parent class name if method
        embedding: Optional 768-dim embedding vector
        extra_properties: Optional additional properties

    Returns:
        Node ID (path)
    """
    # Current timestamp
    now = int(datetime.utcnow().timestamp() * 1000)

    # Build properties
    properties = {
        'name': name,
        'path': path,
        'description': description,
        'type_name': 'U4_Code_Artifact',
        'level': 'L2',
        'scope_ref': scope_ref,
        'created_at': now,
        'updated_at': now,
        'valid_from': now,
        'language': language,
        'visibility': 'public'  # Default visibility
    }

    # Add optional properties
    if lines_of_code is not None:
        properties['lines_of_code'] = lines_of_code
    if complexity is not None:
        properties['complexity'] = complexity
    if is_method:
        properties['is_method'] = is_method
    if parent_class:
        properties['parent_class'] = parent_class
    if embedding:
        # Store embedding as string (FalkorDB doesn't support array properties natively)
        properties['embedding'] = json.dumps(embedding)
        properties['embedding_dim'] = len(embedding)

    # Add extra properties
    if extra_properties:
        properties.update(extra_properties)

    # Build Cypher MERGE query (idempotent)
    # Use path as unique identifier
    cypher = f"""
    MERGE (artifact:U4_Code_Artifact {{path: $path}})
    ON CREATE SET
        artifact.name = $name,
        artifact.description = $description,
        artifact.type_name = $type_name,
        artifact.level = $level,
        artifact.scope_ref = $scope_ref,
        artifact.created_at = $created_at,
        artifact.updated_at = $updated_at,
        artifact.valid_from = $valid_from,
        artifact.language = $language,
        artifact.visibility = $visibility
    ON MATCH SET
        artifact.updated_at = $updated_at
    """

    # Add optional properties to SET clause
    optional_props = ['lines_of_code', 'complexity', 'is_method', 'parent_class', 'embedding', 'embedding_dim']
    for prop in optional_props:
        if prop in properties:
            cypher += f",\n        artifact.{prop} = ${prop}"

    cypher += "\n    RETURN artifact.path as node_id"

    # Execute query
    try:
        result = graph.query(cypher, properties)
        node_id = result.result_set[0][0] if result.result_set else path
        return node_id

    except Exception as e:
        logger.error(f"Failed to create U4_Code_Artifact node: {path}")
        logger.error(f"Error: {e}")
        raise


def create_relationship_link(
    graph,
    source_path: str,
    target_path: str,
    link_type: str,
    confidence: float = 1.0,
    properties: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Create relationship link between code artifacts.

    Args:
        graph: FalkorDB graph connection
        source_path: Source artifact path
        target_path: Target artifact path
        link_type: Link type (U4_CALLS, U4_DEPENDS_ON, etc.)
        confidence: Confidence score (0-1)
        properties: Optional additional link properties

    Returns:
        True if successful
    """
    now = int(datetime.utcnow().timestamp() * 1000)

    # Build link properties
    link_props = {
        'confidence': confidence,
        'created_at': now,
        'valid_from': now
    }

    if properties:
        link_props.update(properties)

    # Build Cypher query
    cypher = f"""
    MATCH (source:U4_Code_Artifact {{path: $source_path}})
    MATCH (target:U4_Code_Artifact {{path: $target_path}})
    MERGE (source)-[r:{link_type}]->(target)
    ON CREATE SET
        r.confidence = $confidence,
        r.created_at = $created_at,
        r.valid_from = $valid_from
    RETURN count(r) as link_count
    """

    params = {
        'source_path': source_path,
        'target_path': target_path,
        'confidence': confidence,
        'created_at': now,
        'valid_from': now
    }

    try:
        result = graph.query(cypher, params)
        return True

    except Exception as e:
        logger.warning(f"Failed to create {link_type} link: {source_path} -> {target_path}")
        logger.warning(f"Error: {e}")
        return False


# ============================================================================
# Ingestion Pipeline
# ============================================================================

@dataclass
class IngestionStats:
    """Track ingestion statistics."""
    functions_ingested: int = 0
    classes_ingested: int = 0
    embeddings_generated: int = 0
    calls_linked: int = 0
    imports_linked: int = 0
    errors: int = 0


def ingest_extraction_results(
    extraction_json_path: Path,
    graph_name: str,
    scope_ref: str,
    language: str,
    generate_embeddings: bool = True
) -> IngestionStats:
    """
    Ingest extraction results into FalkorDB.

    Args:
        extraction_json_path: Path to extraction JSON from python_ast_extractor.py
        graph_name: FalkorDB graph name (e.g., "graphcare_scopelock")
        scope_ref: Client organization ID (e.g., "org_scopelock")
        language: Programming language (e.g., "python")
        generate_embeddings: Whether to generate semantic embeddings

    Returns:
        IngestionStats with counts
    """
    stats = IngestionStats()

    # Load extraction results
    logger.info(f"Loading extraction results from: {extraction_json_path}")
    extraction_data = json.loads(extraction_json_path.read_text(encoding="utf-8"))

    # Connect to FalkorDB
    graph = get_falkordb_connection(graph_name)

    # Initialize embedding service if needed
    embedding_service = None
    if generate_embeddings:
        logger.info("Initializing embedding service...")
        embedding_service = get_embedding_service()

    # Process each file
    for file_path, file_data in extraction_data["files"].items():
        logger.info(f"\nProcessing: {file_path}")

        # Skip files with parse errors
        if file_data.get("parse_errors"):
            logger.warning(f"  ⚠️  Skipping (parse errors): {file_data['parse_errors']}")
            stats.errors += 1
            continue

        # Ingest functions
        for func in file_data["functions"]:
            try:
                # Build path (file::class::function or file::function)
                if func.get("is_method") and func.get("parent_class"):
                    artifact_path = f"{file_path}::{func['parent_class']}::{func['name']}"
                else:
                    artifact_path = f"{file_path}::{func['name']}"

                # Build description
                desc_parts = []
                if func.get("docstring"):
                    desc_parts.append(func["docstring"].split("\n")[0][:200])  # First line, max 200 chars
                if func.get("parameters"):
                    params = ", ".join(func["parameters"])
                    desc_parts.append(f"Parameters: {params}")
                description = ". ".join(desc_parts) if desc_parts else f"Function: {func['name']}"

                # Generate embedding
                embedding = None
                if embedding_service:
                    # Build code snippet for embedding (signature + docstring)
                    code_snippet = f"def {func['name']}({', '.join(func['parameters'])})"
                    if func.get("return_type"):
                        code_snippet += f" -> {func['return_type']}"
                    if func.get("docstring"):
                        code_snippet += f":\n    \"\"\"{func['docstring'][:300]}\"\"\""

                    metadata = {
                        'path': artifact_path,
                        'lang': language,
                        'description': description
                    }

                    _, embedding = embedding_service.embed_code_artifact(code_snippet, metadata)
                    stats.embeddings_generated += 1

                # Calculate LOC (approximation from line_start/line_end)
                loc = func['line_end'] - func['line_start'] + 1 if func.get('line_end') else None

                # Create node
                create_code_artifact_node(
                    graph=graph,
                    path=artifact_path,
                    name=func['name'],
                    description=description,
                    scope_ref=scope_ref,
                    language=language,
                    lines_of_code=loc,
                    complexity=func.get('complexity'),
                    is_method=func.get('is_method', False),
                    parent_class=func.get('parent_class'),
                    embedding=embedding,
                    extra_properties={
                        'is_async': func.get('is_async', False),
                        'decorators': json.dumps(func.get('decorators', [])),
                        'parameters': json.dumps(func.get('parameters', [])),
                        'return_type': func.get('return_type', '')
                    }
                )

                stats.functions_ingested += 1
                logger.info(f"  ✅ Function: {artifact_path}")

            except Exception as e:
                logger.error(f"  ❌ Failed to ingest function {func['name']}: {e}")
                stats.errors += 1

        # Ingest classes
        for cls in file_data["classes"]:
            try:
                # Build path (file::class)
                artifact_path = f"{file_path}::{cls['name']}"

                # Build description
                desc_parts = []
                if cls.get("docstring"):
                    desc_parts.append(cls["docstring"].split("\n")[0][:200])
                if cls.get("bases"):
                    desc_parts.append(f"Inherits from: {', '.join(cls['bases'])}")
                description = ". ".join(desc_parts) if desc_parts else f"Class: {cls['name']}"

                # Generate embedding
                embedding = None
                if embedding_service:
                    # Build code snippet
                    code_snippet = f"class {cls['name']}"
                    if cls.get("bases"):
                        code_snippet += f"({', '.join(cls['bases'])})"
                    if cls.get("docstring"):
                        code_snippet += f":\n    \"\"\"{cls['docstring'][:300]}\"\"\""

                    metadata = {
                        'path': artifact_path,
                        'lang': language,
                        'description': description
                    }

                    _, embedding = embedding_service.embed_code_artifact(code_snippet, metadata)
                    stats.embeddings_generated += 1

                # Calculate LOC
                loc = cls['line_end'] - cls['line_start'] + 1 if cls.get('line_end') else None

                # Create node
                create_code_artifact_node(
                    graph=graph,
                    path=artifact_path,
                    name=cls['name'],
                    description=description,
                    scope_ref=scope_ref,
                    language=language,
                    lines_of_code=loc,
                    embedding=embedding,
                    extra_properties={
                        'bases': json.dumps(cls.get('bases', [])),
                        'decorators': json.dumps(cls.get('decorators', [])),
                        'methods': json.dumps(cls.get('methods', [])),
                        'attributes': json.dumps(cls.get('attributes', []))
                    }
                )

                stats.classes_ingested += 1
                logger.info(f"  ✅ Class: {artifact_path}")

            except Exception as e:
                logger.error(f"  ❌ Failed to ingest class {cls['name']}: {e}")
                stats.errors += 1

    # Second pass: Create U4_CALLS links
    logger.info("\n\nCreating U4_CALLS links...")
    for file_path, file_data in extraction_data["files"].items():
        for func in file_data["functions"]:
            # Build source path
            if func.get("is_method") and func.get("parent_class"):
                source_path = f"{file_path}::{func['parent_class']}::{func['name']}"
            else:
                source_path = f"{file_path}::{func['name']}"

            # Create links for each call
            for called_func in func.get("calls", []):
                # Try to find target function (simple heuristic: match by name)
                # Real implementation would need better resolution (imports, namespaces)
                for target_file, target_data in extraction_data["files"].items():
                    for target_func in target_data["functions"]:
                        if target_func["name"] == called_func or called_func.endswith(f".{target_func['name']}"):
                            # Build target path
                            if target_func.get("is_method") and target_func.get("parent_class"):
                                target_path = f"{target_file}::{target_func['parent_class']}::{target_func['name']}"
                            else:
                                target_path = f"{target_file}::{target_func['name']}"

                            # Create link
                            if create_relationship_link(graph, source_path, target_path, "U4_CALLS"):
                                stats.calls_linked += 1

    logger.info(f"  ✅ Created {stats.calls_linked} U4_CALLS links")

    return stats


# ============================================================================
# CLI Interface
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest code extraction results into FalkorDB")
    parser.add_argument("extraction_json", type=Path, help="Path to extraction JSON file")
    parser.add_argument("--graph", required=True, help="FalkorDB graph name (e.g., graphcare_scopelock)")
    parser.add_argument("--scope", required=True, help="Client scope ref (e.g., org_scopelock)")
    parser.add_argument("--language", default="python", help="Programming language (default: python)")
    parser.add_argument("--no-embeddings", action="store_true", help="Skip embedding generation")

    args = parser.parse_args()

    if not args.extraction_json.exists():
        print(f"Error: Extraction JSON not found: {args.extraction_json}")
        sys.exit(1)

    print(f"Ingesting extraction results into FalkorDB...")
    print(f"  Graph: {args.graph}")
    print(f"  Scope: {args.scope}")
    print(f"  Language: {args.language}")
    print(f"  Embeddings: {'Disabled' if args.no_embeddings else 'Enabled'}")
    print("=" * 80)

    stats = ingest_extraction_results(
        extraction_json_path=args.extraction_json,
        graph_name=args.graph,
        scope_ref=args.scope,
        language=args.language,
        generate_embeddings=not args.no_embeddings
    )

    print("=" * 80)
    print("\nIngestion Summary:")
    print(f"  Functions ingested: {stats.functions_ingested}")
    print(f"  Classes ingested: {stats.classes_ingested}")
    print(f"  Embeddings generated: {stats.embeddings_generated}")
    print(f"  U4_CALLS links created: {stats.calls_linked}")
    print(f"  U4_DEPENDS_ON links created: {stats.imports_linked}")
    print(f"  Errors: {stats.errors}")
    print("\n✅ Ingestion complete!")
