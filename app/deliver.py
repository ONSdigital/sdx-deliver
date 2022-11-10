import hashlib

import structlog

from app.encrypt import encrypt_output
from app.meta_wrapper import MetaWrapper
from app.output_type import OutputType
from app.publish import send_message
from app.store import write_to_bucket

logger = structlog.get_logger()


def deliver(meta_data: MetaWrapper, data_bytes: bytes):
    """
    Encrypts any unencrypted data, writes to the appropriate location within the outputs GCP bucket and notifies DAP
    via PubSub
    """
    logger.info("No delivery required as this is an integration environment")
