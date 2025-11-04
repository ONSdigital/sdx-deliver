from abc import abstractmethod
from typing import Protocol, Self

from app.definitions.config_schema import File
from app.definitions.context import Context
from app.definitions.location_key import LocationKey
from app.definitions.lookup_key import LookupKey
from app.definitions.message_schema import Location
from app.definitions.submission_type import SubmissionTypeBase


class LocationHelper(Protocol):
    def get_location_key(self, lookup_key: LookupKey) -> LocationKey: ...
    def is_prod_env(self) -> bool: ...


class SubmissionType(SubmissionTypeBase):

    def __init__(self, location_helper: LocationHelper):
        self._location_helper = location_helper

    def _is_prod_env(self) -> bool:
        return self._location_helper.is_prod_env()

    def _get_ftp_path(self: Self) -> str:
        return "SDX_Prod" if self._is_prod_env() else "SDX_PREPROD"

    @abstractmethod
    def create_file_config(self, context: Context) -> dict[str, list[File]]:
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
        location_key: LocationKey = self._location_helper.get_location_key(lookup_key)

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
        filelist: list[File] = self.create_file_config(context)[key]

        result: list[Location] = []
        for file in filelist:
            lookup_key: LookupKey = file["location"]
            location_key: LocationKey = self._location_helper.get_location_key(lookup_key)
            result.append({
                "location_type": location_key["location_type"],
                "location_name": location_key["location_name"],
                "path": file["path"],
                "filename": self.get_output_filename(filename, context)
            })

        return result
