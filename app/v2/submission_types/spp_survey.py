from typing import Optional, Final

from app.v2.definitions.config_schema import LocationKey, File
from app.v2.definitions.location_key_lookup import LocationKeyLookupBase
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.message_schema import Location
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

    def __init__(self, location_key_lookup: LocationKeyLookupBase):
        super().__init__(location_key_lookup)
        self.source_path = "survey"

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

    def _get_mapping(self, filename) -> str:
        split_string = filename.split(".")
        if len(split_string) == 1:
            return _PCK
        extension = split_string[1].lower()
        if extension == "jpg":
            return _IMAGE
        if extension == "csv":
            return _INDEX
        if extension == "dat":
            return _RECEIPT
        return _JSON

    def get_actions(self) -> list[str]:
        return [DECRYPT, UNZIP]

    def get_outputs(self, filename: str, survey_id: Optional[str] = None) -> list[Location]:
        key: str = self._get_mapping(filename)
        file: File = self.get_file_config(survey_id)[key]

        lookup_key: LookupKey = file["location"]
        location_key: LocationKey = self._location_key_lookup.get_location_key(lookup_key)

        return [{
            "location_type": location_key["location_type"],
            "location_name": location_key["location_name"],
            "path": file["path"],
            "filename": filename
        }]


