from app.services.rag.memory import append_turn, clear_history, get_history


def test_history_starts_empty_for_a_new_session():
    clear_history("test-session-a")
    assert get_history("test-session-a") == []


def test_append_turn_adds_user_and_assistant_messages():
    session = "test-session-b"
    clear_history(session)

    append_turn(session, "Quelle est sa stack ?", "Python et FastAPI.")

    assert get_history(session) == [
        {"role": "user", "content": "Quelle est sa stack ?"},
        {"role": "assistant", "content": "Python et FastAPI."},
    ]


def test_history_is_trimmed_to_max_turns():
    session = "test-session-c"
    clear_history(session)

    for i in range(10):
        append_turn(session, f"Question {i}", f"Answer {i}")

    history = get_history(session)
    assert len(history) == 10  # MAX_TURNS(5) * 2 messages per turn
    assert history[0]["content"] == "Question 5"  # oldest turn still kept


def test_sessions_are_isolated_from_each_other():
    clear_history("session-x")
    clear_history("session-y")

    append_turn("session-x", "Question for x", "Answer for x")

    assert get_history("session-y") == []
