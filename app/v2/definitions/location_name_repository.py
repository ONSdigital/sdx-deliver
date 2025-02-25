from abc import ABC, abstractmethod


class LocationNameRepositoryBase(ABC):

    @abstractmethod
    def get_location_name(self, key: str) -> str:
        pass
