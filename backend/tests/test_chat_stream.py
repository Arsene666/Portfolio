import asyncio
from unittest.mock import patch

from app.services.rag import chat_service
from app.services.rag.memory import clear_history


async def _collect(agen):
    return [item async for item in agen]


async def _fake_stream_llm(messages):  # noqa: ARG001 — signature must match stream_llm
    for chunk in ["Bonjour", ", je suis ", "l'assistant."]:
        yield chunk


async def _fake_stream_llm_error(messages):  # noqa: ARG001
    from app.services.rag.llm_client import LLMError

    raise LLMError("boom")
    yield  # pragma: no cover — makes this an async generator function


def test_stream_answer_yields_tokens_then_a_single_done_event():
    session = "stream-test-1"
    clear_history(session)

    fake_results = [
        {"score": 0.9, "source_name": "cv.md", "section": "Profil", "content": "..."},
    ]

    with (
        patch("app.services.rag.chat_service.embed_query", return_value=[0.0] * 10),
        patch("app.services.rag.chat_service.search", return_value=fake_results),
        patch("app.services.rag.chat_service.stream_llm", new=_fake_stream_llm),
    ):
        events = asyncio.run(
            _collect(chat_service.stream_answer("Qui es-tu ?", session_id=session))
        )

    token_events = [e for e in events if e["type"] == "token"]
    done_events = [e for e in events if e["type"] == "done"]

    assert "".join(e["content"] for e in token_events) == "Bonjour, je suis l'assistant."
    assert len(done_events) == 1
    assert done_events[0]["sources"] == ["cv.md"]
    assert done_events[0]["confidence"] == "high"


def test_stream_answer_saves_the_full_answer_to_memory():
    session = "stream-test-2"
    clear_history(session)

    fake_results = [
        {"score": 0.9, "source_name": "cv.md", "section": "Profil", "content": "..."},
    ]

    with (
        patch("app.services.rag.chat_service.embed_query", return_value=[0.0] * 10),
        patch("app.services.rag.chat_service.search", return_value=fake_results),
        patch("app.services.rag.chat_service.stream_llm", new=_fake_stream_llm),
    ):
        asyncio.run(
            _collect(chat_service.stream_answer("Question", session_id=session))
        )

    from app.services.rag.memory import get_history

    history = get_history(session)
    assert history[-1] == {
        "role": "assistant",
        "content": "Bonjour, je suis l'assistant.",
    }


def test_stream_answer_low_similarity_never_calls_stream_llm():
    session = "stream-test-3"
    clear_history(session)

    with (
        patch("app.services.rag.chat_service.embed_query", return_value=[0.0] * 10),
        patch(
            "app.services.rag.chat_service.search",
            return_value=[{"score": 0.1, "source_name": "cv.md", "section": "x", "content": "..."}],
        ),
    ):
        events = asyncio.run(
            _collect(chat_service.stream_answer("random", session_id=session))
        )

    assert events[-1]["type"] == "done"
    assert events[-1]["confidence"] == "no_context"
    assert events[-1]["sources"] == []


def test_stream_answer_llm_error_yields_error_message_then_done():
    session = "stream-test-4"
    clear_history(session)

    fake_results = [
        {"score": 0.9, "source_name": "cv.md", "section": "Profil", "content": "..."},
    ]

    with (
        patch("app.services.rag.chat_service.embed_query", return_value=[0.0] * 10),
        patch("app.services.rag.chat_service.search", return_value=fake_results),
        patch("app.services.rag.chat_service.stream_llm", new=_fake_stream_llm_error),
    ):
        events = asyncio.run(
            _collect(chat_service.stream_answer("Qui es-tu ?", session_id=session))
        )

    assert events[-1]["type"] == "done"
    assert events[-1]["confidence"] == "no_context"
    assert any("went wrong" in e.get("content", "") for e in events if e["type"] == "token")
