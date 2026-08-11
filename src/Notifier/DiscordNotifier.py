from .HttpNotifier import HttpNotifier
from .Notification import Notification

MAX_DISCORD_CONTENT_LENGTH = 2000


def _split_message(message: str) -> list[str]:
    """Zerlegt den Text in Stuecke, die Discords Laengenlimit einhalten."""
    if len(message) <= MAX_DISCORD_CONTENT_LENGTH:
        return [message]

    chunks: list[str] = []
    current: list[str] = []
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


class DiscordNotifier(HttpNotifier):
    name = "discord"

    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    def send(self, notification: Notification) -> None:
        for chunk in _split_message(notification.body):
            self._post(
                self.webhook_url,
                json={"username": notification.title, "content": chunk},
            )
