from typing import Final

from app.definitions.config_schema import File
from app.definitions import LookupKey
from app.path_helper import get_ftp_path
from app.definitions import BusinessSurveyContext
from app.submission_types.bases.survey_submission import SurveySubmission

# file types
_PCK: Final[str] = "pck"
_IMAGE: Final[str] = "image"
_INDEX: Final[str] = "index"
_RECEIPT: Final[str] = "receipt"
_EQ_JSON: Final[str] = "eq_json"

# file extensions
_JPG: Final[str] = "jpg"
_CSV: Final[str] = "csv"
_DAT: Final[str] = "dat"


class LegacySubmissionType(SurveySubmission):

    def get_file_config(self, context: BusinessSurveyContext) -> dict[str, [File]]:
        return {
            _PCK: [{
                "location": LookupKey.FTP,
                "path": f"{get_ftp_path()}/EDC_QData"
            }],
            _IMAGE: [self.get_ftp_image()],
            _INDEX: [self.get_ftp_index()],
            _RECEIPT: [self.get_ftp_receipt()],
        }

    def get_mapping(self, filename: str) -> str:
        split_string = filename.split(".")
        if len(split_string) == 1:
            return _PCK
        extension = split_string[1].lower()
        if extension == _JPG:
            return _IMAGE
        elif extension == _CSV:
            return _INDEX
        else:
            return _RECEIPT
