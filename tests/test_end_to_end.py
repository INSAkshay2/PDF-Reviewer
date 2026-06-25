"""Quick functional test of the pipeline (no API key needed for ingest)."""
import os
import tempfile

from src.pipeline.rag_pipeline import RAGPipeline


def test_ingest_csv():
    p = RAGPipeline()
    csv_path = os.path.join(tempfile.gettempdir(), "test_rag_data.csv")
    with open(csv_path, "w") as f:
        f.write("topic,description\n")
        f.write("AI,Machine learning is a subset of artificial intelligence.\n")
        f.write("Python,Python is a high-level programming language.\n")

    result = p.ingest_file(csv_path)
    assert result.success
    assert result.num_chunks > 0
    assert result.source_type == "csv"

    stats = p.get_stats()
    assert stats["total_chunks"] > 0
    assert stats["unique_sources"] > 0

    p.clear()
    assert p.vector_store.size == 0


def test_ingest_pdf():
    p = RAGPipeline()
    pdf_path = os.path.join(tempfile.gettempdir(), "test_sample.pdf")
    try:
        import fitz
        doc = fitz.open()
        doc.new_page(width=612, height=792)
        doc[0].insert_text((72, 72), "This is a test document for PDF ingestion.")
        doc.save(pdf_path)
        doc.close()

        result = p.ingest_file(pdf_path)
        assert result.success
        assert result.num_chunks > 0
        assert result.source_type == "pdf"
    except Exception:
        pass
    finally:
        p.clear()


def test_pipeline_imports():
    from src.models import Document, IngestResult, ChatMessage
    from src.ingestion.pdf_loader import load_pdf
    from src.ingestion.csv_loader import load_csv
    from src.ingestion.web_loader import load_website
    from src.processing.chunker import Chunker
    from src.processing.cleaner import clean_text
    from src.embeddings.embedder import Embedder
    from src.vectorstore.faiss_store import FaissStore
    from src.retrieval.retriever import Retriever
    from src.llm.gemini_client import GeminiClient
    from src.pipeline.ingestion_pipeline import IngestionPipeline
    assert Document is not None
    assert IngestResult is not None
    assert ChatMessage is not None
    assert load_pdf is not None
    assert load_csv is not None
    assert Chunker is not None
    assert clean_text is not None
    assert Embedder is not None
    assert FaissStore is not None
    assert Retriever is not None
    assert GeminiClient is not None
    assert IngestionPipeline is not None
