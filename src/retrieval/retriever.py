from typing import List, Tuple
from src.embeddings.embedder import Embedder
from src.vectorstore.faiss_store import FaissStore
from src.models import Document

class Retriever:
    """Retrieves relevant documents from the vector store."""

    def __init__(self, vector_store: FaissStore, embedder: Embedder, top_k: int = 5):
        self.vector_store = vector_store
        self.embedder = embedder
        self.top_k = top_k

    def retrieve(self, query: str) -> List[Tuple[Document, float]]:
        """Embeds the query and retrieves the top-k matching documents."""
        query_embedding = self.embedder.embed_query(query)
        return self.vector_store.search(query_embedding, top_k=self.top_k)

