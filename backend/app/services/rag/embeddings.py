"""Embedding client using Cohere's hosted Embed API — deliberately *not* a
local model.

Two different local approaches were tried first (sentence-transformers,
then the lighter fastembed) and both still pushed Render's free-tier
512MB memory limit over the edge under real traffic. Calling a hosted API
instead removes the model from this process's memory entirely; the only
cost is a network round-trip per request, which is a fine trade-off for a
low-traffic portfolio chat.
"""

import httpx

from app.core.config import get_settings

COHERE_EMBED_URL = "https://api.cohere.ai/v1/embed"


class EmbeddingError(Exception):
    """Raised when the Cohere embed API call fails."""


async def _embed(texts: list[str], input_type: str) -> list[list[float]]:
    settings = get_settings()

    if not settings.cohere_api_key:
        raise EmbeddingError(
            "COHERE_API_KEY is not set in .env — get a free key at "
            "dashboard.cohere.com."
        )

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            COHERE_EMBED_URL,
            headers={
                "Authorization": f"Bearer {settings.cohere_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "texts": texts,
                "model": settings.embedding_model_name,
                "input_type": input_type,
            },
        )

    if response.status_code != 200:
        raise EmbeddingError(
            f"Cohere embed request failed ({response.status_code}): "
            f"{response.text[:300]}"
        )

    data = response.json()
    return data["embeddings"]


async def embed_passages(texts: list[str]) -> list[list[float]]:
    """Embed document chunks for storage. Cohere distinguishes documents
    from queries via input_type, for better retrieval quality."""
    return await _embed(texts, input_type="search_document")


async def embed_query(text: str) -> list[float]:
    """Embed an incoming user question."""
    vectors = await _embed([text], input_type="search_query")
    return vectors[0]