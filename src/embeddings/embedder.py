"""Local embedding generation using sentence-transformers."""

import logging

import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


class Embedder:
    """Wrapper around BGE embedding models for documents and queries."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5", batch_size: int = 32):
        self.model_name = model_name
        self.batch_size = batch_size
        logger.info("Loading embedding model: %s", model_name)
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def embed_documents(self, texts: list[str]) -> np.ndarray:
        """Embed document chunks for indexing."""
        if not texts:
            return np.array([]).reshape(0, self.dimension)

        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            normalize_embeddings=True,
            show_progress_bar=len(texts) > 50,
        )
        return np.asarray(embeddings, dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        """Embed a search query with the BGE retrieval prefix."""
        prefixed = f"{BGE_QUERY_PREFIX}{query}"
        embedding = self.model.encode(
            prefixed,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return np.asarray(embedding, dtype=np.float32)
