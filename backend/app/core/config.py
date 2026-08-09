from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings, loaded from environment variables or .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Portfolio API"
    environment: str = "development"
    api_prefix: str = "/api/v1"

    # CORS
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Placeholders for future phases (RAG, LLM, DB) - not used yet in Phase 1
    database_url: str = "sqlite:///./portfolio.db"
    qdrant_url: str | None = None
    qdrant_api_key: str | None = None
    qdrant_collection_name: str = "portfolio_knowledge"
    embedding_model_name: str = "intfloat/multilingual-e5-small"
    openrouter_api_key: str | None = None
    llm_model_name: str = "openrouter/free"
    llm_temperature: float = 0.2
    rag_top_k: int = 5
    rag_similarity_threshold: float = 0.55


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance, so the .env file is parsed only once."""
    return Settings()
