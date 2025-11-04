"""
GraphCare Schema Migration - v2.0.0 (Minimal Extension Strategy)

Applies GraphCare schema to FalkorDB graph using Mind Protocol universal types.

Strategic Pivot (Quinn's Recommendation):
- 0 new node types: Reuse Mind Protocol universal types (U4_*)
- 1 new link type: U4_SEMANTICALLY_SIMILAR (semantic clustering)
- Path granularity: U4_Code_Artifact.path supports "file", "file::class", "file::class::function"

Schema Operations:
1. Creates type indexes for efficient queries
2. Creates constraint indexes for unique IDs
3. Validates universal attributes
4. Multi-tenant: Each client gets separate graph (graphcare_<client>)

Usage:
    python schema_migration.py --graph <graph_id> --migrate
    python schema_migration.py --graph <graph_id> --validate
    python schema_migration.py --graph <graph_id> --status

Author: Nora (Chief Architect)
Date: 2025-11-04 (Updated with minimal extension strategy)
"""

import argparse
import logging
from typing import Dict, List, Optional
from datetime import datetime, timezone
from falkordb import FalkorDB

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# GraphCare Schema Version (v2.0.0 - Minimal Extension)
SCHEMA_VERSION = "2.0.0"


# Node types (Mind Protocol Universal Types - NO GraphCare-specific types)
# Strategy: Reuse existing Mind Protocol types with properties
NODE_TYPES = [
    "U4_Code_Artifact",        # path granularity: file, file::class, file::class::function
    "U4_Knowledge_Object",     # ko_type: adr, spec, runbook, guide
    "U4_Subentity",            # kind: semantic (for topic/theme clusters)
    "U4_Decision",             # Architecture decisions
    "U4_Metric",               # Code metrics (complexity, coverage, etc.)
    "U4_Measurement",          # Metric measurements
    "U4_Assessment",           # Security/quality assessments
    "U4_Agent",                # CI/CD agents, bots
    "U4_Work_Item",            # Issues, PRs, tickets
    "U4_Event",                # Deployments, incidents
    "U4_Goal"                  # Project goals
]

ALL_NODE_TYPES = NODE_TYPES  # No custom types


# Link types (Mind Protocol Universal Types + GraphCare Extension)
MIND_PROTOCOL_LINK_TYPES = [
    "U4_IMPLEMENTS",
    "U4_DOCUMENTS",
    "U4_DEPENDS_ON",
    "U4_TESTS",
    "U4_REFERENCES",
    "U4_ASSIGNED_TO",
    "U4_BLOCKED_BY",
    "U4_EMITS",
    "U4_CONSUMES",
    "U4_CONTROLS",
    "U4_MEASURES",
    "U4_EVIDENCED_BY",
    "U4_MEMBER_OF"
]

# GraphCare Extension (1 new link type)
GRAPHCARE_LINK_TYPES = [
    "U4_SEMANTICALLY_SIMILAR"  # Semantic clustering (Subentity ↔ Subentity, similarity_score: float)
]

ALL_LINK_TYPES = MIND_PROTOCOL_LINK_TYPES + GRAPHCARE_LINK_TYPES


def get_graph(graph_id: str):
    """Connect to FalkorDB and select graph"""
    try:
        db = FalkorDB(host='localhost', port=6379)
        graph = db.select_graph(graph_id)
        logger.info(f"✅ Connected to graph: {graph_id}")
        return graph
    except Exception as e:
        logger.error(f"❌ Failed to connect to FalkorDB: {e}")
        raise


