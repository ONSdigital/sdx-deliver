import unittest

from unittest.mock import patch, Mock
from app.output_type import OutputType
from app.store import write_to_bucket


class TestStore(unittest.TestCase):

    @patch('app.store.sdx_app')
    @patch('app.store.CONFIG')
    def test_write_to_bucket(self, mock_config: Mock, mock_app: Mock):
        mock_config.BUCKET_NAME = "ons-sdx-test-outputs"
        filename = "9010576d-f3df-4011-aa42-adecd9bee011"
        data = "my data"

        write_to_bucket(data, filename, OutputType.DAP)

        mock_app.gcs_write.assert_called_with(data, filename, "ons-sdx-test-outputs", "dap")
