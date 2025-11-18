#!/usr/bin/env python3
"""
GraphCare Graph Linter - Validates L2 graph structure

Runs 7 structural checks (C1-C7) adapted from Mind Protocol:
- C1: Valid node/link types (U4_* schema)
- C2: Required metadata fields
- C3: Confidence/base_weight/energy in valid range [0,1]
- C4: No orphan nodes (all nodes connected)
- C5: No duplicate edges
- C6: No self-loops (unless allowed)
- C7: Bidirectional edge consistency

Author: Mel (Chief Care Coordinator, GraphCare)
Date: 2025-11-05
Pattern: Mind Protocol lint_graph.py adapted for REST API + U4 types
"""

import requests
import sys
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum

# API Configuration
API_URL = "https://mindprotocol.onrender.com/admin/query"
API_KEY = "Sxv48F2idLAXMnvqQTdvlQ4gArsDVhK4ROGyU"


class Severity(str, Enum):
    """Violation severity levels."""
    ERROR = "ERROR"
    WARNING = "WARNING"


@dataclass
class Violation:
    """A lint violation."""
    check: str
    severity: Severity
    message: str
    node_id: str = None
    edge: Tuple[str, str, str] = None
    metadata: Dict[str, Any] = None


class GraphLinter:
    """
    Validates L2 graph structure against U4 schema and quality standards.
    """

    # Valid U4 node types for L2 (organizational graphs)
    VALID_NODE_TYPES = {
        'U4_Agent', 'U4_Code_Artifact', 'U4_Knowledge_Object',
        'U4_Assessment', 'U4_Work_Item', 'U4_Event', 'U4_Goal',
        'U4_Resource', 'U4_Subentity', 'U4_Policy', 'Layer',
        'GraphCare_Schema'
    }

    # Valid U4 link types for L2
    VALID_LINK_TYPES = {
        'U4_MEMBER_OF', 'U4_DEPENDS_ON', 'U4_ENABLES', 'U4_CALLS',
        'U4_IMPLEMENTS', 'U4_DOCUMENTS', 'U4_TESTS', 'U4_REFINES',
        'U4_VALIDATES', 'U4_RELATES_TO', 'IN_LAYER', 'USES_SCHEMA',
        'EXPOSES'
    }

    # Edge types that allow self-loops
    ALLOWED_SELF_LOOPS = {'U4_REFINES'}

    def __init__(self, graph_name: str, config: Dict[str, bool] = None):
        """
        Initialize linter.

        Args:
            graph_name: FalkorDB graph name to lint
            config: Check enable/disable config (default: all enabled)
        """
        self.graph_name = graph_name
        self.headers = {
            "X-API-Key": API_KEY,
            "Content-Type": "application/json"
        }
        self.config = config or {
            'enable_c1_check': True,
            'enable_c2_check': True,
            'enable_c3_check': True,
            'enable_c4_check': True,
            'enable_c5_check': True,
            'enable_c6_check': True,
            'enable_c7_check': True,
        }

    def execute_query(self, cypher: str) -> Dict[str, Any]:
        """Execute Cypher query via REST API."""
        payload = {"graph_name": self.graph_name, "query": cypher}
        try:
            response = requests.post(API_URL, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def run_all_checks(self) -> List[Violation]:
        """Run all enabled checks."""
        violations = []

        if self.config.get('enable_c1_check'):
            violations.extend(self.check_c1_valid_types())

        if self.config.get('enable_c2_check'):
            violations.extend(self.check_c2_required_metadata())

        if self.config.get('enable_c3_check'):
            violations.extend(self.check_c3_value_ranges())

        if self.config.get('enable_c4_check'):
            violations.extend(self.check_c4_no_orphans())

        if self.config.get('enable_c5_check'):
            violations.extend(self.check_c5_no_duplicates())

        if self.config.get('enable_c6_check'):
            violations.extend(self.check_c6_no_self_loops())

        if self.config.get('enable_c7_check'):
            violations.extend(self.check_c7_bidirectional_consistency())

        return violations

    def check_c1_valid_types(self) -> List[Violation]:
        """C1: Validate node and link types against U4 schema."""
        violations = []

        # Check node types
        cypher = "MATCH (n) RETURN DISTINCT labels(n) AS labels"
        result = self.execute_query(cypher)

        if 'error' in result:
            violations.append(Violation(
                check="C1", severity=Severity.ERROR,
                message=f"Failed to query node types: {result['error']}"
            ))
            return violations

        if 'result' in result and len(result['result']) >= 2:
            for row in result['result'][1]:
                labels = row[0] if row else []
                for label in labels if isinstance(labels, list) else [labels]:
                    if label not in self.VALID_NODE_TYPES:
                        violations.append(Violation(
                            check="C1", severity=Severity.WARNING,
                            message=f"Unknown node type: {label}"
                        ))

        # Check link types
        cypher = "MATCH ()-[r]->() RETURN DISTINCT type(r) AS type"
        result = self.execute_query(cypher)

        if 'result' in result and len(result['result']) >= 2:
            for row in result['result'][1]:
                link_type = row[0] if row else None
                if link_type and link_type not in self.VALID_LINK_TYPES:
                    violations.append(Violation(
                        check="C1", severity=Severity.WARNING,
                        message=f"Unknown link type: {link_type}"
                    ))

        return violations

    def check_c2_required_metadata(self) -> List[Violation]:
        """C2: Validate required metadata fields on nodes and edges."""
        violations = []

        # Required universal node fields (from U4 schema)
        required_node_fields = {'id', 'level', 'scope_ref'}

        cypher = "MATCH (n) RETURN n.id as id, keys(n) as props LIMIT 100"
        result = self.execute_query(cypher)

        if 'result' in result and len(result['result']) >= 2:
            for row in result['result'][1]:
                node_id = row[0]
                props_str = row[1] if len(row) > 1 else ""

                # Parse property keys (FalkorDB returns string like "[id, name, ...]")
                if isinstance(props_str, str):
                    props_str = props_str.strip('[]')
                    props = set(p.strip() for p in props_str.split(',') if p.strip())
                else:
                    props = set(props_str) if props_str else set()

                missing = required_node_fields - props
                if missing:
                    violations.append(Violation(
                        check="C2", severity=Severity.ERROR,
                        message=f"Node missing required fields: {missing}",
                        node_id=node_id
                    ))

        return violations

    def check_c3_value_ranges(self) -> List[Violation]:
        """C3: Validate confidence/base_weight/energy in range [0,1]."""
        violations = []

        # Check edge confidence and energy
        cypher = """
        MATCH ()-[r]->()
        WHERE r.confidence IS NOT NULL OR r.energy IS NOT NULL
        RETURN r.confidence as conf, r.energy as energy, type(r) as type
        LIMIT 100
        """
        result = self.execute_query(cypher)

        if 'result' in result and len(result['result']) >= 2:
            for row in result['result'][1]:
                conf = row[0] if row else None
                energy = row[1] if len(row) > 1 else None
                edge_type = row[2] if len(row) > 2 else "unknown"

                if conf is not None and not (0 <= float(conf) <= 1):
                    violations.append(Violation(
                        check="C3", severity=Severity.ERROR,
                        message=f"Confidence out of range [0,1]: {conf}",
                        metadata={'edge_type': edge_type}
                    ))

                if energy is not None and not (0 <= float(energy) <= 1):
                    violations.append(Violation(
                        check="C3", severity=Severity.ERROR,
                        message=f"Energy out of range [0,1]: {energy}",
                        metadata={'edge_type': edge_type}
                    ))

        # Check node base_weight
        cypher = """
        MATCH (n)
        WHERE n.base_weight IS NOT NULL
        RETURN n.id as id, n.base_weight as weight
        LIMIT 100
        """
        result = self.execute_query(cypher)

        if 'result' in result and len(result['result']) >= 2:
            for row in result['result'][1]:
                node_id = row[0] if row else None
                weight = row[1] if len(row) > 1 else None

                if weight is not None and not (0 <= float(weight) <= 1):
                    violations.append(Violation(
                        check="C3", severity=Severity.ERROR,
                        message=f"base_weight out of range [0,1]: {weight}",
                        node_id=node_id
                    ))

        return violations

    def check_c4_no_orphans(self) -> List[Violation]:
        """C4: Ensure no orphan nodes (all nodes have at least one edge)."""
        violations = []

        cypher = """
        MATCH (n)
        WHERE NOT (n)-[]-()
        RETURN n.id AS id, labels(n) AS labels
        LIMIT 50
        """
        result = self.execute_query(cypher)

        if 'result' in result and len(result['result']) >= 2:
            for row in result['result'][1]:
                node_id = row[0] if row else "unknown"
                labels = row[1] if len(row) > 1 else []

                violations.append(Violation(
                    check="C4", severity=Severity.WARNING,
                    message=f"Orphan node (no connections)",
                    node_id=node_id,
                    metadata={'labels': labels}
                ))

        return violations

    def check_c5_no_duplicates(self) -> List[Violation]:
        """C5: Ensure no duplicate edges (same source→target→type)."""
        violations = []

        cypher = """
        MATCH (a)-[r]->(b)
        WITH a.id AS source, b.id AS target, type(r) AS edge_type, COUNT(*) AS cnt
        WHERE cnt > 1
        RETURN source, target, edge_type, cnt
        """
        result = self.execute_query(cypher)

        if 'result' in result and len(result['result']) >= 2:
            for row in result['result'][1]:
                source = row[0] if row else "unknown"
                target = row[1] if len(row) > 1 else "unknown"
                edge_type = row[2] if len(row) > 2 else "unknown"
                count = row[3] if len(row) > 3 else 0

                violations.append(Violation(
                    check="C5", severity=Severity.ERROR,
                    message=f"Duplicate edge ({count} instances)",
                    edge=(source, target, edge_type)
                ))

        return violations

    def check_c6_no_self_loops(self) -> List[Violation]:
        """C6: Ensure no disallowed self-loops."""
        violations = []

        cypher = """
        MATCH (n)-[r]->(n)
        RETURN type(r) AS edge_type, n.id AS node_id
        """
        result = self.execute_query(cypher)

        if 'result' in result and len(result['result']) >= 2:
            for row in result['result'][1]:
                edge_type = row[0] if row else "unknown"
                node_id = row[1] if len(row) > 1 else "unknown"

                if edge_type not in self.ALLOWED_SELF_LOOPS:
                    violations.append(Violation(
                        check="C6", severity=Severity.ERROR,
                        message=f"Disallowed self-loop: {edge_type}",
                        node_id=node_id
                    ))

        return violations

    def check_c7_bidirectional_consistency(self) -> List[Violation]:
        """C7: Validate bidirectional edge consistency."""
        violations = []

        cypher = """
        MATCH (a)-[r1]->(b)-[r2]->(a)
        RETURN a.id AS node_a, b.id AS node_b,
               type(r1) AS type_ab, type(r2) AS type_ba
        LIMIT 20
        """
        result = self.execute_query(cypher)

        if 'result' in result and len(result['result']) >= 2:
            for row in result['result'][1]:
                node_a = row[0] if row else "unknown"
                node_b = row[1] if len(row) > 1 else "unknown"
                type_ab = row[2] if len(row) > 2 else "unknown"
                type_ba = row[3] if len(row) > 3 else "unknown"

                # Bidirectional edges should be intentional
                violations.append(Violation(
                    check="C7", severity=Severity.WARNING,
                    message=f"Bidirectional edges (review if intentional): {type_ab} ↔ {type_ba}",
                    edge=(node_a, node_b, f"{type_ab}↔{type_ba}")
                ))

        return violations

    def format_report(self, violations: List[Violation]) -> str:
        """Format violations as human-readable report."""
        if not violations:
            return "✅ All checks passed! Graph structure valid.\n"

        lines = ["=" * 80, "GraphCare Graph Lint Report", "=" * 80, ""]

        # Group by check
        by_check: Dict[str, List[Violation]] = {}
        for v in violations:
            by_check.setdefault(v.check, []).append(v)

        # Count by severity
        errors = sum(1 for v in violations if v.severity == Severity.ERROR)
        warnings = sum(1 for v in violations if v.severity == Severity.WARNING)

        lines.append(f"Total violations: {len(violations)} ({errors} errors, {warnings} warnings)")
        lines.append("")

        # Report by check
        for check_id in sorted(by_check.keys()):
            check_violations = by_check[check_id]
            lines.append(f"[{check_id}] {len(check_violations)} violations:")

            for v in check_violations[:10]:
                severity_icon = "❌" if v.severity == Severity.ERROR else "⚠️"
                lines.append(f"  {severity_icon} {v.message}")

                if v.node_id:
                    lines.append(f"      Node: {v.node_id}")
                if v.edge:
                    lines.append(f"      Edge: {v.edge[0]} → {v.edge[1]} ({v.edge[2]})")

            if len(check_violations) > 10:
                lines.append(f"  ... and {len(check_violations) - 10} more")

            lines.append("")

        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python lint_graph.py <graph_name>")
        print("\nExample:")
        print("  python lint_graph.py scopelock")
        sys.exit(1)

    graph_name = sys.argv[1]

    print(f"Linting graph: {graph_name}\n")

    linter = GraphLinter(graph_name)
    violations = linter.run_all_checks()

    print(linter.format_report(violations))

    # Exit code: 0 if no errors, 1 if errors
    has_errors = any(v.severity == Severity.ERROR for v in violations)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
