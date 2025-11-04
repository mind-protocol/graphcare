"""
GraphCare Corpus Analyzer - Analyze client codebase structure

Generates:
- File type distribution
- Documentation coverage metrics
- Code structure analysis
- Initial extraction strategy recommendation

Author: Quinn (Chief Cartographer, GraphCare)
Date: 2025-11-04
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


class CorpusAnalyzer:
    """Analyze client corpus structure and recommend extraction strategy."""

    def __init__(self, repo_path: str):
        """Initialize analyzer with repository path."""
        self.repo_path = Path(repo_path)
        self.file_counts = defaultdict(int)
        self.doc_files = []
        self.code_files = []
        self.config_files = []
        self.total_size = 0

    def scan_repository(self):
        """Scan repository and categorize files."""
        exclude_dirs = {'.git', 'node_modules', '__pycache__', '.next', 'dist', 'build', 'test-results'}

        for root, dirs, files in os.walk(self.repo_path):
            # Exclude certain directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.repo_path)

                # Get file extension
                ext = file_path.suffix.lower()

                # Categorize file
                if ext == '.md':
                    self.doc_files.append(str(rel_path))
                    self.file_counts['documentation'] += 1
                elif ext in ['.py']:
                    self.code_files.append(str(rel_path))
                    self.file_counts['python'] += 1
                elif ext in ['.ts', '.tsx']:
                    self.code_files.append(str(rel_path))
                    self.file_counts['typescript'] += 1
                elif ext in ['.js', '.jsx']:
                    self.code_files.append(str(rel_path))
                    self.file_counts['javascript'] += 1
                elif ext in ['.yaml', '.yml', '.json', '.toml']:
                    self.config_files.append(str(rel_path))
                    self.file_counts['config'] += 1
                else:
                    self.file_counts['other'] += 1

                # Track size
                try:
                    self.total_size += file_path.stat().st_size
                except:
                    pass

    def detect_documentation_types(self) -> Dict[str, List[str]]:
        """Detect documentation types (ADR, spec, guide, etc.)."""
        doc_types = {
            'architecture': [],
            'specification': [],
            'guide': [],
            'readme': [],
            'workflow': [],
            'identity': [],  # CLAUDE.md files
            'other': []
        }

        for doc_path in self.doc_files:
            doc_lower = doc_path.lower()

            if 'architecture' in doc_lower or 'arch' in doc_lower:
                doc_types['architecture'].append(doc_path)
            elif 'spec' in doc_lower or 'specification' in doc_lower:
                doc_types['specification'].append(doc_path)
            elif 'guide' in doc_lower or 'tutorial' in doc_lower or 'howto' in doc_lower:
                doc_types['guide'].append(doc_path)
            elif 'readme' in doc_lower:
                doc_types['readme'].append(doc_path)
            elif 'workflow' in doc_lower or 'sync' in doc_lower or 'roadmap' in doc_lower:
                doc_types['workflow'].append(doc_path)
            elif 'claude' in doc_lower:
                doc_types['identity'].append(doc_path)
            else:
                doc_types['other'].append(doc_path)

        return doc_types

    def detect_code_structure(self) -> Dict[str, any]:
        """Analyze code structure."""
        structure = {
            'backend': {
                'python_files': [],
                'entry_points': [],
                'services': [],
                'total': 0
            },
            'frontend': {
                'typescript_files': [],
                'components': [],
                'pages': [],
                'total': 0
            },
            'scripts': {
                'automation': [],
                'total': 0
            }
        }

        for code_path in self.code_files:
            if 'backend' in code_path or code_path.endswith('.py'):
                structure['backend']['python_files'].append(code_path)
                structure['backend']['total'] += 1

                if 'main.py' in code_path or 'app.py' in code_path:
                    structure['backend']['entry_points'].append(code_path)
                elif any(x in code_path for x in ['service', 'handler', 'controller']):
                    structure['backend']['services'].append(code_path)

            elif 'src' in code_path or code_path.endswith(('.ts', '.tsx', '.jsx')):
                structure['frontend']['typescript_files'].append(code_path)
                structure['frontend']['total'] += 1

                if 'component' in code_path.lower():
                    structure['frontend']['components'].append(code_path)
                elif 'page' in code_path.lower() or 'app' in code_path:
                    structure['frontend']['pages'].append(code_path)

            elif 'script' in code_path:
                structure['scripts']['automation'].append(code_path)
                structure['scripts']['total'] += 1

        return structure

    def calculate_coverage_ratio(self) -> float:
        """Calculate documentation-to-code ratio."""
        total_code = self.file_counts['python'] + self.file_counts['typescript'] + self.file_counts['javascript']
        total_docs = self.file_counts['documentation']

        if total_code == 0:
            return 0.0

        return total_docs / total_code

    def recommend_strategy(self, doc_types: Dict[str, List[str]], code_structure: Dict[str, any], coverage_ratio: float) -> str:
        """Recommend extraction strategy based on corpus characteristics."""

        # Count architecture docs
        arch_docs = len(doc_types['architecture']) + len(doc_types['specification'])
        total_docs = len(self.doc_files)
        total_code = len(self.code_files)

        # Decision logic
        if coverage_ratio > 5.0:
            strategy = "DOCS_FIRST"
            reasoning = f"Very high doc-to-code ratio ({coverage_ratio:.1f}:1). Rich documentation ({total_docs} docs) dominates small codebase ({total_code} files)."
        elif coverage_ratio > 2.0 and arch_docs >= 3:
            strategy = "DOCS_FIRST"
            reasoning = f"High doc-to-code ratio ({coverage_ratio:.1f}:1) with {arch_docs} architectural documents. Documentation likely comprehensive."
        elif coverage_ratio < 0.5:
            strategy = "CODE_FIRST"
            reasoning = f"Low doc-to-code ratio ({coverage_ratio:.1f}:1). Code is primary source of truth."
        elif arch_docs == 0:
            strategy = "CODE_FIRST"
            reasoning = f"No architectural documentation found. Extract from code ({total_code} files)."
        else:
            strategy = "HYBRID"
            reasoning = f"Balanced corpus (ratio: {coverage_ratio:.1f}:1). Extract architecture from docs ({arch_docs} specs), implementation from code."

        return f"{strategy}: {reasoning}"

    def generate_report(self) -> Dict:
        """Generate full corpus analysis report."""
        self.scan_repository()

        doc_types = self.detect_documentation_types()
        code_structure = self.detect_code_structure()
        coverage_ratio = self.calculate_coverage_ratio()
        strategy = self.recommend_strategy(doc_types, code_structure, coverage_ratio)

        report = {
            'repository': str(self.repo_path.name),
            'summary': {
                'total_files': sum(self.file_counts.values()),
                'total_size_mb': round(self.total_size / (1024 * 1024), 2),
                'documentation_files': self.file_counts['documentation'],
                'code_files': self.file_counts['python'] + self.file_counts['typescript'] + self.file_counts['javascript'],
                'config_files': self.file_counts['config'],
                'coverage_ratio': round(coverage_ratio, 2)
            },
            'file_counts': dict(self.file_counts),
            'documentation': {
                'types': {k: len(v) for k, v in doc_types.items()},
                'examples': {k: v[:5] for k, v in doc_types.items() if v}
            },
            'code_structure': {
                'backend': {
                    'total': code_structure['backend']['total'],
                    'entry_points': code_structure['backend']['entry_points'],
                    'services': code_structure['backend']['services'][:10]
                },
                'frontend': {
                    'total': code_structure['frontend']['total'],
                    'pages': code_structure['frontend']['pages'][:10],
                    'components': code_structure['frontend']['components'][:10]
                },
                'scripts': {
                    'total': code_structure['scripts']['total'],
                    'examples': code_structure['scripts']['automation'][:10]
                }
            },
            'extraction_strategy': strategy
        }

        return report

    def print_report(self, report: Dict):
        """Print formatted corpus analysis report."""
        print("=" * 80)
        print(f"CORPUS ANALYSIS REPORT: {report['repository']}")
        print("=" * 80)
        print()

        # Summary
        print("SUMMARY")
        print("-" * 80)
        for key, value in report['summary'].items():
            print(f"  {key.replace('_', ' ').title():30s}: {value}")
        print()

        # Documentation
        print("DOCUMENTATION TYPES")
        print("-" * 80)
        for doc_type, count in report['documentation']['types'].items():
            print(f"  {doc_type.title():20s}: {count:3d} files")
            if doc_type in report['documentation']['examples']:
                for example in report['documentation']['examples'][doc_type][:3]:
                    print(f"    - {example}")
        print()

        # Code Structure
        print("CODE STRUCTURE")
        print("-" * 80)
        print(f"  Backend (Python):          {report['code_structure']['backend']['total']} files")
        if report['code_structure']['backend']['entry_points']:
            print(f"    Entry points: {', '.join(report['code_structure']['backend']['entry_points'])}")
        print(f"  Frontend (TypeScript/JS):  {report['code_structure']['frontend']['total']} files")
        print(f"  Scripts/Automation:        {report['code_structure']['scripts']['total']} files")
        print()

        # Strategy
        print("EXTRACTION STRATEGY RECOMMENDATION")
        print("-" * 80)
        print(f"  {report['extraction_strategy']}")
        print()
        print("=" * 80)


if __name__ == "__main__":
    import sys

    # Get repo path from command line or use scopelock
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "/home/mind-protocol/graphcare/scopelock"

    analyzer = CorpusAnalyzer(repo_path)
    report = analyzer.generate_report()

    # Print report
    analyzer.print_report(report)

    # Save to JSON
    output_path = Path(repo_path) / "corpus_analysis.json"
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"Full report saved to: {output_path}")
