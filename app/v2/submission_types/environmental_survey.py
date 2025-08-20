from typing import Final

from app.v2.definitions.config_schema import File
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.path_helper import get_ns5_path
from app.v2.definitions.context import BusinessSurveyContext
from app.v2.submission_types.bases.survey_submission import SurveySubmission

# file types
_INDEX: Final[str] = "index"
_RECEIPT: Final[str] = "receipt"
_LCREE: Final[str] = "lcree"
_EPE: Final[str] = "epe"

# file extensions
_JPG: Final[str] = "jpg"
_IMAGE: Final[str] = "image"
_CSV: Final[str] = "csv"
_DAT: Final[str] = "dat"


class EnvironmentalSubmissionType(SurveySubmission):

    def get_file_config(self, context: BusinessSurveyContext) -> dict[str, [File]]:
        return {
            _IMAGE: [self.get_ftp_image()],
            _INDEX: [self.get_ftp_index()],
            _RECEIPT: [self.get_ftp_receipt()],
            _LCREE: [{
                "location": LookupKey.NS5,
                "path": f"lcres/LCRES_EQ_data/{get_ns5_path()}/{context['period_id']}/v1"
            }],
            _EPE: [{
                "location": LookupKey.NS5,
                "path": f"epes/EPE_EQ_DATA/{get_ns5_path()}/{context['period_id']}/v1"
            }],
        }

    def get_mapping(self, filename: str) -> str:
        split_string = filename.split(".")
        extension = split_string[1].lower()
        if extension == _JPG:
            return _IMAGE
        elif extension == _CSV:
            return _INDEX
        elif extension == _DAT:
            return _RECEIPT

        if filename.startswith("007"):
            return _LCREE
        else:
            return _EPE
