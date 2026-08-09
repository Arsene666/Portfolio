from typing import Literal

from pydantic import BaseModel


class DocumentChunk(BaseModel):
    chunk_id: str
    content: str
    source_type: Literal["cv", "project", "bio"]
    source_name: str
    section: str | None = None
