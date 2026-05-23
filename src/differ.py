from src.models import Study
from json import dump, load

cache_file = "cached_studies.json"


def _write_studies_to_file(studies: list[Study], filename: str) -> None:
    if not filename.endswith(".json"):
        raise ValueError("Filename must end with .json")
    with open(filename, "w", encoding="utf-8") as f:
        dump([study.__dict__ for study in studies], f, ensure_ascii=False, indent=2)

def _read_studies_from_file(filename: str) -> list[Study]:
    if not filename.endswith(".json"):
        raise ValueError("Filename must end with .json")
    with open(filename, "r", encoding="utf-8") as f:
        data = load(f)
        return [Study(**item) for item in data]

def get_differences(old_studies: list[Study], new_studies: list[Study]) -> list[Study]:
    old_links = {study.link for study in old_studies}
    return [study for study in new_studies if study.link not in old_links]

def get_new_studies(new_studies: list[Study]) -> list[Study]:
    try:
        old_studies = _read_studies_from_file(cache_file)
    except FileNotFoundError:
        old_studies = []
    new_studies = new_studies or []
    differences = get_differences(old_studies, new_studies)
    _write_studies_to_file(new_studies, cache_file)
    return differences
