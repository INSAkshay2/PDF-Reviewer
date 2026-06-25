from pydantic import BaseModel, Field


class Document(BaseModel):
    chunk_id: str = ""
    text: str
    source: str
    source_type: str
    page: int = 1
    score: float = 0.0
    metadata: dict = Field(default_factory=dict)


class IngestResult(BaseModel):
    source: str
    source_type: str
    num_chunks: int
    success: bool = True
    error: str = ""


class ChatMessage(BaseModel):
    role: str
    content: str
    sources: list[dict] = Field(default_factory=list)
