"""Application configuration loaded from environment variables."""

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
INDICES_DIR = DATA_DIR / "indices"


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    embedding_model: str
    llm_model: str
    chunk_size: int
    chunk_overlap: int
    top_k: int
    embedding_batch_size: int
    llm_temperature: float
    uploads_dir: Path
    indices_dir: Path


@lru_cache
def get_settings() -> Settings:
    uploads_dir = UPLOADS_DIR
    indices_dir = INDICES_DIR
    uploads_dir.mkdir(parents=True, exist_ok=True)
    indices_dir.mkdir(parents=True, exist_ok=True)

    return Settings(
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        embedding_model=os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5"),
        llm_model=os.getenv("LLM_MODEL", "gemini-2.5-flash"),
        chunk_size=int(os.getenv("CHUNK_SIZE", "800")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "150")),
        top_k=int(os.getenv("TOP_K", "5")),
        embedding_batch_size=int(os.getenv("EMBEDDING_BATCH_SIZE", "32")),
        llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.1")),
        uploads_dir=uploads_dir,
        indices_dir=indices_dir,
    )
