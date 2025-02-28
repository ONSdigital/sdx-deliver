from abc import ABC, abstractmethod

from app.v2.definitions.config_schema import LocationKey
from app.v2.definitions.location_name_repository import LookupKey


class LocationKeyLookupBase(ABC):

    @abstractmethod
    def get_location_key(self, lookup_key: LookupKey) -> LocationKey:
        pass
