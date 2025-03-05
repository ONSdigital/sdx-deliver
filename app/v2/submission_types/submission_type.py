from abc import abstractmethod
from typing import Optional

from app import CONFIG
from app.v2.definitions.config_schema import File
from app.v2.definitions.location_key_lookup import LocationKeyLookupBase, LocationKey
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.message_schema import Location
from app.v2.definitions.submission_type import SubmissionTypeBase


# Environment descriptions
SDX_PROD = "SDX_Prod"
SDX_PREPROD = "SDX_PREPROD"


class SubmissionType(SubmissionTypeBase):

    def __init__(self, location_key_lookup: LocationKeyLookupBase):
        self._location_key_lookup = location_key_lookup

    @abstractmethod
    def get_file_config(self, survey_id: Optional[str] = None) -> dict[str, File]:
        """
        Return a dictionary of the mappings for each required file.

        The key should be an identifier for that particular file such as "image".
        The value should be a File type that holds the LocationKyLookup and the
        path for the destination of this file.
        """
        pass

    @abstractmethod
    def get_mapping(self, filename) -> str:
        """
        Return a key for the dictionary provided by get_file_config.
        Each filename should return a different key.
        """
        pass

    @abstractmethod
    def get_actions(self) -> list[str]:
        pass

    @abstractmethod
    def get_source_path(self) -> str:
        """
        The path within the GCS bucket to find this submission
        """
        pass

    def get_source(self, filename: str) -> Location:
        lookup_key: LookupKey = LookupKey.SDX
        location_key: LocationKey = self._location_key_lookup.get_location_key(lookup_key)

        return {
            "location_type": location_key["location_type"],
            "location_name": location_key["location_name"],
            "path": self.get_source_path(),
            "filename": filename
        }

    def get_outputs(self, filename: str, survey_id: Optional[str] = None) -> list[Location]:
        key: str = self.get_mapping(filename)
        file: File = self.get_file_config(survey_id)[key]

        lookup_key: LookupKey = file["location"]
        location_key: LocationKey = self._location_key_lookup.get_location_key(lookup_key)

        return [{
            "location_type": location_key["location_type"],
            "location_name": location_key["location_name"],
            "path": file["path"],
            "filename": filename
        }]

    def get_env_prefix(self, lowercase: Optional[bool] = False) -> str:
        """
        Return a string (optionally in lowercase) that describes the environment
        e.g. "ons-sdx-prod"

        This is useful for destination locations that follow a naming convention
        of using the environment within their path.
        """
        result = SDX_PROD if CONFIG.PROJECT_ID == "ons-sdx-prod" else SDX_PREPROD
        if lowercase:
            return result.lower()
        else:
            return result
