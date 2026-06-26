import logging

import numpy as np
import requests

from src.embeddings.base import EmbeddingService

logger = logging.getLogger(__name__)

GEMINI_EMBEDDING_DIMENSION = 3072
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"


class GeminiEmbedder(EmbeddingService):
    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-embedding-001",
        batch_size: int = 32,
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.batch_size = batch_size
        self._dimension = GEMINI_EMBEDDING_DIMENSION

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is required for Gemini embedder. "
                "Set it in your .env file or environment."
            )

        logger.info("Initialized Gemini embedder: %s", model_name)

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed_documents(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.array([]).reshape(0, self.dimension)

        all_embeddings: list[np.ndarray] = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            for text in batch:
                embedding = self._embed_single(text, task_type="RETRIEVAL_DOCUMENT")
                all_embeddings.append(embedding)

        return np.array(all_embeddings, dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        embedding = self._embed_single(query, task_type="RETRIEVAL_QUERY")
        return np.array([embedding], dtype=np.float32)

    def _embed_single(self, text: str, task_type: str) -> list[float]:
        url = f"{GEMINI_API_BASE}/models/{self.model_name}:embedContent"
        payload = {
            "model": f"models/{self.model_name}",
            "content": {"parts": [{"text": text}]},
        }
        response = requests.post(
            url,
            params={"key": self.api_key},
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["embedding"]["values"]
