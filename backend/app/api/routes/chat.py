import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag.chat_service import answer_question, stream_answer

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    """Answer a question using only the retrieved CV/project context."""
    result = await answer_question(payload.message, payload.session_id)
    return ChatResponse(**result)


@router.post("/stream")
async def chat_stream(payload: ChatRequest) -> StreamingResponse:
    """Same as POST /chat, but streams the answer as Server-Sent Events.

    Each event is a JSON payload: {"type": "token", "content": "..."} while
    the answer is being generated, then exactly one
    {"type": "done", "sources": [...], "confidence": "..."} at the end.
    """

    async def event_stream():
        async for event in stream_answer(payload.message, payload.session_id):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
