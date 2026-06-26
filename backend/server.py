import logging
import os
import sys
from pathlib import Path
from functools import lru_cache

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FRONTEND_URL = os.getenv("FRONTEND_URL", "*")


def _normalize_origins(raw_value: str) -> list[str]:
    origins: list[str] = []
    for origin in raw_value.split(","):
        cleaned = origin.strip().rstrip("/")
        if cleaned:
            origins.append(cleaned)
    return origins


allowed_origins = ["*"] if FRONTEND_URL == "*" else _normalize_origins(FRONTEND_URL)
allow_credentials = allowed_origins != ["*"]

app = FastAPI(title="ContextFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("FastAPI app booted — RAG stack not yet loaded")


@lru_cache(maxsize=1)
def get_pipeline():
    logger.info("Initializing RAG pipeline lazily...")
    from src.pipeline.rag_pipeline import RAGPipeline
    return RAGPipeline()


class QueryRequest(BaseModel):
    question: str
    chat_history: list[dict] | None = None


class UrlIngestRequest(BaseModel):
    url: str


@app.get("/api/health")
def health():
    return {"status": "ok", "rag_loaded": False}


@app.get("/api/stats")
def stats():
    pipeline = get_pipeline()
    return pipeline.get_stats()


@app.get("/api/sources")
def sources():
    pipeline = get_pipeline()
    return pipeline.get_source_summary()


ALLOWED_EXTENSIONS = {".pdf", ".csv"}
ALLOWED_MIMETYPES = {
    "application/pdf",
    "text/csv",
    "application/csv",
    "text/plain",
}


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    from src.config import get_settings

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Only PDF and CSV files are accepted.",
        )

    if file.content_type and file.content_type not in ALLOWED_MIMETYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid content type '{file.content_type}'. Only PDF and CSV files are accepted.",
        )

    settings = get_settings()
    settings.uploads_dir.mkdir(parents=True, exist_ok=True)

    file_path = settings.uploads_dir / file.filename
    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    try:
        pipeline = get_pipeline()
        result = pipeline.ingest_file(str(file_path))
        if not result.success and result.error:
            raise HTTPException(status_code=400, detail=result.error)
        return result.model_dump()
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Ingest failed")
        raise HTTPException(
            status_code=500,
            detail="Failed to process the file. Ensure it is a valid text-based PDF or CSV.",
        )


@app.post("/api/ingest-url")
def ingest_url(req: UrlIngestRequest):
    try:
        pipeline = get_pipeline()
        result = pipeline.ingest_url(req.url)
        return result.model_dump()
    except Exception as e:
        logger.exception("URL ingest failed")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/query")
def query(req: QueryRequest):
    try:
        pipeline = get_pipeline()
        result = pipeline.query(req.question, req.chat_history)
        return result
    except Exception as e:
        logger.exception("Query failed")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate an answer. Please try again.",
        )


@app.post("/api/clear")
def clear():
    pipeline = get_pipeline()
    pipeline.clear()
    return {"status": "cleared"}


def main():
    port = int(os.getenv("PORT", "8000"))
    reload_enabled = os.getenv("RELOAD", "false").lower() == "true"
    uvicorn.run("backend.server:app", host="0.0.0.0", port=port, reload=reload_enabled)


if __name__ == "__main__":
    main()
