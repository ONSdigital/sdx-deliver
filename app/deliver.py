import hashlib

from sdx_gcp.app import get_logger

from app.definitions import MessageSchema
from app.encrypt import encrypt_output
from app.message import create_message
from app.meta_wrapper import MetaWrapper
from app.output_type import OutputType
from app.publish import publish_message
from app.store import write_to_bucket

logger = get_logger()


def deliver(meta_data: MetaWrapper, data_bytes: bytes):
    """
    Encrypts any unencrypted data, writes to the appropriate location within the outputs GCP bucket and notifies DAP
    via PubSub
    """
    if meta_data.output_type == OutputType.SEFT:
        encrypted_output = data_bytes
    else:
        logger.info("Encrypting output")
        encrypted_output = encrypt_output(data_bytes)
        encrypted_bytes = encrypted_output.encode()
        meta_data.md5sum = hashlib.md5(encrypted_bytes).hexdigest()
        meta_data.sizeBytes = len(encrypted_bytes)

    logger.info("Storing to bucket")
    path = write_to_bucket(encrypted_output, filename=meta_data.filename, output_type=meta_data.output_type)

    logger.info("Sending DAP notification")

    message: MessageSchema = create_message(meta_data)
    publish_message(message, meta_data.tx_id, path)

    logger.info("Process completed successfully", survey_id=meta_data.survey_id)
