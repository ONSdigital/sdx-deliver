from abc import abstractmethod

from app.v2.definitions.config_schema import File
from app.v2.definitions.location_key_lookup import LocationKeyLookupBase, LocationKey
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.message_schema import Location
from app.v2.definitions.submission_type import SubmissionTypeBase
from app.v2.definitions.context import Context


class SubmissionType(SubmissionTypeBase):

    def __init__(self, location_key_lookup: LocationKeyLookupBase):
        self._location_key_lookup = location_key_lookup

    @abstractmethod
    def get_file_config(self, context: Context) -> dict[str, [File]]:
        pass

    @abstractmethod
    def get_mapping(self, filename) -> str:
        pass

    @abstractmethod
    def get_actions(self) -> list[str]:
        pass

    @abstractmethod
    def get_source_path(self) -> str:
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

    def get_outputs(self, filename: str, context: Context) -> list[Location]:
        key: str = self.get_mapping(filename)
        filelist: list[File] = self.get_file_config(context)[key]

        result: list[Location] = []
        for file in filelist:
            lookup_key: LookupKey = file["location"]
            location_key: LocationKey = self._location_key_lookup.get_location_key(lookup_key)
            result.append({
                "location_type": location_key["location_type"],
                "location_name": location_key["location_name"],
                "path": file["path"],
                "filename": filename
            })

        return result
