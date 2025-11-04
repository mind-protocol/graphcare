"""
Python AST Extractor for GraphCare

Extracts functions, classes, imports, and calls from Python source code using ast.NodeVisitor pattern.
Based on Mind Protocol's mp-lint scanner architecture.

Author: Kai (Chief Engineer, GraphCare)
Created: 2025-11-04
"""

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Any
import json


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class FunctionMetadata:
    """Metadata for a Python function."""
    name: str
    file_path: str
    line_start: int
    line_end: int
    parameters: List[str]
    return_type: Optional[str]
    decorators: List[str]
    docstring: Optional[str]
    is_async: bool
    is_method: bool  # True if inside a class
    parent_class: Optional[str]  # Class name if method
    calls: List[str]  # Function names called within this function
    complexity: int  # Cyclomatic complexity


@dataclass
class ClassMetadata:
    """Metadata for a Python class."""
    name: str
    file_path: str
    line_start: int
    line_end: int
    bases: List[str]  # Base class names
    decorators: List[str]
    docstring: Optional[str]
    methods: List[str]  # Method names
    attributes: List[str]  # Instance/class attributes


@dataclass
class ImportMetadata:
    """Metadata for an import statement."""
    module: str  # Module being imported (e.g., "os", "pathlib.Path")
    names: List[str]  # Names imported (e.g., ["join", "exists"] for "from os.path import join, exists")
    alias: Optional[str]  # Alias if used (e.g., "pd" for "import pandas as pd")
    file_path: str
    line_number: int
    is_from_import: bool  # True for "from X import Y", False for "import X"


@dataclass
class CallMetadata:
    """Metadata for a function call."""
    function_name: str  # Name of function being called
    file_path: str
    line_number: int
    caller_function: Optional[str]  # Function containing this call
    caller_class: Optional[str]  # Class containing caller function (if method)


@dataclass
class ExtractionResult:
    """Complete extraction results for a Python file."""
    file_path: str
    functions: List[FunctionMetadata] = field(default_factory=list)
    classes: List[ClassMetadata] = field(default_factory=list)
    imports: List[ImportMetadata] = field(default_factory=list)
    calls: List[CallMetadata] = field(default_factory=list)
    parse_errors: List[str] = field(default_factory=list)


# ============================================================================
# AST Visitors (Following Mind Protocol mp-lint pattern)
# ============================================================================

