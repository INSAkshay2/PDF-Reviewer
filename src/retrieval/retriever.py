"""Semantic vector retrieval over FAISS."""

from src.embeddings.embedder import Embedder
from src.models import RetrievalResult
from src.vectorstore.faiss_store import FaissStore


class Retriever:
    """Retrieve relevant document chunks using semantic similarity."""

    def __init__(self, embedder: Embedder, store: FaissStore, top_k: int = 5):
        self.embedder = embedder
        self.store = store
        self.top_k = top_k

    def retrieve(self, query: str) -> list[RetrievalResult]:
        """Embed the query and return the top-k matching chunks."""
        query_embedding = self.embedder.embed_query(query)
        return self.store.search(query_embedding, top_k=self.top_k)
