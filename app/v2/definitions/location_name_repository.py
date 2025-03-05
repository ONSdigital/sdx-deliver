from abc import ABC, abstractmethod
from enum import StrEnum


class LookupKey(StrEnum):
    FTP = "ftp"
    SDX = "sdx"
    SPP = "spp"
    DAP = "dap"


class LocationNameRepositoryBase(ABC):

    @abstractmethod
    def get_location_name(self, key: LookupKey) -> str:
        pass

    @abstractmethod
    def load_location_values(self):
        pass
