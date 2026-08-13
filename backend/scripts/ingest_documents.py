"""Ingest CV/project documents into Qdrant: chunk -> embed -> upsert.

Requires QDRANT_URL, QDRANT_API_KEY, and COHERE_API_KEY to be set in
backend/.env — see the README for how to get a free Cohere key.

Usage:
    python scripts/ingest_documents.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services.rag.chunking import load_and_chunk_documents  # noqa: E402
from app.services.rag.embeddings import embed_passages  # noqa: E402
from app.services.rag.qdrant_store import (  # noqa: E402
    recreate_collection,
    upsert_chunks,
)


async def main() -> None:
    raw_dir = Path(__file__).resolve().parent.parent / "data" / "raw"

    print(f"Loading and chunking documents from {raw_dir} ...")
    chunks = load_and_chunk_documents(raw_dir)
    print(f"  -> {len(chunks)} chunks")

    if not chunks:
        print("No chunks found — check that backend/data/raw/*.md exist.")
        return

    print("Embedding chunks via the Cohere API ...")
    embeddings = await embed_passages([chunk.content for chunk in chunks])
    vector_size = len(embeddings[0])
    print(f"  -> vector size: {vector_size}")

    print("Recreating Qdrant collection and upserting chunks ...")
    recreate_collection(vector_size)
    upsert_chunks(chunks, embeddings)

    print(f"Done. {len(chunks)} chunks are now searchable in Qdrant.")


if __name__ == "__main__":
    asyncio.run(main())