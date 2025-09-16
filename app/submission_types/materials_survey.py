from typing import Final

from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext
from app.definitions.location_name_repository import LookupKey
from app.path_helper import get_ftp_path
from app.submission_types.bases.survey_submission import SurveySubmission

# file types
_INDEX: Final[str] = "index"
_RECEIPT: Final[str] = "receipt"
_JSON: Final[str] = "json"

# file extensions
_JPG: Final[str] = "jpg"
_IMAGE: Final[str] = "image"
_CSV: Final[str] = "csv"
_DAT: Final[str] = "dat"


class MaterialsSubmissionType(SurveySubmission):

    def get_file_config(self, context: BusinessSurveyContext) -> dict[str, list[File]]:
        return {
            _IMAGE: [self.get_ftp_image()],
            _INDEX: [self.get_ftp_index()],
            _RECEIPT: [self.get_ftp_receipt()],
            _JSON: [{
                "location": LookupKey.FTP,
                "path": f"{get_ftp_path()}/EDC_QJson"
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
        else:
            return _JSON
