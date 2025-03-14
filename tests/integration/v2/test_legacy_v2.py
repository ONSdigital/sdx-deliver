import io
import json
import unittest
import zipfile
from unittest.mock import patch, Mock

from sdx_gcp import Request

from app import deliver
from app.routes import FILE_NAME, VERSION, V2, MESSAGE_SCHEMA, SUBMISSION_FILE, TRANSFORMED_FILE, deliver_legacy
from app.v2.definitions.message_schema import SchemaDataV2
from tests.integration.v2 import MockLocationNameMapper, FileHolder, SDX_LOCATION_NAME, FTP_LOCATION_NAME


class TestLegacyV2(unittest.TestCase):

    @patch('app.deliver.write_to_bucket')
    @patch('app.deliver.publish_v2_schema')
    @patch('app.deliver.encrypt_output')
    @patch('app.routes.Flask.jsonify')
    def test_legacy_survey(self,
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
        survey_id = "009"
        period_id = "201605"
        submission_date_str = "20210105"
        submission_date_dm = "0501"

        pck_filename = tx_id
        image_filename = f"S{tx_id_trunc}_1.JPG"
        index_filename = f"EDC_{survey_id}_{submission_date_str}_{tx_id_trunc}.csv"
        receipt_filename = f"REC{submission_date_dm}_{tx_id_trunc}.DAT"
        json_filename = f"{survey_id}_{tx_id_trunc}.json"

        # Create the input zipfile
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(pck_filename, 'This is the content of the pck file.')
            zip_file.writestr(image_filename, 'This is the content of image file.')
            zip_file.writestr(index_filename, 'This is the content of index file.')
            zip_file.writestr(receipt_filename, 'This is the content of the receipt file.')
            zip_file.writestr(json_filename, "This is the content of the json file.")

        zip_bytes = zip_buffer.getvalue()

        # Create the input submission file
        submission_file = {
            "case_id": "8fc3eb0b-2dd7-4acd-a354-5d4f69503233",
            "tx_id": tx_id,
            "type": "uk.gov.ons.edc.eq:surveyresponse",
            "version": "v2",
            "data_version": "0.0.1",
            "origin": "uk.gov.ons.edc.eq",
            "collection_exercise_sid": "44047ed7-2c7b-45d5-a7ad-31a05c6a5965",
            "schema_name": "mbs_0106",
            "flushed": False,
            "submitted_at": "2023-01-18T13:33:19+00:00",
            "launch_language_code": "en",
            "survey_metadata": {
                "survey_id": survey_id,
                "period_id": period_id,
                "ref_p_end_date": "2016-05-31",
                "trad_as": "ESSENTIAL ENTERPRISE LTD.",
                "ru_name": "ESSENTIAL ENTERPRISE LTD.",
                "ref_p_start_date": "2016-05-01",
                "ru_ref": "12346789012A",
                "user_id": "UNKNOWN",
                "form_type": "0106"
            },
            "data": {
                "9999": "Yes, I can report for this period",
                "40": "12000",
                "146": "comment"
            },
            "started_at": "2023-01-18T13:33:00.425419+00:00",
            "submission_language_code": "en"
        }

        # Create the fake Request object

        files_dict = {
            SUBMISSION_FILE: FileHolder(json.dumps(submission_file).encode("utf-8")),
            TRANSFORMED_FILE: FileHolder(zip_bytes)
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

        response = deliver_legacy(MockRequest(data), tx_id)
        self.assertTrue(response["success"])

        expected_v2_message: SchemaDataV2 = {
            "schema_version": "2",
            "sensitivity": "High",
            "sizeBytes": 19,
            "md5sum": "3190f8a68aad6a9e33a624c318516ebb",
            "context": {
                "survey_id": survey_id,
                "period_id": period_id,
                "ru_ref": "12346789012A"
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
                            "path": "SDX_PREPROD/EDC_QData",
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
                },
                {
                    "input": json_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": FTP_LOCATION_NAME,
                            "path": "SDX_PREPROD/EDC_QJson",
                            "filename": json_filename
                        }
                    ]
                }
            ]
        }

        mock_publish_v2_schema.assert_called_with(expected_v2_message, tx_id)
