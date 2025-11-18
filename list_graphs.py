#!/usr/bin/env python3
"""List all graphs in production FalkorDB."""

import requests

API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"

# Query system to list graphs
payload = {
    "graph_name": "system",  # System graph
    "query": "CALL db.labels()"  # List all labels/graphs
}

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

print("Querying production FalkorDB for available graphs...")

try:
    response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

except Exception as e:
    print(f"Error: {e}")
