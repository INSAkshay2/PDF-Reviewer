import logging
from pathlib import Path

import fitz

from src.models import Document

logger = logging.getLogger(__name__)


def load_pdf(file_path: str | Path) -> list[Document]:
    pdf_path = Path(file_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    source_file = pdf_path.name
    documents: list[Document] = []

    with fitz.open(pdf_path) as doc:
        for page_index in range(len(doc)):
            page = doc[page_index]
            text = page.get_text("text").strip()

            if not text:
                logger.warning(
                    "Page %d in '%s' has no extractable text (may be scanned/image-only).",
                    page_index + 1, source_file,
                )
                continue

            documents.append(Document(
                text=text,
                source=source_file,
                source_type="pdf",
                page=page_index + 1,
                metadata={"file_path": str(pdf_path)},
            ))

    if not documents:
        raise ValueError(
            f"No text could be extracted from '{source_file}'. "
            "The PDF may be image-based; OCR is not supported."
        )

    return documents
