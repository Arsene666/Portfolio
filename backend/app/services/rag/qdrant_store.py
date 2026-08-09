"""All direct interaction with Qdrant lives here. The rest of the app only
ever calls these functions — never the qdrant_client library directly.
"""

from functools import lru_cache

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import get_settings
from app.schemas.rag import DocumentChunk


@lru_cache
def get_qdrant_client() -> QdrantClient:
    settings = get_settings()
    if not settings.qdrant_url or not settings.qdrant_api_key:
        raise RuntimeError(
            "QDRANT_URL and QDRANT_API_KEY must be set in .env before using "
            "the RAG store. See the Qdrant Cloud setup instructions in the "
            "backend README."
        )
    return QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)


def recreate_collection(vector_size: int) -> None:
    """Drop and recreate the collection so re-running ingestion is always
    a clean, idempotent full refresh rather than accumulating stale points."""
    settings = get_settings()
    client = get_qdrant_client()

    existing = [c.name for c in client.get_collections().collections]
    if settings.qdrant_collection_name in existing:
        client.delete_collection(settings.qdrant_collection_name)

    client.create_collection(
        collection_name=settings.qdrant_collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )


def upsert_chunks(chunks: list[DocumentChunk], embeddings: list[list[float]]) -> None:
    settings = get_settings()
    client = get_qdrant_client()

    points = [
        PointStruct(
            id=i,
            vector=embedding,
            payload={
                "chunk_id": chunk.chunk_id,
                "content": chunk.content,
                "source_type": chunk.source_type,
                "source_name": chunk.source_name,
                "section": chunk.section,
            },
        )
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings, strict=True))
    ]

    client.upsert(collection_name=settings.qdrant_collection_name, points=points)


def search(query_embedding: list[float], top_k: int = 5) -> list[dict]:
    """Return the top_k closest chunks (as payload dicts) to a query embedding."""
    settings = get_settings()
    client = get_qdrant_client()

    results = client.query_points(
        collection_name=settings.qdrant_collection_name,
        query=query_embedding,
        limit=top_k,
        with_payload=True,
    )

    return [
        {**point.payload, "score": point.score} for point in results.points
    ]
