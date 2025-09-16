import json

from app import get_logger
from app.definitions.message_schema import MessageSchemaV2
from app.settings import settings

logger = get_logger()


def publish_v2_message(message: MessageSchemaV2, tx_id: str):
    attributes = {
        'tx_id': tx_id
    }

    dap_topic: str = settings().dap_topic_id
    sdx_app.publish_to_pubsub(dap_topic, json.dumps(message), attributes)
