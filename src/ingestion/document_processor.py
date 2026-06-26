import logging
import re
from typing import List

from src.models import Document
from src.processing.cleaner import clean_text

logger = logging.getLogger(__name__)

# Regex to detect long base64-like sequences (probable inline image/embedded data)
_BASE64_LIKE = re.compile(r"[A-Za-z0-9+/=]{100,}")


def _looks_like_binary(text: str) -> bool:
    """Check if text contains long base64-encoded sequences (probable binary data)."""
    if _BASE64_LIKE.search(text):
        return True
    # Check for high ratio of non-printable chars
    if len(text) > 50:
        printable = sum(1 for c in text if c.isprintable() or c in "\n\r\t")
        if printable / len(text) < 0.8:
            return True
    return False


def process_documents(documents: List[Document]) -> List[Document]:
    cleaned = []
    for doc in documents:
        doc.text = clean_text(doc.text)
        if _looks_like_binary(doc.text):
            logger.warning(
                "Skipping page %d from '%s': text appears to contain binary/encoded data",
                doc.page, doc.source,
            )
            continue
        cleaned.append(doc)
    return cleaned
