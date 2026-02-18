from app.definitions.location import LocationBase
from app.definitions.location_path import LocationPath
from app.definitions.lookup_key import LookupKey
from app.definitions.survey_type import SurveyType


class OutputGenerator:
    def __init__(self, location_service: LocationBase):
        self._location_service = location_service

    def generate_outputs(self, survey_type: SurveyType, survey_id: str) -> LocationPath:
        if survey_type == SurveyType.SEFT:
            if survey_id == "141":
                return {
                    "location": LookupKey.NS2,
                    "path": f"s&e/ASHE/{self.get_ashe_folder()}"
                }

    def get_ashe_folder(self) -> str:
        if self._location_service.is_prod_env():
            return "ASHE_Python_Submissions"
        else:
            return "ASHE_Python_Submissions_TEST"
