
from dotenv import load_dotenv

from src.differ import Differ
from src.models import Study
from src.Notifier.ConsoleNotifier import ConsoleNotifier
from src.Notifier.DiscordNotifier import DiscordNotifier
from src.Notifier.NotifierService import NotifierService
from src.Notifier.NtfyNotifier import NtfyNotifier
from src.Scraper.scraper import Scraper
from src.secrets_provider import SecretsProvider
from src.StudyCache import StudyCache

load_dotenv()

def main() -> None:
    secrets = SecretsProvider()
    website_link: str = "https://psywue.sona-systems.com/"
    cached_studies_file: str = "cached_studies.json"

    scraper = Scraper(secrets.sona_username, secrets.sona_password, website_link, headless=True)
    available_studies: list[Study] = scraper.scrape_available_studies() 
    newStudyCache = StudyCache(studies=available_studies)
    oldStudyCache = StudyCache.from_file(cached_studies_file)

    differ = Differ(oldStudyCache, newStudyCache)
    new_studies: list[Study] = differ.get_new_studies()
    print(f"Found {len(new_studies)} new studies.")

    discord_notifier = DiscordNotifier(secrets.discord_webhook_url)
    console_notifier = ConsoleNotifier()
    ntfy_notifier = NtfyNotifier(secrets.ntfy_webhook_url)

    NotifierService(discord_notifier).send_study_notification(new_studies)

    print(f"Time since last check: {differ.get_time_difference()}")

    newStudyCache.to_file(cached_studies_file)

if __name__ == "__main__":
        main()
    #print(f"An error occurred: {e}")
