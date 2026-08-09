"""Embedding model wrapper using fastembed (ONNX Runtime) instead of
sentence-transformers/PyTorch — chosen specifically to fit within Render's
free-tier 512MB memory limit. Importing torch + sentence-transformers alone
uses over 700MB; fastembed's ONNX backend uses a fraction of that.
"""

from functools import lru_cache

from fastembed import TextEmbedding

from app.core.config import get_settings


@lru_cache
def get_embedding_model() -> TextEmbedding:
    settings = get_settings()
    return TextEmbedding(
        model_name=settings.embedding_model_name,
        cache_dir="/app/.fastembed_cache",
    )


def embed_passages(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    return [vec.tolist() for vec in model.embed(texts)]


def embed_query(text: str) -> list[float]:
    model = get_embedding_model()
    return next(model.embed([text])).tolist()