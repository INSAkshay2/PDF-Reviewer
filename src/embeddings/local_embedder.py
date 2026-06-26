"""Local embedding generation using sentence-transformers (for development only)."""

import logging
import os

import numpy as np

from src.embeddings.base import EmbeddingService

logger = logging.getLogger(__name__)

BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


class LocalEmbedder(EmbeddingService):
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5", batch_size: int = 32):
        self.model_name = model_name
        self.batch_size = batch_size

        os.environ.setdefault("TQDM_DISABLE", "1")

        from sentence_transformers import SentenceTransformer

        logger.info("Loading local embedding model: %s", model_name)
        self._model = SentenceTransformer(model_name)
        self._dimension = self._model.get_embedding_dimension()

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed_documents(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.array([]).reshape(0, self.dimension)

        embeddings = self._model.encode(
            texts,
            batch_size=self.batch_size,
            normalize_embeddings=True,
            show_progress_bar=len(texts) > 50,
        )
        return np.asarray(embeddings, dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        prefixed = f"{BGE_QUERY_PREFIX}{query}"
        embedding = self._model.encode(
            prefixed,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return np.asarray(embedding, dtype=np.float32)
