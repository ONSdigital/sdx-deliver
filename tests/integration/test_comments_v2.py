import io
import unittest
import zipfile
from typing import Final
from unittest.mock import patch, Mock

from sdx_gcp import Request

from app import deliver
from app.routes import FILE_NAME, VERSION, V2, MESSAGE_SCHEMA, ZIP_FILE, deliver_comments
from app.v2.definitions.location_name_repository import LocationNameRepositoryBase
from app.v2.definitions.message_schema import SchemaDataV2
from app.v2.message_config import FTP, SDX, SPP, DAP

SDX_LOCATION_NAME: Final[str] = "sdx_location_name"
FTP_LOCATION_NAME: Final[str] = "ftp_location_name"
SPP_LOCATION_NAME: Final[str] = "spp_location_name"
DAP_LOCATION_NAME: Final[str] = "dap_location_name"


class MockLocationNameMapper(LocationNameRepositoryBase):
    def __init__(self):
        self.locations_mapping = None

    def get_location_name(self, key: str) -> str:
        return self.locations_mapping[key]

    def load_location_values(self):
        self.locations_mapping = {
            FTP: FTP_LOCATION_NAME,
            SDX: SDX_LOCATION_NAME,
            SPP: SPP_LOCATION_NAME,
            DAP: DAP_LOCATION_NAME
        }


class FileHolder:

    def __init__(self, file_bytes: bytes):
        self._file_bytes = file_bytes

    def read(self) -> bytes:
        return self._file_bytes


class TestCommentsV2(unittest.TestCase):

    @patch('app.deliver.write_to_bucket')
    @patch('app.deliver.publish_v2_schema')
    @patch('app.deliver.encrypt_output')
    @patch('app.routes.Flask.jsonify')
    def test_comments(self,
                      mock_jsonify: Mock,
                      mock_encrypt: Mock,
                      mock_publish_v2_schema: Mock,
                      mock_write_to_bucket: Mock):
        deliver.location_name_mapper = MockLocationNameMapper()
        mock_encrypt.return_value = "My encrypted output"
        mock_write_to_bucket.return_value = "My fake bucket path"
        mock_jsonify.return_value = {"success": True}

        tx_id = "2025-01-01.zip:ftp"  # why?
        input_filename = "2025-01-01.zip"

        # Create the input zipfile
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("file1", 'Some comments.')
            zip_file.writestr("file2", 'Some more comments.')
            zip_file.writestr("file3", 'Even more comments!')

        zip_bytes = zip_buffer.getvalue()

        # Create the fake Request object

        files_dict = {
            ZIP_FILE: FileHolder(zip_bytes)
        }

        data = {
            FILE_NAME: input_filename,
            "tx_id": tx_id,
            VERSION: V2,
            MESSAGE_SCHEMA: V2
        }

        class MockRequest(Request):
            files = files_dict
            args = data

        # Call the endpoint
        response = deliver_comments(MockRequest(data), tx_id)
        self.assertTrue(response["success"])

        expected_v2_message: SchemaDataV2 = {
            "schema_version": "2",
            "sensitivity": "High",
            "sizeBytes": 19,
            "md5sum": "3190f8a68aad6a9e33a624c318516ebb",
            "context": {
                "title": "Comments.zip",
            },
            "source": {
                "location_type": "gcs",
                "location_name": SDX_LOCATION_NAME,
                "path": "comments",
                "filename": input_filename
            },
            "actions": ["decrypt"],
            "targets": [
                {
                    "input": input_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": FTP_LOCATION_NAME,
                            "path": "SDX_PREPROD/EDC_Submissions/Comments",
                            "filename": input_filename
                        }
                    ]
                }
            ]
        }

        mock_publish_v2_schema.assert_called_with(expected_v2_message, tx_id)
