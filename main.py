from time import sleep
from src.differ import Differ
from src.discord_notifier import send_study_notification, send_error_notification
from src.models import Study
from src.scraper import Scraper
from src.StudyCache import StudyCache
from dotenv import load_dotenv
from os import getenv
load_dotenv()

def main() -> None:
    if not all([getenv("SONA_USERNAME"), getenv("SONA_PASSWORD"), getenv("DISCORD_WEBHOOK_URL")]):
        raise ValueError("Missing required environment variables. Please check your .env file or environment secrets.")

    username: str = getenv("SONA_USERNAME")
    password: str = getenv("SONA_PASSWORD")
    webhook_url: str = getenv("DISCORD_WEBHOOK_URL")
    website_link: str = "https://psywue.sona-systems.com/"
    cached_studies_file: str = "cached_studies.json"

    scraper = Scraper(username, password, website_link, headless=True)
    available_studies: list[Study] = scraper.scrape_available_studies() 
    newStudyCache = StudyCache(studies=available_studies)
    oldStudyCache = StudyCache.from_file(cached_studies_file)

    differ = Differ(oldStudyCache, newStudyCache)
    print(f"Found {len(differ.get_new_studies())} new studies.")
    for study in differ.get_new_studies():
        print(f"Sending notification for study: {study.title}")
        send_study_notification(study, webhook_url)
        sleep(1)  # Sleep to avoid hitting rate limits
    print(f"Time since last check: {differ.get_time_difference()}")

    newStudyCache.to_file(cached_studies_file)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        webhook_url = getenv("DISCORD_WEBHOOK_URL")
        if webhook_url:
            send_error_notification(e, webhook_url)
        raise
