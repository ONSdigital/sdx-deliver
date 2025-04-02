import json

from sdx_gcp.app import get_logger

from app import CONFIG, sdx_app
from app.definitions import MessageSchema
from app.v2.definitions.message_schema import MessageSchemaV2

logger = get_logger()


def publish_message(message: MessageSchema, tx_id: str, path: str):
    """
    Publishes message to DAP
    """
    # NIFI can't handle forward slash
    key = path.replace("/", "|")
    attributes = {
        'gcs.bucket': CONFIG.BUCKET_NAME,
        'gcs.key': key,
        'tx_id': tx_id
    }

    sdx_app.publish_to_pubsub(CONFIG.DAP_TOPIC_ID, json.dumps(message), attributes)

    logger.info("Published message to DAP topic", gcs_key=key)


def publish_v2_message(message: MessageSchemaV2, tx_id: str):
    attributes = {
        'tx_id': tx_id
    }

    sdx_app.publish_to_pubsub(CONFIG.DAP_TOPIC_ID, json.dumps(message), attributes)
