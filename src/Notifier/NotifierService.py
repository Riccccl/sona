from src.models import Study

from .INotifier import INotifier


class NotifierService:
    def __init__(self, notifier: "INotifier"):
        self.notifier = notifier

    def send_study_notification(self, studies: list[Study]) -> None:
        self.notifier.send_study_notification(studies)