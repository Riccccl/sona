import requests
from src.models import Study

MAX_DISCORD_CONTENT_LENGTH = 2000


def _split_message(message: str) -> list[str]:
    if len(message) <= MAX_DISCORD_CONTENT_LENGTH:
        return [message]

    chunks: list[str] = []
    current = []
    current_len = 0

    for line in message.splitlines(keepends=True):
        if current_len + len(line) > MAX_DISCORD_CONTENT_LENGTH:
            if current:
                chunks.append(''.join(current))
                current = []
                current_len = 0

            if len(line) > MAX_DISCORD_CONTENT_LENGTH:
                for i in range(0, len(line), MAX_DISCORD_CONTENT_LENGTH):
                    chunks.append(line[i:i + MAX_DISCORD_CONTENT_LENGTH])
                continue

        current.append(line)
        current_len += len(line)

    if current:
        chunks.append(''.join(current))

    return chunks


def send_notification(message: str, webhook_url: str) -> None:
    try:
        for chunk in _split_message(message):
            payload = {
                "content": chunk
            }
            r = requests.post(url=webhook_url, json=payload)
            if r.status_code != 204:
                raise RuntimeError(f"Failed to send notification: {r.status_code} {r.text}")
    except Exception as e:
        raise RuntimeError(f"Failed to send notification: {e}")
