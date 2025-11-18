#!/usr/bin/env python3
"""
Scopelock Documentation Extractor
Extracts consciousness design pattern hierarchy: PATTERN → BEHAVIOR_SPEC → VALIDATION → MECHANISM → ALGORITHM → GUIDE

Author: Quinn (Chief Cartographer) + Mel (orchestrator)
Created: 2025-11-05
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any
import hashlib

# Scopelock docs directory
DOCS_DIR = Path("/home/mind-protocol/graphcare/clients/scopelock/docs")

# Section hierarchy (order matters)
SECTION_HIERARCHY = [
    "PATTERN",
    "BEHAVIOR_SPEC",
    "VALIDATION",
    "MECHANISM",
    "ALGORITHM",
    "GUIDE"
]

# ko_type mapping
KO_TYPE_MAP = {
    "PATTERN": "pattern",
    "BEHAVIOR_SPEC": "spec",
    "VALIDATION": "validation",
    "MECHANISM": "mechanism",
    "ALGORITHM": "algorithm",
    "GUIDE": "guide"
}

def generate_node_id(content: str, section_type: str, file_path: str) -> str:
    """Generate stable node ID from content hash."""
    hash_input = f"{file_path}::{section_type}::{content[:100]}"
    return hashlib.md5(hash_input.encode()).hexdigest()[:12]

def extract_sections(md_content: str, file_path: Path) -> List[Dict[str, Any]]:
    """
    Extract PATTERN/BEHAVIOR_SPEC/etc sections from markdown.

    Returns list of section dicts with:
    - section_type: PATTERN, BEHAVIOR_SPEC, etc.
    - content: markdown content
    - level: h2/h3/h4
    """
    sections = []

    # Find all section headers (## PATTERN, ### BEHAVIOR_SPEC, etc.)
    pattern = r'^(#{2,4})\s+(' + '|'.join(SECTION_HIERARCHY) + r')\s*$'

    lines = md_content.split('\n')
    current_section = None
    current_content = []

    for i, line in enumerate(lines):
        match = re.match(pattern, line, re.IGNORECASE)

        if match:
            # Save previous section
            if current_section:
                sections.append({
                    'section_type': current_section['type'],
                    'content': '\n'.join(current_content).strip(),
                    'level': current_section['level'],
                    'line_start': current_section['line_start'],
                    'line_end': i - 1
                })

            # Start new section
            level = len(match.group(1))  # Number of # chars
            section_type = match.group(2).upper()

            current_section = {
                'type': section_type,
                'level': level,
                'line_start': i
            }
            current_content = []

        elif current_section:
            current_content.append(line)

    # Save last section
    if current_section:
        sections.append({
            'section_type': current_section['type'],
            'content': '\n'.join(current_content).strip(),
            'level': current_section['level'],
            'line_start': current_section['line_start'],
            'line_end': len(lines) - 1
        })

    return sections

def create_knowledge_object_node(section: Dict, file_path: Path, doc_name: str) -> Dict[str, Any]:
    """Create U4_Knowledge_Object node from section."""
    section_type = section['section_type']
    content = section['content']

    # Extract title from first line or heading
    lines = content.split('\n')
    title = None
    description = content[:200].replace('\n', ' ').strip()

    for line in lines[:5]:
        if line.strip() and not line.startswith('#'):
            title = line.strip()
            break

    if not title:
        title = f"{doc_name} - {section_type}"

    node_id = generate_node_id(content, section_type, str(file_path))

    return {
        'id': f"ko_{node_id}",
        'type': 'U4_Knowledge_Object',
        'properties': {
            'name': title[:100],
            'description': description,
            'ko_type': KO_TYPE_MAP[section_type],
            'path': str(file_path.relative_to(DOCS_DIR.parent)),
            'scope_ref': 'scopelock',
            'level': 'L2',
            'section_type': section_type,  # PATTERN, BEHAVIOR_SPEC, etc.
            'line_start': section['line_start'],
            'line_end': section['line_end'],
            'content_length': len(content),
            'markdown_content': content[:1000]  # First 1000 chars for queryability
        }
    }

def extract_feature_name(file_path: Path) -> str:
    """Extract feature name from file path."""
    # e.g., docs/automation/01_proof_regeneration.md → "Proof Regeneration"
    stem = file_path.stem

    # Remove number prefix
    name = re.sub(r'^\d+_', '', stem)

    # Convert underscores to spaces and title case
    return name.replace('_', ' ').title()

def process_file(file_path: Path) -> Dict[str, Any]:
    """Process single markdown file."""
    print(f"Processing: {file_path.relative_to(DOCS_DIR.parent)}")

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ⚠️  Error reading file: {e}")
        return {'nodes': [], 'relationships': []}

    sections = extract_sections(content, file_path)

    if not sections:
        print(f"  ⚠️  No consciousness design sections found")
        return {'nodes': [], 'relationships': []}

    doc_name = extract_feature_name(file_path)
    nodes = []
    relationships = []

    # Create nodes for each section
    for section in sections:
        node = create_knowledge_object_node(section, file_path, doc_name)
        nodes.append(node)

    # Create U4_MEMBER_OF relationships (hierarchy)
    # PATTERN → BEHAVIOR_SPEC → VALIDATION → MECHANISM → ALGORITHM → GUIDE
    for i in range(len(nodes) - 1):
        parent_node = nodes[i]
        child_node = nodes[i + 1]

        # Only link if they follow hierarchy order
        parent_section = parent_node['properties']['section_type']
        child_section = child_node['properties']['section_type']

        parent_idx = SECTION_HIERARCHY.index(parent_section)
        child_idx = SECTION_HIERARCHY.index(child_section)

        if child_idx == parent_idx + 1:
            relationships.append({
                'type': 'U4_MEMBER_OF',
                'source': child_node['id'],
                'target': parent_node['id'],
                'properties': {
                    'membership_type': 'structural',
                    'role': f"{child_section.lower()}_layer",
                    'scope_ref': 'scopelock'
                }
            })

    print(f"  ✅ Extracted {len(nodes)} sections, {len(relationships)} relationships")

    return {
        'nodes': nodes,
        'relationships': relationships,
        'file_path': str(file_path.relative_to(DOCS_DIR.parent)),
        'doc_name': doc_name
    }

def main():
    """Main extraction loop."""
    print("="*80)
    print("Scopelock Documentation Extraction")
    print("Extracting consciousness design pattern hierarchy")
    print("="*80)

    all_nodes = []
    all_relationships = []
    files_processed = 0

    # Find all markdown files
    md_files = sorted(DOCS_DIR.rglob("*.md"))

    print(f"\nFound {len(md_files)} markdown files")
    print()

    for md_file in md_files:
        result = process_file(md_file)

        if result['nodes']:
            all_nodes.extend(result['nodes'])
            all_relationships.extend(result['relationships'])
            files_processed += 1

    print()
    print("="*80)
    print("Extraction Summary")
    print("="*80)
    print(f"Files processed: {files_processed}/{len(md_files)}")
    print(f"Knowledge objects extracted: {len(all_nodes)}")
    print(f"Hierarchical relationships: {len(all_relationships)}")

    # Breakdown by ko_type
    ko_types = {}
    for node in all_nodes:
        ko_type = node['properties']['ko_type']
        ko_types[ko_type] = ko_types.get(ko_type, 0) + 1

    print("\nBreakdown by type:")
    for ko_type in ['pattern', 'spec', 'validation', 'mechanism', 'algorithm', 'guide']:
        count = ko_types.get(ko_type, 0)
        print(f"  {ko_type}: {count}")

    # Save to JSON
    output = {
        'metadata': {
            'source': 'scopelock_docs',
            'scope_ref': 'scopelock',
            'extraction_date': '2025-11-05',
            'files_processed': files_processed,
            'total_files': len(md_files)
        },
        'nodes': all_nodes,
        'relationships': all_relationships
    }

    output_path = Path(__file__).parent / "scopelock_docs_extraction.json"
    output_path.write_text(json.dumps(output, indent=2), encoding='utf-8')

    print(f"\n✅ Extraction complete: {output_path}")
    print()

if __name__ == "__main__":
    main()
