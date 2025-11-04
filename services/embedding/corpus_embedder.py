"""
GraphCare Corpus Embedder - Embed all client documents and code

Processes entire client corpus and generates embeddings for:
- Documentation files (.md)
- Code files (.py, .ts, .tsx, .js, .jsx)
- Config files (.yaml, .json, .toml)

Outputs embeddings + metadata for clustering and type classification.

Author: Quinn (Chief Cartographer, GraphCare)
Date: 2025-11-04
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List
from embedding_service import get_embedding_service

class CorpusEmbedder:
    """Embed entire client corpus for semantic analysis."""

    def __init__(self, repo_path: str, output_dir: str = None):
        """
        Initialize corpus embedder.

        Args:
            repo_path: Path to client repository
            output_dir: Path to save embeddings (default: repo_path/embeddings/)
        """
        self.repo_path = Path(repo_path)
        self.output_dir = Path(output_dir) if output_dir else self.repo_path / "embeddings"
        self.output_dir.mkdir(exist_ok=True)

        self.embedding_service = get_embedding_service()
        self.embeddings = []
        self.errors = []

    def read_file_content(self, file_path: Path) -> str:
        """Read file content with encoding fallback."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                return f"[ERROR: Could not read file - {e}]"

    def embed_file(self, file_path: Path, file_type: str) -> Dict:
        """
        Embed a single file.

        Args:
            file_path: Path to file
            file_type: Type classification (doc, code, config)

        Returns:
            Dict with embedding + metadata
        """
        rel_path = file_path.relative_to(self.repo_path)
        content = self.read_file_content(file_path)

        # Truncate very long files (keep first 2000 chars for embedding)
        content_preview = content[:2000] if len(content) > 2000 else content

        # Metadata
        metadata = {
            'path': str(rel_path),
            'type': file_type,
            'extension': file_path.suffix,
            'name': file_path.name,
            'size': len(content),
            'lines': content.count('\n') + 1
        }

        # Detect document type for markdown files
        if file_path.suffix == '.md':
            name_lower = file_path.name.lower()
            if 'architecture' in name_lower or 'arch' in name_lower:
                metadata['doc_type'] = 'architecture'
            elif 'spec' in name_lower:
                metadata['doc_type'] = 'specification'
            elif 'guide' in name_lower or 'tutorial' in name_lower:
                metadata['doc_type'] = 'guide'
            elif 'readme' in name_lower:
                metadata['doc_type'] = 'readme'
            elif 'claude' in name_lower:
                metadata['doc_type'] = 'identity'
            else:
                metadata['doc_type'] = 'other'

        # Embed
        if file_type == 'doc':
            embeddable_text, embedding = self.embedding_service.embed_document(
                content_preview, metadata
            )
        elif file_type == 'code':
            embeddable_text, embedding = self.embedding_service.embed_code_artifact(
                content_preview, metadata
            )
        else:
            # Config files - simple embedding
            embeddable_text = f"Config: {rel_path}. {content_preview[:300]}"
            embedding = self.embedding_service.embed(embeddable_text)

        return {
            'path': str(rel_path),
            'metadata': metadata,
            'embeddable_text': embeddable_text[:500],  # Truncate for storage
            'embedding': embedding,
            'full_content': content  # Store full content for later use
        }

    def scan_and_embed(self):
        """Scan repository and embed all relevant files."""
        exclude_dirs = {'.git', 'node_modules', '__pycache__', '.next', 'dist', 'build', 'test-results', 'embeddings'}

        file_extensions = {
            'doc': ['.md'],
            'code': ['.py', '.ts', '.tsx', '.js', '.jsx'],
            'config': ['.yaml', '.yml', '.json', '.toml']
        }

        total_files = 0
        processed = 0

        print(f"Scanning repository: {self.repo_path}")
        print(f"Embedding service ready: {self.embedding_service.backend}")
        print()

        for root, dirs, files in os.walk(self.repo_path):
            # Exclude directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                file_path = Path(root) / file
                ext = file_path.suffix.lower()

                # Determine file type
                file_type = None
                for ftype, extensions in file_extensions.items():
                    if ext in extensions:
                        file_type = ftype
                        break

                if not file_type:
                    continue

                total_files += 1

                try:
                    print(f"[{processed + 1}] Embedding: {file_path.relative_to(self.repo_path)}", end='')

                    result = self.embed_file(file_path, file_type)
                    self.embeddings.append(result)

                    processed += 1
                    print(f" ✓ ({len(result['embedding'])} dims)")

                except Exception as e:
                    error_msg = f"Failed to embed {file_path.relative_to(self.repo_path)}: {e}"
                    self.errors.append(error_msg)
                    print(f" ✗ ERROR: {e}")

        print()
        print(f"Embedding complete: {processed}/{total_files} files processed")
        if self.errors:
            print(f"Errors: {len(self.errors)}")

    def save_embeddings(self):
        """Save embeddings to JSON file."""
        output_file = self.output_dir / "corpus_embeddings.json"

        # Separate metadata and embeddings for efficient storage
        metadata_file = self.output_dir / "corpus_metadata.json"
        embeddings_file = self.output_dir / "embeddings_matrix.json"

        # Save full embeddings (for semantic search)
        with open(output_file, 'w') as f:
            json.dump(self.embeddings, f, indent=2)

        # Save metadata only (for analysis)
        metadata_only = [
            {
                'path': item['path'],
                'metadata': item['metadata'],
                'embeddable_text': item['embeddable_text']
            }
            for item in self.embeddings
        ]

        with open(metadata_file, 'w') as f:
            json.dump(metadata_only, f, indent=2)

        # Save embeddings matrix (for clustering)
        embeddings_matrix = {
            'paths': [item['path'] for item in self.embeddings],
            'vectors': [item['embedding'] for item in self.embeddings]
        }

        with open(embeddings_file, 'w') as f:
            json.dump(embeddings_matrix, f, indent=2)

        print(f"Embeddings saved to:")
        print(f"  - Full: {output_file}")
        print(f"  - Metadata: {metadata_file}")
        print(f"  - Matrix: {embeddings_file}")

        # Save errors if any
        if self.errors:
            errors_file = self.output_dir / "embedding_errors.txt"
            with open(errors_file, 'w') as f:
                for error in self.errors:
                    f.write(f"{error}\n")
            print(f"  - Errors: {errors_file}")

    def generate_summary(self):
        """Generate embedding summary statistics."""
        summary = {
            'total_files': len(self.embeddings),
            'by_type': {},
            'by_extension': {},
            'total_content_size': 0,
            'embedding_dim': len(self.embeddings[0]['embedding']) if self.embeddings else 0
        }

        for item in self.embeddings:
            # Count by type
            file_type = item['metadata']['type']
            summary['by_type'][file_type] = summary['by_type'].get(file_type, 0) + 1

            # Count by extension
            ext = item['metadata']['extension']
            summary['by_extension'][ext] = summary['by_extension'].get(ext, 0) + 1

            # Total size
            summary['total_content_size'] += item['metadata']['size']

        summary['total_content_size_mb'] = round(summary['total_content_size'] / (1024 * 1024), 2)

        print()
        print("=" * 80)
        print("EMBEDDING SUMMARY")
        print("=" * 80)
        print(f"Total files embedded: {summary['total_files']}")
        print(f"Embedding dimensions: {summary['embedding_dim']}")
        print(f"Total content size: {summary['total_content_size_mb']} MB")
        print()
        print("By type:")
        for ftype, count in summary['by_type'].items():
            print(f"  {ftype:10s}: {count:3d} files")
        print()
        print("By extension:")
        for ext, count in sorted(summary['by_extension'].items()):
            print(f"  {ext:10s}: {count:3d} files")
        print("=" * 80)

        return summary


if __name__ == "__main__":
    # Get repo path from command line
    if len(sys.argv) < 2:
        print("Usage: python corpus_embedder.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]

    embedder = CorpusEmbedder(repo_path)
    embedder.scan_and_embed()
    embedder.save_embeddings()
    summary = embedder.generate_summary()
