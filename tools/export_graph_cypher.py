#!/usr/bin/env python3
"""
Export FalkorDB graph to Cypher CREATE statements

Usage:
    python3 export_graph_cypher.py <graph_name> <output_file>

Example:
    python3 export_graph_cypher.py scopelock scopelock_export.cypher
"""

import sys
import json
from datetime import datetime
from falkordb import FalkorDB
from typing import Any, Dict, List


def escape_string(s: str) -> str:
    """Escape string for Cypher"""
    if s is None:
        return "null"
    # Escape backslashes and quotes
    s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{s}"'


def format_value(value: Any) -> str:
    """Format Python value for Cypher"""
    if value is None:
        return "null"
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        return escape_string(value)
    elif isinstance(value, list):
        # Handle arrays
        items = [format_value(v) for v in value]
        return f"[{', '.join(items)}]"
    elif isinstance(value, dict):
        # JSON encode dicts
        return escape_string(json.dumps(value))
    else:
        return escape_string(str(value))


def export_graph(graph_name: str, output_file: str):
    """Export graph to Cypher CREATE statements"""

    db = FalkorDB(host='localhost', port=6379)
    graph = db.select_graph(graph_name)

    print(f"Exporting graph: {graph_name}")

    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write(f"// FalkorDB Graph Export: {graph_name}\n")
        f.write(f"// Generated: {datetime.now().isoformat()}\n")
        f.write(f"// Tool: export_graph_cypher.py\n\n")

        # Export nodes
        print("Exporting nodes...")
        nodes_query = "MATCH (n) RETURN n"
        nodes_result = graph.query(nodes_query)

        node_count = 0
        node_id_map = {}  # Map internal IDs to variable names

        for row in nodes_result.result_set:
            node = row[0]
            labels = node.labels
            properties = node.properties

            # Generate unique variable name
            var_name = f"n{node_count}"
            node_id_map[node.id] = var_name

            # Build label string
            label_str = ":".join(labels) if labels else ""

            # Build properties
            props = []
            for key, value in properties.items():
                props.append(f"{key}: {format_value(value)}")

            props_str = "{" + ", ".join(props) + "}" if props else ""

            # Write CREATE statement (with semicolon)
            if label_str and props_str:
                f.write(f"CREATE ({var_name}:{label_str} {props_str});\n")
            elif label_str:
                f.write(f"CREATE ({var_name}:{label_str});\n")
            elif props_str:
                f.write(f"CREATE ({var_name} {props_str});\n")
            else:
                f.write(f"CREATE ({var_name});\n")

            node_count += 1

            if node_count % 100 == 0:
                print(f"  Exported {node_count} nodes...")

        print(f"✓ Exported {node_count} nodes")

        # Export relationships
        print("\nExporting relationships...")
        rels_query = "MATCH (s)-[r]->(t) RETURN s, r, t"
        rels_result = graph.query(rels_query)

        rel_count = 0
        for row in rels_result.result_set:
            source = row[0]
            rel = row[1]
            target = row[2]

            # Get variable names
            source_var = node_id_map.get(source.id, f"n{source.id}")
            target_var = node_id_map.get(target.id, f"n{target.id}")

            # Build relationship type
            rel_type = rel.relation

            # Build properties
            props = []
            for key, value in rel.properties.items():
                props.append(f"{key}: {format_value(value)}")

            props_str = "{" + ", ".join(props) + "}" if props else ""

            # Write CREATE statement (with semicolon)
            f.write(f"\n// Relationship {rel_count + 1}\n")
            if props_str:
                f.write(f"CREATE ({source_var})-[:{rel_type} {props_str}]->({target_var});\n")
            else:
                f.write(f"CREATE ({source_var})-[:{rel_type}]->({target_var});\n")

            rel_count += 1

        print(f"✓ Exported {rel_count} relationships")

        # Write footer
        f.write(f"\n// Export complete: {node_count} nodes, {rel_count} relationships\n")

    print(f"\n✅ Export complete: {output_file}")
    print(f"   Nodes: {node_count}")
    print(f"   Relationships: {rel_count}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 export_graph_cypher.py <graph_name> <output_file>")
        print("Example: python3 export_graph_cypher.py scopelock scopelock_export.cypher")
        sys.exit(1)

    graph_name = sys.argv[1]
    output_file = sys.argv[2]

    export_graph(graph_name, output_file)
