import time

import requests

from src.models import Study

from .INotifier import INotifier


class DiscordNotifier(INotifier):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    @staticmethod
    def _create_payload_from_study(study: Study) -> dict:
        return {
            "username": f"{study.title}",
            "content":  f" **Bezahlung:** {study.compensation}\n"
                        f" **Beschreibung:** {study.short_description}\n"
                        f" **Link:** {study.link}"
        }

    def send_study_notification(self, studies: list[Study]) -> None:
        for study in studies:
            payload = self._create_payload_from_study(study)
            try:
                response = requests.post(url=self.webhook_url, json=payload)
                
                print(f"{response.status_code} : {response.text if response.text else 'No response text'}")
                time.sleep(1)  # Sleep to avoid hitting rate limits
            except Exception as e:  # noqa: BLE001
                print(f"{e.__class__.__name__}: Failed to send notification for study '{study.title}': {e}")
