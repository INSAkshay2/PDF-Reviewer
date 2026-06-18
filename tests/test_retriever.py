"""Tests for the semantic retriever."""

import numpy as np
import pytest

from src.models import Chunk
from src.retrieval.retriever import Retriever
from src.vectorstore.faiss_store import FaissStore


class MockEmbedder:
    dimension = 4

    def embed_query(self, query: str) -> np.ndarray:
        if "learning" in query.lower():
            return np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        return np.array([0.0, 1.0, 0.0, 0.0], dtype=np.float32)


def test_retriever_returns_ranked_results():
    store = FaissStore(dimension=4)
    chunks = [
        Chunk(
            chunk_id="doc.pdf::p1::c0",
            text="Machine learning basics",
            source_file="doc.pdf",
            page_number=1,
        ),
        Chunk(
            chunk_id="doc.pdf::p2::c0",
            text="Cooking recipes for pasta",
            source_file="doc.pdf",
            page_number=2,
        ),
    ]
    embeddings = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
        ],
        dtype=np.float32,
    )
    store.add_chunks(chunks, embeddings)

    retriever = Retriever(embedder=MockEmbedder(), store=store, top_k=2)
    results = retriever.retrieve("What is machine learning?")

    assert len(results) == 2
    assert results[0].chunk.text == "Machine learning basics"
    assert results[0].score >= results[1].score


def test_retriever_empty_store():
    store = FaissStore(dimension=4)
    retriever = Retriever(embedder=MockEmbedder(), store=store, top_k=5)
    results = retriever.retrieve("Any question")
    assert results == []
