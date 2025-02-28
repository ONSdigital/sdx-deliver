from typing import Optional, Final

from app.v2.definitions.config_schema import File, LocationKey
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.message_schema import Location
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


class SppAndDapSubmissionType(SubmissionType):

    def get_source_path(self) -> str:
        return "survey"

    def get_actions(self) -> list[str]:
        return [DECRYPT, UNZIP]

    def get_file_config(self, survey_id: Optional[str] = None) -> dict[str, File | list[File]]:
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
            _JSON: [
                {
                    "location": LookupKey.SPP,
                    "path": f"sdc-response/{survey_id}/"
                },
                {
                    "location": LookupKey.DAP,
                    "path": f"landing_zone/{self.get_env_prefix()}/{survey_id}"
                }
            ]
        }

    def get_outputs(self, filename: str, survey_id: Optional[str] = None) -> list[Location]:
        key: str = self.get_mapping(filename)
        if key == _JSON:
            file_list: list[File] = self.get_file_config(survey_id)[key]
        else:
            file_list: list[File] = [self.get_file_config(survey_id)[key]]

        results: list[Location] = []

        for file in file_list:
            lookup_key: LookupKey = file["location"]
            location_key: LocationKey = self._location_key_lookup.get_location_key(lookup_key)

            results.append({
                "location_type": location_key["location_type"],
                "location_name": location_key["location_name"],
                "path": file["path"],
                "filename": filename
            })

        return results

    def get_mapping(self, filename) -> str:
        split_string = filename.split(".")
        extension = split_string[1].lower()
        if extension == _JPG:
            return _IMAGE
        if extension == _CSV:
            return _INDEX
        if extension == _DAT:
            return _RECEIPT
        return _JSON
