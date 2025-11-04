"""
Dependency Analyzer for GraphCare

Builds call graphs, import graphs, and detects circular dependencies.
Analyzes coupling metrics and identifies tech debt.

Author: Kai (Chief Engineer, GraphCare)
Created: 2025-11-04
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict, deque


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class CallGraphNode:
    """Node in the function call graph."""
    function_name: str
    file_path: str
    calls: List[str]  # Functions this function calls
    called_by: List[str] = field(default_factory=list)  # Functions that call this
    complexity: int = 1


@dataclass
class ImportGraphNode:
    """Node in the module import graph."""
    module_path: str  # Relative path (e.g., "app/main.py")
    imports: List[str]  # Modules this module imports
    imported_by: List[str] = field(default_factory=list)  # Modules that import this


@dataclass
class CircularDependency:
    """Detected circular dependency."""
    cycle: List[str]  # List of nodes forming the cycle
    cycle_type: str  # "function_call" or "module_import"
    severity: str  # "high", "medium", "low"


@dataclass
class CouplingMetrics:
    """Coupling metrics for a node."""
    node_name: str
    afferent_coupling: int  # How many depend on me (incoming edges)
    efferent_coupling: int  # How many I depend on (outgoing edges)
    instability: float  # Efferent / (Afferent + Efferent)


@dataclass
class DependencyAnalysisResult:
    """Complete dependency analysis results."""
    repo_path: str
    call_graph: Dict[str, CallGraphNode] = field(default_factory=dict)
    import_graph: Dict[str, ImportGraphNode] = field(default_factory=dict)
    circular_dependencies: List[CircularDependency] = field(default_factory=list)
    coupling_metrics: List[CouplingMetrics] = field(default_factory=list)


# ============================================================================
# Call Graph Builder
# ============================================================================

class CallGraphBuilder:
    """Builds function call graph from extraction results."""

    def __init__(self, extraction_json: str):
        """
        Initialize with extraction JSON.

        Args:
            extraction_json: JSON string from python_ast_extractor.py output
        """
        self.data = json.loads(extraction_json)
        self.call_graph: Dict[str, CallGraphNode] = {}

    def build(self) -> Dict[str, CallGraphNode]:
        """Build complete call graph."""
        # First pass: Create nodes for all functions
        for file_path, file_data in self.data["files"].items():
            for func in file_data["functions"]:
                # Create unique function identifier (file:function)
                func_id = f"{file_path}:{func['name']}"

                node = CallGraphNode(
                    function_name=func['name'],
                    file_path=file_path,
                    calls=func['calls'],
                    complexity=func['complexity']
                )
                self.call_graph[func_id] = node

        # Second pass: Build reverse edges (called_by)
        for caller_id, caller_node in self.call_graph.items():
            for callee_name in caller_node.calls:
                # Find callee in graph (may be in same file or different file)
                callee_ids = self._find_function_by_name(callee_name)

                for callee_id in callee_ids:
                    if callee_id in self.call_graph:
                        self.call_graph[callee_id].called_by.append(caller_id)

        return self.call_graph

    def _find_function_by_name(self, func_name: str) -> List[str]:
        """Find all function IDs matching a function name."""
        # Handle method calls (e.g., "obj.method" -> "method")
        if "." in func_name:
            func_name = func_name.split(".")[-1]

        matching_ids = []
        for func_id, node in self.call_graph.items():
            if node.function_name == func_name:
                matching_ids.append(func_id)

        return matching_ids


# ============================================================================
# Import Graph Builder
# ============================================================================

class ImportGraphBuilder:
    """Builds module import graph from extraction results."""

    def __init__(self, extraction_json: str, repo_root: Path):
        """
        Initialize with extraction JSON.

        Args:
            extraction_json: JSON string from python_ast_extractor.py output
            repo_root: Path to repository root (for resolving relative imports)
        """
        self.data = json.loads(extraction_json)
        self.repo_root = repo_root
        self.import_graph: Dict[str, ImportGraphNode] = {}

    def build(self) -> Dict[str, ImportGraphNode]:
        """Build complete import graph."""
        # First pass: Create nodes for all modules
        for file_path in self.data["files"].keys():
            rel_path = self._get_relative_path(file_path)
            node = ImportGraphNode(
                module_path=rel_path,
                imports=[]
            )
            self.import_graph[rel_path] = node

        # Second pass: Build edges from imports
        for file_path, file_data in self.data["files"].items():
            source_module = self._get_relative_path(file_path)

            for imp in file_data["imports"]:
                # Resolve import to file path
                target_module = self._resolve_import(file_path, imp)

                if target_module and target_module in self.import_graph:
                    # Add forward edge
                    self.import_graph[source_module].imports.append(target_module)

                    # Add reverse edge
                    self.import_graph[target_module].imported_by.append(source_module)

        return self.import_graph

    def _get_relative_path(self, file_path: str) -> str:
        """Convert absolute file path to relative module path."""
        # Remove repo root prefix
        path = Path(file_path)
        try:
            rel = path.relative_to(self.repo_root)
            return str(rel)
        except ValueError:
            return str(path)

    def _resolve_import(self, source_file: str, import_data: Dict) -> Optional[str]:
        """
        Resolve import statement to actual file path.

        This is a simplified heuristic. Real implementation would need:
        - PYTHONPATH resolution
        - Package structure analysis
        - External vs internal import detection
        """
        module = import_data["module"]
        is_from_import = import_data["is_from_import"]

        # Skip external imports (heuristic: no "." prefix and common external packages)
        external_packages = {"fastapi", "pydantic", "typing", "os", "sys", "pathlib", "json", "datetime", "asyncio"}
        if not module.startswith(".") and any(module.startswith(pkg) for pkg in external_packages):
            return None

        # Handle relative imports (e.g., "from . import X" or "from .services import Y")
        if module.startswith("."):
            source_path = Path(source_file)
            source_dir = source_path.parent

            # Count dots to determine relative level
            level = 0
            while level < len(module) and module[level] == ".":
                level += 1

            # Go up 'level' directories
            target_dir = source_dir
            for _ in range(level - 1):
                target_dir = target_dir.parent

            # Append module path (minus dots)
            module_suffix = module[level:]
            if module_suffix:
                target_path = target_dir / module_suffix.replace(".", "/")
            else:
                target_path = target_dir

            # Try to find Python file
            if target_path.suffix != ".py":
                # Try __init__.py first
                if (target_path / "__init__.py").exists():
                    return self._get_relative_path(str(target_path / "__init__.py"))
                # Try .py file
                target_py = target_path.with_suffix(".py")
                if target_py.exists():
                    return self._get_relative_path(str(target_py))

        # Handle absolute internal imports (e.g., "from app.services import X")
        # Heuristic: Look for matching file in repo
        for file_path in self.data["files"].keys():
            if module.replace(".", "/") in file_path:
                return self._get_relative_path(file_path)

        return None


# ============================================================================
# Circular Dependency Detector
# ============================================================================

class CircularDependencyDetector:
    """Detects circular dependencies using Tarjan's algorithm."""

    def __init__(self, graph: Dict[str, any]):
        """
        Initialize with a dependency graph.

        Args:
            graph: Dictionary of node_id -> node with 'calls' or 'imports' attribute
        """
        self.graph = graph
        self.cycles: List[List[str]] = []

    def detect(self, edge_attr: str = "calls") -> List[CircularDependency]:
        """
        Detect circular dependencies.

        Args:
            edge_attr: Attribute name for edges ("calls" for call graph, "imports" for import graph)

        Returns:
            List of detected circular dependencies
        """
        # Use DFS-based cycle detection
        visited = set()
        rec_stack = set()
        path = []

        def dfs(node_id: str):
            visited.add(node_id)
            rec_stack.add(node_id)
            path.append(node_id)

            # Get neighbors
            node = self.graph[node_id]
            neighbors = getattr(node, edge_attr, [])

            for neighbor in neighbors:
                if neighbor not in self.graph:
                    continue

                if neighbor not in visited:
                    dfs(neighbor)
                elif neighbor in rec_stack:
                    # Cycle detected!
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    self.cycles.append(cycle)

            path.pop()
            rec_stack.remove(node_id)

        # Run DFS from each unvisited node
        for node_id in self.graph:
            if node_id not in visited:
                dfs(node_id)

        # Convert cycles to CircularDependency objects
        cycle_type = "function_call" if edge_attr == "calls" else "module_import"
        circular_deps = []

        for cycle in self.cycles:
            # Assess severity based on cycle length
            if len(cycle) <= 3:
                severity = "high"  # Short cycles are problematic
            elif len(cycle) <= 6:
                severity = "medium"
            else:
                severity = "low"  # Long cycles may be acceptable

            circular_deps.append(CircularDependency(
                cycle=cycle,
                cycle_type=cycle_type,
                severity=severity
            ))

        return circular_deps


