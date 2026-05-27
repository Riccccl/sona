

from datetime import datetime

from src.StudyCache import StudyCache
from src.models import Study


class Differ:

    def __init__(self, old_study_cache: StudyCache, new_study_cache: StudyCache) -> None:
        self.old_study_cache = old_study_cache
        self.new_study_cache = new_study_cache

    def get_time_difference(self) -> datetime:
        old_study_date = self.old_study_cache.get_date_created()
        new_study_date = self.new_study_cache.get_date_created()
        return new_study_date - old_study_date
    
    def get_new_studies(self) -> list[Study]:
        old_studies = self.old_study_cache.get_studies()
        new_studies = self.new_study_cache.get_studies()
        
        old_links = {study.link for study in old_studies}
        return [study for study in new_studies if study.link not in old_links]