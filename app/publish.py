import json

from app import get_logger
from app.definitions import MessageSchemaV2

logger = get_logger()


def publish_v2_message(message: MessageSchemaV2, tx_id: str):
    attributes = {
        'tx_id': tx_id
    }

    sdx_app.publish_to_pubsub(CONFIG.DAP_TOPIC_ID, json.dumps(message), attributes)
