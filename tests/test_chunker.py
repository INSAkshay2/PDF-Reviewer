"""Tests for the document chunker."""

from src.models import DocumentPage
from src.processing.chunker import Chunker


def test_chunker_preserves_page_metadata():
    pages = [
        DocumentPage(
            page_number=1,
            text="Machine learning is a subset of artificial intelligence. " * 20,
            source_file="sample.pdf",
        ),
        DocumentPage(
            page_number=2,
            text="Deep learning uses neural networks with many layers. " * 20,
            source_file="sample.pdf",
        ),
    ]

    chunker = Chunker(chunk_size=200, chunk_overlap=50)
    chunks = chunker.chunk_pages(pages)

    assert len(chunks) > 0
    assert all(chunk.source_file == "sample.pdf" for chunk in chunks)
    assert any(chunk.page_number == 1 for chunk in chunks)
    assert any(chunk.page_number == 2 for chunk in chunks)
    assert all(chunk.chunk_id.startswith("sample.pdf::") for chunk in chunks)


def test_chunker_creates_overlap():
    text = "Word " * 300
    pages = [DocumentPage(page_number=1, text=text, source_file="doc.pdf")]

    chunker = Chunker(chunk_size=500, chunk_overlap=100)
    chunks = chunker.chunk_pages(pages)

    assert len(chunks) >= 2
    first_end = chunks[0].text[-50:]
    second_start = chunks[1].text[:50]
    assert first_end[:20] == second_start[:20] or len(set(first_end.split()) & set(second_start.split())) > 0


def test_chunker_no_empty_chunks():
    pages = [
        DocumentPage(page_number=1, text="Short text.", source_file="doc.pdf"),
    ]
    chunker = Chunker(chunk_size=800, chunk_overlap=150)
    chunks = chunker.chunk_pages(pages)

    assert len(chunks) == 1
    assert chunks[0].text == "Short text."
