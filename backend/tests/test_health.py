from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_200():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check_returns_ok_status():
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "ok"
    assert body["app_name"] == "Portfolio API"
    assert "environment" in body


def test_openapi_docs_are_available():
    response = client.get("/docs")
    assert response.status_code == 200
