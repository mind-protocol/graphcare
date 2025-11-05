"""
TypeScript/TSX Ingestion Pipeline for GraphCare

Ingests extracted TypeScript code artifacts into FalkorDB using U4_Code_Artifact nodes.

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

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from services.embedding.embedding_service import get_embedding_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_falkordb_connection(graph_name: str):
    """Get FalkorDB graph connection."""
    try:
        from falkordb import FalkorDB
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


def create_typescript_artifact_node(
    graph,
    path: str,
    name: str,
    description: str,
    scope_ref: str,
    language: str,
    artifact_type: str,
    embedding: Optional[List[float]] = None,
    extra_properties: Optional[Dict[str, Any]] = None
) -> str:
    """Create U4_Code_Artifact node for TypeScript code."""
    now = int(datetime.utcnow().timestamp() * 1000)

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
        'visibility': 'public',
        'artifact_type': artifact_type
    }

    if embedding:
        properties['embedding'] = json.dumps(embedding)
        properties['embedding_dim'] = len(embedding)

    if extra_properties:
        properties.update(extra_properties)

    cypher = """
    MERGE (artifact:U4_Code_Artifact {path: $path})
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
        artifact.visibility = $visibility,
        artifact.artifact_type = $artifact_type
    ON MATCH SET
        artifact.updated_at = $updated_at
    """

    optional_props = ['embedding', 'embedding_dim', 'is_async', 'is_exported', 'body_lines', 'function_type']
    for prop in optional_props:
        if prop in properties:
            cypher += f",\n        artifact.{prop} = ${prop}"

    cypher += "\n    RETURN artifact.path as node_id"

    try:
        result = graph.query(cypher, properties)
        node_id = result.result_set[0][0] if result.result_set else path
        return node_id
    except Exception as e:
        logger.error(f"Failed to create U4_Code_Artifact node: {path}")
        logger.error(f"Error: {e}")
        raise


@dataclass
class TSIngestionStats:
    """Track ingestion statistics."""
    functions_ingested: int = 0
    components_ingested: int = 0
    classes_ingested: int = 0
    embeddings_generated: int = 0
    errors: int = 0


def ingest_typescript_results(
    extraction_json_path: Path,
    graph_name: str,
    scope_ref: str,
    language: str,
    generate_embeddings: bool = True
) -> TSIngestionStats:
    """
    Ingest TypeScript extraction results into FalkorDB.

    Args:
        extraction_json_path: Path to extraction JSON from typescript_extractor.py
        graph_name: FalkorDB graph name
        scope_ref: Client organization ID
        language: Programming language (typescript, javascript)
        generate_embeddings: Whether to generate semantic embeddings

    Returns:
        TSIngestionStats with counts
    """
    stats = TSIngestionStats()

    logger.info(f"Loading extraction results from: {extraction_json_path}")
    extraction_data = json.loads(extraction_json_path.read_text(encoding="utf-8"))

    graph = get_falkordb_connection(graph_name)

    embedding_service = None
    if generate_embeddings:
        logger.info("Initializing embedding service...")
        embedding_service = get_embedding_service()

    for file_path, file_data in extraction_data["files"].items():
        logger.info(f"\nProcessing: {file_path}")

        if file_data.get("parse_errors"):
            logger.warning(f"  ⚠️  Skipping (parse errors): {file_data['parse_errors']}")
            stats.errors += 1
            continue

        # Ingest functions
        for func in file_data["functions"]:
            try:
                artifact_path = f"{file_path}::{func['name']}"

                params = ", ".join(func.get("parameters", []))
                return_type = func.get("return_type", "unknown")
                description = f"Function: {func['name']}({params})"
                if return_type:
                    description += f" -> {return_type}"

                embedding = None
                if embedding_service:
                    code_snippet = f"function {func['name']}({params})"
                    if return_type:
                        code_snippet += f": {return_type}"

                    metadata = {
                        'path': artifact_path,
                        'lang': language,
                        'description': description
                    }

                    _, embedding = embedding_service.embed_code_artifact(code_snippet, metadata)
                    stats.embeddings_generated += 1

                create_typescript_artifact_node(
                    graph=graph,
                    path=artifact_path,
                    name=func['name'],
                    description=description,
                    scope_ref=scope_ref,
                    language=language,
                    artifact_type="function",
                    embedding=embedding,
                    extra_properties={
                        'is_async': func.get('is_async', False),
                        'is_exported': func.get('is_exported', False),
                        'body_lines': func.get('body_lines', 0),
                        'function_type': func.get('function_type', 'function'),
                        'parameters': json.dumps(func.get('parameters', []))
                    }
                )

                stats.functions_ingested += 1
                logger.info(f"  ✅ Function: {artifact_path}")

            except Exception as e:
                logger.error(f"  ❌ Failed to ingest function {func['name']}: {e}")
                stats.errors += 1

        # Ingest components
        for comp in file_data["components"]:
            try:
                artifact_path = f"{file_path}::{comp['name']}"

                description = f"{comp['component_type']}: {comp['name']}"
                if comp.get('props_type'):
                    description += f" (props: {comp['props_type']})"

                embedding = None
                if embedding_service:
                    code_snippet = f"React component {comp['name']}"
                    if comp.get('props_type'):
                        code_snippet += f" with props: {comp['props_type']}"

                    metadata = {
                        'path': artifact_path,
                        'lang': language,
                        'description': description
                    }

                    _, embedding = embedding_service.embed_code_artifact(code_snippet, metadata)
                    stats.embeddings_generated += 1

                create_typescript_artifact_node(
                    graph=graph,
                    path=artifact_path,
                    name=comp['name'],
                    description=description,
                    scope_ref=scope_ref,
                    language=language,
                    artifact_type="component",
                    embedding=embedding,
                    extra_properties={
                        'component_type': comp['component_type'],
                        'is_exported': comp.get('is_exported', False),
                        'is_default_export': comp.get('is_default_export', False)
                    }
                )

                stats.components_ingested += 1
                logger.info(f"  ✅ Component: {artifact_path}")

            except Exception as e:
                logger.error(f"  ❌ Failed to ingest component {comp['name']}: {e}")
                stats.errors += 1

        # Ingest classes
        for cls in file_data["classes"]:
            try:
                artifact_path = f"{file_path}::{cls['name']}"

                description = f"Class: {cls['name']}"
                if cls.get('extends'):
                    description += f" extends {cls['extends']}"

                embedding = None
                if embedding_service:
                    code_snippet = f"class {cls['name']}"
                    if cls.get('extends'):
                        code_snippet += f" extends {cls['extends']}"

                    metadata = {
                        'path': artifact_path,
                        'lang': language,
                        'description': description
                    }

                    _, embedding = embedding_service.embed_code_artifact(code_snippet, metadata)
                    stats.embeddings_generated += 1

                create_typescript_artifact_node(
                    graph=graph,
                    path=artifact_path,
                    name=cls['name'],
                    description=description,
                    scope_ref=scope_ref,
                    language=language,
                    artifact_type="class",
                    embedding=embedding,
                    extra_properties={
                        'extends': cls.get('extends', ''),
                        'implements': json.dumps(cls.get('implements', [])),
                        'is_exported': cls.get('is_exported', False)
                    }
                )

                stats.classes_ingested += 1
                logger.info(f"  ✅ Class: {artifact_path}")

            except Exception as e:
                logger.error(f"  ❌ Failed to ingest class {cls['name']}: {e}")
                stats.errors += 1

    return stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest TypeScript extraction results into FalkorDB")
    parser.add_argument("extraction_json", type=Path, help="Path to extraction JSON file")
    parser.add_argument("--graph", required=True, help="FalkorDB graph name")
    parser.add_argument("--scope", required=True, help="Client scope ref")
    parser.add_argument("--language", default="typescript", help="Programming language")
    parser.add_argument("--no-embeddings", action="store_true", help="Skip embedding generation")

    args = parser.parse_args()

    if not args.extraction_json.exists():
        print(f"Error: Extraction JSON not found: {args.extraction_json}")
        sys.exit(1)

    print(f"Ingesting TypeScript results into FalkorDB...")
    print(f"  Graph: {args.graph}")
    print(f"  Scope: {args.scope}")
    print(f"  Language: {args.language}")
    print("=" * 80)

    stats = ingest_typescript_results(
        extraction_json_path=args.extraction_json,
        graph_name=args.graph,
        scope_ref=args.scope,
        language=args.language,
        generate_embeddings=not args.no_embeddings
    )

    print("=" * 80)
    print("\nIngestion Summary:")
    print(f"  Functions ingested: {stats.functions_ingested}")
    print(f"  Components ingested: {stats.components_ingested}")
    print(f"  Classes ingested: {stats.classes_ingested}")
    print(f"  Embeddings generated: {stats.embeddings_generated}")
    print(f"  Errors: {stats.errors}")
    print("\n✅ Ingestion complete!")
