from typing import Final

from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext
from app.definitions.lookup_key import LookupKey
from app.submission_types.bases.survey_submission import SurveySubmission

# file types
_PCK: Final[str] = "pck"
_IMAGE: Final[str] = "image"
_INDEX: Final[str] = "index"
_RECEIPT: Final[str] = "receipt"

# file extensions
_JPG: Final[str] = "jpg"
_CSV: Final[str] = "csv"
_DAT: Final[str] = "dat"


class DextaSubmissionType(SurveySubmission):
    def get_file_config(self, context: BusinessSurveyContext) -> dict[str, list[File]]:
        return {
            _PCK: [{"location": LookupKey.FTP, "path": f"{self._get_ftp_path()}/SDC_QData"}],
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
