
import json
import unittest
from typing import Final
from unittest.mock import patch, Mock

from sdx_gcp import Request

from app import deliver
from app.routes import FILE_NAME, VERSION, V2, MESSAGE_SCHEMA, SUBMISSION_FILE, deliver_feedback
from app.v2.definitions.location_name_repository import LocationNameRepositoryBase, LookupKey
from app.v2.definitions.message_schema import SchemaDataV2
from app.v2.message_builder import BUSINESS_CONTEXT
from app.v2.submission_types.submission_type import SDX_PREPROD

SDX_LOCATION_NAME: Final[str] = "sdx_location_name"
FTP_LOCATION_NAME: Final[str] = "ftp_location_name"
SPP_LOCATION_NAME: Final[str] = "spp_location_name"
DAP_LOCATION_NAME: Final[str] = "dap_location_name"


class MockLocationNameMapper(LocationNameRepositoryBase):
    def __init__(self):
        self.locations_mapping = None

    def get_location_name(self, key: LookupKey) -> str:
        return self.locations_mapping[key.value]

    def load_location_values(self):
        ftp_key = LookupKey.FTP.value
        sdx_key = LookupKey.SDX.value
        spp_key = LookupKey.SPP.value
        dap_key = LookupKey.DAP.value
        self.locations_mapping = {
            ftp_key: FTP_LOCATION_NAME,
            sdx_key: SDX_LOCATION_NAME,
            spp_key: SPP_LOCATION_NAME,
            dap_key: DAP_LOCATION_NAME
        }


class FileHolder:

    def __init__(self, file_bytes: bytes):
        self._file_bytes = file_bytes

    def read(self) -> bytes:
        return self._file_bytes


class TestFeedbackV2(unittest.TestCase):

    @patch('app.deliver.write_to_bucket')
    @patch('app.deliver.publish_v2_schema')
    @patch('app.deliver.encrypt_output')
    @patch('app.routes.Flask.jsonify')
    @patch('app.meta_wrapper.get_current_time')
    def test_feedback_survey(self,
                             mock_get_current_time: Mock,
                             mock_jsonify: Mock,
                             mock_encrypt: Mock,
                             mock_publish_v2_schema: Mock,
                             mock_write_to_bucket: Mock):
        deliver.location_name_repo = MockLocationNameMapper()
        mock_encrypt.return_value = "My encrypted output"
        mock_write_to_bucket.return_value = "My fake bucket path"
        mock_jsonify.return_value = {"success": True}
        mock_get_current_time.return_value = "16-25-27_26-02-2025"

        tx_id = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        input_filename = tx_id
        output_filename = f'{tx_id}-fb-16-25-27_26-02-2025'
        survey_id = "009"
        period_id = "202505"

        # Create the input submission file
        submission_file = {
            "tx_id": tx_id,
            "type": "uk.gov.ons.edc.eq:feedback",
            "version": "v2",
            "data_version": "0.0.1",
            "origin": "uk.gov.ons.edc.eq",
            "flushed": False,
            "submitted_at": "2016-05-21T16:37:56.551086",
            "launch_language_code": "en",
            "submission_language_code": "en",
            "collection_exercise_sid": "9ced8dc9-f2f3-49f3-95af-2f3ca0b74ee3",
            "schema_name": "mbs_0001",
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
                "form_type": "0253",
                "period_id": period_id,
                "period_str": "January 2021",
                "ref_p_end_date": "2021-06-01",
                "ref_p_start_date": "2021-01-01",
                "ru_name": "ACME T&T Limited",
                "ru_ref": "49900000001A",
                "trad_as": "ACME LTD.",
                "user_id": "64389274239"
            },
            "data": {
                "feedback_rating": "Easy",
                "feedback_text": "Page design feedback"
            }
        }

        # Create the fake Request object

        files_dict = {
            SUBMISSION_FILE: FileHolder(json.dumps(submission_file).encode("utf-8")),
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
        response = deliver_feedback(MockRequest(data), tx_id)
        self.assertTrue(response["success"])

        expected_v2_message: SchemaDataV2 = {
            "schema_version": "2",
            "sensitivity": "High",
            "sizeBytes": 19,
            "md5sum": "3190f8a68aad6a9e33a624c318516ebb",
            "context": {
                "context_type": BUSINESS_CONTEXT,
                "survey_id": survey_id,
                "period_id": period_id,
                "ru_ref": "49900000001A"
            },
            "source": {
                "location_type": "gcs",
                "location_name": SDX_LOCATION_NAME,
                "path": "feedback",
                "filename": output_filename
            },
            "actions": ["decrypt"],
            "targets": [
                {
                    "input": output_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": FTP_LOCATION_NAME,
                            "path": f"{SDX_PREPROD}/EDC_QFeedback",
                            "filename": output_filename
                        }
                    ]
                }
            ]
        }

        mock_publish_v2_schema.assert_called_with(expected_v2_message, tx_id)
