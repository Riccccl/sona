from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright, Locator
from models import Study
from scraper import Scraper
from discord_notifier import send_notification
from dotenv import load_dotenv
from os import getenv
load_dotenv()

username: str = getenv("SONA_USERNAME")
password: str = getenv("SONA_PASSWORD")
webhook_url: str = getenv("DISCORD_WEBHOOK_URL")
website_link: str = "https://psywue.sona-systems.com/"

def main() -> None:
    #studies = Scraper.scrape_studies(username, password, website_link)
    send_notification("Hallo aus dem Script", webhook_url)
    pass

if __name__ == "__main__":
    main()