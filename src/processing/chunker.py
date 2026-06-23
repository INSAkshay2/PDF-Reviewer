from typing import List
from src.models import Document

class Chunker:
    """Splits documents into smaller chunks."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # Using langchain's text splitter as it's robust
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Chunks a list of documents."""
        chunks = []
        for doc in documents:
            text_chunks = self._text_splitter.split_text(doc.text)
            for i, text_chunk in enumerate(text_chunks):
                chunk_doc = Document(
                    text=text_chunk,
                    source=doc.source,
                    source_type=doc.source_type,
                    page=doc.page,
                    # Carry over metadata and add chunk index
                    metadata={**doc.metadata, "chunk_index": i}
                )
                chunks.append(chunk_doc)
        return chunks

