"""Embedding service abstraction with factory support."""

import logging

from src.config import get_settings

logger = logging.getLogger(__name__)


def create_embedder():
    settings = get_settings()
    provider = settings.embedding_provider

    if provider == "gemini":
        from src.embeddings.gemini_embedder import GeminiEmbedder

        logger.info("Creating Gemini embedding service")
        return GeminiEmbedder(
            api_key=settings.gemini_api_key,
            model_name=settings.embedding_model,
            batch_size=settings.embedding_batch_size,
        )

    if provider == "local":
        from src.embeddings.local_embedder import LocalEmbedder

        logger.info("Creating local embedding service: %s", settings.embedding_model)
        return LocalEmbedder(
            model_name=settings.embedding_model,
            batch_size=settings.embedding_batch_size,
        )

    raise ValueError(
        f"Unknown embedding provider: {provider}. "
        f"Set EMBEDDING_PROVIDER to 'gemini' or 'local'."
    )
