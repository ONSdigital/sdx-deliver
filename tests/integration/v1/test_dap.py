import json
import unittest
from unittest.mock import patch, Mock

from sdx_gcp import Request

from app.definitions import MessageSchema
from app.routes import FILE_NAME, VERSION, V2, SUBMISSION_FILE, deliver_dap, V1
from tests.integration.v1 import FileHolder


class DapTest(unittest.TestCase):

    @patch('app.deliver.write_to_bucket')
    @patch('app.deliver.publish_message')
    @patch('app.deliver.encrypt_output')
    @patch('app.message.get_formatted_current_utc')
    @patch('app.message.CONFIG')
    @patch('app.routes.Flask.jsonify')
    def test_dap_v1(self,
                    mock_jsonify: Mock,
                    mock_config: Mock,
                    mock_time: Mock,
                    mock_encrypt: Mock,
                    mock_publish_message: Mock,
                    mock_write_to_bucket: Mock):
        fake_path = "My fake bucket path"
        fake_time = "2021-10-10T08:42:24.737Z"
        fake_project = "ons-sdx-fake"
        mock_time.return_value = fake_time
        mock_config.PROJECT_ID = fake_project
        mock_config.DATA_SENSITIVITY = "High"
        mock_encrypt.return_value = "My encrypted output"
        mock_write_to_bucket.return_value = fake_path
        mock_jsonify.return_value = {"success": True}

        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        output_filename = f'{input_filename}.json:dap'
        survey_id = "283"
        period_id = "202505"
        ru_ref = "49900000001A"

        submission_file = {
            "origin": "uk.gov.ons.edc.eq",
            "started_at": "2020-03-23T10:45:54.331913",
            "submitted_at": "2020-03-23T10:49:52.869221",
            "survey_id": "283",
            "tx_id": tx_id,
            "type": "uk.gov.ons.edc.eq:surveyresponse",
            "version": "0.0.1",
            "case_id": "846b8188-8235-4025-a5ef-5b98c693d6f1",
            "flushed": False,
            "collection": {
                "exercise_sid": "cfee310c-082f-4c09-99af-46e14fb9ec71",
                "instrument_id": "0001",
                "period": period_id
            },
            "metadata": {
                "ref_period_end_date": "2016-05-31",
                "ref_period_start_date": "2016-05-01",
                "ru_ref": ru_ref,
                "user_id": "UNKNOWN"
            },
            "data": {
                "1": "Yes",
                "10": "Yes",
                "11": "Importing comment",
                "12": "It will get harder",
            }
        }

        # Create the fake Request object

        files_dict = {
            SUBMISSION_FILE: FileHolder(json.dumps(submission_file).encode("utf-8")),
        }

        data = {
            FILE_NAME: input_filename,
            VERSION: V1,
            "tx_id": tx_id,
        }

        class MockRequest(Request):
            files = files_dict
            args = data

        # Call the endpoint
        response = deliver_dap(MockRequest(data), tx_id)
        self.assertTrue(response["success"])

        expected_message: MessageSchema = {
            'version': '1',
            'files': [{
                'name': output_filename,
                'sizeBytes': 19,
                'md5sum': '3190f8a68aad6a9e33a624c318516ebb',
            }],
            'sensitivity': 'High',
            'sourceName': fake_project,
            'manifestCreated': fake_time,
            'description': f"{survey_id} survey response for period {period_id} sample unit {ru_ref}",
            'dataset': f'{survey_id}',
            'schemaversion': '1',
            'iterationL1': period_id
        }

        mock_publish_message.assert_called_with(expected_message, tx_id, fake_path)

    @patch('app.deliver.write_to_bucket')
    @patch('app.deliver.publish_message')
    @patch('app.deliver.encrypt_output')
    @patch('app.message.get_formatted_current_utc')
    @patch('app.message.CONFIG')
    @patch('app.routes.Flask.jsonify')
    def test_dap_v2(self,
                    mock_jsonify: Mock,
                    mock_config: Mock,
                    mock_time: Mock,
                    mock_encrypt: Mock,
                    mock_publish_message: Mock,
                    mock_write_to_bucket: Mock):
        fake_path = "My fake bucket path"
        fake_time = "2021-10-10T08:42:24.737Z"
        fake_project = "ons-sdx-fake"
        mock_time.return_value = fake_time
        mock_config.PROJECT_ID = fake_project
        mock_config.DATA_SENSITIVITY = "High"
        mock_encrypt.return_value = "My encrypted output"
        mock_write_to_bucket.return_value = fake_path
        mock_jsonify.return_value = {"success": True}

        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        output_filename = f'{input_filename}.json:dap'
        survey_id = "283"
        period_id = "202505"
        ru_ref = "49900000001A"

        submission_file = {
            "tx_id": tx_id,
            "type": "uk.gov.ons.edc.eq:surveyresponse",
            "version": "v2",
            "data_version": "0.0.3",
            "origin": "uk.gov.ons.edc.eq",
            "flushed": False,
            "submitted_at": "2016-05-21T16:37:56.551086",
            "launch_language_code": "en",
            "submission_language_code": "en",
            "collection_exercise_sid": "9ced8dc9-f2f3-49f3-95af-2f3ca0b74ee3",
            "schema_name": "bics_0001",
            "started_at": "2016-05-21T16:33:30.665144",
            "case_id": "a386b2de-a615-42c8-a0f4-e274f9eb28ee",
            "region_code": "GB-ENG",
            "channel": "RAS",
            "survey_metadata": {
                "survey_id": survey_id,
                "case_ref": "1000000000000001",
                "case_type": "B",
                "display_address": "ONS, Government Buildings, Cardiff Rd",
                "employment_date": "2021-03-01",
                "form_type": "0001",
                "period_id": period_id,
                "period_str": "January 2021",
                "ref_p_end_date": "2021-06-01",
                "ref_p_start_date": "2021-01-01",
                "ru_name": "ACME T&T Limited",
                "ru_ref": ru_ref,
                "trad_as": "ACME LTD.",
                "user_id": "64389274239"
            },
            "data": {
                "9999": "Yes, I can report for this period",
                "40": "12000",
                "146": "comment"
            }
        }

        # Create the fake Request object

        files_dict = {
            SUBMISSION_FILE: FileHolder(json.dumps(submission_file).encode("utf-8")),
        }

        data = {
            FILE_NAME: input_filename,
            VERSION: V2,
            "tx_id": tx_id,
        }

        class MockRequest(Request):
            files = files_dict
            args = data

        # Call the endpoint
        response = deliver_dap(MockRequest(data), tx_id)
        self.assertTrue(response["success"])

        expected_message: MessageSchema = {
            'version': '1',
            'files': [{
                'name': output_filename,
                'sizeBytes': 19,
                'md5sum': '3190f8a68aad6a9e33a624c318516ebb',
            }],
            'sensitivity': 'High',
            'sourceName': fake_project,
            'manifestCreated': fake_time,
            'description': f"{survey_id} survey response for period {period_id} sample unit {ru_ref}",
            'dataset': f'{survey_id}',
            'schemaversion': '1',
            'iterationL1': period_id
        }

        mock_publish_message.assert_called_with(expected_message, tx_id, fake_path)
