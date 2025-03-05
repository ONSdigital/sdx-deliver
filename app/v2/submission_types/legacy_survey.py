from typing import Optional, Final

from app.v2.definitions.config_schema import File
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.submission_type import UNZIP, DECRYPT
from app.v2.submission_types.submission_type import SubmissionType

# file types
_PCK: Final[str] = "pck"
_INDEX: Final[str] = "index"
_RECEIPT: Final[str] = "receipt"
_JSON: Final[str] = "json"

# file extensions
_JPG: Final[str] = "jpg"
_IMAGE: Final[str] = "image"
_CSV: Final[str] = "csv"
_DAT: Final[str] = "dat"


class LegacySubmissionType(SubmissionType):

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
            _IMAGE: {
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_QImages/Images"
            },
            _INDEX: {
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_QImages/Index"
            },
            _RECEIPT: {
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_QReceipts"
            },
            _JSON: {
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_QJson"
            }
        }

    def get_mapping(self, filename) -> str:
        """
        For Legacy submissions the Files can be
        determined by the file extension alone.
        """
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
        return _JSON
