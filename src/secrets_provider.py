
from functools import cached_property
from os import getenv

from dotenv import load_dotenv

load_dotenv()

class SecretsProvider:
    """Provides secrets from environment variables or .env file.

    Secrets are resolved lazily: a missing environment variable only raises
    once the corresponding attribute is actually accessed.
    """

    def __init__(self,
                 discord_webhook_url: str | None = None,
                 ntfy_webhook_url: str | None = None,
                 sona_username: str | None = None,
                 sona_password: str | None = None):
        if discord_webhook_url is not None:
            self.discord_webhook_url = discord_webhook_url
        if ntfy_webhook_url is not None:
            self.ntfy_webhook_url = ntfy_webhook_url
        if sona_username is not None:
            self.sona_username = sona_username
        if sona_password is not None:
            self.sona_password = sona_password

    @cached_property
    def discord_webhook_url(self) -> str:
        return self._get_secret("DISCORD_WEBHOOK_URL")

    @cached_property
    def ntfy_webhook_url(self) -> str:
        return self._get_secret("NTFY_WEBHOOK_URL")

    @cached_property
    def sona_username(self) -> str:
        return self._get_secret("SONA_USERNAME")

    @cached_property
    def sona_password(self) -> str:
        return self._get_secret("SONA_PASSWORD")

    def _get_secret(self, secret_name: str) -> str:
        """Retrieve a secret from environment variables or .env file.

        :raises: ValueError if the secret is not found or empty.
        """
        secret_value = getenv(secret_name)
        if not secret_value:
            raise ValueError(f"Missing required environment variable: {secret_name}. Please check your .env file or environment secrets.")
        return secret_value
