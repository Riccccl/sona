from src.models import Study


def test_gives_vph_true() -> None:
    study = Study(title="S", compensation="1.0 VPH", short_description="", link="")
    assert study.gives_vph is True


def test_gives_vph_case_insensitive() -> None:
    study = Study(title="S", compensation="1.0 vph", short_description="", link="")
    assert study.gives_vph is True


def test_gives_vph_false() -> None:
    study = Study(title="S", compensation="0.5 VP-Stunden", short_description="", link="")
    assert study.gives_vph is False


def test_study_str_contains_title() -> None:
    study = Study(title="My Study", compensation="1.0 VPH", short_description="Online", link="http://example.com")
    assert "My Study" in str(study)


def test_study_str_contains_all_fields() -> None:
    study = Study(title="My Study", compensation="1.0 VPH", short_description="Online", link="http://example.com")
    result = str(study)
    assert "1.0 VPH" in result
    assert "Online" in result
    assert "http://example.com" in result
