from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.base import Base
from app.db.session import engine

settings = get_settings()
configure_logging(settings.environment)

# Phase 2: simple create_all for dev (SQLite). Swap for Alembic migrations
# once a real Postgres database is provisioned in a later phase.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Backend API powering the portfolio: projects, CV, RAG chat, and ML demos.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    """Simple root route so hitting the base URL doesn't 404."""
    return {"message": f"{settings.app_name} is running. See /docs for the API reference."}
