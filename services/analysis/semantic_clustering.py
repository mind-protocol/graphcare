"""
GraphCare Semantic Clustering - Cluster documents by semantic similarity

Uses embeddings to identify:
- Semantic themes (what topics exist in the corpus?)
- Knowledge clusters (which docs are related?)
- Coverage gaps (what's missing?)

Author: Quinn (Chief Cartographer, GraphCare)
Date: 2025-11-04
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict, Counter
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score


class SemanticClusterer:
    """Cluster corpus by semantic similarity."""

    def __init__(self, embeddings_file: str):
        """
        Initialize clusterer with embeddings file.

        Args:
            embeddings_file: Path to embeddings_matrix.json
        """
        self.embeddings_file = Path(embeddings_file)
        self.vectors = None
        self.paths = None
        self.metadata = None
        self.clusters = None
        self.cluster_labels = None

    def load_embeddings(self):
        """Load embeddings matrix."""
        print(f"Loading embeddings from: {self.embeddings_file}")

        with open(self.embeddings_file, 'r') as f:
            data = json.load(f)

        self.paths = data['paths']
        self.vectors = np.array(data['vectors'])

        print(f"  Loaded {len(self.paths)} documents")
        print(f"  Embedding dimensions: {self.vectors.shape[1]}")
        print()

        # Load metadata
        metadata_file = self.embeddings_file.parent / "corpus_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata_list = json.load(f)
                self.metadata = {item['path']: item['metadata'] for item in metadata_list}

    def cluster_kmeans(self, n_clusters: int = 15):
        """
        Cluster using KMeans.

        Args:
            n_clusters: Number of clusters to create
        """
        print(f"Clustering with KMeans (n_clusters={n_clusters})...")

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.cluster_labels = kmeans.fit_predict(self.vectors)

        # Calculate silhouette score (quality metric)
        silhouette = silhouette_score(self.vectors, self.cluster_labels)

        print(f"  Silhouette score: {silhouette:.4f} (higher = better separation)")
        print()

        return silhouette

    def cluster_dbscan(self, eps: float = 0.3, min_samples: int = 3):
        """
        Cluster using DBSCAN (density-based).

        Args:
            eps: Maximum distance between samples
            min_samples: Minimum samples in neighborhood
        """
        print(f"Clustering with DBSCAN (eps={eps}, min_samples={min_samples})...")

        dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
        self.cluster_labels = dbscan.fit_predict(self.vectors)

        n_clusters = len(set(self.cluster_labels)) - (1 if -1 in self.cluster_labels else 0)
        n_noise = list(self.cluster_labels).count(-1)

        print(f"  Found {n_clusters} clusters")
        print(f"  Noise points: {n_noise}")
        print()

        return n_clusters, n_noise

    def analyze_clusters(self) -> Dict:
        """Analyze cluster composition and characteristics."""
        clusters = defaultdict(list)

        for idx, label in enumerate(self.cluster_labels):
            path = self.paths[idx]
            clusters[label].append({
                'path': path,
                'metadata': self.metadata.get(path, {}) if self.metadata else {}
            })

        cluster_analysis = {}

        for cluster_id, members in clusters.items():
            # Skip noise cluster in DBSCAN
            if cluster_id == -1:
                continue

            # Analyze file types in cluster
            types = Counter([m['metadata'].get('type', 'unknown') for m in members])
            extensions = Counter([m['metadata'].get('extension', 'unknown') for m in members])

            # Detect dominant document type
            doc_types = [m['metadata'].get('doc_type') for m in members if m['metadata'].get('doc_type')]
            doc_types_counter = Counter(doc_types) if doc_types else Counter()

            # Calculate cluster coherence (avg pairwise similarity)
            cluster_indices = [idx for idx, label in enumerate(self.cluster_labels) if label == cluster_id]
            cluster_vectors = self.vectors[cluster_indices]

            # Compute centroid
            centroid = np.mean(cluster_vectors, axis=0)

            # Compute avg distance to centroid (coherence metric)
            distances = [np.dot(centroid, vec) for vec in cluster_vectors]  # Cosine similarity
            avg_coherence = np.mean(distances)

            # Infer cluster theme from paths
            paths_in_cluster = [m['path'] for m in members]
            theme = self._infer_theme(paths_in_cluster)

            cluster_analysis[cluster_id] = {
                'size': len(members),
                'theme': theme,
                'coherence': float(avg_coherence),
                'types': dict(types),
                'extensions': dict(extensions),
                'doc_types': dict(doc_types_counter),
                'sample_paths': paths_in_cluster[:10]
            }

        self.clusters = cluster_analysis
        return cluster_analysis

    def _infer_theme(self, paths: List[str]) -> str:
        """Infer cluster theme from file paths."""
        # Extract directory names and file names
        parts = []
        for path in paths:
            parts.extend(Path(path).parts)

        # Count common terms
        term_counts = Counter(parts)

        # Remove generic terms
        generic = {'docs', 'src', 'app', 'components', 'pages', '.md', '.py', '.ts', '.tsx', '.js'}
        filtered = {term: count for term, count in term_counts.items() if term not in generic}

        if not filtered:
            return "miscellaneous"

        # Get most common term
        most_common = sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:3]
        theme_terms = [term for term, count in most_common]

        return " + ".join(theme_terms)

    def print_cluster_summary(self):
        """Print cluster analysis summary."""
        print("=" * 80)
        print("SEMANTIC CLUSTERING SUMMARY")
        print("=" * 80)
        print()

        sorted_clusters = sorted(self.clusters.items(), key=lambda x: x[1]['size'], reverse=True)

        for cluster_id, analysis in sorted_clusters:
            print(f"CLUSTER {cluster_id}: {analysis['theme']}")
            print(f"  Size: {analysis['size']} documents")
            print(f"  Coherence: {analysis['coherence']:.4f} (cosine similarity)")
            print(f"  Types: {', '.join(f'{k}={v}' for k, v in analysis['types'].items())}")

            if analysis['doc_types']:
                print(f"  Doc types: {', '.join(f'{k}={v}' for k, v in analysis['doc_types'].items())}")

            print(f"  Sample paths:")
            for path in analysis['sample_paths'][:5]:
                print(f"    - {path}")
            print()

        print("=" * 80)

    def save_clusters(self, output_dir: str):
        """Save cluster analysis to JSON."""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        # Save cluster assignments
        assignments = {
            'cluster_labels': self.cluster_labels.tolist(),
            'paths': self.paths,
            'n_clusters': len(self.clusters)
        }

        assignments_file = output_dir / "cluster_assignments.json"
        with open(assignments_file, 'w') as f:
            json.dump(assignments, f, indent=2)

        # Save cluster analysis (convert int keys to strings for JSON)
        clusters_serializable = {str(k): v for k, v in self.clusters.items()}

        analysis_file = output_dir / "cluster_analysis.json"
        with open(analysis_file, 'w') as f:
            json.dump(clusters_serializable, f, indent=2)

        print(f"Cluster results saved to:")
        print(f"  - Assignments: {assignments_file}")
        print(f"  - Analysis: {analysis_file}")


if __name__ == "__main__":
    import sys

    # Get embeddings file from command line
    if len(sys.argv) < 2:
        print("Usage: python semantic_clustering.py <embeddings_matrix.json>")
        sys.exit(1)

    embeddings_file = sys.argv[1]
    output_dir = Path(embeddings_file).parent

    clusterer = SemanticClusterer(embeddings_file)
    clusterer.load_embeddings()

    # Try KMeans first
    print("=" * 80)
    print("ATTEMPTING KMEANS CLUSTERING")
    print("=" * 80)
    print()

    silhouette = clusterer.cluster_kmeans(n_clusters=15)

    # Analyze and print
    clusterer.analyze_clusters()
    clusterer.print_cluster_summary()

    # Save results
    clusterer.save_clusters(output_dir)
