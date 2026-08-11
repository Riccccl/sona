import logging

from .INotifier import INotifier
from .Notification import Notification

log = logging.getLogger(__name__)


class ConsoleNotifier(INotifier):
    """Gibt Benachrichtigungen nur aus - fuer Trockenlaeufe ohne Netzwerk."""

    name = "console"

    def send(self, notification: Notification) -> None:
        log.info("%s\n%s", notification.title, notification.body)
