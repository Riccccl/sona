import logging
from collections.abc import Callable
from os import getenv

from src.secrets_provider import SecretsProvider

from .ConsoleNotifier import ConsoleNotifier
from .DiscordNotifier import DiscordNotifier
from .INotifier import INotifier
from .NtfyNotifier import NtfyNotifier

log = logging.getLogger(__name__)

DEFAULT_NOTIFIERS = "ntfy"

# Ein neuer Kanal braucht genau zwei Dinge: eine INotifier-Implementierung und
# eine Zeile hier. Umschalten im Betrieb laeuft ueber die Umgebungsvariable
# NOTIFIERS und kommt ohne Codeaenderung aus.
NOTIFIER_REGISTRY: dict[str, Callable[[SecretsProvider], INotifier]] = {
    ConsoleNotifier.name: lambda _: ConsoleNotifier(),
    DiscordNotifier.name: lambda secrets: DiscordNotifier(secrets.discord_webhook_url),
    NtfyNotifier.name: lambda secrets: NtfyNotifier(secrets.ntfy_webhook_url),
}


def build_notifiers(secrets: SecretsProvider, enabled: str | None = None) -> list[INotifier]:
    """Baut die aktiven Notifier.

    :param enabled: kommaseparierte Kanalnamen; ohne Angabe wird die Umgebungs-
        variable NOTIFIERS gelesen.
    :raises ValueError: wenn ein Kanalname nicht in der Registry steht.
    """
    if enabled is None:
        enabled = getenv("NOTIFIERS") or DEFAULT_NOTIFIERS

    # dict.fromkeys entfernt Duplikate und haelt die Reihenfolge stabil.
    names = list(dict.fromkeys(name.strip().lower() for name in enabled.split(",") if name.strip()))

    notifiers: list[INotifier] = []
    for name in names:
        factory = NOTIFIER_REGISTRY.get(name)
        if factory is None:
            raise ValueError(
                f"Unbekannter Notifier: '{name}'. "
                f"Gueltig sind: {', '.join(sorted(NOTIFIER_REGISTRY))}."
            )
        # Secrets werden erst hier aufgeloest (SecretsProvider ist lazy), damit
        # ein nicht aktivierter Kanal keine Credentials verlangt.
        notifiers.append(factory(secrets))

    log.info("Aktive Notifier: %s", ", ".join(n.name for n in notifiers) or "keine")
    return notifiers
