"""
GraphCare Embedding Service - Generate semantic embeddings for client L2 graphs

Adapted from Mind Protocol's consciousness embedding service.
Focuses on organizational knowledge (L2) using universal types:
- U4_Knowledge_Object (specs, ADRs, guides, runbooks)
- U4_Code_Artifact (source files, functions, classes)
- U3_Pattern (best practices, anti-patterns)
- U4_Subentity (semantic clusters, themes)

Author: Quinn (Chief Cartographer, GraphCare)
Date: 2025-11-04
Pattern: Zero-cost local embeddings for client knowledge graphs
"""

import logging
from typing import Dict, Any, List, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Generates embeddings for client organizational knowledge.

    Uses local models (zero API cost) to create semantic embeddings
    that enable:
    - Semantic clustering of documents and code
    - Cross-reference detection
    - Similar content discovery
    - Coverage gap analysis
    """

    def __init__(self, backend: str = 'sentence-transformers'):
        """
        Initialize embedding service.

        Args:
            backend: 'sentence-transformers' or 'ollama'
                sentence-transformers: Pure Python, works immediately
                ollama: Requires Ollama server running
        """
        self.backend = backend
        self.embedding_dim = 768
        self.model = None

        if backend == 'sentence-transformers':
            self._init_sentence_transformers()
        elif backend == 'ollama':
            self._init_ollama()
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def _init_sentence_transformers(self):
        """Initialize SentenceTransformers backend (all-mpnet-base-v2)."""
        try:
            from sentence_transformers import SentenceTransformer

            # all-mpnet-base-v2: 768 dims, SOTA performance, CPU-friendly
            self.model = SentenceTransformer('all-mpnet-base-v2')
            logger.info("[GraphCare:EmbeddingService] Loaded SentenceTransformer: all-mpnet-base-v2 (768 dims)")

        except ImportError:
            logger.error("[GraphCare:EmbeddingService] sentence-transformers not installed. Run: pip install sentence-transformers")
            raise
        except Exception as e:
            logger.error(f"[GraphCare:EmbeddingService] Failed to load SentenceTransformer: {e}")
            raise

    def _init_ollama(self):
        """Initialize Ollama backend (nomic-embed-text)."""
        try:
            import ollama

            # Verify Ollama is running and has nomic-embed-text model
            models = ollama.list()
            if 'nomic-embed-text' not in [m['name'] for m in models.get('models', [])]:
                logger.warning("[GraphCare:EmbeddingService] nomic-embed-text not found. Run: ollama pull nomic-embed-text")

            self.model = 'nomic-embed-text'
            logger.info("[GraphCare:EmbeddingService] Using Ollama backend: nomic-embed-text (768 dims)")

        except ImportError:
            logger.error("[GraphCare:EmbeddingService] ollama not installed. Run: pip install ollama")
            raise
        except Exception as e:
            logger.error(f"[GraphCare:EmbeddingService] Failed to connect to Ollama: {e}")
            raise

    def embed(self, text: str) -> List[float]:
        """
        Generate 768-dim embedding from text.

        Args:
            text: Embeddable text (semantic content)

        Returns:
            768-dimensional embedding vector
        """
        if not text or not text.strip():
            logger.warning("[GraphCare:EmbeddingService] Empty text provided for embedding")
            return [0.0] * self.embedding_dim

        try:
            if self.backend == 'sentence-transformers':
                embedding = self.model.encode(text, convert_to_numpy=True)

                # L2 normalization for stable cosine similarity
                norm = np.linalg.norm(embedding)
                if norm > 0:
                    embedding = embedding / norm

                return embedding.tolist()

            elif self.backend == 'ollama':
                import ollama
                response = ollama.embeddings(
                    model=self.model,
                    prompt=text
                )
                embedding_array = np.array(response['embedding'])

                # L2 normalization for stable cosine similarity
                norm = np.linalg.norm(embedding_array)
                if norm > 0:
                    embedding_array = embedding_array / norm

                return embedding_array.tolist()

        except Exception as e:
            logger.error(f"[GraphCare:EmbeddingService] Embedding generation failed: {e}")
            # Return zero vector as fallback
            return [0.0] * self.embedding_dim

    def embed_document(self, content: str, metadata: Dict[str, Any] = None) -> Tuple[str, List[float]]:
        """
        Embed a client document (spec, ADR, guide, code file).

        Args:
            content: Full document content (markdown, code, etc.)
            metadata: Optional metadata (path, type, title, etc.)

        Returns:
            (embeddable_text, embedding_vector) tuple
        """
        # For documents, use first 500 chars + metadata for embedding
        # (Full content would be stored separately in FalkorDB)
        metadata = metadata or {}

        title = metadata.get('title', metadata.get('name', ''))
        doc_type = metadata.get('type', metadata.get('ko_type', ''))
        path = metadata.get('path', '')

        # Truncate content for embedding (full content stored in FalkorDB)
        content_preview = content[:500] if len(content) > 500 else content

        # Build embeddable text
        parts = []
        if title:
            parts.append(f"Title: {title}")
        if doc_type:
            parts.append(f"Type: {doc_type}")
        if path:
            parts.append(f"Path: {path}")
        parts.append(content_preview)

        embeddable_text = ". ".join(parts)

        # Generate embedding
        embedding = self.embed(embeddable_text)

        return (embeddable_text, embedding)

    def embed_code_artifact(self, code: str, metadata: Dict[str, Any]) -> Tuple[str, List[float]]:
        """
        Embed a code artifact (file, class, function).

        Args:
            code: Source code content
            metadata: Required metadata (path, lang, etc.)

        Returns:
            (embeddable_text, embedding_vector) tuple
        """
        path = metadata.get('path', '')
        lang = metadata.get('lang', '')
        description = metadata.get('description', '')

        # For code, use path + first 300 chars + docstring/comments
        code_preview = code[:300] if len(code) > 300 else code

        # Build embeddable text
        parts = [f"Code: {path}"]
        if lang:
            parts.append(f"Language: {lang}")
        if description:
            parts.append(description)
        parts.append(code_preview)

        embeddable_text = ". ".join(parts)

        # Generate embedding
        embedding = self.embed(embeddable_text)

        return (embeddable_text, embedding)


# Global singleton instance
_embedding_service = None


def get_embedding_service(backend: str = 'sentence-transformers') -> EmbeddingService:
    """
    Get or create global embedding service instance.

    Args:
        backend: 'sentence-transformers' or 'ollama'

    Returns:
        EmbeddingService singleton
    """
    global _embedding_service

    if _embedding_service is None:
        _embedding_service = EmbeddingService(backend=backend)

    return _embedding_service


if __name__ == "__main__":
    # Test embedding service
    import json

    service = get_embedding_service()

    # Test document embedding
    doc_content = """
    # Authentication Architecture

    This document describes the authentication system architecture.
    We use JWT tokens with RSA signing for secure authentication.
    Tokens expire after 24 hours and must be refreshed.
    """

    doc_metadata = {
        'title': 'Authentication Architecture',
        'type': 'spec',
        'path': 'docs/architecture/auth.md'
    }

    embeddable_text, embedding = service.embed_document(doc_content, doc_metadata)

    print("Document Embedding Test:")
    print(f"  Embeddable text: {embeddable_text[:200]}...")
    print(f"  Embedding dims: {len(embedding)}")
    print(f"  First 5 values: {embedding[:5]}")
    print(f"  L2 norm: {np.linalg.norm(embedding):.6f} (should be ~1.0)")

    # Test code embedding
    code_content = """