class PythonASTExtractor(ast.NodeVisitor):
    """
    Main extractor using ast.NodeVisitor pattern.

    Extracts all functions, classes, imports, and calls from Python source code.
    Handles nesting (methods inside classes, nested functions).
    """

    def __init__(self, file_path: Path, source_code: str):
        self.file_path = str(file_path)
        self.source_code = source_code
        self.source_lines = source_code.splitlines()

        # Extraction results
        self.functions: List[FunctionMetadata] = []
        self.classes: List[ClassMetadata] = []
        self.imports: List[ImportMetadata] = []
        self.calls: List[CallMetadata] = []

        # Context tracking (for nested structures)
        self.current_class: Optional[str] = None
        self.current_function: Optional[str] = None
        self.function_calls_buffer: List[str] = []  # Calls within current function

        # Parent tracking (for walking with context)
        self._parent_map: Dict[ast.AST, Optional[ast.AST]] = {}

    def extract(self) -> ExtractionResult:
        """Main extraction method. Returns complete extraction results."""
        try:
            tree = ast.parse(self.source_code, filename=self.file_path)
            self._build_parent_map(tree)
            self.visit(tree)

            return ExtractionResult(
                file_path=self.file_path,
                functions=self.functions,
                classes=self.classes,
                imports=self.imports,
                calls=self.calls,
                parse_errors=[]
            )
        except SyntaxError as e:
            return ExtractionResult(
                file_path=self.file_path,
                parse_errors=[f"SyntaxError at line {e.lineno}: {e.msg}"]
            )
        except Exception as e:
            return ExtractionResult(
                file_path=self.file_path,
                parse_errors=[f"Extraction error: {str(e)}"]
            )

    def _build_parent_map(self, node: ast.AST, parent: Optional[ast.AST] = None):
        """Build parent reference map for context-aware traversal."""
        self._parent_map[node] = parent
        for child in ast.iter_child_nodes(node):
            self._build_parent_map(child, node)

    def _get_parent(self, node: ast.AST) -> Optional[ast.AST]:
        """Get parent node."""
        return self._parent_map.get(node)

    def _get_docstring(self, node: ast.AST) -> Optional[str]:
        """Extract docstring from function/class node."""
        if (isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and
            node.body and
            isinstance(node.body[0], ast.Expr) and
            isinstance(node.body[0].value, ast.Constant) and
            isinstance(node.body[0].value.value, str)):
            return node.body[0].value.value
        return None

    def _get_decorator_names(self, node: ast.AST) -> List[str]:
        """Extract decorator names from function/class node."""
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            return []

        decorators = []
        for dec in node.decorator_list:
            if isinstance(dec, ast.Name):
                decorators.append(dec.id)
            elif isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name):
                decorators.append(dec.func.id)
            elif isinstance(dec, ast.Attribute):
                decorators.append(ast.unparse(dec))
        return decorators

    def _calculate_complexity(self, node: ast.AST) -> int:
        """
        Calculate cyclomatic complexity for a function.

        Complexity = 1 + number of decision points (if, while, for, except, and, or, etc.)
        """
        complexity = 1

        for child in ast.walk(node):
            # Decision points that increase complexity
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.BoolOp) and isinstance(child.op, (ast.And, ast.Or)):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.comprehension) and child.ifs:
                complexity += len(child.ifs)

        return complexity

    def _get_line_end(self, node: ast.AST) -> int:
        """Get the ending line number of a node."""
        if hasattr(node, 'end_lineno') and node.end_lineno is not None:
            return node.end_lineno
        return node.lineno  # Fallback to start line

    # ========================================================================
    # Visitors
    # ========================================================================

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Extract function metadata."""
        self._extract_function(node, is_async=False)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Extract async function metadata."""
        self._extract_function(node, is_async=True)
        self.generic_visit(node)

    def _extract_function(self, node: ast.AST, is_async: bool):
        """Common logic for extracting function/method metadata."""
        # Save previous context
        prev_function = self.current_function
        prev_calls = self.function_calls_buffer

        # Set current context
        self.current_function = node.name
        self.function_calls_buffer = []

        # Extract parameters
        parameters = [arg.arg for arg in node.args.args]

        # Extract return type (if annotated)
        return_type = None
        if node.returns:
            return_type = ast.unparse(node.returns)

        # Check if this is a method (inside a class)
        is_method = self.current_class is not None

        # Create metadata
        func_meta = FunctionMetadata(
            name=node.name,
            file_path=self.file_path,
            line_start=node.lineno,
            line_end=self._get_line_end(node),
            parameters=parameters,
            return_type=return_type,
            decorators=self._get_decorator_names(node),
            docstring=self._get_docstring(node),
            is_async=is_async,
            is_method=is_method,
            parent_class=self.current_class if is_method else None,
            calls=[],  # Will be filled after visiting children
            complexity=self._calculate_complexity(node)
        )

        # Visit children to collect calls
        for child in ast.iter_child_nodes(node):
            self.visit(child)

        # Assign collected calls
        func_meta.calls = self.function_calls_buffer.copy()

        # Save function metadata
        self.functions.append(func_meta)

        # Restore previous context
        self.current_function = prev_function
        self.function_calls_buffer = prev_calls

    def visit_ClassDef(self, node: ast.ClassDef):
        """Extract class metadata."""
        # Save previous context
        prev_class = self.current_class

        # Set current context
        self.current_class = node.name

        # Extract base classes
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(ast.unparse(base))

        # Extract methods (will be filled during traversal)
        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(item.name)

        # Extract attributes (simple heuristic: assignments in __init__ or at class level)
        attributes = self._extract_class_attributes(node)

        # Create metadata
        class_meta = ClassMetadata(
            name=node.name,
            file_path=self.file_path,
            line_start=node.lineno,
            line_end=self._get_line_end(node),
            bases=bases,
            decorators=self._get_decorator_names(node),
            docstring=self._get_docstring(node),
            methods=methods,
            attributes=attributes
        )

        # Save class metadata
        self.classes.append(class_meta)

        # Visit children (will extract methods)
        self.generic_visit(node)

        # Restore previous context
        self.current_class = prev_class

    def _extract_class_attributes(self, node: ast.ClassDef) -> List[str]:
        """Extract instance and class attributes."""
        attributes = set()

        # Class-level assignments
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                attributes.add(item.target.id)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.add(target.id)

        # Instance attributes in __init__ (self.x = ...)
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == "__init__":
                for stmt in ast.walk(item):
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self":
                                attributes.add(target.attr)

        return sorted(list(attributes))

    def visit_Import(self, node: ast.Import):
        """Extract import statements (import X, import Y as Z)."""
        for alias in node.names:
            import_meta = ImportMetadata(
                module=alias.name,
                names=[alias.name],
                alias=alias.asname,
                file_path=self.file_path,
                line_number=node.lineno,
                is_from_import=False
            )
            self.imports.append(import_meta)

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Extract from-import statements (from X import Y, Z)."""
        module = node.module or ""
        names = [alias.name for alias in node.names]

        # Handle "from . import X" (relative imports)
        if node.level > 0:
            module = "." * node.level + module

        import_meta = ImportMetadata(
            module=module,
            names=names,
            alias=None,  # from-imports don't have module-level alias
            file_path=self.file_path,
            line_number=node.lineno,
            is_from_import=True
        )
        self.imports.append(import_meta)

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        """Extract function calls."""
        # Get function name
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = ast.unparse(node.func)

        if func_name:
            # Add to current function's call list
            if self.current_function:
                self.function_calls_buffer.append(func_name)

            # Create call metadata
            call_meta = CallMetadata(
                function_name=func_name,
                file_path=self.file_path,
                line_number=node.lineno,
                caller_function=self.current_function,
                caller_class=self.current_class
            )
            self.calls.append(call_meta)

        self.generic_visit(node)


# ============================================================================
# Repository-Level Extraction
# ============================================================================

@dataclass
class RepositoryExtractionResult:
    """Aggregated extraction results for an entire repository."""
    repo_path: str
    file_results: Dict[str, ExtractionResult] = field(default_factory=dict)

    @property
    def all_functions(self) -> List[FunctionMetadata]:
        """Get all functions across all files."""
        functions = []
        for result in self.file_results.values():
            functions.extend(result.functions)
        return functions

    @property
    def all_classes(self) -> List[ClassMetadata]:
        """Get all classes across all files."""
        classes = []
        for result in self.file_results.values():
            classes.extend(result.classes)
        return classes

    @property
    def all_imports(self) -> List[ImportMetadata]:
        """Get all imports across all files."""
        imports = []
        for result in self.file_results.values():
            imports.extend(result.imports)
        return imports

    @property
    def all_calls(self) -> List[CallMetadata]:
        """Get all calls across all files."""
        calls = []
        for result in self.file_results.values():
            calls.extend(result.calls)
        return calls

    def to_json(self) -> str:
        """Export results as JSON."""
        data = {
            "repo_path": self.repo_path,
            "summary": {
                "total_files": len(self.file_results),
                "total_functions": len(self.all_functions),
                "total_classes": len(self.all_classes),
                "total_imports": len(self.all_imports),
                "total_calls": len(self.all_calls)
            },
            "files": {}
        }

        for file_path, result in self.file_results.items():
            data["files"][file_path] = {
                "functions": [
                    {
                        "name": f.name,
                        "line_start": f.line_start,
                        "line_end": f.line_end,
                        "parameters": f.parameters,
                        "return_type": f.return_type,
                        "decorators": f.decorators,
                        "is_async": f.is_async,
                        "is_method": f.is_method,
                        "parent_class": f.parent_class,
                        "calls": f.calls,
                        "complexity": f.complexity
                    }
                    for f in result.functions
                ],
                "classes": [
                    {
                        "name": c.name,
                        "line_start": c.line_start,
                        "line_end": c.line_end,
                        "bases": c.bases,
                        "decorators": c.decorators,
                        "methods": c.methods,
                        "attributes": c.attributes
                    }
                    for c in result.classes
                ],
                "imports": [
                    {
                        "module": i.module,
                        "names": i.names,
                        "alias": i.alias,
                        "line_number": i.line_number,
                        "is_from_import": i.is_from_import
                    }
                    for i in result.imports
                ],
                "parse_errors": result.parse_errors
            }

        return json.dumps(data, indent=2)


def extract_repository(repo_path: Path, pattern: str = "**/*.py") -> RepositoryExtractionResult:
    """
    Extract all Python files from a repository.

    Args:
        repo_path: Path to repository root
        pattern: Glob pattern for files to extract (default: **/*.py)

    Returns:
        RepositoryExtractionResult with all extracted data
    """
    result = RepositoryExtractionResult(repo_path=str(repo_path))

    # Find all Python files
    python_files = list(repo_path.glob(pattern))

    print(f"Found {len(python_files)} Python files in {repo_path}")

    for file_path in python_files:
        print(f"Extracting: {file_path.relative_to(repo_path)}")

        try:
            source_code = file_path.read_text(encoding="utf-8")
            extractor = PythonASTExtractor(file_path, source_code)
            file_result = extractor.extract()
            result.file_results[str(file_path)] = file_result

            if file_result.parse_errors:
                print(f"  ⚠️  Parse errors: {file_result.parse_errors}")
            else:
                print(f"  ✅ Extracted: {len(file_result.functions)} functions, {len(file_result.classes)} classes")

        except Exception as e:
            print(f"  ❌ Failed to extract {file_path}: {e}")
            result.file_results[str(file_path)] = ExtractionResult(
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
        print("Usage: python python_ast_extractor.py <repo_path> [output.json]")
        sys.exit(1)

    repo_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)

    print(f"Extracting repository: {repo_path}")
    print("=" * 80)

    result = extract_repository(repo_path)

    print("=" * 80)
    print(f"\nExtraction Summary:")
    print(f"  Files processed: {len(result.file_results)}")
    print(f"  Total functions: {len(result.all_functions)}")
    print(f"  Total classes: {len(result.all_classes)}")
    print(f"  Total imports: {len(result.all_imports)}")
    print(f"  Total calls: {len(result.all_calls)}")

    # Calculate complexity statistics
    complexities = [f.complexity for f in result.all_functions]
    if complexities:
        avg_complexity = sum(complexities) / len(complexities)
        max_complexity = max(complexities)
        high_complexity_count = sum(1 for c in complexities if c > 15)

        print(f"\nComplexity Metrics:")
        print(f"  Average complexity: {avg_complexity:.2f}")
        print(f"  Max complexity: {max_complexity}")
        print(f"  Functions with high complexity (>15): {high_complexity_count}")

    # Export to JSON if requested
    if output_path:
        output_path.write_text(result.to_json(), encoding="utf-8")
        print(f"\nResults exported to: {output_path}")
