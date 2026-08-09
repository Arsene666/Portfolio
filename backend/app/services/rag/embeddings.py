"""Wraps the embedding model so the rest of the app never talks to
sentence-transformers directly — if the model changes later, this is the
only file that needs to change.

Uses a multilingual model since the source documents are in French. The
model runs locally (no external API key needed), but downloading its
weights the first time requires internet access.
"""

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.core.config import get_settings


@lru_cache
def get_embedding_model() -> SentenceTransformer:
    settings = get_settings()
    return SentenceTransformer(settings.embedding_model_name)


def embed_passages(texts: list[str]) -> list[list[float]]:
    """Embed document chunks for storage. multilingual-e5 models expect a
    'passage: ' prefix on the text being indexed for best retrieval quality."""
    model = get_embedding_model()
    prefixed = [f"passage: {text}" for text in texts]
    embeddings = model.encode(prefixed, normalize_embeddings=True)
    return embeddings.tolist()


def embed_query(text: str) -> list[float]:
    """Embed an incoming user question. Same model, 'query: ' prefix."""
    model = get_embedding_model()
    embedding = model.encode(f"query: {text}", normalize_embeddings=True)
    return embedding.tolist()
