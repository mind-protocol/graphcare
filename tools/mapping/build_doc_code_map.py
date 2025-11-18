#!/usr/bin/env python3
"""
Build Documentation-Code Mapping from @ Annotations

Scans code files and documentation for @ annotations, builds JSON map.

@implements MECHANISM:DOC_CODE_MAPPING
@governs_by
  PATTERN: docs/strategy/GRAPHCARE_ROLE_SPEC.md#service-3-health-monitoring
  GUIDE: docs/team/DOC_CODE_MAPPING_SPEC.md

Author: Mel "Bridgekeeper"
Created: 2025-11-16
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Base directory
BASE_DIR = Path("/home/mind-protocol/graphcare")

# Scope (organization)
SCOPE = "graphcare"

# Directories to scan
CODE_DIRS = ["tools", "services"]
DOCS_DIRS = ["docs"]

# Output file
OUTPUT_FILE = BASE_DIR / "docs/team/doc_code_map.json"


def make_id(node_type: str, path: str, element: Optional[str] = None) -> str:
    """
    Generate guessable ID.

    Format: {scope}@{node_type}:{path}:{element}
    Example: graphcare@U4_Code_Artifact:tools/embed_graph_nodes.py:NodeEmbedder.embed_batch
    """
    if element:
        return f"{SCOPE}@{node_type}:{path}:{element}"
    return f"{SCOPE}@{node_type}:{path}"


def parse_annotation_block(content: str, start_marker: str) -> Dict[str, Any]:
    """
    Parse @ annotation block from docstring or markdown.

    Example:
        @implements ALGORITHM:NODE_EMBEDDING
        @governs_by
          PATTERN: docs/strategy/GRAPHCARE_ROLE_SPEC.md#service-3
          ALGORITHM: docs/operations/DOCS_AS_VIEWS.md#embedding
        @dependencies
          ENABLES: tools/query_semantic.py#semantic_search
    """
    result = {}

    # Extract @implements
    implements_match = re.search(r'@implements\s+(\w+):(\w+)', content)
    if implements_match:
        result['implements_level'] = implements_match.group(1)
        result['implements_component'] = implements_match.group(2)

    # Extract @governs_by (multi-line)
    governs_match = re.search(r'@governs_by\s*\n((?:\s+\w+:.*\n?)+)', content)
    if governs_match:
        governs_by = {}
        for line in governs_match.group(1).strip().split('\n'):
            line = line.strip()
            if ':' in line:
                level, doc_path = line.split(':', 1)
                governs_by[level.strip()] = [doc_path.strip()]
        result['governs_by'] = governs_by

    # Extract @dependencies (multi-line)
    deps_match = re.search(r'@dependencies\s*\n((?:\s+\w+:.*\n?)+)', content)
    if deps_match:
        dependencies = {}
        for line in deps_match.group(1).strip().split('\n'):
            line = line.strip()
            if ':' in line:
                dep_type, target = line.split(':', 1)
                dep_type = dep_type.strip()
                if dep_type not in dependencies:
                    dependencies[dep_type] = []
                dependencies[dep_type].append(target.strip())
        result['dependencies'] = dependencies

    # Extract @section_type (for docs)
    section_type_match = re.search(r'@section_type\s+(\w+)', content)
    if section_type_match:
        result['section_type'] = section_type_match.group(1)

    # Extract @component (for docs)
    component_match = re.search(r'@component\s+(\w+)', content)
    if component_match:
        result['component'] = component_match.group(1)

    # Extract @implemented_by (for docs, multi-line)
    impl_by_match = re.search(r'@implemented_by\s*\n((?:\s+-.*\n?)+)', content)
    if impl_by_match:
        implemented_by = []
        for line in impl_by_match.group(1).strip().split('\n'):
            line = line.strip()
            if line.startswith('-'):
                implemented_by.append(line[1:].strip())
        result['implemented_by'] = implemented_by

    # Extract @governs (for docs, multi-line)
    governs_match = re.search(r'@governs\s*\n((?:\s+-.*\n?)+)', content)
    if governs_match:
        governs = []
        for line in governs_match.group(1).strip().split('\n'):
            line = line.strip()
            if line.startswith('-'):
                target = line[1:].strip()
                # Parse relationship type if present (e.g., "target (ENABLES)")
                rel_match = re.search(r'(.+?)\s*\((\w+)\)', target)
                if rel_match:
                    governs.append({
                        'target': rel_match.group(1).strip(),
                        'relationship': rel_match.group(2).strip()
                    })
                else:
                    governs.append({'target': target, 'relationship': 'GOVERNS'})
        result['governs'] = governs

    # Extract @governed_by (for docs, multi-line)
    governed_match = re.search(r'@governed_by\s*\n((?:\s+-.*\n?)+)', content)
    if governed_match:
        governed_by = []
        for line in governed_match.group(1).strip().split('\n'):
            line = line.strip()
            if line.startswith('-'):
                target = line[1:].strip()
                # Parse level if present (e.g., "target (PATTERN)")
                level_match = re.search(r'(.+?)\s*\((\w+)\)', target)
                if level_match:
                    governed_by.append({
                        'target': level_match.group(1).strip(),
                        'level': level_match.group(2).strip()
                    })
                else:
                    governed_by.append({'target': target, 'level': 'UNKNOWN'})
        result['governed_by'] = governed_by

    return result


def extract_python_annotations(file_path: Path) -> List[Dict[str, Any]]:
    """Extract @ annotations from Python file."""
    mappings = []

    try:
        content = file_path.read_text()
        relative_path = str(file_path.relative_to(BASE_DIR))

        # Module-level docstring
        module_doc_match = re.match(r'^"""(.*?)"""', content, re.DOTALL)
        if module_doc_match:
            annotations = parse_annotation_block(module_doc_match.group(1), '@')
            if annotations:
                mappings.append({
                    'id': make_id('U4_Code_Artifact', relative_path),
                    'implementation': {
                        'type': 'file',
                        'path': relative_path,
                        'element': None
                    },
                    **annotations
                })

        # Function/class docstrings (simplified - would need AST parsing for robustness)
        # For now, just extract from obvious patterns
        func_pattern = r'def\s+(\w+)\s*\([^)]*\):\s*"""(.*?)"""'
        for match in re.finditer(func_pattern, content, re.DOTALL):
            func_name = match.group(1)
            docstring = match.group(2)
            annotations = parse_annotation_block(docstring, '@')
            if annotations:
                mappings.append({
                    'id': make_id('U4_Code_Artifact', relative_path, func_name),
                    'implementation': {
                        'type': 'function',
                        'path': relative_path,
                        'element': func_name
                    },
                    **annotations
                })

        class_pattern = r'class\s+(\w+)(?:\([^)]*\))?:\s*"""(.*?)"""'
        for match in re.finditer(class_pattern, content, re.DOTALL):
            class_name = match.group(1)
            docstring = match.group(2)
            annotations = parse_annotation_block(docstring, '@')
            if annotations:
                mappings.append({
                    'id': make_id('U4_Code_Artifact', relative_path, class_name),
                    'implementation': {
                        'type': 'class',
                        'path': relative_path,
                        'element': class_name
                    },
                    **annotations
                })

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")

    return mappings


def extract_markdown_annotations(file_path: Path) -> List[Dict[str, Any]]:
    """Extract @ annotations from Markdown file."""
    sections = []

    try:
        content = file_path.read_text()
        relative_path = str(file_path.relative_to(BASE_DIR))

        # Find all markdown sections with @ annotations
        # Pattern: ## Section Title\n@annotation_type...
        # Stop at next ## or end of annotation block
        section_pattern = r'^##\s+(.+?)$\n((?:@(?:section_type|component|implemented_by|governs|governed_by)[^\n]*\n(?:\s+-[^\n]*\n)*)+)'

        for match in re.finditer(section_pattern, content, re.MULTILINE):
            section_title = match.group(1).strip()
            annotations_block = match.group(2).strip()

            # Convert section title to anchor (lowercase, hyphens, remove special chars)
            section_anchor = (section_title.lower()
                             .replace(' ', '-')
                             .replace('(', '')
                             .replace(')', '')
                             .replace(',', '')
                             .replace('/', '-'))

            annotations = parse_annotation_block(annotations_block, '@')
            if annotations:
                sections.append({
                    'id': make_id('U4_Knowledge_Object', relative_path, section_anchor),
                    'path': relative_path,
                    'section': section_anchor,
                    'section_title': section_title,
                    **annotations
                })

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")

    return sections


def scan_directory(base_path: Path, subdirs: List[str], extractor_func) -> List[Dict[str, Any]]:
    """Scan directories for files and extract annotations."""
    results = []

    for subdir in subdirs:
        dir_path = base_path / subdir
        if not dir_path.exists():
            print(f"Directory not found: {dir_path}")
            continue

        # Determine file pattern based on extractor
        if extractor_func == extract_python_annotations:
            pattern = "**/*.py"
        elif extractor_func == extract_markdown_annotations:
            pattern = "**/*.md"
        else:
            continue

        for file_path in dir_path.glob(pattern):
            extracted = extractor_func(file_path)
            results.extend(extracted)
            if extracted:
                print(f"✓ {file_path.relative_to(BASE_DIR)}: {len(extracted)} mappings")

    return results


def build_map() -> Dict[str, Any]:
    """Build complete documentation-code map."""
    print("Building documentation-code map...")
    print()

    # Scan code files
    print("Scanning code files...")
    code_mappings = scan_directory(BASE_DIR, CODE_DIRS, extract_python_annotations)
    print(f"Found {len(code_mappings)} code mappings")
    print()

    # Scan documentation files
    print("Scanning documentation files...")
    doc_sections = scan_directory(BASE_DIR, DOCS_DIRS, extract_markdown_annotations)
    print(f"Found {len(doc_sections)} documentation sections")
    print()

    # Build final structure
    map_data = {
        'version': '1.0',
        'generated': datetime.now().isoformat(),
        'mappings': code_mappings,
        'documentation_sections': doc_sections
    }

    return map_data


def validate_map(map_data: Dict[str, Any]) -> List[str]:
    """Validate map for broken references and orphans."""
    warnings = []

    # Build index of all known IDs
    all_ids = set()
    for mapping in map_data['mappings']:
        all_ids.add(mapping['id'])
    for section in map_data['documentation_sections']:
        all_ids.add(section['id'])

    # Check code mappings
    for mapping in map_data['mappings']:
        # Check governs_by references
        if 'governs_by' in mapping:
            for level, doc_refs in mapping['governs_by'].items():
                for doc_ref in doc_refs:
                    # Check if referenced doc exists (simplified check)
                    doc_path = doc_ref.split('#')[0]
                    full_path = BASE_DIR / doc_path
                    if not full_path.exists():
                        warnings.append(f"⚠️  {mapping['id']} references non-existent doc: {doc_ref}")

        # Check for orphans (code without governing docs)
        if 'governs_by' not in mapping or not mapping['governs_by']:
            warnings.append(f"⚠️  Orphan code (no governing docs): {mapping['id']}")

    # Check documentation sections
    for section in map_data['documentation_sections']:
        # Check implemented_by references
        if 'implemented_by' in section:
            for impl_ref in section['implemented_by']:
                # Check if referenced code exists (simplified check)
                code_path = impl_ref.split('#')[0]
                full_path = BASE_DIR / code_path
                if not full_path.exists():
                    warnings.append(f"⚠️  {section['id']} references non-existent code: {impl_ref}")

        # Check for orphan docs (no implementations)
        if section.get('section_type') in ['ALGORITHM', 'GUIDE']:
            if 'implemented_by' not in section or not section['implemented_by']:
                warnings.append(f"⚠️  Orphan doc (no implementations): {section['id']} ({section.get('section_type')})")

    return warnings


def main():
    """Main entry point."""
    # Build map
    map_data = build_map()

    # Validate
    print("Validating map...")
    warnings = validate_map(map_data)
    if warnings:
        print(f"\nValidation warnings ({len(warnings)}):")
        for warning in warnings[:20]:  # Show first 20
            print(warning)
        if len(warnings) > 20:
            print(f"... and {len(warnings) - 20} more")
    else:
        print("✓ No validation warnings")
    print()

    # Write output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(map_data, indent=2))
    print(f"✓ Wrote map to {OUTPUT_FILE.relative_to(BASE_DIR)}")
    print()

    # Summary
    print("Summary:")
    print(f"  Code mappings: {len(map_data['mappings'])}")
    print(f"  Doc sections: {len(map_data['documentation_sections'])}")
    print(f"  Validation warnings: {len(warnings)}")


if __name__ == '__main__':
    main()
