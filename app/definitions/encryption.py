from abc import ABC, abstractmethod


class EncryptionBase(ABC):

    @abstractmethod
    def encrypt(self, data_bytes: bytes) -> str:
        pass
