"""Diagnostic script: isolates whether a Qdrant issue is connection/auth
related, or specific to creating a collection.

Usage:
    python scripts/diagnose_qdrant.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.config import get_settings  # noqa: E402


def main() -> None:
    settings = get_settings()

    print(f"QDRANT_URL: {settings.qdrant_url}")
    print(f"QDRANT_API_KEY set: {bool(settings.qdrant_api_key)}")
    print()

    from qdrant_client import QdrantClient

    client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)

    print("Step 1 — can we list collections? (tests connection + auth)")
    try:
        collections = client.get_collections()
        print(f"  OK. Existing collections: {[c.name for c in collections.collections]}")
    except Exception as e:
        print(f"  FAILED at connection/auth level: {type(e).__name__}: {e}")
        return

    print()
    print("Step 2 — can we create a throwaway test collection?")
    from qdrant_client.models import Distance, VectorParams

    test_name = "diagnostic_test_collection"
    try:
        if test_name in [c.name for c in client.get_collections().collections]:
            client.delete_collection(test_name)
        client.create_collection(
            collection_name=test_name,
            vectors_config=VectorParams(size=4, distance=Distance.COSINE),
        )
        print("  OK. Test collection created successfully.")
        client.delete_collection(test_name)
        print("  Cleaned up test collection.")
    except Exception as e:
        print(f"  FAILED at create_collection: {type(e).__name__}: {e}")
        return

    print()
    print("Everything works. Qdrant is correctly configured.")


if __name__ == "__main__":
    main()
