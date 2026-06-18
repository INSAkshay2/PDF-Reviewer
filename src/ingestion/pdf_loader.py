"""Extract text and metadata from PDF files using PyMuPDF."""

import logging
from pathlib import Path

import fitz

from src.models import DocumentPage

logger = logging.getLogger(__name__)


def load_pdf(path: str | Path) -> list[DocumentPage]:
    """Load a PDF and return one DocumentPage per non-empty page."""
    pdf_path = Path(path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    source_file = pdf_path.name
    pages: list[DocumentPage] = []

    with fitz.open(pdf_path) as doc:
        for page_index in range(len(doc)):
            page = doc[page_index]
            text = page.get_text("text").strip()

            if not text:
                logger.warning(
                    "Page %d in '%s' has no extractable text (may be scanned/image-only).",
                    page_index + 1,
                    source_file,
                )
                continue

            pages.append(
                DocumentPage(
                    page_number=page_index + 1,
                    text=text,
                    source_file=source_file,
                )
            )

    if not pages:
        raise ValueError(
            f"No text could be extracted from '{source_file}'. "
            "The PDF may be image-based; OCR is not supported in Phase 1."
        )

    return pages
