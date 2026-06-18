"""Text cleaning utilities for extracted document content."""

import re


def clean_text(text: str) -> str:
    """Normalize whitespace and fix common PDF extraction artifacts."""
    if not text:
        return ""

    text = text.replace("\x00", "")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
