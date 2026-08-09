"""Targeted diagnostic: reproduces the exact collection name and vector
size used by the real ingestion script, and prints as much detail about
any failure as the client exposes.

Usage:
    python scripts/diagnose_qdrant_detailed.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.config import get_settings  # noqa: E402


def main() -> None:
    settings = get_settings()

    from qdrant_client import QdrantClient
    from qdrant_client.http.exceptions import UnexpectedResponse
    from qdrant_client.models import Distance, VectorParams

    client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)

    name = settings.qdrant_collection_name  # real name: "portfolio_knowledge"
    size = 384  # real embedding size

    print(f"Collection name: {name}")
    print(f"Vector size: {size}")
    print()

    existing = [c.name for c in client.get_collections().collections]
    print(f"Existing collections before: {existing}")
    if name in existing:
        print(f"Deleting pre-existing '{name}' ...")
        client.delete_collection(name)

    print(f"Creating '{name}' with size={size} ...")
    try:
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )
        print("OK — collection created successfully.")
    except UnexpectedResponse as e:
        print(f"FAILED: status_code={e.status_code}")
        print(f"reason_phrase={e.reason_phrase}")
        print(f"content={e.content}")
        print(f"headers={dict(e.headers) if e.headers else None}")
    except Exception as e:
        print(f"FAILED with a different exception type: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
