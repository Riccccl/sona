from src.models import Study


def format_study_info(study: Study) -> str:
    return f"**{study.title}**\n" #\
           #f"Beschreibung: {study.short_description}\n" \
           #f"Bezahlung: {study.compensation}\n" \
           #f"Link: {study.link}\n"