
from os import getenv

from dotenv import load_dotenv

load_dotenv()

class SecretsProvider:

    def __init__(self, 
                 discord_webhook_url: str | None = None, 
                 ntfy_webhook_url: str | None = None, 
                 sona_username: str | None = None, 
                 sona_password: str | None = None):
        self.discord_webhook_url: str= self._get_secret("DISCORD_WEBHOOK_URL") if discord_webhook_url is None else discord_webhook_url
        self.ntfy_webhook_url: str= self._get_secret("NTFY_WEBHOOK_URL") if ntfy_webhook_url is None else ntfy_webhook_url
        self.sona_username: str= self._get_secret("SONA_USERNAME") if sona_username is None else sona_username
        self.sona_password: str = self._get_secret("SONA_PASSWORD") if sona_password is None else sona_password

    def _get_secret(self, secret_name: str) -> str:
        """Retrieve a secret from environment variables or .env file.
        
        :raises: ValueError if the secret is not found.
        """
        secret_value = getenv(secret_name)
        if secret_value is None:
            raise ValueError(f"Missing required environment variable: {secret_name}. Please check your .env file or environment secrets.")
        return secret_value

