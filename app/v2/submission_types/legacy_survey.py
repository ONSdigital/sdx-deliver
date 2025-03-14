from typing import Optional, Final

from app.v2.definitions.config_schema import File
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.submission_type import UNZIP, DECRYPT
from app.v2.submission_types.bases.survey_type import SurveyType

# file types
_PCK: Final[str] = "pck"
_INDEX: Final[str] = "index"
_RECEIPT: Final[str] = "receipt"
_EQ_JSON: Final[str] = "eq_json"

# file extensions
_JPG: Final[str] = "jpg"
_IMAGE: Final[str] = "image"
_CSV: Final[str] = "csv"
_DAT: Final[str] = "dat"


class LegacySubmissionType(SurveyType):

    def get_source_path(self) -> str:
        return "survey"

    def get_actions(self) -> list[str]:
        return [DECRYPT, UNZIP]

    def get_file_config(self, survey_id: Optional[str] = None) -> dict[str, File]:
        return {
            _PCK: {
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_QData"
            },
            _IMAGE: self.get_ftp_image(),
            _INDEX: self.get_ftp_index(),
            _RECEIPT: self.get_ftp_receipt(),
            _EQ_JSON: self.get_ftp_eq_json()
        }

    def get_mapping(self, filename) -> str:
        split_string = filename.split(".")
        if len(split_string) == 1:
            return _PCK
        extension = split_string[1].lower()
        if extension == _JPG:
            return _IMAGE
        if extension == _CSV:
            return _INDEX
        if extension == _DAT:
            return _RECEIPT
        return _EQ_JSON
