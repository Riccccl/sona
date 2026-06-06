from datetime import datetime

import pytest

from src.models import Study
from src.StudyCache import StudyCache


@pytest.fixture
def sample_study() -> Study:
    return Study(
        title="Test Study",
        compensation="0.5 VP-Stunden",
        short_description="Online",
        link="https://psywue.sona-systems.com/exp.aspx?experiment_id=1",
    )


@pytest.fixture
def another_study() -> Study:
    return Study(
        title="Another Study",
        compensation="1.0 VPH",
        short_description="Lab",
        link="https://psywue.sona-systems.com/exp.aspx?experiment_id=2",
    )


@pytest.fixture
def sample_cache(sample_study: Study) -> StudyCache:
    return StudyCache(
        date_created=datetime(2024, 1, 1, 10, 0, 0),
        studies=[sample_study],
    )
