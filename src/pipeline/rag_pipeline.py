from typing import List
from src.config import FAISS_INDEX_PATH
from src.embeddings.embedder import Embedder
from src.vectorstore.faiss_store import FaissStore
from src.retrieval.retriever import Retriever
from src.llm.gemini_client import GeminiClient
from src.models import Document

class RAGPipeline:
    """Orchestrates the retrieval and answer generation pipeline."""

    def __init__(self):
        self.embedder = Embedder()
        # The dimension must match the model used by Embedder
        self.vector_store = FaissStore(index_path=FAISS_INDEX_PATH, dimension=self.embedder.dimension)
        self.retriever = Retriever(vector_store=self.vector_store, embedder=self.embedder)
        self.llm_client = GeminiClient()

    def query(self, question: str) -> dict:
        """
        Takes a question, retrieves relevant documents, and generates an answer.
        
        Returns:
            A dictionary containing the answer and the source documents.
        """
        retrieved_results = self.retriever.retrieve(question)
        
        # Unpack the results from the retriever
        source_documents = [doc for doc, score in retrieved_results]

        if not source_documents:
            return {
                "answer": "I could not find any relevant information in the indexed documents.",
                "sources": []
            }

        answer = self.llm_client.generate_answer(question, source_documents)

        return {
            "answer": answer,
            "sources": source_documents
        }

