from os import getenv
from time import sleep

from dotenv import load_dotenv

from src.differ import Differ
from src.discord_notifier import send_study_notification
from src.models import Study
from src.scraper import Scraper
from src.StudyCache import StudyCache

load_dotenv()


def main() -> None:
    username = getenv("SONA_USERNAME") or ""
    password = getenv("SONA_PASSWORD") or ""
    webhook_url = getenv("DISCORD_WEBHOOK_URL") or ""
    if not all([username, password, webhook_url]):
        raise ValueError("Missing required environment variables. Please check your .env file or environment secrets.")
    website_link: str = "https://psywue.sona-systems.com/"
    cached_studies_file: str = "cached_studies.json"

    scraper = Scraper(username, password, website_link, headless=True)
    available_studies: list[Study] = scraper.scrape_available_studies()
    new_study_cache = StudyCache(studies=available_studies)
    old_study_cache = StudyCache.from_file(cached_studies_file)

    differ = Differ(old_study_cache, new_study_cache)
    print(f"Found {len(differ.get_new_studies())} new studies.")
    for study in differ.get_new_studies():
        print(f"Sending notification for study: {study.title}")
        send_study_notification(study, webhook_url)
        sleep(1)  # avoid hitting Discord webhook rate limits
    print(f"Time since last check: {differ.get_time_difference()}")

    new_study_cache.to_file(cached_studies_file)


if __name__ == "__main__":
    main()
