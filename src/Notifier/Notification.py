from dataclasses import dataclass

from src.models import Study


@dataclass(frozen=True)
class Notification:
    """Der Inhalt einer Benachrichtigung, unabhaengig vom Zielkanal.

    Der Text wird hier einmal aufgebaut; die Notifier rendern daraus nur noch
    ihr jeweiliges Transportformat.
    """

    title: str
    compensation: str
    description: str
    link: str

    @staticmethod
    def from_study(study: Study) -> "Notification":
        return Notification(
            title=study.title,
            compensation=study.compensation,
            description=study.short_description,
            link=study.link,
        )

    @property
    def body(self) -> str:
        return (
            f" **Bezahlung:** {self.compensation}\n"
            f" **Beschreibung:** {self.description}\n"
            f" **Link:** {self.link}"
        )
