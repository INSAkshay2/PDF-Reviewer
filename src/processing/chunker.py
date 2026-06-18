"""Document chunking with overlap and page-level metadata preservation."""

from src.models import Chunk, DocumentPage
from src.processing.cleaner import clean_text


class Chunker:
    """Split document pages into overlapping chunks while preserving metadata."""

    SEPARATORS = ["\n\n", "\n", ". ", " "]

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 150):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_pages(self, pages: list[DocumentPage]) -> list[Chunk]:
        """Chunk each page independently to preserve accurate page numbers."""
        all_chunks: list[Chunk] = []

        for page in pages:
            cleaned = clean_text(page.text)
            if not cleaned:
                continue

            page_chunks = self._split_text(cleaned)
            for index, (text, char_start, char_end) in enumerate(page_chunks):
                chunk_id = f"{page.source_file}::p{page.page_number}::c{index}"
                all_chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        text=text,
                        source_file=page.source_file,
                        page_number=page.page_number,
                        char_start=char_start,
                        char_end=char_end,
                    )
                )

        return all_chunks

    def _split_text(self, text: str) -> list[tuple[str, int, int]]:
        """Recursively split text into chunks with overlap."""
        if len(text) <= self.chunk_size:
            return [(text, 0, len(text))]

        chunks: list[tuple[str, int, int]] = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = min(start + self.chunk_size, text_len)

            if end < text_len:
                split_at = self._find_split_point(text, start, end)
                if split_at <= start:
                    split_at = end
                end = split_at

            chunk_text = text[start:end].strip()
            if chunk_text:
                leading = len(text[start:end]) - len(text[start:end].lstrip())
                chunk_start = start + leading
                chunk_end = chunk_start + len(chunk_text)
                chunks.append((chunk_text, chunk_start, chunk_end))

            if end >= text_len:
                break

            start = max(end - self.chunk_overlap, start + 1)

        return chunks

    def _find_split_point(self, text: str, start: int, end: int) -> int:
        """Find the best separator boundary within the chunk window."""
        window = text[start:end]
        min_acceptable = int(self.chunk_size * 0.5)

        for separator in self.SEPARATORS:
            pos = window.rfind(separator)
            if pos >= min_acceptable:
                return start + pos + len(separator)

        return end
