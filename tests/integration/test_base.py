import os
import unittest
from pathlib import Path
from typing import Self, Optional, cast

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sdx_base.run import run
from sdx_base.server.server import RouterConfig

from app.definitions.encryption import EncryptionBase
from app.definitions.gcp import GcpBase
from app.definitions.message_schema import MessageSchemaV2
from app.dependencies import get_encryption_service, get_gcp_service
from app.routes import router
from app.settings import Settings


class MockSecretReader:

    def get_secret(self, _project_id: str, secret_id: str) -> str:
        return secret_id


class MockEncryptor(EncryptionBase):

    def encrypt(self, data_bytes: bytes) -> str:
        return "decrypted data"

    def get_md5_and_size(self, data_bytes: bytes) -> tuple[str, int]:
        return "md5sum", 10


class MockGcp(GcpBase):
    _message: Optional[MessageSchemaV2]

    def __init__(self):
        self._message = None

    def publish_v2_message(self, message: MessageSchemaV2, tx_id: str):
        print("pretending to publish a message")
        self._message = message

    def store(self, data: bytes, filename: str, sub_dir: str):
        print("pretending to store data")

    def get_message(self) -> MessageSchemaV2:
        if self._message:
            return cast(MessageSchemaV2, self._message)
        raise(Exception("No message sent"))


class TestBase(unittest.TestCase):

    def setUp(self: Self):
        os.environ["PROJECT_ID"] = "ons-sdx-sandbox"
        os.environ["DATA_SENSITIVITY"] = "Low"
        os.environ["DATA_RECIPIENT"] = "mock-recipient"
        proj_root = Path(__file__).parent.parent.parent  # sdx-deliver dir

        router_config = RouterConfig(router)
        app: FastAPI = run(Settings,
                           routers=[router_config],
                           proj_root=proj_root,
                           secret_reader=MockSecretReader(),
                           serve=lambda a, b: a
                           )

        self.mock_encryptor = MockEncryptor()
        self.mock_gcp = MockGcp()
        app.dependency_overrides[get_encryption_service] = lambda: self.mock_encryptor
        app.dependency_overrides[get_gcp_service] = lambda: self.mock_gcp
        self.app = app
        self.client = TestClient(app)
