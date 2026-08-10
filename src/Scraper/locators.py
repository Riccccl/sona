from dataclasses import dataclass


@dataclass
class Locators:
    AVAILABLE_STUDIES: str = "#lnkStudySignupLink"
    PARTICIPATED_STUDIES: str = "#ctl00_ContentPlaceHolder1_lnkMyScheduleAndCredits3"

    AUTH_BUTTON: str = "#ctl00_ContentPlaceHolder1_default_auth_button"

    PARTICIPANT_BUTTON: str = "#ctl00_ContentPlaceHolder1_pnlShowOptionS"

    AVAILABLE_STUDIES_TABLE: str = 'table.table.table-bordered.table-striped[aria-label="Studies with available timeslots"]'

    PARTICIPATED_STUDIES_TABLE: str = "table.table-bordered.table-striped.table-condensed.cf"

    TABLE_BODY_ROW: str = "tbody tr"

    TABLE_CELL: str = "td"


LOCATORS = Locators()