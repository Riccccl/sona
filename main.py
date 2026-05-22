from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright, Locator
from models import Study
from scraper import Scraper
from discord_notifier import send_notification
from dotenv import load_dotenv
from os import getenv
load_dotenv()

def main() -> None:
    #if not all([getenv("SONA_USERNAME"), getenv("SONA_PASSWORD"), getenv("DISCORD_WEBHOOK_URL")]):
        #pass
        #raise ValueError("Missing required environment variables. Please check your .env file or environment secrets.")
    #username: str = getenv("SONA_USERNAME")
    #password: str = getenv("SONA_PASSWORD")
    webhook_url: str = getenv("DISCORD_WEBHOOK_URL")
    #website_link: str = "https://psywue.sona-systems.com/"


    #studies = Scraper.scrape_studies(username, password, website_link)
    send_notification("Hallo aus dem Script", webhook_url)

if __name__ == "__main__":
    main()