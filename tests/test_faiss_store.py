"""Tests for the FAISS vector store."""

import numpy as np
import pytest

from src.models import Chunk
from src.vectorstore.faiss_store import FaissStore


def _make_chunks(count: int) -> list[Chunk]:
    return [
        Chunk(
            chunk_id=f"doc.pdf::p1::c{i}",
            text=f"Chunk text number {i}",
            source_file="doc.pdf",
            page_number=1,
            char_start=i * 10,
            char_end=(i + 1) * 10,
        )
        for i in range(count)
    ]


def test_faiss_add_and_search():
    dimension = 8
    store = FaissStore(dimension=dimension)
    chunks = _make_chunks(5)
    embeddings = np.random.randn(5, dimension).astype(np.float32)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norms

    store.add_chunks(chunks, embeddings)
    assert store.size == 5

    query = embeddings[2]
    results = store.search(query, top_k=3)

    assert len(results) == 3
    assert results[0].chunk.chunk_id == chunks[2].chunk_id
    assert results[0].score > results[1].score


def test_faiss_save_and_load(tmp_path):
    dimension = 4
    store = FaissStore(dimension=dimension)
    chunks = _make_chunks(3)
    embeddings = np.random.randn(3, dimension).astype(np.float32)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norms

    store.add_chunks(chunks, embeddings)
    prefix = tmp_path / "test_doc"
    store.save(prefix)

    loaded = FaissStore.load(prefix)
    assert loaded.size == 3
    assert loaded.chunks[0].chunk_id == chunks[0].chunk_id

    query = embeddings[1]
    original_results = store.search(query, top_k=2)
    loaded_results = loaded.search(query, top_k=2)
    assert original_results[0].chunk.chunk_id == loaded_results[0].chunk.chunk_id


def test_faiss_dimension_mismatch_raises():
    store = FaissStore(dimension=4)
    chunks = _make_chunks(1)
    bad_embeddings = np.random.randn(1, 8).astype(np.float32)

    with pytest.raises(ValueError, match="dimension"):
        store.add_chunks(chunks, bad_embeddings)
