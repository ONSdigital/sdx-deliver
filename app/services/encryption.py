import hashlib
from typing import Self, Protocol

import gnupg
from sdx_base.errors.retryable import RetryableError
from sdx_base.settings.service import SECRET

from app import get_logger
from app.definitions.encryption import EncryptionBase

logger = get_logger()


class GpgSettings(Protocol):
    dap_public_gpg: SECRET
    data_recipient: str


class EncryptionService(EncryptionBase):

    def __init__(self, gpg_settings: GpgSettings):
        gpg = gnupg.GPG()
        gpg.import_keys(gpg_settings.dap_public_gpg)
        self._recipients: list[str] = [gpg_settings.data_recipient]

    def encrypt(self: Self, data_bytes: bytes) -> str:
        """
        Encrypts data using DAP public key (GPG)
        """
        encrypted_data = gnupg.GPG().encrypt(data_bytes,
                                             recipients=self._recipients,
                                             always_trust=True)

        if encrypted_data.ok:
            logger.info("Successfully encrypted payload")
        else:
            logger.error("Failed to encrypt payload")
            logger.error(encrypted_data.status)
            raise RetryableError("Failed to encrypt payload")

        return str(encrypted_data)

    def get_md5_and_size(self, data_bytes: bytes) -> tuple[str, int]:
        md5sum: str = hashlib.md5(data_bytes).hexdigest()
        size_bytes: int = len(data_bytes)
        return md5sum, size_bytes
