from models import Study
import requests


def send_notification(message: str, webhook_url: str) -> None:
    try:
        payload = {
            "content": message
        }
        requests.post(url=webhook_url, json=payload)
    except Exception as e:
        print(f"Error sending notification: {e}")
        raise e