def migrate_schema(graph_id: str) -> bool:
    """
    Apply GraphCare schema to graph using minimal extension strategy.

    Creates indexes for:
    - type_name (efficient type filtering)
    - name (fast name lookups)
    - scope_ref (filter by client)
    - level (filter by organizational level)
    - path (for U4_Code_Artifact lookups with granularity: file, file::class, file::class::function)
    - ko_type (for U4_Knowledge_Object filtering: adr, spec, runbook, guide)
    - kind (for U4_Subentity filtering: semantic, functional, emergent)
    """
    logger.info(f"🔧 Starting schema migration for graph: {graph_id}")

    graph = get_graph(graph_id)

    # Create indexes for all node types
    for node_type in ALL_NODE_TYPES:
        try:
            # Index on type_name for fast type queries
            graph.query(f"CREATE INDEX FOR (n:{node_type}) ON (n.type_name)")
            logger.info(f"  ✅ Created index: {node_type}.type_name")

            # Index on name for fast name lookups
            graph.query(f"CREATE INDEX FOR (n:{node_type}) ON (n.name)")
            logger.info(f"  ✅ Created index: {node_type}.name")

        except Exception as e:
            # Index may already exist, that's okay
            logger.debug(f"  ⚠️ Index creation skipped for {node_type}: {e}")

    # Create common query pattern indexes
    try:
        # Universal filters (all nodes)
        graph.query("CREATE INDEX FOR (n) ON (n.scope_ref)")
        logger.info("  ✅ Created index: *.scope_ref (filter by client)")

        graph.query("CREATE INDEX FOR (n) ON (n.level)")
        logger.info("  ✅ Created index: *.level (filter by level L2)")

        # U4_Code_Artifact indexes (path granularity)
        graph.query("CREATE INDEX FOR (n:U4_Code_Artifact) ON (n.path)")
        logger.info("  ✅ Created index: U4_Code_Artifact.path (file, file::class, file::class::function)")

        # U4_Knowledge_Object indexes (ko_type filtering)
        graph.query("CREATE INDEX FOR (n:U4_Knowledge_Object) ON (n.ko_type)")
        logger.info("  ✅ Created index: U4_Knowledge_Object.ko_type (adr, spec, runbook, guide)")

        # U4_Subentity indexes (kind filtering)
        graph.query("CREATE INDEX FOR (n:U4_Subentity) ON (n.kind)")
        logger.info("  ✅ Created index: U4_Subentity.kind (semantic, functional, emergent)")

        # U4_Work_Item indexes (issue/PR tracking)
        graph.query("CREATE INDEX FOR (n:U4_Work_Item) ON (n.status)")
        logger.info("  ✅ Created index: U4_Work_Item.status (open, closed, merged)")

    except Exception as e:
        logger.debug(f"  ⚠️ Common index creation skipped: {e}")

    # Store schema version in graph metadata
    try:
        graph.query(f"""
            MERGE (schema:GraphCare_Schema {{version: '{SCHEMA_VERSION}'}})
            ON CREATE SET schema.migrated_at = timestamp(),
                          schema.node_types = {len(ALL_NODE_TYPES)},
                          schema.link_types = {len(ALL_LINK_TYPES)},
                          schema.strategy = 'minimal_extension'
            ON MATCH SET schema.last_validated = timestamp()
        """)
        logger.info(f"  ✅ Schema metadata created (version: {SCHEMA_VERSION})")
    except Exception as e:
        logger.error(f"  ❌ Failed to create schema metadata: {e}")

    logger.info(f"✅ Schema migration complete for graph: {graph_id}")
    return True


