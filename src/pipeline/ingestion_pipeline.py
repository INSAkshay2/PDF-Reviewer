import logging
import os
from pathlib import Path

from src.config import UPLOADS_DIR
from src.embeddings.embedder import Embedder
from src.ingestion.csv_loader import load_csv
from src.ingestion.document_processor import process_documents
from src.ingestion.pdf_loader import load_pdf
from src.ingestion.web_loader import load_website
from src.models import Document, IngestResult
from src.processing.chunker import Chunker
from src.vectorstore.faiss_store import FaissStore

logger = logging.getLogger(__name__)


class IngestionPipeline:
    def __init__(
        self,
        embedder: Embedder,
        chunker: Chunker,
        vector_store: FaissStore,
    ):
        self.embedder = embedder
        self.chunker = chunker
        self.vector_store = vector_store

    def ingest_file(self, file_path: str | Path) -> IngestResult:
        file_path = str(file_path)
        if file_path.endswith(".pdf"):
            return self._ingest_pdf(file_path)
        elif file_path.endswith(".csv"):
            return self._ingest_csv(file_path)
        else:
            return IngestResult(
                source=os.path.basename(file_path),
                source_type="unknown",
                num_chunks=0,
                success=False,
                error=f"Unsupported file type: {file_path}",
            )

    def ingest_url(self, url: str, timeout: int = 30) -> IngestResult:
        try:
            documents = load_website(url, timeout=timeout)
            return self._process_and_store(documents, url, "website")
        except Exception as e:
            logger.exception("URL ingestion failed")
            return IngestResult(
                source=url,
                source_type="website",
                num_chunks=0,
                success=False,
                error=str(e),
            )

    def _ingest_pdf(self, file_path: str) -> IngestResult:
        try:
            documents = load_pdf(file_path)
            source = os.path.basename(file_path)
            return self._process_and_store(documents, source, "pdf")
        except Exception as e:
            logger.exception("PDF ingestion failed")
            return IngestResult(
                source=os.path.basename(file_path),
                source_type="pdf",
                num_chunks=0,
                success=False,
                error=str(e),
            )

    def _ingest_csv(self, file_path: str) -> IngestResult:
        try:
            documents = load_csv(file_path)
            source = os.path.basename(file_path)
            return self._process_and_store(documents, source, "csv")
        except Exception as e:
            logger.exception("CSV ingestion failed")
            return IngestResult(
                source=os.path.basename(file_path),
                source_type="csv",
                num_chunks=0,
                success=False,
                error=str(e),
            )

    def _process_and_store(
        self,
        documents: list[Document],
        source: str,
        source_type: str,
    ) -> IngestResult:
        processed = process_documents(documents)
        chunks = self.chunker.chunk_documents(processed)
        if not chunks:
            return IngestResult(
                source=source,
                source_type=source_type,
                num_chunks=0,
                success=False,
                error="No chunks produced.",
            )

        texts = [c.text for c in chunks]
        embeddings = self.embedder.embed_documents(texts)
        self.vector_store.add_documents(chunks, embeddings)

        logger.info("Ingested %s: %d chunks", source, len(chunks))
        return IngestResult(
            source=source,
            source_type=source_type,
            num_chunks=len(chunks),
            success=True,
        )

    @staticmethod
    def save_uploaded_file(uploaded_file) -> str:
        file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
