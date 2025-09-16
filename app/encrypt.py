import gnupg

from app import get_logger
from app.settings import settings

logger = get_logger()


def setup_keys():
    if not settings().encryption_key_set:
        gpg = gnupg.GPG()
        gpg_key = settings().dap_public_gpg
        gpg.import_keys(gpg_key)
        settings().encryption_key_set = True


def encrypt_output(data_bytes: bytes) -> str:
    """
    Encrypts data using DAP public key (GPG)
    """

    recipients = [settings().data_recipient]
    encrypted_data = gnupg.GPG().encrypt(data_bytes, recipients=recipients, always_trust=True)

    if encrypted_data.ok:
        logger.info("Successfully encrypted output")
    else:
        logger.error("Failed to encrypt output")
        logger.error(encrypted_data.status)

    return str(encrypted_data)
