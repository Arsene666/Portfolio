import asyncio
from unittest.mock import patch

from app.services.rag import chat_service
from app.services.rag.memory import clear_history


def test_low_similarity_returns_no_context_without_calling_llm():
    """The core anti-hallucination guardrail: below the threshold, the LLM
    must never even be called."""
    with (
        patch("app.services.rag.chat_service.embed_query", return_value=[0.0] * 10),
        patch(
            "app.services.rag.chat_service.search",
            return_value=[
                {
                    "score": 0.1,
                    "source_name": "cv.md",
                    "section": "Profil",
                    "content": "...",
                }
            ],
        ),
        patch("app.services.rag.chat_service.call_llm") as mock_llm,
    ):
        result = asyncio.run(
            chat_service.answer_question("unrelated question", session_id="t1")
        )

    assert result["confidence"] == "no_context"
    assert result["sources"] == []
    mock_llm.assert_not_called()


def test_no_search_results_returns_no_context():
    with (
        patch("app.services.rag.chat_service.embed_query", return_value=[0.0] * 10),
        patch("app.services.rag.chat_service.search", return_value=[]),
        patch("app.services.rag.chat_service.call_llm") as mock_llm,
    ):
        result = asyncio.run(chat_service.answer_question("anything", session_id="t2"))

    assert result["confidence"] == "no_context"
    mock_llm.assert_not_called()


def test_high_similarity_calls_llm_and_returns_sorted_unique_sources():
    fake_results = [
        {"score": 0.9, "source_name": "cv.md", "section": "Compétences", "content": "Python, FastAPI"},
        {"score": 0.8, "source_name": "projects.md", "section": "RAG assistant", "content": "..."},
        {"score": 0.76, "source_name": "cv.md", "section": "Profil", "content": "..."},
    ]

    with (
        patch("app.services.rag.chat_service.embed_query", return_value=[0.0] * 10),
        patch("app.services.rag.chat_service.search", return_value=fake_results),
        patch(
            "app.services.rag.chat_service.call_llm", return_value="Réponse test"
        ) as mock_llm,
    ):
        result = asyncio.run(
            chat_service.answer_question("Quelle est sa stack ?", session_id="t3")
        )

    assert result["answer"] == "Réponse test"
    assert result["sources"] == ["cv.md", "projects.md"]  # sorted, deduplicated
    assert result["confidence"] == "high"
    mock_llm.assert_called_once()


def test_moderate_similarity_is_low_confidence_but_still_answers():
    fake_results = [
        {"score": 0.6, "source_name": "cv.md", "section": "Formation", "content": "..."},
    ]

    with (
        patch("app.services.rag.chat_service.embed_query", return_value=[0.0] * 10),
        patch("app.services.rag.chat_service.search", return_value=fake_results),
        patch("app.services.rag.chat_service.call_llm", return_value="Réponse"),
    ):
        result = asyncio.run(
            chat_service.answer_question("Où a-t-il étudié ?", session_id="t4")
        )

    assert result["confidence"] == "low"
    assert result["answer"] == "Réponse"


def test_llm_error_is_handled_gracefully():
    from app.services.rag.llm_client import LLMError

    fake_results = [
        {"score": 0.9, "source_name": "cv.md", "section": "Profil", "content": "..."},
    ]

    with (
        patch("app.services.rag.chat_service.embed_query", return_value=[0.0] * 10),
        patch("app.services.rag.chat_service.search", return_value=fake_results),
        patch(
            "app.services.rag.chat_service.call_llm",
            side_effect=LLMError("boom"),
        ),
    ):
        result = asyncio.run(chat_service.answer_question("Qui es-tu ?", session_id="t5"))

    assert result["confidence"] == "no_context"
    assert "went wrong" in result["answer"]


def test_retrieval_failure_returns_graceful_message_not_a_crash():
    """If Qdrant isn't configured yet or the embedding model can't load,
    the service should degrade gracefully instead of raising."""
    with (
        patch(
            "app.services.rag.chat_service.embed_query",
            side_effect=RuntimeError("model not available"),
        ),
        patch("app.services.rag.chat_service.call_llm") as mock_llm,
    ):
        result = asyncio.run(chat_service.answer_question("Quelque chose", session_id="t6"))

    assert result["confidence"] == "no_context"
    assert "reachable" in result["answer"]
    mock_llm.assert_not_called()


def test_conversation_history_is_sent_to_the_llm_on_the_next_turn():
    """The actual memory feature: a second question in the same session
    should include the prior exchange in the messages sent to the LLM."""
    session = "history-test-session"
    clear_history(session)

    fake_results = [
        {"score": 0.9, "source_name": "cv.md", "section": "Profil", "content": "..."},
    ]

    with (
        patch("app.services.rag.chat_service.embed_query", return_value=[0.0] * 10),
        patch("app.services.rag.chat_service.search", return_value=fake_results),
        patch(
            "app.services.rag.chat_service.call_llm", return_value="Première réponse"
        ),
    ):
        asyncio.run(
            chat_service.answer_question("Première question", session_id=session)
        )

    with (
        patch("app.services.rag.chat_service.embed_query", return_value=[0.0] * 10),
        patch("app.services.rag.chat_service.search", return_value=fake_results),
        patch(
            "app.services.rag.chat_service.call_llm", return_value="Deuxième réponse"
        ) as mock_llm_second_call,
    ):
        asyncio.run(
            chat_service.answer_question("Deuxième question", session_id=session)
        )

    sent_messages = mock_llm_second_call.call_args[0][0]
    contents = [m["content"] for m in sent_messages]

    assert "Première question" in contents
    assert "Première réponse" in contents
    assert "Deuxième question" in contents


def test_different_sessions_do_not_share_history():
    clear_history("session-alpha")
    clear_history("session-beta")

    fake_results = [
        {"score": 0.9, "source_name": "cv.md", "section": "Profil", "content": "..."},
    ]

    with (
        patch("app.services.rag.chat_service.embed_query", return_value=[0.0] * 10),
        patch("app.services.rag.chat_service.search", return_value=fake_results),
        patch("app.services.rag.chat_service.call_llm", return_value="Réponse alpha"),
    ):
        asyncio.run(
            chat_service.answer_question("Question alpha", session_id="session-alpha")
        )

    with (
        patch("app.services.rag.chat_service.embed_query", return_value=[0.0] * 10),
        patch("app.services.rag.chat_service.search", return_value=fake_results),
        patch(
            "app.services.rag.chat_service.call_llm", return_value="Réponse beta"
        ) as mock_llm_beta,
    ):
        asyncio.run(
            chat_service.answer_question("Question beta", session_id="session-beta")
        )

    sent_messages = mock_llm_beta.call_args[0][0]
    contents = [m["content"] for m in sent_messages]

    assert "Question alpha" not in contents
    assert "Réponse alpha" not in contents
