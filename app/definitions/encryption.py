from abc import ABC, abstractmethod


class EncryptionBase(ABC):
    @abstractmethod
    def encrypt(self, data_bytes: bytes) -> str:
        pass

    @abstractmethod
    def get_md5_and_size(self, data_bytes: bytes) -> tuple[str, int]:
        pass
