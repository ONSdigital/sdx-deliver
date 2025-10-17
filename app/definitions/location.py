from abc import ABC, abstractmethod, ABCMeta

from sdx_base.utilities.singleton import SingletonMeta

from app.definitions.location_key import LocationKey
from app.definitions.lookup_key import LookupKey


class LocationBase(ABC):

    @abstractmethod
    def is_prod_env(self) -> bool:
        pass

    @abstractmethod
    def get_location_key(self, lookup_key: LookupKey) -> LocationKey:
        pass
