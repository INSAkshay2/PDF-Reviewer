import logging

import numpy as np
from google import genai

from src.embeddings.base import EmbeddingService

logger = logging.getLogger(__name__)

class GeminiEmbedder(EmbeddingService):
    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-embedding-001",
        batch_size: int = 32,
    ):
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is required for Gemini embedder. "
                "Set it in your .env file or environment."
            )

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.batch_size = batch_size
        self._dimension = self._probe_dimension()

        logger.info("Initialized Gemini embedder: %s (dimension=%d)", model_name, self._dimension)

    @property
    def dimension(self) -> int:
        return self._dimension

    def _probe_dimension(self) -> int:
        try:
            probe = self.client.models.embed_content(
                model=self.model_name,
                contents=["probe"],
            )
            return len(probe.embeddings[0].values)
        except Exception:
            logger.warning(
                "Could not probe embedding dimension for %s, using default 768",
                self.model_name,
            )
            return 768

    def embed_documents(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.array([]).reshape(0, self.dimension)

        all_embeddings: list[np.ndarray] = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            try:
                response = self.client.models.embed_content(
                    model=self.model_name,
                    contents=batch,
                )
                for emb in response.embeddings:
                    all_embeddings.append(np.array(emb.values, dtype=np.float32))
            except Exception as e:
                logger.error(
                    "Gemini embedding failed for batch %d/%d: %s",
                    i // self.batch_size + 1,
                    (len(texts) + self.batch_size - 1) // self.batch_size,
                    e,
                )
                raise RuntimeError(
                    f"Embedding failed for {len(batch)} text(s). "
                    "Ensure the file contains valid text content."
                ) from e

        return np.array(all_embeddings, dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        try:
            response = self.client.models.embed_content(
                model=self.model_name,
                contents=[query],
            )
            return np.array([response.embeddings[0].values], dtype=np.float32)
        except Exception as e:
            logger.error("Gemini query embedding failed: %s", e)
            raise RuntimeError(
                "Query embedding failed. Please try again."
            ) from e