# ============================================================================
# Coupling Metrics Calculator
# ============================================================================

class CouplingMetricsCalculator:
    """Calculates coupling metrics for dependency graph."""

    def __init__(self, graph: Dict[str, any], edge_attr: str, reverse_edge_attr: str):
        """
        Initialize with a dependency graph.

        Args:
            graph: Dictionary of node_id -> node
            edge_attr: Attribute for outgoing edges (e.g., "calls", "imports")
            reverse_edge_attr: Attribute for incoming edges (e.g., "called_by", "imported_by")
        """
        self.graph = graph
        self.edge_attr = edge_attr
        self.reverse_edge_attr = reverse_edge_attr

    def calculate(self) -> List[CouplingMetrics]:
        """Calculate coupling metrics for all nodes."""
        metrics = []

        for node_id, node in self.graph.items():
            afferent = len(getattr(node, self.reverse_edge_attr, []))
            efferent = len(getattr(node, self.edge_attr, []))

            # Calculate instability (I = Efferent / (Afferent + Efferent))
            total = afferent + efferent
            instability = efferent / total if total > 0 else 0.0

            metrics.append(CouplingMetrics(
                node_name=node_id,
                afferent_coupling=afferent,
                efferent_coupling=efferent,
                instability=instability
            ))

        return metrics


