from src.models import Document
from src.processing.chunker import Chunker


def test_chunker_preserves_metadata():
    docs = [
        Document(
            text="Machine learning is a subset of artificial intelligence. " * 20,
            source="sample.pdf", source_type="pdf", page=1,
        ),
        Document(
            text="Deep learning uses neural networks with many layers. " * 20,
            source="sample.pdf", source_type="pdf", page=2,
        ),
    ]
    chunker = Chunker(chunk_size=200, chunk_overlap=50)
    chunks = chunker.chunk_documents(docs)

    assert len(chunks) > 0
    assert all(ch.source == "sample.pdf" for ch in chunks)
    assert any(ch.page == 1 for ch in chunks)
    assert any(ch.page == 2 for ch in chunks)


def test_chunker_creates_overlap():
    text = "Word " * 300
    docs = [Document(text=text, source="doc.pdf", source_type="pdf", page=1)]
    chunker = Chunker(chunk_size=500, chunk_overlap=100)
    chunks = chunker.chunk_documents(docs)

    assert len(chunks) >= 2


def test_chunker_no_empty_chunks():
    docs = [Document(text="Short text.", source="doc.pdf", source_type="pdf", page=1)]
    chunker = Chunker(chunk_size=800, chunk_overlap=150)
    chunks = chunker.chunk_documents(docs)

    assert len(chunks) == 1
    assert chunks[0].text == "Short text."
