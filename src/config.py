import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    embedding_model: str
    embedding_provider: str
    llm_model: str
    chunk_size: int
    chunk_overlap: int
    top_k: int
    embedding_batch_size: int
    llm_temperature: float
    url_timeout: int
    uploads_dir: Path
    indices_dir: Path
    faiss_index_path: str


@lru_cache
def get_settings() -> Settings:
    load_dotenv()

    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    is_render = os.getenv("RENDER", "").lower() == "true"

    if is_render:
        base_dir = PROJECT_ROOT / "data"
    else:
        data_dir_env = os.getenv("DATA_DIR", "")
        base_dir = Path(data_dir_env) if data_dir_env else (PROJECT_ROOT / "data")

    uploads_dir = Path(os.getenv("UPLOADS_DIR", str(base_dir / "uploads")))
    indices_dir = Path(os.getenv("INDICES_DIR", str(base_dir / "indices")))
    faiss_index_path = os.getenv(
        "FAISS_INDEX_PATH", str(indices_dir / "knowledge_base")
    )

    uploads_dir.mkdir(parents=True, exist_ok=True)
    indices_dir.mkdir(parents=True, exist_ok=True)

    return Settings(
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        embedding_model=os.getenv("EMBEDDING_MODEL", "gemini-embedding-001"),
        embedding_provider=os.getenv("EMBEDDING_PROVIDER", "gemini"),
        llm_model=os.getenv("LLM_MODEL", "gemini-2.5-flash"),
        chunk_size=int(os.getenv("CHUNK_SIZE", "800")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "150")),
        top_k=int(os.getenv("TOP_K", "5")),
        embedding_batch_size=int(os.getenv("EMBEDDING_BATCH_SIZE", "32")),
        llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.1")),
        url_timeout=int(os.getenv("URL_TIMEOUT", "30")),
        uploads_dir=uploads_dir,
        indices_dir=indices_dir,
        faiss_index_path=faiss_index_path,
    )
