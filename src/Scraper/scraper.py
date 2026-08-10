from playwright.sync_api import Browser, BrowserContext, Locator, Page, sync_playwright

from src.models import Study

from .locators import LOCATORS


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
            page.goto(self.website_link)
            self._anmeldungsdialog_bedienen(page)
            page.click(LOCATORS.PARTICIPATED_STUDIES)
            studies: list[Study] = self._extract_participated_studies_from_table(page)
            return studies

    def scrape_available_studies(self) -> list[Study]:
        with sync_playwright() as playwright:
            browser: Browser = playwright.chromium.launch(headless=self.headless)
            context: BrowserContext = browser.new_context()
            page: Page = context.new_page()
            page.goto(self.website_link)

            self._anmeldungsdialog_bedienen(page)

            page.click(LOCATORS.AVAILABLE_STUDIES)
            studies: list[Study] = self._extract_available_studies_from_table(page)
            return studies

    def extract_rows_from_table(self, page: Page, table_locator: str) -> list[Locator]:
        table: Locator = page.locator(table_locator)
        table.wait_for()  # sicherstellen, dass die Tabelle existiert
        rows: list[Locator] = table.locator(LOCATORS.TABLE_BODY_ROW).all()
        return rows
    
    def _extract_available_studies_from_table(self, page: Page) -> list[Study]:
        rows: list[Locator] = self.extract_rows_from_table(page, LOCATORS.AVAILABLE_STUDIES_TABLE)
        studies: list[Study] = []
        for row in rows:
            cells = row.locator(LOCATORS.TABLE_CELL).all()
            if len(cells) >= 3:
                #timeslot: str = cells[0].inner_text()
                title: str = cells[1].locator('p strong').inner_text()
                compensation: str = cells[1].locator('span[id*="LabelCredits"]').inner_text()
                short_description: str = cells[1].locator('span[id*="LabelStudyType"]').inner_text()
                link = cells[1].locator('a').get_attribute('href')
                #eligibility: str = cells[2].inner_text()

                study = Study(
                    title=title,
                    compensation=compensation,
                    short_description=short_description,
                    link = self.website_link + link if link else self.website_link,
                )
                studies.append(study)
        return studies

    def _extract_participated_studies_from_table(self, page: Page) -> list[Study]:
        rows: list[Locator] = self.extract_rows_from_table(page, LOCATORS.PARTICIPATED_STUDIES_TABLE)
        studies: list[Study] = []
        for row in rows:
            cells = row.locator(LOCATORS.TABLE_CELL).all()
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
        page.click(LOCATORS.AUTH_BUTTON)
        if page.is_visible(LOCATORS.PARTICIPANT_BUTTON):
                page.click(LOCATORS.PARTICIPANT_BUTTON)
