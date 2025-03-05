from typing import Optional, Final

from sdx_gcp.errors import DataError

from app.v2.definitions.config_schema import File
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.submission_type import UNZIP, DECRYPT
from app.v2.submission_types.submission_type import SubmissionType

# file types
_PCK: Final[str] = "pck"
_INDEX: Final[str] = "index"
_RECEIPT: Final[str] = "receipt"
_JSON: Final[str] = "json"
_SPP: Final[str] = "spp"

# file extensions
_JPG: Final[str] = "jpg"
_IMAGE: Final[str] = "image"
_CSV: Final[str] = "csv"
_DAT: Final[str] = "dat"


def is_spp_json_filename(filename: str) -> bool:
    if filename[3:8] == "_SDC_" and filename[-5:] == ".json":
        return True
    return False


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
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_QJson"
            },
            _SPP: {
                "location": LookupKey.SPP,
                "path": f"sdc-response/{survey_id}/"
            }
        }

    def get_mapping(self, filename) -> str:
        split_string = filename.split(".")
        if len(split_string) < 2:
            raise DataError("All filenames to SPP should have a file extension!")
        if is_spp_json_filename(filename):
            return _SPP
        extension = split_string[1].lower()
        if extension == _JPG:
            return _IMAGE
        if extension == _CSV:
            return _INDEX
        if extension == _DAT:
            return _RECEIPT
        return _JSON
