import base64
import json
import logging

from sdc.crypto.encrypter import encrypt
from structlog import wrap_logger

from app import key_store
from app.output_type import OutputType

logger = wrap_logger(logging.getLogger(__name__))

KEY_PURPOSE_SUBMISSION = 'submission'


def encrypt_output(data_bytes: bytes, output_type: OutputType) -> str:
    if output_type == OutputType.DAP:
        return encrypt_json(data_bytes)
    elif output_type == OutputType.FEEDBACK:
        return encrypt_feedback(data_bytes)
    else:
        return encrypt_zip(data_bytes)


def encrypt_json(data_bytes: bytes) -> str:
    claims = data_bytes.decode("utf-8")
    claim_str = json.dumps(claims)
    logger.info(f'claim_str: {claim_str}')
    encrypted_payload = encrypt(claim_str, key_store, KEY_PURPOSE_SUBMISSION)
    logger.info("successfully encrypted json payload")
    return encrypted_payload


def encrypt_feedback(data_bytes: bytes) -> str:
    claims = {'feedback': data_bytes.decode("utf-8")}
    encrypted_payload = encrypt(json.dumps(claims), key_store, KEY_PURPOSE_SUBMISSION)
    logger.info("successfully encrypted feedback payload")
    return encrypted_payload


def encrypt_zip(zip_bytes: bytes) -> str:
    claims = {'zip': base64.b64encode(zip_bytes).decode()}
    encrypted_payload = encrypt(json.dumps(claims), key_store, KEY_PURPOSE_SUBMISSION)
    logger.info("successfully encrypted zip payload")
    return encrypted_payload
