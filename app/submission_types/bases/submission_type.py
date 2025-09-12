from abc import abstractmethod

from app.definitions.config_schema import File
from app.definitions import LocationKeyLookupBase, LocationKey
from app.definitions import LookupKey
from app.definitions import Location
from app.definitions import SubmissionTypeBase
from app.definitions import Context


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

    def get_output_filename(self, filename: str, _context: Context) -> str:
        return filename

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
                "filename": self.get_output_filename(filename, context)
            })

        return result
