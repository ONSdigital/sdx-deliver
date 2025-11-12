from abc import ABC, abstractmethod


class ZipBase(ABC):
    @abstractmethod
    def unzip(self, data_bytes: bytes) -> list[str]:
        pass
