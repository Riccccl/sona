import logging

from src.differ import Differ
from src.models import Study
from src.Notifier.NotifierFactory import build_notifiers
from src.Notifier.NotifierService import NotifierService
from src.Scraper.scraper import Scraper
from src.secrets_provider import SecretsProvider
from src.StudyCache import StudyCache

log = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    secrets = SecretsProvider()
    website_link: str = "https://psywue.sona-systems.com/"
    cached_studies_file: str = "cached_studies.json"

    scraper = Scraper(secrets.sona_username, secrets.sona_password, website_link, headless=True)
    available_studies: list[Study] = scraper.scrape_available_studies()
    newStudyCache = StudyCache(studies=available_studies)
    oldStudyCache = StudyCache.from_file(cached_studies_file)

    differ = Differ(oldStudyCache, newStudyCache)
    new_studies: list[Study] = differ.get_new_studies()
    log.info("Found %d new studies.", len(new_studies))

    undelivered: list[Study] = NotifierService(build_notifiers(secrets)).send_study_notification(
        new_studies
    )

    log.info("Time since last check: %s", differ.get_time_difference())

    if undelivered:
        # Nicht zugestellte Studien bleiben aus dem Cache draussen, damit der
        # naechste Lauf sie erneut als neu erkennt und nachmeldet.
        undelivered_links = {study.link for study in undelivered}
        newStudyCache.studies = [
            study for study in newStudyCache.studies if study.link not in undelivered_links
        ]

    newStudyCache.to_file(cached_studies_file)

    if undelivered:
        raise SystemExit(
            f"{len(undelivered)} von {len(new_studies)} Benachrichtigungen konnten nicht "
            f"zugestellt werden - sie werden im naechsten Lauf erneut versucht."
        )


if __name__ == "__main__":
    main()
