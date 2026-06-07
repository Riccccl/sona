import os
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright, Locator
from src.models import Study


class Scraper:
    def __init__(self, username: str, password: str, website_link: str, headless: bool = True) -> None:
        self.username = username
        self.password = password
        self.website_link = website_link
        self.headless = headless

    def scrape_participated_studies(self) -> list[Study]:
        with sync_playwright() as playwright:
            browser: Browser = playwright.chromium.launch(headless=self.headless)
            context: BrowserContext = browser.new_context()
            page: Page = context.new_page()
            try:
                page.goto(self.website_link)
                self._anmeldungsdialog_bedienen(page)
                self._in_participated_studies_navigieren(page)
                return self._extract_participated_studies_from_table(page)
            except Exception:
                os.makedirs("screenshots", exist_ok=True)
                page.screenshot(path="screenshots/error_participated_studies.png", full_page=True)
                raise

    def scrape_available_studies(self) -> list[Study]:
        with sync_playwright() as playwright:
            browser: Browser = playwright.chromium.launch(headless=self.headless)
            context: BrowserContext = browser.new_context()
            page: Page = context.new_page()
            try:
                page.goto(self.website_link)
                self._anmeldungsdialog_bedienen(page)
                self._in_available_studies_navigieren(page)
                return self._extract_available_studies_from_table(page)
            except Exception:
                os.makedirs("screenshots", exist_ok=True)
                page.screenshot(path="screenshots/error_available_studies.png", full_page=True)
                raise
    
    def _extract_available_studies_from_table(self, page: Page) -> list[Study]:
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
                    link = self.website_link + link,
                )
                studies.append(study)
        return studies

    def _extract_participated_studies_from_table(self, page: Page) -> list[Study]:
        table: Locator = page.locator('table.table-bordered.table-striped.table-condensed.cf')
        table.wait_for()  # sicherstellen, dass die Tabelle existiert
        rows: list[Locator] = table.locator('tbody tr').all()
        studies: list[Study] = []
        for row in rows:
            cells = row.locator('td').all()
            first_cell: Locator = cells[0]
            title: str = first_cell.locator('a[id^="ctl00_ContentPlaceHolder1_repStudySignUps_"][id$="_HyperLinkStudyName"]').inner_text() 
            compensation: str = first_cell.locator('span[id^="ctl00_ContentPlaceHolder1_repStudySignUps_"][id$="_LabelCredits"]').inner_text()
            short_description: str = ""
            link = ""
            study = Study(
                title=title,
                compensation=compensation,
                short_description=short_description,
                link = self.website_link + link,
            )
            studies.append(study)
        return studies

    def _anmeldungsdialog_bedienen(self, page: Page) -> None:
        page.get_by_label('Benutzername').fill(self.username)
        page.get_by_label('Passwort').fill(self.password)
        page.click("#ctl00_ContentPlaceHolder1_default_auth_button")
        if page.is_visible("#ctl00_ContentPlaceHolder1_pnlShowOptionS"):
                page.click("#ctl00_ContentPlaceHolder1_pnlShowOptionS")

    def _in_available_studies_navigieren(self, page: Page) -> None:
        page.click("#lnkStudySignupLink")

    def _in_participated_studies_navigieren(self, page: Page) -> None:
        page.click("#ctl00_ContentPlaceHolder1_lnkMyScheduleAndCredits3")