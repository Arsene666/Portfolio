"""Diagnostic: shows the real similarity scores Qdrant returns for a
question, so we can tell whether RAG_SIMILARITY_THRESHOLD is miscalibrated
for the current embedding model, or something else is actually broken.

Usage:
    python scripts/diagnose_similarity.py "Why should I hire Arsène?"
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.config import get_settings  # noqa: E402
from app.services.rag.embeddings import embed_query  # noqa: E402
from app.services.rag.qdrant_store import get_qdrant_client  # noqa: E402


async def main() -> None:
    question = sys.argv[1] if len(sys.argv) > 1 else "Why should I hire Arsène?"
    settings = get_settings()

    print(f"Question: {question!r}")
    print(f"Current RAG_SIMILARITY_THRESHOLD: {settings.rag_similarity_threshold}")
    print(f"Embedding model: {settings.embedding_model_name}")
    print()

    client = get_qdrant_client()
    collections = [c.name for c in client.get_collections().collections]
    print(f"Collections found: {collections}")

    if settings.qdrant_collection_name not in collections:
        print(f"PROBLEM: collection '{settings.qdrant_collection_name}' does not exist.")
        return

    count = client.count(settings.qdrant_collection_name).count
    print(f"Points in '{settings.qdrant_collection_name}': {count}")
    print()

    query_vector = await embed_query(question)
    results = client.query_points(
        collection_name=settings.qdrant_collection_name,
        query=query_vector,
        limit=5,
        with_payload=True,
    )

    print("Top 5 matches (real scores):")
    for point in results.points:
        section = point.payload.get("section")
        source = point.payload.get("source_name")
        content_preview = point.payload.get("content", "")[:80].replace("\n", " ")
        above = "PASSES" if point.score >= settings.rag_similarity_threshold else "below threshold"
        print(f"  score={point.score:.4f} [{above}]  {source} / {section}")
        print(f"    \"{content_preview}...\"")


if __name__ == "__main__":
    asyncio.run(main())