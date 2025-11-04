#!/usr/bin/env python3
"""
Batch Import Script for L2 Graphs to FalkorDB

Splits large Cypher files into batches and imports via API endpoint.
Handles retries and provides progress tracking.
"""

import requests
import json
import sys
from pathlib import Path
from typing import List

# API Configuration
API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"

def read_cypher_file(filepath: str) -> List[str]:
    """Read Cypher file and split into individual statements."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by statement (each MERGE or CREATE is one statement)
    # Statements end with semicolon
    statements = []
    current_statement = []

    for line in content.split('\n'):
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith('//'):
            continue

        current_statement.append(line)

        # Statement ends with semicolon
        if line.endswith(';'):
            statements.append('\n'.join(current_statement))
            current_statement = []

    # Add any remaining statement
    if current_statement:
        statements.append('\n'.join(current_statement))

    return statements

def execute_statement(graph_name: str, statement: str) -> dict:
    """Execute a single Cypher statement."""
    payload = {
        "graph_name": graph_name,
        "query": statement
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

def import_graph(cypher_file: str, graph_name: str, batch_size: int = 20):
    """Import L2 graph statement by statement."""
    print(f"📥 Reading Cypher file: {cypher_file}")
    statements = read_cypher_file(cypher_file)
    total = len(statements)
    print(f"✅ Found {total} Cypher statements")
    print(f"⚡ Executing statements one at a time (FalkorDB doesn't support multi-statement queries)")
    print()

    # Execute statements one at a time
    success_count = 0
    fail_count = 0
    failed_statements = []

    for i, statement in enumerate(statements, 1):
        # Show progress every 10 statements
        if i % 10 == 0 or i == 1:
            print(f"⏳ Progress: {i}/{total} ({int(i/total*100)}%)... ", end='', flush=True)

        result = execute_statement(graph_name, statement)

        if result['success']:
            success_count += 1
            if i % 10 == 0 or i == 1:
                print("✅")
        else:
            fail_count += 1
            failed_statements.append((i, statement[:100], result['error']))
            if i % 10 == 0 or i == 1:
                print(f"❌")
            # Print first error detail
            if fail_count == 1:
                print(f"\n⚠️  First error on statement {i}:")
                print(f"   Statement: {statement[:200]}...")
                print(f"   Error: {result['error']}\n")

    print()
    print(f"📊 Import Summary:")
    print(f"  ✅ Successful statements: {success_count}/{total}")
    print(f"  ❌ Failed statements: {fail_count}/{total}")

    if fail_count == 0:
        print()
        print("🎉 Graph import complete!")

        # Verify import
        print("\n🔍 Verifying import...")
        verify_payload = {
            "graph_name": graph_name,
            "query": "MATCH (n) RETURN count(n) as node_count"
        }
        verify_response = requests.post(API_URL, json=verify_payload, headers={"X-API-Key": API_KEY, "Content-Type": "application/json"})

        if verify_response.ok:
            data = verify_response.json()
            print(f"✅ Verification successful!")
            print(f"   Node count: {data}")
        else:
            print(f"⚠️  Verification failed: {verify_response.text}")
    else:
        print("\n⚠️  Some batches failed. Check errors above.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python import_graph_batched.py <cypher_file> <graph_name> [batch_size]")
        print()
        print("Example:")
        print("  python import_graph_batched.py scopelock/l2_graph/scopelock_l2_graph.cypher scopelock 20")
        sys.exit(1)

    cypher_file = sys.argv[1]
    graph_name = sys.argv[2]
    batch_size = int(sys.argv[3]) if len(sys.argv) > 3 else 20

    if not Path(cypher_file).exists():
        print(f"❌ Error: File not found: {cypher_file}")
        sys.exit(1)

    import_graph(cypher_file, graph_name, batch_size)
