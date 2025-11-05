"""
TypeScript/TSX Extractor for GraphCare

Extracts functions, components, classes, and imports from TypeScript/TSX source code.
Uses regex-based parsing for Python compatibility (no Node.js required).

Author: Kai (Chief Engineer, GraphCare)
Created: 2025-11-04
"""

import re
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class TSFunctionMetadata:
    """Metadata for a TypeScript function."""
    name: str
    file_path: str
    line_number: int
    function_type: str  # "function", "arrow", "method"
    parameters: List[str]
    return_type: Optional[str]
    is_async: bool
    is_exported: bool
    is_default_export: bool
    body_lines: int


@dataclass
class TSComponentMetadata:
    """Metadata for a React component."""
    name: str
    file_path: str
    line_number: int
    component_type: str  # "function_component", "class_component"
    props_type: Optional[str]
    is_exported: bool
    is_default_export: bool


@dataclass
class TSClassMetadata:
    """Metadata for a TypeScript class."""
    name: str
    file_path: str
    line_number: int
    extends: Optional[str]
    implements: List[str]
    is_exported: bool


@dataclass
class TSImportMetadata:
    """Metadata for an import statement."""
    module: str
    imports: List[str]
    default_import: Optional[str]
    file_path: str
    line_number: int
    is_type_import: bool


@dataclass
class TSExtractionResult:
    """Complete extraction results for a TypeScript file."""
    file_path: str
    functions: List[TSFunctionMetadata] = field(default_factory=list)
    components: List[TSComponentMetadata] = field(default_factory=list)
    classes: List[TSClassMetadata] = field(default_factory=list)
    imports: List[TSImportMetadata] = field(default_factory=list)
    parse_errors: List[str] = field(default_factory=list)


# ============================================================================
# TypeScript Extractor
# ============================================================================

