from typing import ClassVar

import requests

from .INotifier import INotifier


class HttpNotifier(INotifier):
    """Basis fuer Kanaele, die per HTTP zustellen.

    Buendelt Timeout und Statuspruefung an einer Stelle, damit die konkreten
    Notifier nur noch ihr Payload-Format bauen muessen.
    """

    TIMEOUT: ClassVar[float] = 10.0

    def _post(self, url: str, **kwargs) -> requests.Response:
        """Sendet die Anfrage und wirft bei einem Fehlerstatus."""
        response = requests.post(url=url, timeout=self.TIMEOUT, **kwargs)
        response.raise_for_status()
        return response
