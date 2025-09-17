import json

from sdx_base.services.pubsub import PubsubService

from app import get_logger
from app.definitions.message_schema import MessageSchemaV2
from app.settings import settings

logger = get_logger()


class PublishService:

    def __init__(self, pubsub_service: PubsubService):
        self._pubsub = pubsub_service

    def publish_v2_message(self, message: MessageSchemaV2, tx_id: str):
        attributes = {
            'tx_id': tx_id
        }

        dap_topic: str = settings().dap_topic_id
        self._pubsub.publish_message(dap_topic, json.dumps(message), attributes)
