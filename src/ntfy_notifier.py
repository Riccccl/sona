import requests
from src.models import Study

SONA_BASE_URL = "https://psywue.sona-systems.com"


def send_ntfy_notification(study: Study, ntfy_url: str) -> None:
    body = f"{study.compensation}\n{study.short_description}"
    actions = f"view, Studie öffnen, {study.link}; view, SONA Übersicht, {SONA_BASE_URL}"

    try:
        r = requests.post(
            url=ntfy_url,
            data=body.encode("utf-8"),
            headers={
                "Title": study.title,
                "Tags": "+1,books",
                "Priority": "default",
                "Click": study.link,
                "Actions": actions,
            },
        )
        if r.status_code != 200:
            raise RuntimeError(f"Failed to send ntfy notification: {r.status_code} {r.text}")
    except Exception as e:
        raise RuntimeError(f"Failed to send ntfy notification: {e}")
