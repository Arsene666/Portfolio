from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_endpoint_returns_answer_and_sources():
    with patch(
        "app.api.routes.chat.answer_question",
        return_value={
            "answer": "Il a fait un stage chez Movalib.",
            "sources": ["cv.md"],
            "confidence": "high",
        },
    ):
        response = client.post(
            "/api/v1/chat",
            json={"session_id": "test-session", "message": "Parle-moi de son stage"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "Il a fait un stage chez Movalib."
    assert body["sources"] == ["cv.md"]
    assert body["confidence"] == "high"


def test_chat_endpoint_rejects_missing_message():
    response = client.post("/api/v1/chat", json={"session_id": "test-session"})
    assert response.status_code == 422


def test_chat_stream_endpoint_returns_sse_formatted_events():
    async def fake_stream_answer(question, session_id):  # noqa: ARG001
        yield {"type": "token", "content": "Bon"}
        yield {"type": "token", "content": "jour"}
        yield {"type": "done", "sources": ["cv.md"], "confidence": "high"}

    with patch("app.api.routes.chat.stream_answer", new=fake_stream_answer):
        response = client.post(
            "/api/v1/chat/stream",
            json={"session_id": "test-session", "message": "Salut"},
        )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")

    body = response.text
    assert 'data: {"type": "token", "content": "Bon"}' in body
    assert 'data: {"type": "token", "content": "jour"}' in body
    assert '"type": "done"' in body
    assert '"sources": ["cv.md"]' in body
