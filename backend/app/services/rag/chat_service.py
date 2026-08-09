"""Ties embeddings + Qdrant + the LLM together to answer a question.

The core anti-hallucination guardrail lives here: if nothing retrieved is
similar enough to the question, the LLM is never even called — the
assistant says it doesn't know, instead of risking an invented answer.
"""

from collections.abc import AsyncGenerator
from typing import Literal, TypedDict

from app.core.config import get_settings
from app.services.rag.embeddings import embed_query
from app.services.rag.llm_client import LLMError, call_llm, stream_llm
from app.services.rag.memory import append_turn, get_history, get_question_count
from app.services.rag.qdrant_store import search

NO_CONTEXT_ANSWER = (
    "I don't have that detail about Arsène's background, sorry. Feel free "
    "to check his resume directly, or ask me something else about his "
    "projects, skills, or experience."
)

RETRIEVAL_ERROR_ANSWER = (
    "The knowledge base isn't reachable right now (Qdrant or the embedding "
    "model may not be configured yet). Please try again shortly."
)

LLM_ERROR_ANSWER = (
    "Something went wrong while contacting the language model. Please try "
    "again in a moment."
)

LIMIT_REACHED_ANSWER = (
    "You've reached the question limit for this conversation — that's a "
    "deliberate limit to keep this demo available for everyone. Feel free "
    "to reach out directly through the contact form for anything else!"
)

HIGH_CONFIDENCE_THRESHOLD = 0.75


class ChatResult(TypedDict):
    answer: str
    sources: list[str]
    confidence: Literal["high", "low", "no_context"]


class StreamEvent(TypedDict, total=False):
    type: Literal["token", "done"]
    content: str  # present when type == "token"
    sources: list[str]  # present when type == "done"
    confidence: Literal["high", "low", "no_context"]  # present when type == "done"


def _build_system_prompt(context: str) -> str:
    return (
        "You are Arsène Godonou's personal AI assistant, embedded on his "
        "portfolio website. You speak on his behalf to recruiters and "
        "visitors, in a natural, warm, and direct tone — like a knowledgeable "
        "colleague introducing him, not a document search tool.\n\n"
        "Ground rules:\n"
        "- Only state facts that are supported by the background information "
        "below. Never invent details, dates, numbers, or experiences.\n"
        "- If something isn't covered by that information, say plainly that "
        "you don't have that detail about Arsène — offer to help with "
        "something else instead, don't apologize at length.\n"
        "- Never mention 'context', 'documents', 'the provided information', "
        "'based on the text above', or anything that exposes the retrieval "
        "mechanism. Just answer as if you simply know this about Arsène.\n"
        "- Reply in the same language the question was asked in.\n"
        "- Be concise: a few sentences, not a report. No bullet-point dumps "
        "unless the question specifically asks for a list.\n\n"
        f"What you know about Arsène:\n{context}"
    )


async def answer_question(question: str, session_id: str = "default") -> ChatResult:
    settings = get_settings()

    if get_question_count(session_id) >= settings.max_questions_per_session:
        return {"answer": LIMIT_REACHED_ANSWER, "sources": [], "confidence": "no_context"}

    try:
        query_embedding = embed_query(question)
        results = search(query_embedding, top_k=settings.rag_top_k)
    except Exception:  # noqa: BLE001 — any retrieval failure is a "not ready" state
        return {"answer": RETRIEVAL_ERROR_ANSWER, "sources": [], "confidence": "no_context"}

    if not results or results[0]["score"] < settings.rag_similarity_threshold:
        return {"answer": NO_CONTEXT_ANSWER, "sources": [], "confidence": "no_context"}

    context = "\n\n---\n\n".join(
        f"[{r['source_name']} - {r['section']}]\n{r['content']}" for r in results
    )
    system_prompt = _build_system_prompt(context)
    history = get_history(session_id)
    messages = [
        {"role": "system", "content": system_prompt},
        *history,
        {"role": "user", "content": question},
    ]

    try:
        answer = await call_llm(messages)
    except LLMError:
        return {"answer": LLM_ERROR_ANSWER, "sources": [], "confidence": "no_context"}

    append_turn(session_id, question, answer)

    sources = sorted({r["source_name"] for r in results})
    confidence: Literal["high", "low"] = (
        "high" if results[0]["score"] >= HIGH_CONFIDENCE_THRESHOLD else "low"
    )

    return {"answer": answer, "sources": sources, "confidence": confidence}


async def stream_answer(
    question: str, session_id: str = "default"
) -> AsyncGenerator[StreamEvent, None]:
    """Same orchestration and guardrails as answer_question, but yields
    the answer as it's generated instead of waiting for the full text.

    Always ends with exactly one {"type": "done", ...} event, so the caller
    knows when the stream is finished and can read the final sources.
    """
    settings = get_settings()

    try:
        query_embedding = embed_query(question)
        results = search(query_embedding, top_k=settings.rag_top_k)
    except Exception:  # noqa: BLE001 — any retrieval failure is a "not ready" state
        yield {"type": "token", "content": RETRIEVAL_ERROR_ANSWER}
        yield {"type": "done", "sources": [], "confidence": "no_context"}
        return

    if not results or results[0]["score"] < settings.rag_similarity_threshold:
        yield {"type": "token", "content": NO_CONTEXT_ANSWER}
        yield {"type": "done", "sources": [], "confidence": "no_context"}
        return

    context = "\n\n---\n\n".join(
        f"[{r['source_name']} - {r['section']}]\n{r['content']}" for r in results
    )
    system_prompt = _build_system_prompt(context)
    history = get_history(session_id)
    messages = [
        {"role": "system", "content": system_prompt},
        *history,
        {"role": "user", "content": question},
    ]

    full_answer = ""
    try:
        async for chunk in stream_llm(messages):
            full_answer += chunk
            yield {"type": "token", "content": chunk}
    except LLMError:
        yield {"type": "token", "content": LLM_ERROR_ANSWER}
        yield {"type": "done", "sources": [], "confidence": "no_context"}
        return

    append_turn(session_id, question, full_answer)

    sources = sorted({r["source_name"] for r in results})
    confidence: Literal["high", "low"] = (
        "high" if results[0]["score"] >= HIGH_CONFIDENCE_THRESHOLD else "low"
    )

    yield {"type": "done", "sources": sources, "confidence": confidence}
