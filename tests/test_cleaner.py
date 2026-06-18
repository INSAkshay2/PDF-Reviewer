"""Tests for text cleaning."""

from src.processing.cleaner import clean_text


def test_clean_text_fixes_hyphenation():
    raw = "This is a docu-\nment about AI."
    cleaned = clean_text(raw)
    assert "docu-\nment" not in cleaned
    assert "document" in cleaned


def test_clean_text_collapses_whitespace():
    raw = "Hello    world\n\n\n\nTest"
    cleaned = clean_text(raw)
    assert "Hello world" in cleaned
    assert "\n\n\n" not in cleaned
