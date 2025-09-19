import json

from typing import Protocol
from sdx_base.services.pubsub import PubsubService
from sdx_base.services.storage import StorageService

from app import get_logger
from app.definitions.gcp import GcpBase
from app.definitions.message_schema import MessageSchemaV2

logger = get_logger()


class GcpSettings(Protocol):
    project_id: str
    dap_topic_id: str

    def get_bucket_name(self) -> str: ...


class GcpService(GcpBase):

    def __init__(self, pubsub_service: PubsubService,
                 storage_service: StorageService,
                 settings: GcpSettings):
        self._pubsub_service = pubsub_service
        self._storage_service = storage_service
        self._settings = settings

    def publish_v2_message(self, message: MessageSchemaV2, tx_id: str):
        attributes = {
            'tx_id': tx_id
        }

        dap_topic_id: str = self._settings.dap_topic_id
        self._pubsub_service.publish_message(dap_topic_id,
                                             json.dumps(message),
                                             attributes)

    def store(self,
              data: bytes,
              filename: str,
              sub_dir: str):
        self._storage_service.write(data,
                                    filename=filename,
                                    bucket_name=self._settings.get_bucket_name(),
                                    project_id=self._settings.project_id,
                                    sub_dir=sub_dir)
