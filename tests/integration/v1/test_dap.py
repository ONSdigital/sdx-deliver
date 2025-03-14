import json
import unittest
from typing import Final
from unittest.mock import patch, Mock

from sdx_gcp import Request

from app import deliver
from app.definitions import MessageSchema
from app.routes import FILE_NAME, VERSION, V2, SUBMISSION_FILE, MESSAGE_SCHEMA, deliver_dap, V1
from app.v2.definitions.message_schema import MessageSchemaV2
from tests.integration.v1 import FileHolder


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
        survey_id = "283"
        period_id = "202505"
        ruref = "49900000001A"

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
                "ru_ref": ruref,
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
            VERSION: V1,
            "tx_id": tx_id,
            MESSAGE_SCHEMA: V1
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
                'sizeBytes': 0,
                'md5sum': '',
            }],
            'sensitivity': 'High',
            'sourceName': '',
            'manifestCreated': '',
            'description': '',
            'dataset': '',
            'schemaversion': '1',
            'iterationL1': period_id
        }

        mock_publish_v2_schema.assert_called_with(expected_message, tx_id)
