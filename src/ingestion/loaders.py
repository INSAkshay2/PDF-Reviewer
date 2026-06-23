import os
import requests
from typing import List
from bs4 import BeautifulSoup
import pypdf
import csv

from src.models import Document

def load_pdf(file_path: str) -> List[Document]:
    """Loads documents from a PDF file."""
    reader = pypdf.PdfReader(file_path)
    documents = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            documents.append(Document(
                text=text,
                source=os.path.basename(file_path),
                source_type="pdf",
                page=i + 1,
                metadata={"file_path": file_path}
            ))
    return documents

def load_website(url: str) -> List[Document]:
    """Loads documents from a website URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # A simple approach: get all text. This can be improved.
        text = soup.get_text(separator='\n', strip=True)
        return [Document(
            text=text,
            source=url,
            source_type="website",
            metadata={"url": url}
        )]
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return []

def load_csv(file_path: str) -> List[Document]:
    """Loads documents from a CSV file, treating each row as a document."""
    documents = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            # Combine all columns into a single text string
            text = ". ".join(f"{k}: {v}" for k, v in row.items())
            documents.append(Document(
                text=text,
                source=os.path.basename(file_path),
                source_type="csv",
                metadata={"file_path": file_path, "row": i + 1}
            ))
    return documents
