import json
import unittest
from unittest.mock import patch, Mock

from sdx_gcp import Request

from app import deliver
from app.routes import FILE_NAME, V2, MESSAGE_SCHEMA, SEFT_FILE, METADATA_FILE, deliver_seft
from app.v2.definitions.message_schema import MessageSchemaV2
from tests.integration.v2 import MockLocationNameMapper, FileHolder, SDX_LOCATION_NAME, FTP_LOCATION_NAME


class TestSeftV2(unittest.TestCase):

    @patch('app.deliver.write_to_bucket')
    @patch('app.deliver.publish_v2_message')
    @patch('app.deliver.encrypt_output')
    @patch('app.routes.Flask.jsonify')
    def test_seft(self,
                  mock_jsonify: Mock,
                  mock_encrypt: Mock,
                  mock_publish_v2_schema: Mock,
                  mock_write_to_bucket: Mock):
        deliver.location_name_repo = MockLocationNameMapper()
        mock_encrypt.return_value = "My encrypted output"
        mock_write_to_bucket.return_value = "My fake bucket path"
        mock_jsonify.return_value = {"success": True}

        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = "14112300153_202203_141_20220623072928.xlsx.gpg"
        survey_id = "141"
        period_id = "202203"
        ruref = "14112300153"
        size_bytes = 19
        md5sum = "3190f8a68aad6a9e33a624c318516ebb"

        # Create the fake Request object
        metadata = {
            'filename': input_filename,
            'md5sum': md5sum,
            'period': period_id,
            'ru_ref': ruref,
            'sizeBytes': size_bytes,
            'survey_id': survey_id,
            'tx_id': tx_id
        }

        files_dict = {
            METADATA_FILE: FileHolder(json.dumps(metadata).encode("utf-8")),
            SEFT_FILE: FileHolder(json.dumps("seft_file_contents").encode("utf-8")),
        }

        data = {
            FILE_NAME: input_filename,
            "tx_id": tx_id,
            MESSAGE_SCHEMA: V2
        }

        class MockRequest(Request):
            files = files_dict
            args = data

        # Call the endpoint
        response = deliver_seft(MockRequest(data), tx_id)
        self.assertTrue(response["success"])

        expected_v2_message: MessageSchemaV2 = {
            "schema_version": "2",
            "sensitivity": "High",
            "sizeBytes": size_bytes,
            "md5sum": md5sum,
            "context": {
                "survey_id": survey_id,
                "period_id": period_id,
                "ru_ref": ruref
            },
            "source": {
                "location_type": "gcs",
                "location_name": SDX_LOCATION_NAME,
                "path": "seft",
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
                            "path": "SDX_PREPROD/EDC_Submissions/141",
                            "filename": input_filename
                        }
                    ]
                }
            ]
        }

        mock_publish_v2_schema.assert_called_with(expected_v2_message, tx_id)
