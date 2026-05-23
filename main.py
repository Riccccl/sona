from time import sleep
from src.discord_notifier import send_notification
from src.scraper import scrape_studies
from src.text_formatter import format_study_info
from src.differ import get_new_studies
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


    scraped_studies = scrape_studies(username, password, website_link, headless=True)
    studies = get_new_studies(scraped_studies)
    if not studies:
        print("Keine neuen Studien verfügbar.")
        return

    for study in studies:
        
        message: str = format_study_info(study)
        sleep(2)  # Optional: Vermeiden von Rate-Limiting durch Discord
        send_notification(message, webhook_url)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e
    #print(f"An error occurred: {e}")