class TypeScriptExtractor:
    """Extracts TypeScript/TSX code structures using regex patterns."""

    def __init__(self, file_path: Path, source_code: str):
        self.file_path = str(file_path)
        self.source_code = source_code
        self.lines = source_code.splitlines()

        self.functions: List[TSFunctionMetadata] = []
        self.components: List[TSComponentMetadata] = []
        self.classes: List[TSClassMetadata] = []
        self.imports: List[TSImportMetadata] = []
        self.errors: List[str] = []

    def extract(self) -> TSExtractionResult:
        """Main extraction method."""
        try:
            self._extract_imports()
            self._extract_functions()
            self._extract_classes()
            self._extract_react_components()

            return TSExtractionResult(
                file_path=self.file_path,
                functions=self.functions,
                components=self.components,
                classes=self.classes,
                imports=self.imports,
                parse_errors=self.errors
            )

        except Exception as e:
            return TSExtractionResult(
                file_path=self.file_path,
                parse_errors=[f"Extraction error: {str(e)}"]
            )

    def _extract_imports(self):
        """Extract import statements."""
        named_import_pattern = r"import\s+(?:type\s+)?\{([^}]+)\}\s+from\s+['\"]([^'\"]+)['\"]"
        default_import_pattern = r"import\s+([A-Z][a-zA-Z0-9]*)\s+from\s+['\"]([^'\"]+)['\"]"
        namespace_import_pattern = r"import\s+\*\s+as\s+([a-zA-Z0-9]+)\s+from\s+['\"]([^'\"]+)['\"]"

        for i, line in enumerate(self.lines, 1):
            line = line.strip()
            is_type_import = 'import type' in line

            # Named imports
            match = re.search(named_import_pattern, line)
            if match:
                imports_str = match.group(1)
                module = match.group(2)
                imports = [imp.strip() for imp in imports_str.split(',')]

                self.imports.append(TSImportMetadata(
                    module=module,
                    imports=imports,
                    default_import=None,
                    file_path=self.file_path,
                    line_number=i,
                    is_type_import=is_type_import
                ))
                continue

            # Default import
            match = re.search(default_import_pattern, line)
            if match:
                default_import = match.group(1)
                module = match.group(2)

                self.imports.append(TSImportMetadata(
                    module=module,
                    imports=[],
                    default_import=default_import,
                    file_path=self.file_path,
                    line_number=i,
                    is_type_import=is_type_import
                ))
                continue

            # Namespace import
            match = re.search(namespace_import_pattern, line)
            if match:
                namespace = match.group(1)
                module = match.group(2)

                self.imports.append(TSImportMetadata(
                    module=module,
                    imports=[],
                    default_import=namespace,
                    file_path=self.file_path,
                    line_number=i,
                    is_type_import=is_type_import
                ))

    def _extract_functions(self):
        """Extract function declarations."""
        func_pattern = r"(export\s+)?(default\s+)?(async\s+)?function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(([^)]*)\)\s*(?::\s*([^{]+))?\s*\{"
        arrow_pattern = r"(export\s+)?(default\s+)?const\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*(async\s+)?\(([^)]*)\)\s*(?::\s*([^=>{]+))?\s*=>"

        for i, line in enumerate(self.lines, 1):
            # Function declarations
            match = re.search(func_pattern, line)
            if match:
                is_exported = bool(match.group(1))
                is_default = bool(match.group(2))
                is_async = bool(match.group(3))
                name = match.group(4)
                params_str = match.group(5) or ""
                return_type = match.group(6).strip() if match.group(6) else None

                params = self._parse_parameters(params_str)
                body_lines = self._estimate_body_lines(i - 1)

                self.functions.append(TSFunctionMetadata(
                    name=name,
                    file_path=self.file_path,
                    line_number=i,
                    function_type="function",
                    parameters=params,
                    return_type=return_type,
                    is_async=is_async,
                    is_exported=is_exported,
                    is_default_export=is_default,
                    body_lines=body_lines
                ))

            # Arrow functions
            match = re.search(arrow_pattern, line)
            if match:
                is_exported = bool(match.group(1))
                is_default = bool(match.group(2))
                name = match.group(3)
                is_async = bool(match.group(4))
                params_str = match.group(5) or ""
                return_type = match.group(6).strip() if match.group(6) else None

                params = self._parse_parameters(params_str)
                body_lines = self._estimate_body_lines(i - 1)

                self.functions.append(TSFunctionMetadata(
                    name=name,
                    file_path=self.file_path,
                    line_number=i,
                    function_type="arrow",
                    parameters=params,
                    return_type=return_type,
                    is_async=is_async,
                    is_exported=is_exported,
                    is_default_export=is_default,
                    body_lines=body_lines
                ))

    def _extract_classes(self):
        """Extract class declarations."""
        class_pattern = r"(export\s+)?(default\s+)?class\s+([A-Z][a-zA-Z0-9_]*)\s*(?:extends\s+([A-Z][a-zA-Z0-9_<>,\s]*))?\s*(?:implements\s+([A-Z][a-zA-Z0-9_<>,\s]*))?\s*\{"

        for i, line in enumerate(self.lines, 1):
            match = re.search(class_pattern, line)
            if match:
                is_exported = bool(match.group(1))
                name = match.group(3)
                extends = match.group(4).strip() if match.group(4) else None
                implements_str = match.group(5).strip() if match.group(5) else ""

                implements = [i.strip() for i in implements_str.split(',')] if implements_str else []

                self.classes.append(TSClassMetadata(
                    name=name,
                    file_path=self.file_path,
                    line_number=i,
                    extends=extends,
                    implements=implements,
                    is_exported=is_exported
                ))

    def _extract_react_components(self):
        """Extract React components."""
        # Look for default exports that are likely components (capitalized names)
        export_default_pattern = r"export\s+default\s+(?:function\s+)?([A-Z][a-zA-Z0-9]*)"

        for i, line in enumerate(self.lines, 1):
            match = re.search(export_default_pattern, line)
            if match:
                name = match.group(1)

                # Check if it's already captured as a function
                already_captured = any(f.name == name for f in self.functions)
                if already_captured:
                    continue

                # Check if it returns JSX (heuristic)
                is_jsx = self._check_jsx_return(i - 1)

                if is_jsx:
                    self.components.append(TSComponentMetadata(
                        name=name,
                        file_path=self.file_path,
                        line_number=i,
                        component_type="function_component",
                        props_type=None,
                        is_exported=True,
                        is_default_export=True
                    ))

    def _parse_parameters(self, params_str: str) -> List[str]:
        """Parse parameter string into list of parameter names."""
        if not params_str.strip():
            return []

        params = []
        for param in params_str.split(','):
            param = param.strip()
            if ':' in param:
                param = param.split(':')[0].strip()
            if '=' in param:
                param = param.split('=')[0].strip()
            if param and param not in ['...']:
                params.append(param)
        return params

    def _estimate_body_lines(self, start_line: int) -> int:
        """Estimate function body line count by finding closing brace."""
        brace_count = 0
        started = False

        for i in range(start_line, len(self.lines)):
            line = self.lines[i]
            for char in line:
                if char == '{':
                    brace_count += 1
                    started = True
                elif char == '}':
                    brace_count -= 1

            if started and brace_count == 0:
                return i - start_line + 1

        return 1

    def _check_jsx_return(self, start_line: int) -> bool:
        """Check if function returns JSX (heuristic)."""
        for i in range(start_line, min(start_line + 20, len(self.lines))):
            line = self.lines[i]
            if 'return <' in line or ('return' in line and '<' in line):
                return True
            if 'return null' in line or 'return false' in line:
                return False
        return False


