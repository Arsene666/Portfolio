from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.project import Project
from app.schemas.project import ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectRead])
def list_projects(
    tag: str | None = Query(default=None, description="Filter by a tech stack tag, e.g. 'FastAPI'"),
    featured_only: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> list[Project]:
    """List all projects, optionally filtered by tech tag or featured status."""
    stmt = select(Project).order_by(Project.created_at.desc())
    projects = db.execute(stmt).scalars().all()

    if tag:
        projects = [p for p in projects if tag.lower() in [t.lower() for t in p.tech_stack]]
    if featured_only:
        projects = [p for p in projects if p.is_featured]

    return projects


@router.get("/{slug}", response_model=ProjectRead)
def get_project(slug: str, db: Session = Depends(get_db)) -> Project:
    """Fetch a single project by its slug."""
    stmt = select(Project).where(Project.slug == slug)
    project = db.execute(stmt).scalar_one_or_none()

    if project is None:
        raise HTTPException(status_code=404, detail=f"Project '{slug}' not found")

    return project
