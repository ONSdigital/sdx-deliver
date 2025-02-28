from typing import Optional, Final

from app.v2.definitions.config_schema import File
from app.v2.definitions.location_key_lookup import LocationKeyLookupBase
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.message_config import DECRYPT, UNZIP
from app.v2.submission_types.submission_type import SubmissionType

_PCK: Final[str] = "pck"
_JPG: Final[str] = "jpg"
_IMAGE: Final[str] = "image"
_CSV: Final[str] = "csv"
_ZIP: Final[str] = "zip"
_GPG: Final[str] = "gpg"
_INDEX: Final[str] = "index"
_DAT: Final[str] = "dat"
_RECEIPT: Final[str] = "receipt"
_JSON: Final[str] = "json"


class SppSubmissionType(SubmissionType):

    def get_source_path(self) -> str:
        return "survey"

    def get_actions(self) -> list[str]:
        return [DECRYPT, UNZIP]

    def get_file_config(self, survey_id: Optional[str] = None) -> dict[str, File]:
        return {
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
                "location": LookupKey.SPP,
                "path": f"sdc-response/{survey_id}/"
            }
        }

    def get_mapping(self, filename) -> str:
        split_string = filename.split(".")
        extension = split_string[1].lower()
        if extension == "jpg":
            return _IMAGE
        if extension == "csv":
            return _INDEX
        if extension == "dat":
            return _RECEIPT
        return _JSON
