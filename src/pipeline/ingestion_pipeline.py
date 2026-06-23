from typing import List, Union
import os

from src.config import FAISS_INDEX_PATH, UPLOADS_DIR
from src.ingestion.loaders import load_pdf, load_website, load_csv
from src.ingestion.document_processor import process_documents
from src.processing.chunker import Chunker
from src.embeddings.embedder import Embedder
from src.vectorstore.faiss_store import FaissStore

def ingest_file(file_path: str) -> None:
    """Ingests a single file (PDF or CSV)."""
    if file_path.endswith(".pdf"):
        documents = load_pdf(file_path)
    elif file_path.endswith(".csv"):
        documents = load_csv(file_path)
    else:
        print(f"Unsupported file type: {file_path}")
        return

    _process_and_store(documents)

def ingest_url(url: str) -> None:
    """Ingests content from a URL."""
    documents = load_website(url)
    _process_and_store(documents)

def _process_and_store(documents: List):
    """Helper function to process and store documents."""
    if not documents:
        return

    processed_docs = process_documents(documents)
    
    chunker = Chunker()
    chunks = chunker.chunk_documents(processed_docs)
    
    embedder = Embedder()
    embeddings = embedder.embed_documents([chunk.text for chunk in chunks])
    
    # Dimension should match your embedding model
    vector_store = FaissStore(index_path=FAISS_INDEX_PATH, dimension=embeddings.shape[1])
    vector_store.add_documents(chunks, embeddings)

    print(f"Successfully ingested and indexed {len(chunks)} chunks.")

def save_uploaded_file(uploaded_file) -> str:
    """Saves an uploaded file to the uploads directory and returns its path."""
    file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path
