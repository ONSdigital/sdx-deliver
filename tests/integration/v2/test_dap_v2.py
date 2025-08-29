import io
import json
import unittest
import zipfile
from unittest.mock import patch, Mock

from sdx_gcp import Request

from app.v2 import deliver
from app.v2.definitions.context_type import ContextType
from app.v2.definitions.survey_type import SurveyType
from app.v2.routes import FILE_NAME, ZIP_FILE, CONTEXT, deliver_survey
from app.v2.definitions.message_schema import MessageSchemaV2
from tests.integration.v2 import MockLocationNameMapper, FileHolder, SDX_LOCATION_NAME, DAP_LOCATION_NAME


class TestDapV2(unittest.TestCase):

    @patch('app.v2.deliver.sdx_app.gcs_write')
    @patch('app.v2.deliver.publish_v2_message')
    @patch('app.v2.deliver.encrypt_output')
    @patch('app.v2.routes.Flask.jsonify')
    def test_dap(self,
                 mock_jsonify: Mock,
                 mock_encrypt: Mock,
                 mock_publish_v2_schema: Mock,
                 mock_write_to_bucket: Mock):
        deliver.location_name_repo = MockLocationNameMapper()
        mock_encrypt.return_value = "My encrypted output"
        mock_write_to_bucket.return_value = "My fake bucket path"
        mock_jsonify.return_value = {"success": True}

        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = tx_id
        output_filename = f'{tx_id}.json'
        survey_id = "283"
        period_id = "202505"
        ru_ref = "49900000001A"

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(output_filename, "This is the content of the json file.")

        zip_bytes = zip_buffer.getvalue()

        # Create the fake Request object

        files_dict = {
            ZIP_FILE: FileHolder(zip_bytes)
        }

        context = {
            "survey_type": SurveyType.DAP,
            "context_type": ContextType.BUSINESS_SURVEY,
            "tx_id": tx_id,
            "survey_id": survey_id,
            "period_id": period_id,
            "ru_ref": ru_ref,
        }

        data = {
            FILE_NAME: input_filename,
            "tx_id": tx_id,
            CONTEXT: json.dumps(context)
        }

        class MockRequest(Request):
            files = files_dict
            args = data

        # Call the endpoint
        response = deliver_survey(MockRequest(data), tx_id)
        self.assertTrue(response["success"])

        expected_v2_message: MessageSchemaV2 = {
            "schema_version": "2",
            "sensitivity": "High",
            "sizeBytes": 19,
            "md5sum": "3190f8a68aad6a9e33a624c318516ebb",
            "context": {
                "survey_id": survey_id,
                "period_id": period_id,
                "ru_ref": ru_ref,
                "context_type": ContextType.BUSINESS_SURVEY,
            },
            "source": {
                "location_type": "gcs",
                "location_name": SDX_LOCATION_NAME,
                "path": "survey",
                "filename": input_filename
            },
            "actions": ["decrypt", "unzip"],
            "targets": [
                {
                    "input": output_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": DAP_LOCATION_NAME,
                            "path": f"Covid_Survey/pre-prod/{survey_id}/{period_id}",
                            "filename": output_filename
                        }
                    ]
                }
            ]
        }

        mock_publish_v2_schema.assert_called_with(expected_v2_message, tx_id)