# ============================================================================
# Main Analyzer
# ============================================================================

def analyze_dependencies(extraction_json_path: Path, repo_root: Path) -> DependencyAnalysisResult:
    """
    Perform complete dependency analysis.

    Args:
        extraction_json_path: Path to JSON output from python_ast_extractor.py
        repo_root: Path to repository root

    Returns:
        DependencyAnalysisResult with all analysis results
    """
    # Load extraction results
    extraction_json = extraction_json_path.read_text(encoding="utf-8")
    data = json.loads(extraction_json)

    result = DependencyAnalysisResult(repo_path=data["repo_path"])

    print("Building call graph...")
    call_graph_builder = CallGraphBuilder(extraction_json)
    result.call_graph = call_graph_builder.build()
    print(f"  ✅ Call graph: {len(result.call_graph)} functions")

    print("Building import graph...")
    import_graph_builder = ImportGraphBuilder(extraction_json, repo_root)
    result.import_graph = import_graph_builder.build()
    print(f"  ✅ Import graph: {len(result.import_graph)} modules")

    print("Detecting circular dependencies (call graph)...")
    call_cycle_detector = CircularDependencyDetector(result.call_graph)
    call_cycles = call_cycle_detector.detect(edge_attr="calls")
    result.circular_dependencies.extend(call_cycles)
    print(f"  ✅ Call graph cycles: {len(call_cycles)}")

    print("Detecting circular dependencies (import graph)...")
    import_cycle_detector = CircularDependencyDetector(result.import_graph)
    import_cycles = import_cycle_detector.detect(edge_attr="imports")
    result.circular_dependencies.extend(import_cycles)
    print(f"  ✅ Import graph cycles: {len(import_cycles)}")

    print("Calculating coupling metrics...")
    call_coupling_calc = CouplingMetricsCalculator(result.call_graph, "calls", "called_by")
    result.coupling_metrics = call_coupling_calc.calculate()
    print(f"  ✅ Coupling metrics: {len(result.coupling_metrics)} nodes")

    return result


