from typing import Literal

from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: Literal["high", "low", "no_context"]
