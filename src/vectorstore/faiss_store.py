import logging
import pickle
from pathlib import Path
from typing import List, Tuple

import faiss
import numpy as np

from src.models import Document

logger = logging.getLogger(__name__)


class FaissStore:
    def __init__(self, index_path: str | Path, dimension: int):
        self.index_path = Path(index_path)
        self.dimension = dimension
        self._loaded = False
        self.index = faiss.IndexIDMap(faiss.IndexFlatIP(dimension))
        self.documents: List[Document] = []

    def ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        self._load()

    @property
    def size(self) -> int:
        self.ensure_loaded()
        return len(self.documents)

    def add_documents(self, documents: List[Document], embeddings: np.ndarray) -> None:
        self.ensure_loaded()
        if not documents:
            return
        if embeddings.shape[0] != len(documents):
            raise ValueError(
                f"Embedding count ({embeddings.shape[0]}) "
                f"does not match document count ({len(documents)})"
            )
        if embeddings.shape[1] != self.dimension:
            raise ValueError(
                f"Embedding dimension ({embeddings.shape[1]}) "
                f"does not match index dimension ({self.dimension})"
            )

        start_id = self.index.ntotal
        ids = np.arange(start_id, start_id + len(documents), dtype=np.int64)
        vectors = np.ascontiguousarray(embeddings, dtype=np.float32)

        self.index.add_with_ids(vectors, ids)
        self.documents.extend(documents)
        self._save()

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[Document, float]]:
        self.ensure_loaded()
        if self.size == 0:
            return []

        k = min(top_k, self.size)
        query_vector = np.ascontiguousarray(
            query_embedding.reshape(1, -1), dtype=np.float32
        )
        scores, indices = self.index.search(query_vector, k)

        results: List[Tuple[Document, float]] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0 and idx < len(self.documents):
                doc = self.documents[idx].model_copy()
                doc.score = float(score)
                results.append((doc, float(score)))
        return results

    def get_all_embeddings(self) -> np.ndarray:
        self.ensure_loaded()
        if self.size == 0:
            return np.array([]).reshape(0, self.dimension)
        return self.index.reconstruct_n(0, self.size)

    def clear(self) -> None:
        self.ensure_loaded()
        self.index = faiss.IndexIDMap(faiss.IndexFlatIP(self.dimension))
        self.documents = []
        self._save()

    def _save(self) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        index_file = self.index_path.with_suffix(".index")
        meta_file = self.index_path.with_suffix(".pkl")
        faiss.write_index(self.index, str(index_file))
        with open(meta_file, "wb") as f:
            pickle.dump(self.documents, f)
        logger.info("Saved FAISS index (%d docs) to %s", self.size, index_file)

    def _load(self) -> None:
        index_file = self.index_path.with_suffix(".index")
        meta_file = self.index_path.with_suffix(".pkl")
        if not index_file.exists() or not meta_file.exists():
            return

        try:
            loaded_index = faiss.read_index(str(index_file))
            loaded_dim = loaded_index.d

            if loaded_dim != self.dimension:
                logger.warning(
                    "Existing index dimension (%d) differs from model dimension (%d). "
                    "Clearing old index. Re-upload documents to rebuild.",
                    loaded_dim, self.dimension,
                )
                self.index = faiss.IndexIDMap(faiss.IndexFlatIP(self.dimension))
                self.documents = []
                return

            self.index = loaded_index
            with open(meta_file, "rb") as f:
                self.documents = pickle.load(f)
            logger.info(
                "Loaded FAISS index (%d docs) from %s",
                self.size, index_file,
            )
        except Exception as e:
            logger.warning("Failed to load existing index, starting fresh: %s", e)
            self.index = faiss.IndexIDMap(faiss.IndexFlatIP(self.dimension))
            self.documents = []
