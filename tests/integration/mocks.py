from typing import Self, Optional, Final

from app.definitions.encryption import EncryptionBase
from app.definitions.gcp import GcpBase
from app.definitions.message_schema import MessageSchemaV2


NIFI_LOCATION_FTP: Final[str] = "ftp_location_name"
NIFI_LOCATION_SPP: Final[str] = "spp_location_name"
NIFI_LOCATION_DAP: Final[str] = "dap_location_name"
NIFI_LOCATION_NS5: Final[str] = "ns5_location_name"


class MockSettings:
    project_id: str
    app_name: str
    app_version: str
    port: int
    logging_level: str
    data_sensitivity: str
    data_recipient: str
    dap_topic_id: str
    dap_public_gpg: str
    nifi_location_ftp: str
    nifi_location_spp: str
    nifi_location_dap: str
    nifi_location_ns5: str

    def __init__(self: Self):
        self.project_id: str = "sdx-sandbox"
        self.app_name: str = "sdx-deliver"
        self.app_version: str = "1.0.0"
        self.port: int = 5000
        self.logging_level: str = "INFO"
        self.data_sensitivity: str = "Low"
        self.data_recipient: str = "test_recipient"
        self.dap_topic_id: str = "dap-topic"
        self.dap_public_gpg: str = "public_gpg"
        self.nifi_location_ftp: str = NIFI_LOCATION_FTP
        self.nifi_location_spp: str = NIFI_LOCATION_SPP
        self.nifi_location_dap: str = NIFI_LOCATION_DAP
        self.nifi_location_ns5: str = NIFI_LOCATION_NS5

    def get_bucket_name(self) -> str:
        return f'{self.project_id}-outputs'


def get_mock_settings() -> MockSettings:
    return MockSettings()


class MockEncryptor(EncryptionBase):

    def encrypt(self, data_bytes: bytes) -> str:
        return "decrypted data"

    def get_md5_and_size(self, data_bytes: bytes) -> tuple[str, int]:
        return "md5sum", 10


def get_mock_encryptor() -> MockEncryptor:
    return MockEncryptor()


class MockGcp(GcpBase):
    _message: Optional[MessageSchemaV2] = None

    @classmethod
    def get_message(cls) -> MessageSchemaV2:
        if cls._message:
            return cls._message
        else:
            raise Exception("message not set!")

    def publish_v2_message(self, message: MessageSchemaV2, tx_id: str):
        print("pretending to publish a message")
        MockGcp._message = message

    def store(self, data: bytes, filename: str, sub_dir: str):
        print("pretending to store data")


def get_mock_gcp() -> MockGcp:
    return MockGcp()
