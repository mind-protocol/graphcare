#!/usr/bin/env python3
"""
Pretty-print wrapper for ask.py
Shows beam search results in human-readable format.
"""

import sys
import json
import subprocess

def format_node(node: dict, indent: str = "") -> str:
    """Format a node for display."""
    lines = []

    name = node.get('name', 'Unknown')
    labels = node.get('labels', [])

    # Parse labels if string
    if isinstance(labels, str):
        labels = labels.strip('[]').split(',')

    label_str = labels[0] if labels else "Unknown"

    lines.append(f"{indent}🔵 {label_str}")
    lines.append(f"{indent}   Name: {name[:80]}")

    if node.get('description'):
        desc = node['description'][:100] + "..." if len(node['description']) > 100 else node['description']
        lines.append(f"{indent}   Desc: {desc}")

    if node.get('path'):
        lines.append(f"{indent}   Path: {node['path']}")

    if node.get('ko_type'):
        lines.append(f"{indent}   Type: {node['ko_type']}")

    if node.get('lang'):
        lines.append(f"{indent}   Lang: {node['lang']}")

    return "\n".join(lines)


def format_links(links: dict, indent: str = "") -> str:
    """Format links for display."""
    lines = []

    for link in links.get('items', []):
        rel_type = link.get('rel_type', 'UNKNOWN')
        confidence = link.get('confidence', 'N/A')
        energy = link.get('energy', 'N/A')

        lines.append(f"{indent}  ↓ {rel_type} (conf={confidence}, energy={energy})")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python ask_pretty.py \"<question>\" [graph_name]")
        print("\nExamples:")
        print("  python ask_pretty.py \"How does Telegram bot work?\"")
        print("  python ask_pretty.py \"What validates proposals?\" scopelock")
        sys.exit(1)

    # Call ask.py and capture output
    result = subprocess.run(
        ["python3", "tools/ask.py"] + sys.argv[1:],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Error running ask.py:")
        print(result.stderr)
        sys.exit(1)

    # Parse JSON
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("Error parsing JSON:")
        print(result.stdout)
        sys.exit(1)

    # Pretty print
    print("=" * 80)
    print(f"Query: {data['query']}")
    print(f"Graph: {data['graph']}")
    print(f"Path Score: {data.get('path_score', 'N/A')}")
    print(f"Path Depth: {data.get('path_depth', 'N/A')}")
    print("=" * 80)
    print()

    cluster = data.get('cluster', [])

    if not cluster:
        print("No results found.")
        print(f"\nNotes: {data.get('notes', 'N/A')}")
        return

    print(f"Found {len(cluster)} elements in path:\n")

    for i, elem in enumerate(cluster, 1):
        elem_type = elem.get('type', 'unknown')

        if elem_type == 'node':
            print(format_node(elem))
            print()
        elif elem_type == 'links':
            print(format_links(elem, indent="  "))
            print()

    print("=" * 80)
    print(f"Notes: {data.get('notes', 'N/A')}")


if __name__ == '__main__':
    main()
