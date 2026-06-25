from typing import List

from src.models import Document
from src.processing.cleaner import clean_text


def process_documents(documents: List[Document]) -> List[Document]:
    for doc in documents:
        doc.text = clean_text(doc.text)
    return documents
