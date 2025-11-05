"""
FalkorDB Ingestion Pipeline (REST API Mode)

Ingests extracted code artifacts into FalkorDB using REST API.
For production Render deployment where direct Redis connection is not available.

Author: Nora (Chief Architect, GraphCare)
Created: 2025-11-04
"""

import json
import sys
import requests
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
# REST API Configuration
# ============================================================================

API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"


def execute_cypher(graph_name: str, cypher: str, params: Optional[Dict] = None) -> dict:
    """
    Execute Cypher query via REST API.

    Args:
        graph_name: Graph name (e.g., "scopelock")
        cypher: Cypher query
        params: Query parameters (will be inlined)

    Returns:
        API response dict
    """
    # Inline parameters into Cypher (REST API doesn't support parameterized queries)
    if params:
        cypher_inlined = cypher
        for key, value in params.items():
            placeholder = f"${key}"
            if isinstance(value, str):
                # Escape quotes and inline string
                escaped = value.replace("'", "\\'").replace('"', '\\"')
                cypher_inlined = cypher_inlined.replace(placeholder, f"'{escaped}'")
            elif isinstance(value, (int, float)):
                cypher_inlined = cypher_inlined.replace(placeholder, str(value))
            elif isinstance(value, bool):
                cypher_inlined = cypher_inlined.replace(placeholder, str(value).lower())
            else:
                logger.warning(f"Unsupported parameter type for {key}: {type(value)}")
        cypher = cypher_inlined

    payload = {
        "graph_name": graph_name,
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
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e), "response": response.text if 'response' in locals() else None}


# ============================================================================
# Node Creation
# ============================================================================

