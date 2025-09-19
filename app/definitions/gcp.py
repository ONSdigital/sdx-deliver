from abc import ABC, abstractmethod

from app.definitions.message_schema import MessageSchemaV2


class GcpBase(ABC):

    @abstractmethod
    def publish_v2_message(self, message: MessageSchemaV2, tx_id: str):
        pass

    @abstractmethod
    def store(self, data: bytes, filename: str, sub_dir: str):
        pass