def export_analysis_report(result: DependencyAnalysisResult, output_path: Path):
    """Export analysis results as human-readable report."""
    lines = []

    lines.append("=" * 80)
    lines.append("DEPENDENCY ANALYSIS REPORT")
    lines.append("=" * 80)
    lines.append(f"\nRepository: {result.repo_path}\n")

    # Call Graph Summary
    lines.append("## Call Graph")
    lines.append(f"  Total functions: {len(result.call_graph)}")
    lines.append(f"  Total calls: {sum(len(node.calls) for node in result.call_graph.values())}")
    lines.append("")

    # Import Graph Summary
    lines.append("## Import Graph")
    lines.append(f"  Total modules: {len(result.import_graph)}")
    lines.append(f"  Total imports: {sum(len(node.imports) for node in result.import_graph.values())}")
    lines.append("")

    # Circular Dependencies
    lines.append("## Circular Dependencies")
    if result.circular_dependencies:
        for i, cycle in enumerate(result.circular_dependencies, 1):
            lines.append(f"\n### Cycle {i} ({cycle.severity} severity, {cycle.cycle_type})")
            for node in cycle.cycle:
                lines.append(f"  → {node}")
    else:
        lines.append("  ✅ No circular dependencies detected")
    lines.append("")

    # Coupling Metrics (Top 10 most coupled)
    lines.append("## Coupling Metrics (Top 10 Most Coupled)")
    sorted_metrics = sorted(result.coupling_metrics, key=lambda m: m.afferent_coupling + m.efferent_coupling, reverse=True)[:10]
    for metric in sorted_metrics:
        lines.append(f"\n  {metric.node_name}")
        lines.append(f"    Afferent (incoming): {metric.afferent_coupling}")
        lines.append(f"    Efferent (outgoing): {metric.efferent_coupling}")
        lines.append(f"    Instability: {metric.instability:.2f}")
    lines.append("")

    # High Instability Nodes (potential refactor candidates)
    lines.append("## High Instability Nodes (>0.8)")
    high_instability = [m for m in result.coupling_metrics if m.instability > 0.8 and m.efferent_coupling > 0]
    if high_instability:
        for metric in sorted(high_instability, key=lambda m: m.instability, reverse=True):
            lines.append(f"  {metric.node_name}: {metric.instability:.2f}")
    else:
        lines.append("  ✅ No highly unstable nodes")
    lines.append("")

    # Write report
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport exported to: {output_path}")


# ============================================================================
# CLI Interface
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python dependency_analyzer.py <extraction_json> <repo_root> [report_output.txt]")
        sys.exit(1)

    extraction_json_path = Path(sys.argv[1])
    repo_root = Path(sys.argv[2])
    report_output = Path(sys.argv[3]) if len(sys.argv) > 3 else None

    if not extraction_json_path.exists():
        print(f"Error: Extraction JSON not found: {extraction_json_path}")
        sys.exit(1)

    if not repo_root.exists():
        print(f"Error: Repository root not found: {repo_root}")
        sys.exit(1)

    print(f"Analyzing dependencies for: {repo_root}")
    print("=" * 80)

    result = analyze_dependencies(extraction_json_path, repo_root)

    print("=" * 80)
    print(f"\nAnalysis Summary:")
    print(f"  Call graph nodes: {len(result.call_graph)}")
    print(f"  Import graph nodes: {len(result.import_graph)}")
    print(f"  Circular dependencies: {len(result.circular_dependencies)}")
    print(f"  Coupling metrics calculated: {len(result.coupling_metrics)}")

    if report_output:
        export_analysis_report(result, report_output)
