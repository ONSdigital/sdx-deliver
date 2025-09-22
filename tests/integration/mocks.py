from typing import Self

from app.definitions.encryption import EncryptionBase
from app.definitions.gcp import GcpBase
from app.definitions.message_schema import MessageSchemaV2


class MockSettings:

    def __init__(self: Self):
        self.project_id: str = "sdx-sandbox"
        self.app_name: str = "sdx-deliver"
        self.app_version: str = "1.0.0"
        self.port: int = 5000
        self.logging_level: str = "INFO"
        self.data_sensitivity: str = "low"
        self.data_recipient: str = "test_recipient"
        self.dap_topic_id: str = "dap-topic"
        self.dap_public_gpg: str = "public_gpg"
        self.nifi_location_ftp: str = "sdx_location_name"
        self.nifi_location_spp: str = "ftp_location_name"
        self.nifi_location_dap: str = "spp_location_name"
        self.nifi_location_ns5: str = "dap_location_name"

    def get_bucket_name(self) -> str:
        return f'{self.project_id}-outputs'


class MockEncryptor(EncryptionBase):

    def encrypt(self, data_bytes: bytes) -> str:
        return "decrypted data"


class MockGcp(GcpBase):

    def publish_v2_message(self, message: MessageSchemaV2, tx_id: str):
        print("published message")

    def store(self, data: bytes, filename: str, sub_dir: str):
        print("storing data")
