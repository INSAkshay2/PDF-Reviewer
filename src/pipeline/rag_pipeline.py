import logging

logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(self):
        from src.config import get_settings
        from src.embeddings import create_embedder
        from src.processing.chunker import Chunker
        from src.vectorstore.faiss_store import FaissStore
        from src.retrieval.retriever import Retriever
        from src.llm.gemini_client import GeminiClient
        from src.pipeline.ingestion_pipeline import IngestionPipeline

        self.settings = get_settings()

        logger.info("Initializing RAG pipeline lazily...")
        logger.info("Creating embedding backend: %s", self.settings.embedding_provider)
        self.embedder = create_embedder()

        self.chunker = Chunker(
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap,
        )

        logger.info("Initializing vector store...")
        self.vector_store = FaissStore(
            index_path=self.settings.faiss_index_path,
            dimension=self.embedder.dimension,
        )

        self.retriever = Retriever(
            embedder=self.embedder,
            vector_store=self.vector_store,
            top_k=self.settings.top_k,
        )

        self.llm = GeminiClient(
            api_key=self.settings.gemini_api_key,
            model_name=self.settings.llm_model,
            temperature=self.settings.llm_temperature,
        )

        self.ingestion = IngestionPipeline(
            embedder=self.embedder,
            chunker=self.chunker,
            vector_store=self.vector_store,
        )

        logger.info("RAG pipeline initialized")

    def ingest_file(self, file_path: str):
        return self.ingestion.ingest_file(file_path)

    def ingest_url(self, url: str):
        return self.ingestion.ingest_url(url)

    def query(self, question: str, chat_history: list | None = None) -> dict:
        self.vector_store.ensure_loaded()

        if not self.vector_store.size:
            return {
                "answer": "No documents have been indexed yet. Upload a document first.",
                "citations": [],
                "grounded": False,
            }

        retrieved = self.retriever.retrieve(question)
        if not retrieved:
            return {
                "answer": "I could not find any relevant information in the indexed documents.",
                "citations": [],
                "grounded": False,
            }

        result = self.llm.generate_answer(
            question=question,
            retrieved_docs=retrieved,
            chat_history=chat_history,
        )
        return result

    def get_stats(self) -> dict:
        self.vector_store.ensure_loaded()
        return {
            "total_chunks": self.vector_store.size,
            "unique_sources": len(set(
                d.source for d in self.vector_store.documents
            )),
            "source_types": {},
        }

    def get_source_summary(self) -> list[dict]:
        self.vector_store.ensure_loaded()
        seen: dict[str, dict] = {}
        for doc in self.vector_store.documents:
            key = doc.source
            if key not in seen:
                seen[key] = {
                    "source": doc.source,
                    "type": doc.source_type,
                    "chunks": 0,
                }
            seen[key]["chunks"] += 1
        return sorted(seen.values(), key=lambda x: x["source"])

    def clear(self) -> None:
        self.vector_store.ensure_loaded()
        self.vector_store.clear()
