from typing import Self, Protocol

import gnupg
from sdx_base.utilities.singleton import SingletonMeta

from app import get_logger

logger = get_logger()


class GpgKeyGetter(Protocol):
    def get_gpg_key(self) -> str: ...
    def get_data_recipient(self) -> str: ...


class EncryptionService(metaclass=SingletonMeta):

    def __init__(self, gpg_getter: GpgKeyGetter):
        self._gpg_getter = gpg_getter
        gpg = gnupg.GPG()
        gpg.import_keys(gpg_getter.get_gpg_key())

    def encrypt(self: Self, data_bytes: bytes) -> str:
        """
        Encrypts data using DAP public key (GPG)
        """

        recipients = [self._gpg_getter.get_data_recipient()]
        encrypted_data = gnupg.GPG().encrypt(data_bytes, recipients=recipients, always_trust=True)

        if encrypted_data.ok:
            logger.info("Successfully encrypted payload")
        else:
            logger.error("Failed to encrypt payload")
            logger.error(encrypted_data.status)

        return str(encrypted_data)
