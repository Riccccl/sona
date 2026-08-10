from abc import ABC, abstractmethod

from src.models import Study


class INotifier(ABC):
    @abstractmethod
    def send_study_notification(self, studies: list[Study]) -> None: ...
