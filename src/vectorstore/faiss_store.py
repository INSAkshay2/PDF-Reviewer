"""FAISS vector store with metadata persistence."""

import json
import logging
from pathlib import Path

import faiss
import numpy as np

from src.models import Chunk, RetrievalResult

logger = logging.getLogger(__name__)


class FaissStore:
    """Store embeddings in FAISS and keep chunk metadata in sync."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.chunks: list[Chunk] = []

    @property
    def size(self) -> int:
        return len(self.chunks)

    def add_chunks(self, chunks: list[Chunk], embeddings: np.ndarray) -> None:
        """Add chunks and their embeddings to the index."""
        if not chunks:
            return

        if embeddings.shape[0] != len(chunks):
            raise ValueError(
                f"Embedding count ({embeddings.shape[0]}) does not match chunk count ({len(chunks)})"
            )
        if embeddings.shape[1] != self.dimension:
            raise ValueError(
                f"Embedding dimension ({embeddings.shape[1]}) does not match index ({self.dimension})"
            )

        vectors = np.ascontiguousarray(embeddings, dtype=np.float32)
        self.index.add(vectors)
        self.chunks.extend(chunks)

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> list[RetrievalResult]:
        """Return the top-k most similar chunks for a query embedding."""
        if self.size == 0:
            return []

        k = min(top_k, self.size)
        query_vector = np.ascontiguousarray(
            query_embedding.reshape(1, -1), dtype=np.float32
        )
        scores, indices = self.index.search(query_vector, k)

        results: list[RetrievalResult] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            results.append(
                RetrievalResult(chunk=self.chunks[idx], score=float(score))
            )
        return results

    def save(self, path_prefix: str | Path) -> None:
        """Persist the FAISS index and chunk metadata to disk."""
        prefix = Path(path_prefix)
        prefix.parent.mkdir(parents=True, exist_ok=True)

        index_path = prefix.with_suffix(".index")
        meta_path = prefix.parent / f"{prefix.name}_meta.json"

        faiss.write_index(self.index, str(index_path))
        meta_payload = {
            "dimension": self.dimension,
            "chunks": [chunk.model_dump() for chunk in self.chunks],
        }
        meta_path.write_text(json.dumps(meta_payload, indent=2), encoding="utf-8")
        logger.info("Saved FAISS index (%d chunks) to %s", self.size, index_path)

    @classmethod
    def load(cls, path_prefix: str | Path) -> "FaissStore":
        """Load a previously saved FAISS index and metadata."""
        prefix = Path(path_prefix)
        index_path = prefix.with_suffix(".index")
        meta_path = prefix.parent / f"{prefix.name}_meta.json"

        if not index_path.exists():
            raise FileNotFoundError(f"FAISS index not found: {index_path}")
        if not meta_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {meta_path}")

        meta_payload = json.loads(meta_path.read_text(encoding="utf-8"))
        dimension = meta_payload["dimension"]
        chunks = [Chunk(**item) for item in meta_payload["chunks"]]

        store = cls(dimension=dimension)
        store.index = faiss.read_index(str(index_path))
        store.chunks = chunks

        if store.index.ntotal != len(store.chunks):
            raise ValueError(
                f"Index vector count ({store.index.ntotal}) "
                f"does not match metadata chunk count ({len(store.chunks)})"
            )

        logger.info("Loaded FAISS index (%d chunks) from %s", store.size, index_path)
        return store
