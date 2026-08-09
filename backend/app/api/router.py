from fastapi import APIRouter

from app.api.routes import chat, health, projects

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(projects.router)
api_router.include_router(chat.router)

# Phase 2+: api_router.include_router(cv.router)
# Phase 5+: api_router.include_router(chat.router)
# Phase 7+: api_router.include_router(demos.router)
# Phase 8+: api_router.include_router(contact.router)
