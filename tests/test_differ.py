from datetime import datetime, timedelta

from src.differ import Differ
from src.models import Study
from src.StudyCache import StudyCache


def _cache(studies: list[Study], dt: datetime | None = None) -> StudyCache:
    return StudyCache(date_created=dt or datetime(2024, 1, 1), studies=studies)


def _study(link: str) -> Study:
    return Study(title="S", compensation="0.5 VP-Stunden", short_description="Online", link=link)


def test_no_new_studies() -> None:
    study = _study("http://example.com/1")
    differ = Differ(_cache([study]), _cache([study]))
    assert differ.get_new_studies() == []


def test_one_new_study() -> None:
    old = _cache([_study("http://example.com/1")])
    new = _cache([_study("http://example.com/1"), _study("http://example.com/2")])
    differ = Differ(old, new)
    result = differ.get_new_studies()
    assert len(result) == 1
    assert result[0].link == "http://example.com/2"


def test_all_new_when_old_is_empty() -> None:
    new = _cache([_study("http://example.com/1"), _study("http://example.com/2")])
    differ = Differ(_cache([]), new)
    assert len(differ.get_new_studies()) == 2


def test_removed_study_not_returned() -> None:
    old = _cache([_study("http://example.com/1"), _study("http://example.com/2")])
    new = _cache([_study("http://example.com/1")])
    differ = Differ(old, new)
    assert differ.get_new_studies() == []


def test_time_difference() -> None:
    t1 = datetime(2024, 1, 1, 10, 0)
    t2 = datetime(2024, 1, 1, 11, 30)
    differ = Differ(_cache([], t1), _cache([], t2))
    assert differ.get_time_difference() == timedelta(hours=1, minutes=30)
