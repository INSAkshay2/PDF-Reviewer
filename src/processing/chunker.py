from typing import List

from src.models import Document


class Chunker:
    """Recursively split documents into chunks with overlap."""

    SEPARATORS = ["\n\n", "\n", ". ", " "]

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 150):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        chunks: List[Document] = []
        for doc in documents:
            text_chunks = self._split_text(doc.text)
            for i, text in enumerate(text_chunks):
                chunks.append(Document(
                    text=text,
                    source=doc.source,
                    source_type=doc.source_type,
                    page=doc.page,
                    metadata={**doc.metadata, "chunk_index": i},
                ))
        return chunks

    def _split_text(self, text: str) -> List[str]:
        if len(text) <= self.chunk_size:
            return [text]

        chunks: list[str] = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = min(start + self.chunk_size, text_len)

            if end < text_len:
                split_at = self._find_split(text, start, end)
                if split_at <= start:
                    split_at = end
                end = split_at

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            if end >= text_len:
                break

            start = max(end - self.chunk_overlap, start + 1)

        return chunks

    def _find_split(self, text: str, start: int, end: int) -> int:
        window = text[start:end]
        min_acceptable = max(int(self.chunk_size * 0.5), 1)

        for sep in self.SEPARATORS:
            pos = window.rfind(sep)
            if pos >= min_acceptable:
                return start + pos + len(sep)

        return end
