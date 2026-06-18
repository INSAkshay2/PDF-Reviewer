# Enterprise Multi-Source Knowledge Assistant — Phase 1

Phase 1 implements a production-style **PDF RAG pipeline** on CPU:

**PDF → Chunking → BGE Embeddings → FAISS → Gemini → Grounded Answer with Citations**

Built with custom modular Python (no LangChain) so each layer is explicit and learnable.

---

## Architecture

```
app/streamlit_app.py          ← User interface
src/pipeline/rag_pipeline.py  ← Orchestrates ingest + query
src/ingestion/pdf_loader.py   ← PyMuPDF text extraction (per page)
src/processing/chunker.py     ← Overlapping chunks with page metadata
src/embeddings/embedder.py    ← BAAI/bge-small-en-v1.5 (local)
src/vectorstore/faiss_store.py← FAISS IndexFlatIP + metadata JSON
src/retrieval/retriever.py    ← Semantic top-k search
src/llm/gemini_client.py      ← Gemini 2.5 Flash grounded generation
```

### Data flow

1. **Upload PDF** → saved to `data/uploads/`
2. **Extract text** per page (preserves page numbers for citations)
3. **Clean + chunk** (~800 chars, 150 overlap, per-page splitting)
4. **Embed chunks** locally with BGE-small (384-dim, normalized)
5. **Store in FAISS** → saved to `data/indices/{doc_id}.index` + `_meta.json`
6. **Ask question** → embed query → FAISS top-5 → Gemini with strict grounding prompt
7. **Answer** with inline citations like `[Source: report.pdf, Page 3]`

---

## Setup

### 1. Clone and install

```bash
cd "PDF Reviewer"
python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure API key

```bash
copy .env.example .env
```

Edit `.env` and set your Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey):

```
GEMINI_API_KEY=your_key_here
```

### 3. Run the app

```bash
streamlit run app/streamlit_app.py
```

Open `http://localhost:8501` in your browser.

---

## Usage

1. Upload a **text-based PDF** in the sidebar
2. Click **Process Document** (first run downloads ~130MB embedding model)
3. Ask questions in the chat interface
4. Expand **Sources** on each answer to see retrieved chunks, pages, and scores

---

## Project Structure

| File | Purpose |
|------|---------|
| `src/config.py` | Environment settings (models, chunk size, paths) |
| `src/models.py` | Pydantic schemas: Chunk, Citation, RAGResponse |
| `src/ingestion/pdf_loader.py` | PyMuPDF page-level extraction |
| `src/processing/cleaner.py` | Whitespace + hyphenation cleanup |
| `src/processing/chunker.py` | Recursive split with overlap |
| `src/embeddings/embedder.py` | sentence-transformers BGE wrapper |
| `src/vectorstore/faiss_store.py` | FAISS index save/load/search |
| `src/retrieval/retriever.py` | Query embedding + top-k retrieval |
| `src/llm/gemini_client.py` | Grounded Gemini generation + citations |
| `src/pipeline/rag_pipeline.py` | End-to-end ingest and query API |
| `app/streamlit_app.py` | Streamlit UI |

---

## Testing

```bash
pytest tests/ -v
```

Tests cover chunking (overlap, page metadata), FAISS save/load/search, and retriever ranking with a mock embedder. Gemini is not called in unit tests.

---

## Debugging Tips

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| No text extracted | Scanned/image PDF | Use a text-native PDF |
| Irrelevant answers | Chunk size mismatch | Tune `CHUNK_SIZE` / `CHUNK_OVERLAP` in `.env` |
| Model ignores context | Weak prompt | Already strict; lower `LLM_TEMPERATURE` |
| Slow first run | Model download | Normal; BGE caches in `~/.cache/huggingface/` |
| API errors | Missing/invalid key | Check `.env` GEMINI_API_KEY |
| FAISS dimension error | Model changed | Re-process the PDF to rebuild index |

---

## Streamlit Cloud Deployment

1. Push repo to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Set main file: `app/streamlit_app.py`
4. Add secret: `GEMINI_API_KEY`
5. Free tier has ~1GB RAM — BGE-small fits; expect 30–60s cold start

---

## Phase 1 Scope

**Included:** PDF ingestion, chunking, local BGE embeddings, FAISS persistence, semantic retrieval, Gemini grounded Q&A, Streamlit UI, citations, chat history.

**Phase 2 (next):** CSV + website ingestion, BGE reranker (top-20 → top-5), sentence-window retrieval.

---

## Dependencies

| Package | Role |
|---------|------|
| `streamlit` | Web UI |
| `pymupdf` | PDF text extraction |
| `sentence-transformers` | Local BGE embeddings |
| `faiss-cpu` | Vector similarity search |
| `google-genai` | Gemini API |
| `pydantic` | Typed data models |
| `python-dotenv` | Environment variables |
| `pytest` | Unit tests |