def authenticate_user(username: str, password: str) -> Token:
    '''Authenticate user and return JWT token'''
    user = db.get_user(username)
    if not user or not verify_password(password, user.password_hash):
        raise AuthenticationError("Invalid credentials")
    return generate_jwt_token(user.id)
"""

    code_metadata = {
        'path': 'src/auth/service.py::authenticate_user',
        'lang': 'py',
        'description': 'User authentication function'
    }

    embeddable_text, embedding = service.embed_code_artifact(code_content, code_metadata)

    print("\nCode Embedding Test:")
    print(f"  Embeddable text: {embeddable_text[:200]}...")
    print(f"  Embedding dims: {len(embedding)}")
    print(f"  First 5 values: {embedding[:5]}")
    print(f"  L2 norm: {np.linalg.norm(embedding):.6f} (should be ~1.0)")

    # Test similarity between related content
    doc2_content = "JWT authentication guide for developers"
    doc2_metadata = {'title': 'JWT Guide', 'type': 'guide'}

    _, embed1 = service.embed_document(doc_content, doc_metadata)
    _, embed2 = service.embed_document(doc2_content, doc2_metadata)

    # Cosine similarity (dot product of normalized vectors)
    similarity = np.dot(embed1, embed2)

    print(f"\nSimilarity Test:")
    print(f"  Doc1: Authentication Architecture")
    print(f"  Doc2: JWT Guide")
    print(f"  Cosine similarity: {similarity:.4f} (higher = more similar)")
