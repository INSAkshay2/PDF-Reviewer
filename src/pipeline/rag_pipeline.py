"""End-to-end RAG pipeline orchestration."""

import hashlib
import logging
from pathlib import Path

from src.config import Settings, get_settings
from src.embeddings.embedder import Embedder
from src.ingestion.pdf_loader import load_pdf
from src.llm.gemini_client import GeminiClient
from src.models import ChatMessage, IngestResult, RAGResponse
from src.processing.chunker import Chunker
from src.retrieval.retriever import Retriever
from src.vectorstore.faiss_store import FaissStore

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Orchestrates PDF ingestion, retrieval, and answer generation."""

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self.embedder = Embedder(
            model_name=self.settings.embedding_model,
            batch_size=self.settings.embedding_batch_size,
        )
        self.chunker = Chunker(
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap,
        )
        self.llm = GeminiClient(
            api_key=self.settings.gemini_api_key,
            model_name=self.settings.llm_model,
            temperature=self.settings.llm_temperature,
        )
        self._stores: dict[str, FaissStore] = {}

    def ingest_pdf(self, file_path: str | Path) -> IngestResult:
        """Load, chunk, embed, and index a PDF document."""
        pdf_path = Path(file_path)
        doc_id = self._make_doc_id(pdf_path)

        logger.info("Ingesting PDF: %s", pdf_path.name)
        pages = load_pdf(pdf_path)
        chunks = self.chunker.chunk_pages(pages)

        if not chunks:
            raise ValueError(f"No chunks produced from '{pdf_path.name}'")

        texts = [chunk.text for chunk in chunks]
        embeddings = self.embedder.embed_documents(texts)

        store = FaissStore(dimension=self.embedder.dimension)
        store.add_chunks(chunks, embeddings)

        index_prefix = self.settings.indices_dir / doc_id
        store.save(index_prefix)
        self._stores[doc_id] = store

        return IngestResult(
            doc_id=doc_id,
            source_file=pdf_path.name,
            num_pages=len(pages),
            num_chunks=len(chunks),
            index_path=str(index_prefix),
        )

    def query(
        self,
        doc_id: str,
        question: str,
        chat_history: list[ChatMessage] | None = None,
    ) -> RAGResponse:
        """Retrieve relevant chunks and generate a grounded answer."""
        store = self.get_store(doc_id)
        retriever = Retriever(
            embedder=self.embedder,
            store=store,
            top_k=self.settings.top_k,
        )
        retrieval_results = retriever.retrieve(question)
        return self.llm.generate_answer(
            question=question,
            retrieval_results=retrieval_results,
            chat_history=chat_history,
        )

    def get_store(self, doc_id: str) -> FaissStore:
        """Return a cached store or load it from disk."""
        if doc_id in self._stores:
            return self._stores[doc_id]

        index_prefix = self.settings.indices_dir / doc_id
        store = FaissStore.load(index_prefix)
        self._stores[doc_id] = store
        return store

    def list_indexed_documents(self) -> list[str]:
        """List doc IDs that have saved indices on disk."""
        indices_dir = self.settings.indices_dir
        doc_ids: list[str] = []
        for meta_file in indices_dir.glob("*_meta.json"):
            doc_ids.append(meta_file.name.replace("_meta.json", ""))
        return sorted(doc_ids)

    def save_uploaded_pdf(self, filename: str, file_bytes: bytes) -> Path:
        """Persist an uploaded PDF to the uploads directory."""
        safe_name = Path(filename).name
        dest = self.settings.uploads_dir / safe_name
        dest.write_bytes(file_bytes)
        return dest

    @staticmethod
    def _make_doc_id(pdf_path: Path) -> str:
        digest = hashlib.md5(str(pdf_path.resolve()).encode()).hexdigest()[:12]
        stem = pdf_path.stem.replace(" ", "_")
        return f"{stem}_{digest}"
