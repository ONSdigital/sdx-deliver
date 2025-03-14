import json
import unittest
from typing import Final
from unittest.mock import patch, Mock

from sdx_gcp import Request

from app import deliver
from app.routes import FILE_NAME, VERSION, V2, SUBMISSION_FILE, MESSAGE_SCHEMA, deliver_dap, V1
from app.v2.definitions.message_schema import SchemaDataV2

SDX_LOCATION_NAME: Final[str] = "sdx_location_name"
FTP_LOCATION_NAME: Final[str] = "ftp_location_name"
SPP_LOCATION_NAME: Final[str] = "spp_location_name"
DAP_LOCATION_NAME: Final[str] = "dap_location_name"


class FileHolder:

    def __init__(self, file_bytes: bytes):
        self._file_bytes = file_bytes

    def read(self) -> bytes:
        return self._file_bytes


class TestDap(unittest.TestCase):

    @patch('app.deliver.write_to_bucket')
    @patch('app.deliver.publish_v2_schema')
    @patch('app.deliver.encrypt_output')
    @patch('app.routes.Flask.jsonify')
    def t_dap(self,
                 mock_jsonify: Mock,
                 mock_encrypt: Mock,
                 mock_publish_v2_schema: Mock,
                 mock_write_to_bucket: Mock):

        mock_encrypt.return_value = "My encrypted output"
        mock_write_to_bucket.return_value = "My fake bucket path"
        mock_jsonify.return_value = {"success": True}

        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = "016931f2-6230-4ca3-b84e-136e02e3f92b.json"
        output_filename = input_filename
        survey_id = "009"
        period_id = "202505"
        ruref = "49900000001A"

        submission_file = {
        }

        # Create the fake Request object

        files_dict = {
            SUBMISSION_FILE: FileHolder(json.dumps(submission_file).encode("utf-8")),
        }

        data = {
            FILE_NAME: input_filename,
            "tx_id": tx_id,
            VERSION: V2,
        }

        class MockRequest(Request):
            files = files_dict
            args = data

        # Call the endpoint
        response = deliver_dap(MockRequest(data), tx_id)
        self.assertTrue(response["success"])

        expected_v2_message: SchemaDataV2 = {
            "schema_version": "2",
            "sensitivity": "High",
            "sizeBytes": 19,
            "md5sum": "3190f8a68aad6a9e33a624c318516ebb",
            "context": {
                "survey_id": survey_id,
                "period_id": period_id,
                "ru_ref": ruref
            },
            "source": {
                "location_type": "gcs",
                "location_name": SDX_LOCATION_NAME,
                "path": "dap",
                "filename": input_filename
            },
            "actions": ["decrypt"],
            "targets": [
                {
                    "input": input_filename,
                    "outputs": [
                        {
                            "location_type": "cdp",
                            "location_name": DAP_LOCATION_NAME,
                            "path": f"landing_zone/sdx_preprod/{survey_id}",
                            "filename": output_filename
                        }
                    ]
                }
            ]
        }

        mock_publish_v2_schema.assert_called_with(expected_v2_message, tx_id)
