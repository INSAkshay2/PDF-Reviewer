import numpy as np

from src.models import Document
from src.retrieval.retriever import Retriever
from src.vectorstore.faiss_store import FaissStore


class MockEmbedder:
    dimension = 4

    def embed_query(self, query: str) -> np.ndarray:
        if "learning" in query.lower():
            return np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        return np.array([0.0, 1.0, 0.0, 0.0], dtype=np.float32)


def test_retriever_returns_ranked_results(tmp_path):
    index_path = tmp_path / "test_index"
    store = FaissStore(index_path=index_path, dimension=4)

    docs = [
        Document(
            text="Machine learning basics",
            source="doc.pdf", source_type="pdf", page=1,
        ),
        Document(
            text="Cooking recipes for pasta",
            source="doc.pdf", source_type="pdf", page=2,
        ),
    ]
    embeddings = np.array(
        [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]],
        dtype=np.float32,
    )
    store.add_documents(docs, embeddings)

    retriever = Retriever(embedder=MockEmbedder(), vector_store=store, top_k=2)
    results = retriever.retrieve("What is machine learning?")

    assert len(results) == 2
    assert results[0][0].text == "Machine learning basics"
    assert results[0][1] >= results[1][1]


def test_retriever_empty_store(tmp_path):
    index_path = tmp_path / "test_index"
    store = FaissStore(index_path=index_path, dimension=4)
    retriever = Retriever(embedder=MockEmbedder(), vector_store=store, top_k=5)
    results = retriever.retrieve("Any question")
    assert results == []