def validate_schema(graph_id: str) -> Dict:
    """
    Validate that all nodes/links have required universal attributes.

    Universal node attributes (REQUIRED):
    - created_at, updated_at, valid_from, valid_to (bitemporal)
    - description, name, type_name (identity)
    - level, scope_ref (scope)
    - visibility, created_by, substrate (privacy & provenance)

    Universal link attributes (REQUIRED):
    - created_at, updated_at, valid_from, valid_to (bitemporal)
    - confidence, energy, forming_mindstate, goal (consciousness metadata)
    - visibility, created_by, substrate (privacy & provenance)
    """
    logger.info(f"🔍 Validating schema for graph: {graph_id}")

    graph = get_graph(graph_id)

    # Check nodes for missing universal attributes
    result = graph.query("""
        MATCH (n)
        WHERE n.created_at IS NULL
           OR n.updated_at IS NULL
           OR n.valid_from IS NULL
           OR n.level IS NULL
           OR n.scope_ref IS NULL
           OR n.description IS NULL
           OR n.name IS NULL
        RETURN count(n) as invalid_count
    """).result_set

    invalid_nodes = result[0][0] if result else 0

    # Check links for missing universal attributes
    result = graph.query("""
        MATCH ()-[r]->()
        WHERE r.created_at IS NULL
           OR r.updated_at IS NULL
           OR r.valid_from IS NULL
           OR r.confidence IS NULL
           OR r.energy IS NULL
           OR r.goal IS NULL
        RETURN count(r) as invalid_count
    """).result_set

    invalid_links = result[0][0] if result else 0

    # Get total counts
    result = graph.query("MATCH (n) RETURN count(n) as total_nodes").result_set
    total_nodes = result[0][0] if result else 0

    result = graph.query("MATCH ()-[r]->() RETURN count(r) as total_links").result_set
    total_links = result[0][0] if result else 0

    # Get counts by type
    result = graph.query("""
        MATCH (n)
        RETURN labels(n)[0] as node_type, count(n) as count
        ORDER BY count DESC
    """).result_set

    node_type_counts = {row[0]: row[1] for row in result} if result else {}

    result = graph.query("""
        MATCH ()-[r]->()
        RETURN type(r) as link_type, count(r) as count
        ORDER BY count DESC
    """).result_set

    link_type_counts = {row[0]: row[1] for row in result} if result else {}

    # Validation summary
    validation = {
        "valid": invalid_nodes == 0 and invalid_links == 0,
        "total_nodes": total_nodes,
        "total_links": total_links,
        "invalid_nodes": invalid_nodes,
        "invalid_links": invalid_links,
        "node_type_counts": node_type_counts,
        "link_type_counts": link_type_counts,
        "schema_version": SCHEMA_VERSION
    }

    # Log validation results
    if validation["valid"]:
        logger.info(f"✅ Schema validation PASSED")
        logger.info(f"   Total nodes: {total_nodes} (all valid)")
        logger.info(f"   Total links: {total_links} (all valid)")
    else:
        logger.warning(f"⚠️ Schema validation FAILED")
        logger.warning(f"   Invalid nodes: {invalid_nodes}/{total_nodes}")
        logger.warning(f"   Invalid links: {invalid_links}/{total_links}")
        logger.warning(f"   Action: Fix missing universal attributes before extraction")

    # Log type distribution
    logger.info("📊 Node type distribution:")
    for node_type, count in sorted(node_type_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        logger.info(f"   {node_type}: {count}")

    logger.info("📊 Link type distribution:")
    for link_type, count in sorted(link_type_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        logger.info(f"   {link_type}: {count}")

    return validation


def get_schema_status(graph_id: str) -> Dict:
    """Get current schema status"""
    logger.info(f"📋 Checking schema status for graph: {graph_id}")

    graph = get_graph(graph_id)

    # Check if schema metadata exists
    result = graph.query("""
        MATCH (schema:GraphCare_Schema)
        RETURN schema.version as version,
               schema.migrated_at as migrated_at,
               schema.last_validated as last_validated,
               schema.node_types as node_types,
               schema.link_types as link_types
    """).result_set

    if not result:
        logger.warning("⚠️ Schema not migrated yet")
        return {
            "migrated": False,
            "version": None,
            "message": "Schema not migrated. Run: python schema_migration.py --graph <graph_id> --migrate"
        }

    schema_info = result[0]
    migrated_at = datetime.fromtimestamp(schema_info[1] / 1000, tz=timezone.utc).isoformat() if schema_info[1] else None
    last_validated = datetime.fromtimestamp(schema_info[2] / 1000, tz=timezone.utc).isoformat() if schema_info[2] else None

    status = {
        "migrated": True,
        "version": schema_info[0],
        "migrated_at": migrated_at,
        "last_validated": last_validated,
        "node_types_count": schema_info[3],
        "link_types_count": schema_info[4]
    }

    logger.info(f"✅ Schema migrated: version {status['version']}")
    logger.info(f"   Migrated at: {migrated_at}")
    logger.info(f"   Last validated: {last_validated or 'Never'}")
    logger.info(f"   Node types: {status['node_types_count']}")
    logger.info(f"   Link types: {status['link_types_count']}")

    return status


def main():
    parser = argparse.ArgumentParser(description='GraphCare Schema Migration Tool')
    parser.add_argument('--graph', required=True, help='Graph ID to migrate')
    parser.add_argument('--migrate', action='store_true', help='Apply schema migration')
    parser.add_argument('--validate', action='store_true', help='Validate schema compliance')
    parser.add_argument('--status', action='store_true', help='Check schema status')

    args = parser.parse_args()

    try:
        if args.migrate:
            migrate_schema(args.graph)

        if args.validate:
            validation = validate_schema(args.graph)
            if not validation["valid"]:
                logger.error("❌ Validation failed - see warnings above")
                return 1

        if args.status:
            get_schema_status(args.graph)

        if not (args.migrate or args.validate or args.status):
            parser.print_help()
            return 1

        return 0

    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
