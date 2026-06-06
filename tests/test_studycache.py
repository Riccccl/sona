import json
from datetime import datetime
from pathlib import Path

from src.models import Study
from src.StudyCache import StudyCache


def test_from_file_missing_returns_empty_cache(tmp_path: Path) -> None:
    cache = StudyCache.from_file(str(tmp_path / "nonexistent.json"))
    assert cache.get_studies() == []
    assert isinstance(cache.get_date_created(), datetime)


def test_roundtrip_preserves_studies(tmp_path: Path, sample_study: Study) -> None:
    original = StudyCache(date_created=datetime(2024, 6, 1, 12, 0, 0), studies=[sample_study])
    path = str(tmp_path / "cache.json")
    original.to_file(path)
    loaded = StudyCache.from_file(path)
    assert len(loaded.get_studies()) == 1
    s = loaded.get_studies()[0]
    assert s.title == sample_study.title
    assert s.compensation == sample_study.compensation
    assert s.short_description == sample_study.short_description
    assert s.link == sample_study.link


def test_roundtrip_preserves_date(tmp_path: Path) -> None:
    t = datetime(2024, 3, 15, 8, 30, 0)
    cache = StudyCache(date_created=t, studies=[])
    path = str(tmp_path / "cache.json")
    cache.to_file(path)
    loaded = StudyCache.from_file(path)
    assert loaded.get_date_created() == t


def test_from_file_corrupt_json_returns_empty(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("not valid json", encoding="utf-8")
    cache = StudyCache.from_file(str(path))
    assert cache.get_studies() == []


def test_from_file_missing_date_returns_empty(tmp_path: Path) -> None:
    path = tmp_path / "nodatecache.json"
    path.write_text(json.dumps({"studies": []}), encoding="utf-8")
    cache = StudyCache.from_file(str(path))
    assert cache.get_studies() == []


def test_empty_cache_has_no_studies() -> None:
    cache = StudyCache()
    assert cache.get_studies() == []


def test_to_file_creates_file(tmp_path: Path) -> None:
    path = str(tmp_path / "out.json")
    StudyCache().to_file(path)
    assert Path(path).exists()
