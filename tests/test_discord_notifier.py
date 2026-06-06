from unittest.mock import MagicMock, patch

import pytest

from src.discord_notifier import (
    BOT_USERNAME,
    MAX_DISCORD_CONTENT_LENGTH,
    _create_payload_from_study,
    _send_notification,
    _split_message,
)
from src.models import Study

# --- _split_message ---

def test_short_message_not_split() -> None:
    msg = "x" * 100
    assert _split_message(msg) == [msg]


def test_message_at_exact_limit_not_split() -> None:
    msg = "x" * MAX_DISCORD_CONTENT_LENGTH
    result = _split_message(msg)
    assert result == [msg]


def test_long_message_split_into_chunks() -> None:
    msg = "x" * (MAX_DISCORD_CONTENT_LENGTH + 500)
    chunks = _split_message(msg)
    assert len(chunks) == 2
    assert all(len(c) <= MAX_DISCORD_CONTENT_LENGTH for c in chunks)
    assert sum(len(c) for c in chunks) == len(msg)


def test_split_preserves_all_content() -> None:
    msg = ("line\n" * 600)  # ~3000 chars, multi-line
    chunks = _split_message(msg)
    assert "".join(chunks) == msg


# --- _create_payload_from_study ---

def test_payload_contains_study_fields() -> None:
    study = Study(title="Test Study", compensation="0.5 VP-Stunden", short_description="Online", link="http://ex.com")
    payload = _create_payload_from_study(study)
    assert "Test Study" in payload["content"]
    assert "0.5 VP-Stunden" in payload["content"]
    assert "Online" in payload["content"]
    assert "http://ex.com" in payload["content"]
    assert payload["username"] == BOT_USERNAME


# --- _send_notification ---

@patch("src.discord_notifier.requests.post")
def test_send_notification_success(mock_post: MagicMock) -> None:
    mock_post.return_value.status_code = 204
    _send_notification({"content": "hello"}, "http://webhook.example.com")
    mock_post.assert_called_once()


@patch("src.discord_notifier.requests.post")
def test_send_notification_bad_status_raises(mock_post: MagicMock) -> None:
    mock_post.return_value.status_code = 400
    mock_post.return_value.text = "Bad Request"
    with pytest.raises(RuntimeError, match="400"):
        _send_notification({"content": "hello"}, "http://webhook.example.com")


@patch("src.discord_notifier.requests.post")
def test_send_notification_network_error_raises(mock_post: MagicMock) -> None:
    import requests as req
    mock_post.side_effect = req.RequestException("Connection refused")
    with pytest.raises(RuntimeError, match="Connection refused"):
        _send_notification({"content": "hello"}, "http://webhook.example.com")
