"""Shared Pydantic data models for the RAG pipeline."""

from pydantic import BaseModel, Field


class DocumentPage(BaseModel):
    page_number: int
    text: str
    source_file: str


class Chunk(BaseModel):
    chunk_id: str
    text: str
    source_file: str
    page_number: int
    char_start: int = 0
    char_end: int = 0


class RetrievalResult(BaseModel):
    chunk: Chunk
    score: float


class Citation(BaseModel):
    source_file: str
    page_number: int
    excerpt: str = ""


class ChatMessage(BaseModel):
    role: str
    content: str


class RAGResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    retrieval_results: list[RetrievalResult] = Field(default_factory=list)
    grounded: bool = True

class Document(BaseModel):
    text: str
    metadata: dict = Field(default_factory=dict)

class IngestResult(BaseModel):
    doc_id: str
    source_file: str
    num_pages: int
    num_chunks: int
    index_path: str
