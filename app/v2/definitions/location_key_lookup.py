from abc import ABC, abstractmethod
from typing import TypedDict

from app.v2.definitions.location_name_repository import LookupKey


class LocationKey(TypedDict):
    location_type: str
    location_name: str


class LocationKeyLookupBase(ABC):

    @abstractmethod
    def get_location_key(self, lookup_key: LookupKey) -> LocationKey:
        pass
