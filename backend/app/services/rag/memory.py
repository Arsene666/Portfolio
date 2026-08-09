"""In-memory conversation history, keyed by session_id.

Deliberately simple — a process-local dict is enough for a single-instance
portfolio deployment. If this ever runs with multiple workers or needs to
survive restarts, swap the storage for Redis or a DB table; the three
functions below are the only thing the rest of the app depends on, so the
swap wouldn't touch chat_service.py at all.
"""

from collections import defaultdict

MAX_TURNS = 5  # keep the last 5 question/answer exchanges per session, for LLM context

_history: dict[str, list[dict[str, str]]] = defaultdict(list)

# Separate from _history on purpose: _history is trimmed to MAX_TURNS so the
# LLM prompt doesn't grow forever, but the question-count limit (used to
# protect the free LLM quota) needs the *real* total, uncapped.
_question_counts: dict[str, int] = defaultdict(int)


def get_history(session_id: str) -> list[dict[str, str]]:
    """Return the stored turns for a session, oldest first."""
    return list(_history[session_id])


def get_question_count(session_id: str) -> int:
    """Total questions asked in this session, never trimmed."""
    return _question_counts[session_id]


def append_turn(session_id: str, question: str, answer: str) -> None:
    """Record a question/answer exchange, trimming to the last MAX_TURNS."""
    _history[session_id].append({"role": "user", "content": question})
    _history[session_id].append({"role": "assistant", "content": answer})
    _history[session_id] = _history[session_id][-MAX_TURNS * 2 :]
    _question_counts[session_id] += 1


def clear_history(session_id: str) -> None:
    _history.pop(session_id, None)
    _question_counts.pop(session_id, None)