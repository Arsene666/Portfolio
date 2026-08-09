from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.project import Project

# In-memory SQLite shared across a single connection for the whole test run,
# completely isolated from the dev/prod database.
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def _seed_one_project():
    db = TestingSessionLocal()
    db.add(
        Project(
            slug="test-project",
            title="Test project",
            short_description="A project used only for tests.",
            problem_statement="Testing the API.",
            architecture_summary="N/A",
            tech_stack=["Python", "FastAPI"],
            is_featured=True,
        )
    )
    db.commit()
    db.close()


def test_list_projects_returns_seeded_project():
    _seed_one_project()

    response = client.get("/api/v1/projects")
    assert response.status_code == 200

    slugs = [p["slug"] for p in response.json()]
    assert "test-project" in slugs


def test_get_project_by_slug():
    response = client.get("/api/v1/projects/test-project")
    assert response.status_code == 200
    assert response.json()["title"] == "Test project"


def test_get_unknown_project_returns_404():
    response = client.get("/api/v1/projects/does-not-exist")
    assert response.status_code == 404


def test_filter_projects_by_tag():
    response = client.get("/api/v1/projects", params={"tag": "FastAPI"})
    assert response.status_code == 200
    assert all("FastAPI" in p["tech_stack"] for p in response.json())
