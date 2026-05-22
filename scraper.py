from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright, Locator
from models import Study

class Scraper:

    @staticmethod
    def scrape_studies(username: str, password: str, website_link: str) -> list[Study]:

        with sync_playwright() as playwright:
            browser: Browser = playwright.chromium.launch(headless=False)
            context: BrowserContext = browser.new_context()
            page: Page = context.new_page()
            page.goto(website_link)
        
            page.get_by_label('Benutzername').fill(username)
            page.get_by_label('Passwort').fill(password)
            page.click("#ctl00_ContentPlaceHolder1_default_auth_button")
            page.click("#ctl00_ContentPlaceHolder1_pnlShowOptionS")
            page.click("#lnkStudySignupLink")
            table: Locator = page.locator('table.table.table-bordered.table-striped[aria-label="Studies with available timeslots"]')
            table.wait_for()  # sicherstellen, dass die Tabelle existiert
            rows: list[Locator] = table.locator('tbody tr').all()
            studies: list[Study] = []
            for row in rows:
                cells = row.locator('td').all()
                if len(cells) >= 3:
                    timeslot: str = cells[0].inner_text()
                    title: str = cells[1].locator('p strong').inner_text()
                    compensation: str = cells[1].locator('span[id*="LabelCredits"]').inner_text()
                    short_description: str = cells[1].locator('span[id*="LabelStudyType"]').inner_text()
                    link = cells[1].locator('a').get_attribute('href')
                    eligibility: str = cells[2].inner_text()

                    study = Study(
                        title=title,
                        compensation=compensation,
                        short_description=short_description,
                        link = website_link + link,
                    )
                    studies.append(study)

            return studies