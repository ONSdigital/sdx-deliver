import json

from sdx_base.services.pubsub import PubsubService

from app import get_logger
from app.definitions.message_schema import MessageSchemaV2

logger = get_logger()


class PublishService:

    def __init__(self, pubsub_service: PubsubService, dap_topic_id: str):
        self._pubsub = pubsub_service
        self._dap_topic_id = dap_topic_id

    def publish_v2_message(self, message: MessageSchemaV2, tx_id: str):
        attributes = {
            'tx_id': tx_id
        }

        self._pubsub.publish_message(self._dap_topic_id,
                                     json.dumps(message),
                                     attributes)