# ============================================================================
# Repository-Level Extraction
# ============================================================================

@dataclass
class TSRepositoryExtractionResult:
    """Aggregated extraction results for a TypeScript repository."""
    repo_path: str
    file_results: Dict[str, TSExtractionResult] = field(default_factory=dict)

    def to_json(self) -> str:
        """Export results as JSON."""
        data = {
            "repo_path": self.repo_path,
            "summary": {
                "total_files": len(self.file_results),
                "total_functions": sum(len(r.functions) for r in self.file_results.values()),
                "total_components": sum(len(r.components) for r in self.file_results.values()),
                "total_classes": sum(len(r.classes) for r in self.file_results.values()),
                "total_imports": sum(len(r.imports) for r in self.file_results.values())
            },
            "files": {}
        }

        for file_path, result in self.file_results.items():
            data["files"][file_path] = {
                "functions": [
                    {
                        "name": f.name,
                        "line_number": f.line_number,
                        "function_type": f.function_type,
                        "parameters": f.parameters,
                        "return_type": f.return_type,
                        "is_async": f.is_async,
                        "is_exported": f.is_exported,
                        "is_default_export": f.is_default_export,
                        "body_lines": f.body_lines
                    }
                    for f in result.functions
                ],
                "components": [
                    {
                        "name": c.name,
                        "line_number": c.line_number,
                        "component_type": c.component_type,
                        "props_type": c.props_type,
                        "is_exported": c.is_exported,
                        "is_default_export": c.is_default_export
                    }
                    for c in result.components
                ],
                "classes": [
                    {
                        "name": c.name,
                        "line_number": c.line_number,
                        "extends": c.extends,
                        "implements": c.implements,
                        "is_exported": c.is_exported
                    }
                    for c in result.classes
                ],
                "imports": [
                    {
                        "module": i.module,
                        "imports": i.imports,
                        "default_import": i.default_import,
                        "line_number": i.line_number,
                        "is_type_import": i.is_type_import
                    }
                    for i in result.imports
                ],
                "parse_errors": result.parse_errors
            }

        return json.dumps(data, indent=2)


def extract_typescript_repository(repo_path: Path) -> TSRepositoryExtractionResult:
    """Extract all TypeScript/TSX files from a repository."""
    result = TSRepositoryExtractionResult(repo_path=str(repo_path))

    ts_files = list(repo_path.glob("**/*.ts")) + list(repo_path.glob("**/*.tsx"))
    js_files = list(repo_path.glob("**/*.js")) + list(repo_path.glob("**/*.jsx"))
    all_files = ts_files + js_files

    print(f"Found {len(all_files)} TypeScript/JavaScript files in {repo_path}")

    for file_path in all_files:
        print(f"Extracting: {file_path.relative_to(repo_path)}")

        try:
            source_code = file_path.read_text(encoding="utf-8")
            extractor = TypeScriptExtractor(file_path, source_code)
            file_result = extractor.extract()
            result.file_results[str(file_path)] = file_result

            if file_result.parse_errors:
                print(f"  ⚠️  Parse errors: {file_result.parse_errors}")
            else:
                print(f"  ✅ Extracted: {len(file_result.functions)} functions, {len(file_result.components)} components, {len(file_result.classes)} classes")

        except Exception as e:
            print(f"  ❌ Failed to extract {file_path}: {e}")
            result.file_results[str(file_path)] = TSExtractionResult(
                file_path=str(file_path),
                parse_errors=[f"Read error: {str(e)}"]
            )

    return result


# ============================================================================
# CLI Interface
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python typescript_extractor.py <repo_path> [output.json]")
        sys.exit(1)

    repo_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)

    print(f"Extracting TypeScript repository: {repo_path}")
    print("=" * 80)

    result = extract_typescript_repository(repo_path)

    print("=" * 80)
    print(f"\nExtraction Summary:")
    print(f"  Files processed: {len(result.file_results)}")
    print(f"  Total functions: {sum(len(r.functions) for r in result.file_results.values())}")
    print(f"  Total components: {sum(len(r.components) for r in result.file_results.values())}")
    print(f"  Total classes: {sum(len(r.classes) for r in result.file_results.values())}")
    print(f"  Total imports: {sum(len(r.imports) for r in result.file_results.values())}")

    if output_path:
        output_path.write_text(result.to_json(), encoding="utf-8")
        print(f"\nResults exported to: {output_path}")
