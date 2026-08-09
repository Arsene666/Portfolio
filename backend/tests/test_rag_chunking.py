from pathlib import Path

from app.services.rag.chunking import load_and_chunk_documents

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def test_chunking_produces_chunks_for_each_source_file():
    chunks = load_and_chunk_documents(RAW_DIR)
    source_names = {c.source_name for c in chunks}
    assert "cv.md" in source_names
    assert "projects.md" in source_names


def test_each_chunk_has_a_section_and_correct_source_type():
    chunks = load_and_chunk_documents(RAW_DIR)
    for chunk in chunks:
        assert chunk.section is not None
        assert chunk.source_type in ("cv", "project", "bio")


def test_no_chunk_exceeds_the_max_char_budget():
    max_chars = 900
    chunks = load_and_chunk_documents(RAW_DIR, max_chars=max_chars)
    for chunk in chunks:
        # A single overlong paragraph could still exceed max_chars slightly;
        # this asserts the chunker isn't silently returning whole documents.
        assert len(chunk.content) <= max_chars * 1.5


def test_chunk_ids_are_unique():
    chunks = load_and_chunk_documents(RAW_DIR)
    ids = [c.chunk_id for c in chunks]
    assert len(ids) == len(set(ids))


def test_long_experience_section_is_split_into_multiple_windows():
    # cv.md's "Expérience professionnelle" section contains two internships
    # and is long enough that it should be split into more than one chunk.
    chunks = load_and_chunk_documents(RAW_DIR)
    experience_chunks = [
        c for c in chunks if c.section == "Expérience professionnelle"
    ]
    assert len(experience_chunks) > 1
