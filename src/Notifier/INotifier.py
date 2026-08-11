from abc import ABC, abstractmethod
from typing import ClassVar

from .Notification import Notification


class INotifier(ABC):
    """Ein Zielkanal fuer Benachrichtigungen.

    Implementierungen kuemmern sich ausschliesslich um das Transportformat.
    Die Schleife ueber die Studien, das Rate-Limit und die Fehlerbehandlung
    liegen im NotifierService - Fehler werden hier deshalb bewusst nach oben
    geworfen statt geschluckt.
    """

    name: ClassVar[str]

    @abstractmethod
    def send(self, notification: Notification) -> None: ...
