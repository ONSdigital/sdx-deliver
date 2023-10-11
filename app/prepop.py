import uuid

from sdx_gcp import Message, TX_ID, Request
from sdx_gcp.app import get_logger

from app import sdx_app, CONFIG

logger = get_logger()


def generate_tx_id(_req: Request) -> TX_ID:
    return str(uuid.uuid4())


def process(message: Message, _tx_id: TX_ID):
    logger.info(f"Deliver (mock NIFI) triggered by PubSub with message: {message}")
    attributes = message["attributes"]
    filename = attributes['objectId']

    data_bytes = sdx_app.gcs_read(filename, CONFIG.NIFI_BUCKET_NAME)

    encrypted_data = CONFIG.GPG.encrypt(data_bytes, recipients=CONFIG.PREPOP_RECIPIENTS, always_trust=True)

    if encrypted_data.ok:
        logger.info("Successfully encrypted prepop data ")
    else:
        logger.error("Failed to encrypt prepop data")
        logger.error(encrypted_data.status)

    prepop_data: str = str(encrypted_data)

    sdx_app.gcs_write(prepop_data, filename, CONFIG.SDS_INPUT_BUCKET_NAME)

    logger.info("Finished NIFI process!")
