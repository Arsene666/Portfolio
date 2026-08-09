from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel):
    slug: str
    title: str
    short_description: str
    problem_statement: str
    architecture_summary: str
    tech_stack: list[str]
    github_url: str | None = None
    demo_url: str | None = None
    demo_slug: str | None = None
    images: list[str] = []
    is_featured: bool = False


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
