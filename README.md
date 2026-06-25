# 🚀 Multi-Source RAG Knowledge Base (Phase 2)

A production-style multi-source RAG (Retrieval-Augmented Generation) knowledge base supporting PDF, CSV, and website ingestion with semantic search and Gemini-powered answers.

## Architecture

```
PDF / CSV / URL
      │
      ▼
Loaders (PyMuPDF / BeautifulSoup / csv.DictReader)
      │
      ▼
Document Processing (clean_text normalization)
      │
      ▼
Chunker (LangChain RecursiveCharacterTextSplitter)
      │
      ▼
BGE Embeddings (BAAI/bge-small-en-v1.5, 384-dim)
      │
      ▼
FAISS Vector Store (IndexIDMap · global index · disk-persisted)
      │
      ▼
Retriever (top-k cosine similarity)
      │
      ▼
Gemini 2.5 Flash (grounded answer generation with citations)
      │
      ▼
Answer + Source Citations
```

## Features

- **Multi-source ingestion**: PDF, CSV, Website URLs
- **Semantic search**: BGE embeddings + FAISS vector similarity
- **Grounded answers**: Gemini 2.5 Flash with strict context grounding
- **Source citations**: Inline `[Source: filename, Page N]` with excerpts
- **Persistent index**: FAISS + metadata saved to disk across sessions
- **Chat history**: Session-based conversation memory
- **3D visualization**: Interactive document embedding space explorer
- **Cyberpunk UI**: Animated gradient background, glassmorphism, neon effects, Three.js particles

## Tech Stack

| Component | Technology |
|-----------|------------|
| UI | Streamlit (custom CSS, glassmorphism, Three.js) |
| PDF | PyMuPDF (fitz) |
| Web | requests + BeautifulSoup (lxml) |
| CSV | csv.DictReader |
| Chunking | LangChain RecursiveCharacterTextSplitter |
| Embeddings | BAAI/bge-small-en-v1.5 (384-dim) |
| Vector DB | FAISS (IndexIDMap) |
| LLM | Google Gemini 2.5 Flash |
| Validation | Pydantic v2 |
| 3D Viz | Plotly + Three.js |
| Tests | pytest |

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:
```
GEMINI_API_KEY=your_key_here
```

Run:
```bash
streamlit run app/streamlit_app.py
```

## Project Structure

```
app/
  streamlit_app.py              UI with 3D visualizations
src/
  config.py                     Environment settings
  models.py                     Unified Document schema
  ingestion/
    pdf_loader.py               PyMuPDF extractor
    web_loader.py               Website scraper
    csv_loader.py               CSV parser
    document_processor.py       Text cleaning pipeline
  processing/
    chunker.py                  LangChain text splitter
    cleaner.py                  Whitespace/hyphenation fixes
  embeddings/
    embedder.py                 BGE SentenceTransformer
  vectorstore/
    faiss_store.py              FAISS global index with persistence
  retrieval/
    retriever.py                Semantic search
  llm/
    gemini_client.py            Gemini API with citations
  pipeline/
    ingestion_pipeline.py       Multi-source ingestion orchestration
    rag_pipeline.py             Query → Retrieve → Generate
tests/
  test_chunker.py
  test_cleaner.py
  test_faiss_store.py
  test_retriever.py
```

## Testing

```bash
pytest tests/ -v
```

## Future Enhancements

- Hybrid search (keyword + vector)
- BGE Reranker for re-ranking
- Sentence Window Retrieval
- Graph RAG
- User authentication
- Cloud deployment
