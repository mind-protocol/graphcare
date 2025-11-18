#!/usr/bin/env python3
"""
Link code artifacts to documentation with U4_IMPLEMENTS relationships.

Strategy: Match by file path and function names to documentation sections.
"""

import requests
import re

API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"
GRAPH_NAME = "scopelock"

def execute_cypher(cypher: str) -> dict:
    """Execute Cypher query."""
    payload = {"graph_name": GRAPH_NAME, "query": cypher}
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        raw = response.json()

        # Parse FalkorDB format
        result = raw.get("result", [])
        if len(result) >= 2:
            columns = result[0]
            rows = result[1]
            return {"success": True, "data": [
                {col: row[i] for i, col in enumerate(columns)}
                for row in rows
            ]}
        return {"success": True, "data": []}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_all_code_artifacts() -> list:
    """Get all U4_Code_Artifact nodes."""
    cypher = """
    MATCH (c:U4_Code_Artifact)
    RETURN ID(c) as id, c.name as name, c.path as path, c.scope_ref as scope_ref
    """

    result = execute_cypher(cypher)
    if result['success']:
        return result['data']
    return []

def get_all_guide_sections() -> list:
    """Get all GUIDE sections (implementation guides)."""
    cypher = """
    MATCH (k:U4_Knowledge_Object)
    WHERE k.scope_ref = 'scopelock' AND k.ko_type = 'guide'
    RETURN k.id as id, k.name as name, k.path as doc_path, k.section_type as section_type
    """

    result = execute_cypher(cypher)
    if result['success']:
        return result['data']
    return []

def create_implements_link(code_id: int, doc_id: str, match_reason: str) -> bool:
    """Create U4_IMPLEMENTS relationship."""
    # Escape match_reason
    match_reason = match_reason.replace("'", "\\'")

    cypher = f"""
    MATCH (code:U4_Code_Artifact)
    WHERE ID(code) = {code_id}
    MATCH (doc:U4_Knowledge_Object {{id: '{doc_id}'}})
    MERGE (code)-[r:U4_IMPLEMENTS {{match_reason: '{match_reason}'}}]->(doc)
    """

    result = execute_cypher(cypher)
    return result['success']

def extract_feature_name(doc_path: str) -> str:
    """Extract feature name from doc path."""
    # e.g., docs/automation/01_proof_regeneration.md → "proof_regeneration"
    match = re.search(r'/(\d+_)?(.+)\.md$', doc_path)
    if match:
        return match.group(2).replace('_', ' ').lower()
    return ""

def match_code_to_docs(code_artifacts: list, guide_sections: list) -> list:
    """Match code artifacts to documentation."""
    links = []

    for code in code_artifacts:
        code_path = code['path'].lower()
        code_name = code['name'].lower()

        for guide in guide_sections:
            doc_path = guide['doc_path'].lower()
            feature_name = extract_feature_name(doc_path)

            # Matching strategies:
            reasons = []

            # 1. File path contains feature name
            if feature_name and feature_name in code_path:
                reasons.append(f"file_path_contains:{feature_name}")

            # 2. Function name matches feature
            if feature_name and feature_name.replace(' ', '') in code_name.replace('_', ''):
                reasons.append(f"function_name_match:{feature_name}")

            # 3. Webhook matching
            if 'webhook' in doc_path and 'webhook' in code_path:
                if 'upwork' in doc_path and 'upwork' in code_path:
                    reasons.append("upwork_webhook_match")
                elif 'telegram' in doc_path and 'telegram' in code_path:
                    reasons.append("telegram_webhook_match")
                elif 'cloudmailin' in doc_path and 'cloudmailin' in code_path:
                    reasons.append("cloudmailin_webhook_match")

            # 4. Proof/evidence matching
            if 'proof' in doc_path and ('proof' in code_path or 'proof' in code_name):
                reasons.append("proof_generation_match")

            # 5. Telegram bot matching
            if 'telegram' in doc_path and 'telegram' in code_path:
                reasons.append("telegram_feature_match")

            # 6. Browser automation matching
            if 'automation' in doc_path and ('automation' in code_path or 'browser' in code_path):
                reasons.append("automation_feature_match")

            # 7. Runner/Claude matching
            if ('emma' in doc_path or 'claude' in doc_path) and 'runner' in code_path:
                reasons.append("claude_runner_match")

            if reasons:
                links.append({
                    'code_id': code['id'],
                    'code_name': code['name'],
                    'doc_id': guide['id'],
                    'doc_name': guide['name'],
                    'reasons': reasons
                })

    return links

def main():
    print("="*80)
    print("Linking Code Artifacts to Documentation")
    print("="*80)

    print("\nFetching code artifacts...")
    code_artifacts = get_all_code_artifacts()
    print(f"Found {len(code_artifacts)} code artifacts")

    print("\nFetching GUIDE sections...")
    guide_sections = get_all_guide_sections()
    print(f"Found {len(guide_sections)} GUIDE sections")

    print("\nMatching code to documentation...")
    links = match_code_to_docs(code_artifacts, guide_sections)
    print(f"Found {len(links)} potential matches")

    print("\nCreating U4_IMPLEMENTS relationships...")
    created = 0
    errors = 0

    for link in links:
        match_reason = ", ".join(link['reasons'])
        success = create_implements_link(link['code_id'], link['doc_id'], match_reason)

        if success:
            created += 1
            print(f"  ✅ {link['code_name']} → {link['doc_name']}")
        else:
            errors += 1
            print(f"  ❌ Failed: {link['code_name']} → {link['doc_name']}")

    print()
    print("="*80)
    print("Link Summary")
    print("="*80)
    print(f"Links created: {created}/{len(links)}")
    print(f"Errors: {errors}")

    if errors == 0:
        print("\n✅ Linking complete!")
    else:
        print(f"\n⚠️  Linking complete with {errors} errors")

if __name__ == "__main__":
    main()
