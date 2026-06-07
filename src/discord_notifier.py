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


def _send_notification(payload: dict, webhook_url: str) -> None:
    try:
        
        r = requests.post(url=webhook_url, json=payload)
        if r.status_code != 204:
            raise RuntimeError(f"Failed to send notification: {r.status_code} {r.text}")
    except Exception as e:
        raise RuntimeError(f"Failed to send notification: {e}")

def _create_payload_from_study(study: Study) -> dict:
    return {
        "username": f"Neue Studie!!!",
        "content":  f"**{study.title}**\n"
                    f" **Bezahlung:** {study.compensation}\n"
                    f" **Beschreibung:** {study.short_description}\n"
                    f" **Link:** {study.link}"
    }

def send_study_notification(study: Study, webhook_url: str) -> None:
    payload = _create_payload_from_study(study)
    _send_notification(payload=payload, webhook_url=webhook_url)

def send_error_notification(error: Exception, webhook_url: str) -> None:
    payload = {
        "username": "SONA Scraper Error",
        "content": f"Scraper ist fehlgeschlagen:\n```\n{type(error).__name__}: {error}\n```"
    }
    _send_notification(payload=payload, webhook_url=webhook_url)