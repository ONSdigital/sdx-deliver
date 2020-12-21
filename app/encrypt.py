import json
import logging

import yaml
from sdc.crypto.key_store import KeyStore
from sdc.crypto.encrypter import encrypt
from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))

KEY_PURPOSE_SUBMISSION = 'submission'


def encrypt_data(data) -> str:
    if isinstance(data, dict):
        data_str = json.dumps(data)
    else:
        data_str = str(data)

    with open("./keys.yml") as file:
        secrets_from_file = yaml.safe_load(file)
    key_store = KeyStore(secrets_from_file)
    encrypted_payload = encrypt(data_str, key_store, KEY_PURPOSE_SUBMISSION)
    logger.info("successfully encrypted payload")
    return encrypted_payload