def create_code_artifact_node(
    graph_name: str,
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
    Create U4_Code_Artifact node via REST API.

    Args:
        graph_name: Graph name
        path: Code path (file::class::function format)
        name: Artifact name
        description: Human-readable description
        scope_ref: Client organization ID
        language: Programming language
        lines_of_code: Optional LOC count
        complexity: Optional cyclomatic complexity
        is_method: Whether this is a method
        parent_class: Parent class name if method
        embedding: Optional embedding vector
        extra_properties: Optional additional properties

    Returns:
        Node ID (path)
    """
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
        'visibility': 'public'
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
        properties['embedding'] = json.dumps(embedding)
        properties['embedding_dim'] = len(embedding)

    # Add extra properties
    if extra_properties:
        properties.update(extra_properties)

    # Build Cypher MERGE query (no parameters - inline everything)
    # Escape strings properly
    def escape(s):
        if s is None:
            return 'null'
        escaped = str(s).replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'").replace('\n', ' ')
        return f"'{escaped}'"

    cypher = f"""
    MERGE (artifact:U4_Code_Artifact {{path: {escape(path)}}})
    ON CREATE SET
        artifact.name = {escape(name)},
        artifact.description = {escape(description)},
        artifact.type_name = {escape('U4_Code_Artifact')},
        artifact.level = {escape('L2')},
        artifact.scope_ref = {escape(scope_ref)},
        artifact.created_at = {now},
        artifact.updated_at = {now},
        artifact.valid_from = {now},
        artifact.language = {escape(language)},
        artifact.visibility = {escape('public')}
    ON MATCH SET
        artifact.updated_at = {now}
    """

    # Add optional properties
    if lines_of_code is not None:
        cypher += f",\n        artifact.lines_of_code = {lines_of_code}"
    if complexity is not None:
        cypher += f",\n        artifact.complexity = {complexity}"
    if is_method:
        cypher += f",\n        artifact.is_method = {str(is_method).lower()}"
    if parent_class:
        cypher += f",\n        artifact.parent_class = {escape(parent_class)}"
    if embedding:
        cypher += f",\n        artifact.embedding = {escape(json.dumps(embedding))}"
        cypher += f",\n        artifact.embedding_dim = {len(embedding)}"

    # Add extra properties
    if extra_properties:
        for key, value in extra_properties.items():
            if isinstance(value, bool):
                cypher += f",\n        artifact.{key} = {str(value).lower()}"
            elif isinstance(value, (int, float)):
                cypher += f",\n        artifact.{key} = {value}"
            else:
                cypher += f",\n        artifact.{key} = {escape(value)}"

    cypher += "\n    RETURN artifact.path as node_id"

    # Execute query
    result = execute_cypher(graph_name, cypher)

    if not result['success']:
        logger.error(f"Failed to create U4_Code_Artifact node: {path}")
        logger.error(f"Error: {result['error']}")
        raise Exception(f"Node creation failed: {result['error']}")

    return path


def create_relationship_link(
    graph_name: str,
    source_path: str,
    target_path: str,
    link_type: str,
    confidence: float = 1.0,
    properties: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Create relationship link via REST API.

    Args:
        graph_name: Graph name
        source_path: Source artifact path
        target_path: Target artifact path
        link_type: Link type (U4_CALLS, U4_DEPENDS_ON, etc.)
        confidence: Confidence score
        properties: Optional additional link properties

    Returns:
        True if successful
    """
    now = int(datetime.utcnow().timestamp() * 1000)

    def escape(s):
        if s is None:
            return 'null'
        escaped = str(s).replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'").replace('\n', ' ')
        return f"'{escaped}'"

    cypher = f"""
    MATCH (source:U4_Code_Artifact {{path: {escape(source_path)}}})
    MATCH (target:U4_Code_Artifact {{path: {escape(target_path)}}})
    MERGE (source)-[r:{link_type}]->(target)
    ON CREATE SET
        r.confidence = {confidence},
        r.created_at = {now},
        r.valid_from = {now}
    RETURN count(r) as link_count
    """

    result = execute_cypher(graph_name, cypher)

    if not result['success']:
        logger.warning(f"Failed to create {link_type} link: {source_path} -> {target_path}")
        logger.warning(f"Error: {result['error']}")
        return False

    return True


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
    Ingest extraction results via REST API.

    Args:
        extraction_json_path: Path to extraction JSON
        graph_name: FalkorDB graph name
        scope_ref: Client organization ID
        language: Programming language
        generate_embeddings: Whether to generate embeddings

    Returns:
        IngestionStats with counts
    """
    stats = IngestionStats()

    # Load extraction results
    logger.info(f"Loading extraction results from: {extraction_json_path}")
    extraction_data = json.loads(extraction_json_path.read_text(encoding="utf-8"))

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
                # Build path
                if func.get("is_method") and func.get("parent_class"):
                    artifact_path = f"{file_path}::{func['parent_class']}::{func['name']}"
                else:
                    artifact_path = f"{file_path}::{func['name']}"

                # Build description
                desc_parts = []
                if func.get("docstring"):
                    desc_parts.append(func["docstring"].split("\n")[0][:200])
                if func.get("parameters"):
                    params = ", ".join(func["parameters"])
                    desc_parts.append(f"Parameters: {params}")
                description = ". ".join(desc_parts) if desc_parts else f"Function: {func['name']}"

                # Generate embedding
                embedding = None
                if embedding_service:
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

                # Calculate LOC
                loc = func['line_end'] - func['line_start'] + 1 if func.get('line_end') else None

                # Create node
                create_code_artifact_node(
                    graph_name=graph_name,
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
                # Build path
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
                    graph_name=graph_name,
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
                        'methods': json.dumps(cls.get('methods', []))
                    }
                )

                stats.classes_ingested += 1
                logger.info(f"  ✅ Class: {artifact_path}")

            except Exception as e:
                logger.error(f"  ❌ Failed to ingest class {cls['name']}: {e}")
                stats.errors += 1

    # Create call relationships
    logger.info("\n\nCreating U4_CALLS relationships...")
    for file_path, file_data in extraction_data["files"].items():
        for func in file_data["functions"]:
            # Build source path
            if func.get("is_method") and func.get("parent_class"):
                source_path = f"{file_path}::{func['parent_class']}::{func['name']}"
            else:
                source_path = f"{file_path}::{func['name']}"

            # Link calls
            for call in func.get("calls", []):
                # Try to find target in extraction data
                target_path = None

                # Search for function in all files
                for search_file, search_data in extraction_data["files"].items():
                    for search_func in search_data["functions"]:
                        if search_func["name"] == call:
                            if search_func.get("is_method") and search_func.get("parent_class"):
                                target_path = f"{search_file}::{search_func['parent_class']}::{search_func['name']}"
                            else:
                                target_path = f"{search_file}::{search_func['name']}"
                            break
                    if target_path:
                        break

                if target_path:
                    created = create_relationship_link(
                        graph_name=graph_name,
                        source_path=source_path,
                        target_path=target_path,
                        link_type="U4_CALLS",
                        confidence=0.8  # Medium confidence (static analysis)
                    )
                    if created:
                        stats.calls_linked += 1

    return stats


# ============================================================================
# CLI Interface
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest code extraction results via REST API")
    parser.add_argument("extraction_json", type=Path, help="Path to extraction JSON file")
    parser.add_argument("--graph", required=True, help="FalkorDB graph name (e.g., scopelock)")
    parser.add_argument("--scope", required=True, help="Client scope ref (e.g., org_scopelock)")
    parser.add_argument("--language", default="python", help="Programming language (default: python)")
    parser.add_argument("--no-embeddings", action="store_true", help="Skip embedding generation")

    args = parser.parse_args()

    if not args.extraction_json.exists():
        print(f"Error: Extraction JSON not found: {args.extraction_json}")
        sys.exit(1)

    print(f"Ingesting extraction results into FalkorDB (REST API mode)...")
    print(f"  Graph: {args.graph}")
    print(f"  Scope: {args.scope}")
    print(f"  Language: {args.language}")
    print(f"  API Endpoint: {API_URL}")
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
    print(f"  Errors: {stats.errors}")
    print("\n✅ Ingestion complete!")
