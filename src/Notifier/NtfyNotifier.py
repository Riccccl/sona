import time

import requests

from src.models import Study

from .INotifier import INotifier


class NtfyNotifier(INotifier):
    def __init__(self, ntfy_webhook_url: str):
        self.webhook_url = ntfy_webhook_url

    @staticmethod
    def _create_payload_from_study(study: Study) -> dict:
        return {
            "data": f"**Bezahlung:** {study.compensation}\n**Beschreibung:** {study.short_description}\n**Link:** {study.link}",
            "headers": {"Title": f"{study.title}"}
        }

    def send_study_notification(self, studies: list[Study]) -> None:
        for study in studies:
            payload: dict = self._create_payload_from_study(study)
            try:
                response = requests.post(url=self.webhook_url, **payload)
                
                print(f"{response.status_code} : {response.text if response.text else 'No response text'}")
                time.sleep(1)  # Sleep to avoid hitting rate limits
            except Exception as e:  # noqa: BLE001
                print(f"{e.__class__.__name__}: Failed to send notification for study '{study.title}': {e}")