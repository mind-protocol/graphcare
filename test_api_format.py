#!/usr/bin/env python3
"""Test API format to understand response structure."""

import requests
import json

API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"
GRAPH_NAME = "scopelock"

def test_query(cypher):
    """Execute query and print full response."""
    payload = {
        "graph_name": GRAPH_NAME,
        "query": cypher
    }

    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    print(f"\n{'='*70}")
    print(f"Query: {cypher}")
    print(f"{'='*70}")

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")

        if response.ok:
            data = response.json()
            print(f"JSON Structure: {json.dumps(data, indent=2)[:500]}")

    except Exception as e:
        print(f"Error: {e}")

# Test simple queries
test_query("MATCH (n) RETURN count(n) as node_count LIMIT 1")
test_query("MATCH (n:U4_Code_Artifact) RETURN n.name LIMIT 1")
