import logging
import time
from collections.abc import Sequence

from src.models import Study

from .INotifier import INotifier
from .Notification import Notification

log = logging.getLogger(__name__)


class NotifierService:
    """Verteilt Benachrichtigungen an alle konfigurierten Kanaele.

    Uebernimmt das, was sonst jeder Notifier doppeln muesste: die Schleife ueber
    die Studien, das Rate-Limit und die Fehlerisolierung. Ein ausgefallener Kanal
    blockiert die uebrigen nicht.
    """

    def __init__(self, notifiers: Sequence[INotifier], rate_limit_seconds: float = 1.0) -> None:
        self.notifiers = list(notifiers)
        self.rate_limit_seconds = rate_limit_seconds

    def send_study_notification(self, studies: list[Study]) -> list[Study]:
        """Meldet jede Studie an alle Kanaele.

        :return: die Studien, die von keinem einzigen Kanal zugestellt wurden.
        """
        if not self.notifiers:
            log.warning("Kein Notifier konfiguriert - %d Studien werden nicht gemeldet.", len(studies))
            return list(studies)

        undelivered: list[Study] = []
        for index, study in enumerate(studies):
            if not self._send_to_all(Notification.from_study(study)):
                undelivered.append(study)
            if index < len(studies) - 1:
                time.sleep(self.rate_limit_seconds)  # Rate-Limits der Webhooks schonen
        return undelivered

    def _send_to_all(self, notification: Notification) -> bool:
        """:return: True, sobald mindestens ein Kanal zugestellt hat."""
        delivered = False
        for notifier in self.notifiers:
            try:
                notifier.send(notification)
                delivered = True
                log.info("'%s' ueber %s gemeldet.", notification.title, notifier.name)
            except Exception:  # noqa: BLE001
                log.exception(
                    "Notifier '%s' konnte '%s' nicht zustellen.", notifier.name, notification.title
                )
        return delivered
