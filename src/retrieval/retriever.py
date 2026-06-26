from typing import List, Tuple

from src.embeddings.base import EmbeddingService
from src.models import Document
from src.vectorstore.faiss_store import FaissStore


class Retriever:
    def __init__(self, embedder: EmbeddingService, vector_store: FaissStore, top_k: int = 5):
        self.embedder = embedder
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(self, query: str) -> List[Tuple[Document, float]]:
        self.vector_store.ensure_loaded()
        query_embedding = self.embedder.embed_query(query)
        return self.vector_store.search(query_embedding, top_k=self.top_k)
