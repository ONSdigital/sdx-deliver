import io
import json
import unittest
import zipfile
from unittest.mock import patch, Mock

from sdx_gcp import Request

from app.v2.definitions.context_type import ContextType
from app.v2.definitions.message_schema import MessageSchemaV2
from app.v2 import deliver
from app.v2.definitions.survey_type import SurveyType
from app.v2.routes import ZIP_FILE, FILE_NAME, CONTEXT, deliver_survey
from tests.integration.v2 import MockLocationNameMapper, FileHolder, SDX_LOCATION_NAME, FTP_LOCATION_NAME


class TestDextaV2(unittest.TestCase):

    @patch('app.v2.deliver.sdx_app.gcs_write')
    @patch('app.v2.deliver.publish_v2_message')
    @patch('app.v2.deliver.encrypt_output')
    @patch('app.v2.routes.Flask.jsonify')
    def test_dexta_survey(self,
                          mock_jsonify: Mock,
                          mock_encrypt: Mock,
                          mock_publish_v2_schema: Mock,
                          mock_write_to_bucket: Mock):
        deliver.location_name_repo = MockLocationNameMapper()
        mock_encrypt.return_value = "My encrypted output"
        mock_write_to_bucket.return_value = "My fake bucket path"
        mock_jsonify.return_value = {"success": True}

        tx_id = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        input_filename = tx_id
        tx_id_trunc = "c37a3efa-593c-4bab"
        survey_id = "073"
        period_id = "201605"
        ru_ref = "12346789012A"
        submission_date_str = "20210105"
        submission_date_dm = "0501"

        pck_filename = tx_id
        image_filename = f"S{tx_id_trunc}_1.JPG"
        index_filename = f"EDC_{survey_id}_{submission_date_str}_{tx_id_trunc}.csv"
        receipt_filename = f"REC{submission_date_dm}_{tx_id_trunc}.DAT"

        # Create the input zipfile
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(pck_filename, 'This is the content of the pck file.')
            zip_file.writestr(image_filename, 'This is the content of image file.')
            zip_file.writestr(index_filename, 'This is the content of index file.')
            zip_file.writestr(receipt_filename, 'This is the content of the receipt file.')

        zip_bytes = zip_buffer.getvalue()

        # Create the fake Request object

        files_dict = {
            ZIP_FILE: FileHolder(zip_bytes)
        }

        context = {
            "survey_type": SurveyType.DEXTA,
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
                    "input": pck_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": FTP_LOCATION_NAME,
                            "path": "SDX_PREPROD/SDC_QData",
                            "filename": pck_filename
                        }
                    ]
                },
                {
                    "input": image_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": FTP_LOCATION_NAME,
                            "path": "SDX_PREPROD/EDC_QImages/Images",
                            "filename": image_filename
                        }
                    ]
                },
                {
                    "input": index_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": FTP_LOCATION_NAME,
                            "path": "SDX_PREPROD/EDC_QImages/Index",
                            "filename": index_filename
                        }
                    ]
                },
                {
                    "input": receipt_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": FTP_LOCATION_NAME,
                            "path": "SDX_PREPROD/EDC_QReceipts",
                            "filename": receipt_filename
                        }
                    ]
                }
            ]
        }

        mock_publish_v2_schema.assert_called_with(expected_v2_message, tx_id)
