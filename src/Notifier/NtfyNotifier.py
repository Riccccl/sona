from email.header import Header

from .HttpNotifier import HttpNotifier
from .Notification import Notification


class NtfyNotifier(HttpNotifier):
    name = "ntfy"

    def __init__(self, ntfy_webhook_url: str) -> None:
        self.webhook_url = ntfy_webhook_url

    def send(self, notification: Notification) -> None:
        self._post(
            self.webhook_url,
            # http.client kodiert str-Bodies und Header als latin-1; Bytes bzw.
            # ein RFC-2047-Header halten Sonderzeichen wie - und EUR heil.
            data=notification.body.encode("utf-8"),
            headers={"Title": Header(notification.title, "utf-8").encode()},
        )
