"""Turn raw markdown documents (CV, project write-ups, bio) into chunks
ready for embedding.

Chunking strategy: split each document by its "## " section headers first
(a chunk boundary that carries real meaning — one chunk = one experience,
one project, one skill category), then, only if a section is too long,
further split it by paragraph into smaller windows so no single chunk is
too large for the embedding model or the LLM's context.
"""

import re
from pathlib import Path
from typing import Literal

from app.schemas.rag import DocumentChunk

DEFAULT_MAX_CHARS = 900


def load_and_chunk_documents(
    raw_dir: Path, max_chars: int = DEFAULT_MAX_CHARS
) -> list[DocumentChunk]:
    """Read every .md file in raw_dir and return their chunks."""
    chunks: list[DocumentChunk] = []

    for path in sorted(raw_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        source_name = path.name
        source_type = _infer_source_type(path.stem)

        for section_title, section_body in _split_into_sections(text):
            windows = _split_into_windows(section_body, max_chars=max_chars)
            for i, window in enumerate(windows):
                chunks.append(
                    DocumentChunk(
                        chunk_id=_make_chunk_id(source_name, section_title, i),
                        content=window,
                        source_type=source_type,
                        source_name=source_name,
                        section=section_title,
                    )
                )

    return chunks


def _infer_source_type(stem: str) -> Literal["cv", "project", "bio"]:
    lowered = stem.lower()
    if "cv" in lowered:
        return "cv"
    if "project" in lowered:
        return "project"
    return "bio"


def _split_into_sections(text: str) -> list[tuple[str, str]]:
    """Split markdown text on '## ' headers, dropping the top-level '# ' title."""
    lines = text.splitlines()
    sections: list[tuple[str, str]] = []
    current_title = "Overview"
    current_lines: list[str] = []

    for line in lines:
        if line.startswith("## "):
            if current_lines:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = line[3:].strip()
            current_lines = []
        elif line.startswith("# "):
            continue  # document title, not a chunk-worthy section
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_title, "\n".join(current_lines).strip()))

    return [(title, body) for title, body in sections if body]


def _split_into_windows(text: str, max_chars: int) -> list[str]:
    """Group paragraphs into windows no larger than max_chars each."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    windows: list[str] = []
    current = ""

    for para in paragraphs:
        candidate = f"{current}\n\n{para}" if current else para
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                windows.append(current)
            current = para

    if current:
        windows.append(current)

    return windows or ([text] if text else [])


def _make_chunk_id(source_name: str, section: str, index: int) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", section.lower()).strip("-")
    return f"{source_name}:{slug}:{index}"
