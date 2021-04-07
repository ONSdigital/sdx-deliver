import unittest

from google.cloud.secretmanager_v1 import SecretManagerServiceClient

import app

from unittest.mock import patch, MagicMock
from app import secret_manager, get_secret, cloud_config
from app.output_type import OutputType
from app.store import write_to_bucket


class TestStore(unittest.TestCase):

    @patch('app.store.CONFIG')
    def test_write_to_bucket(self, mock_config):
        mock_blob = MagicMock()
        mock_config.BUCKET.blob.return_value = mock_blob
        filename = "9010576d-f3df-4011-aa42-adecd9bee011"
        data = "my data"

        write_to_bucket(data, filename, OutputType.DAP)

        mock_config.BUCKET.blob.assert_called_with(f"dap/{filename}")
        mock_blob.upload_from_string.assert_called_with(data)

    @patch('app.secret_manager.secretmanager')
    def test_secret_manager(self, mock_secret_manager):
        project_id = "test"
        secret = "secret"
        secret_manager.client = MagicMock()
        actual = get_secret(project_id, secret)
        self.assertTrue(actual)

    @patch('app.get_secret', return_value='my secret')
    @patch('app.pubsub_v1')
    @patch('app.storage')
    def test_cloud_config(self, mock_bucket, mock_pubsub, mock_secret):
        cloud_config()
        assert app.CONFIG.ENCRYPTION_KEY == 'my secret'
        assert app.CONFIG.BUCKET is not None
        assert app.CONFIG.DAP_PUBLISHER is not None
        assert app.CONFIG.DAP_TOPIC_PATH is not None
        assert app.CONFIG.GPG is not None
