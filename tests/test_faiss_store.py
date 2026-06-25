import numpy as np
import pytest

from src.models import Document
from src.vectorstore.faiss_store import FaissStore


def _make_docs(count: int) -> list[Document]:
    return [
        Document(
            text=f"Chunk text number {i}",
            source="doc.pdf", source_type="pdf", page=1,
        )
        for i in range(count)
    ]


def test_faiss_add_and_search(tmp_path):
    dimension = 8
    index_path = tmp_path / "test_index"
    store = FaissStore(index_path=index_path, dimension=dimension)

    docs = _make_docs(5)
    embeddings = np.random.randn(5, dimension).astype(np.float32)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norms

    store.add_documents(docs, embeddings)
    assert store.size == 5

    query = embeddings[2]
    results = store.search(query, top_k=3)

    assert len(results) == 3
    assert results[0][0].text == docs[2].text
    assert results[0][1] >= results[1][1]


def test_faiss_save_and_load(tmp_path):
    dimension = 4
    index_path = tmp_path / "test_index"
    store = FaissStore(index_path=index_path, dimension=dimension)

    docs = _make_docs(3)
    embeddings = np.random.randn(3, dimension).astype(np.float32)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norms

    store.add_documents(docs, embeddings)

    loaded = FaissStore(index_path=index_path, dimension=dimension)
    assert loaded.size == 3
    assert loaded.documents[0].text == docs[0].text

    query = embeddings[1]
    orig_results = store.search(query, top_k=2)
    loaded_results = loaded.search(query, top_k=2)
    assert orig_results[0][0].text == loaded_results[0][0].text


def test_faiss_dimension_mismatch_raises(tmp_path):
    index_path = tmp_path / "test_index"
    store = FaissStore(index_path=index_path, dimension=4)

    docs = _make_docs(1)
    bad_embeddings = np.random.randn(1, 8).astype(np.float32)

    with pytest.raises(ValueError, match="dimension"):
        store.add_documents(docs, bad_embeddings)
