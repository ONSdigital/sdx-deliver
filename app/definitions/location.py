from abc import ABC, abstractmethod


from app.definitions.location_key import LocationKey
from app.definitions.lookup_key import LookupKey


class LocationBase(ABC):

    @abstractmethod
    def is_prod_env(self) -> bool:
        pass

    @abstractmethod
    def get_location_key(self, lookup_key: LookupKey) -> LocationKey:
        pass
