import faiss
import numpy as np
import os
import pickle
from typing import List, Tuple
from src.models import Document

class FaissStore:
    """Manages the FAISS index and document metadata."""

    def __init__(self, index_path: str, dimension: int = 768):
        self.index_path = index_path
        self.dimension = dimension
        self.index = None
        self.documents = []
        self._load_or_create_index()

    def _load_or_create_index(self):
        """Loads the FAISS index and metadata from disk, or creates them if they don't exist."""
        if os.path.exists(f"{self.index_path}.index") and os.path.exists(f"{self.index_path}.pkl"):
            print(f"Loading existing index from {self.index_path}")
            self.index = faiss.read_index(f"{self.index_path}.index")
            with open(f"{self.index_path}.pkl", "rb") as f:
                self.documents = pickle.load(f)
        else:
            print("Creating new FAISS index.")
            self.index = faiss.IndexIDMap(faiss.IndexFlatIP(self.dimension))
            self.documents = []

    def add_documents(self, chunks: List[Document], embeddings: np.ndarray):
        """Adds documents and their embeddings to the index."""
        if not chunks:
            return

        start_index = self.index.ntotal
        ids = np.arange(start_index, start_index + len(chunks))

        self.index.add_with_ids(embeddings.astype('float32'), ids)
        self.documents.extend(chunks)

        self.save_index()

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[Document, float]]:
        """Searches the index for the most similar documents."""
        if not self.documents:
            return []

        distances, indices = self.index.search(query_embedding.astype('float32'), top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                results.append((self.documents[idx], distances[0][i]))
        return results

    def save_index(self):
        """Saves the FAISS index and metadata to disk."""
        print(f"Saving index to {self.index_path}")
        faiss.write_index(self.index, f"{self.index_path}.index")
        with open(f"{self.index_path}.pkl", "wb") as f:
            pickle.dump(self.documents, f)

