from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.base import Base
from app.db.seed import seed
from app.db.session import engine

settings = get_settings()
configure_logging(settings.environment)

Base.metadata.create_all(bind=engine)

# Re-seed on every boot. Idempotent (skips existing slugs), and necessary
# on hosts like Render's free tier where the local SQLite file is wiped on
# every redeploy/restart — without this, /api/v1/projects would come back
# empty after the app spins back up from an idle sleep.
seed()

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