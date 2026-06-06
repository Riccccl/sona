from __future__ import annotations

from datetime import datetime
from json import JSONDecodeError, dump, load

from src.models import Study


class StudyCache:
    def __init__(self, date_created: datetime = datetime.now(), studies: list[Study] | None = None) -> None:
        self.date_created: datetime = date_created
        self.studies: list[Study] = studies or []

    @staticmethod
    def from_file(filename: str) -> StudyCache:
        try:
            with open(filename, encoding="utf-8") as f:
                data: dict = load(f)
                raw_date = data.get("date_created")
                if raw_date is None:
                    raise ValueError("Missing date_created field")
                return StudyCache(
                    date_created=datetime.fromisoformat(raw_date),
                    studies=[Study(**item) for item in data.get("studies", [])],
                )
        except (FileNotFoundError, KeyError, ValueError, JSONDecodeError):
            return StudyCache(date_created=datetime.now(), studies=[])

    def to_file(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            dump({
                "date_created": self.date_created.isoformat(),
                "studies": [study.__dict__ for study in self.studies]
            }, f, ensure_ascii=False, indent=2)

    def get_date_created(self) -> datetime:
        return self.date_created

    def get_studies(self) -> list[Study]:
        return self.studies
