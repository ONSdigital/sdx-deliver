import io
import json
import unittest
import zipfile
from unittest.mock import patch, Mock

from sdx_gcp import Request

from app import deliver
from app.routes import FILE_NAME, VERSION, V2, MESSAGE_SCHEMA, SUBMISSION_FILE, TRANSFORMED_FILE, deliver_legacy
from app.v2.definitions.location_name_repository import LocationNameRepositoryBase
from app.v2.message_config import FTP, SDX, SPP, DAP


class MockLocationNameMapper(LocationNameRepositoryBase):
    def get_location_name(self, key: str) -> str:
        return self.locations_mapping[key]

    def load_location_values(self):
        self.locations_mapping = {
            FTP: "ftp_location_name",
            SDX: "sdx_location_name",
            SPP: "spp_location_name",
            DAP: "dap_location_name"
        }


class FileHolder:

    def __init__(self, file_bytes: bytes):
        self._file_bytes = file_bytes

    def read(self) -> bytes:
        return self._file_bytes


class TestMbsV2(unittest.TestCase):

    @patch('app.deliver.write_to_bucket')
    @patch('app.deliver.publish_v2_schema')
    @patch('app.deliver.encrypt_output')
    def test_legacy_survey(self, mock_encrypt: Mock, mock_publish_v2_schema, mock_write_to_bucket: Mock):
        deliver.location_name_mapper = MockLocationNameMapper()
        mock_encrypt.return_value = "My encrypted output"
        mock_write_to_bucket.return_value = "My fake bucket path"

        tx_id = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        tx_id_trunc = "c37a3efa-593c-4bab"
        survey_id = "009"
        submission_date_str = "20210105"
        submission_date_dm = "0501"
        data = {
            FILE_NAME: tx_id,
            "tx_id": tx_id,
            VERSION: V2,
            MESSAGE_SCHEMA: V2
        }
        zip_buffer = io.BytesIO()

        # Create a new zip file in the BytesIO object
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add files to the zip file
            zip_file.writestr(tx_id, 'This is the content of the pck file.')
            zip_file.writestr(f"S{tx_id_trunc}_1.JPG", 'This is the content of image file.')
            zip_file.writestr(f"EDC_{survey_id}_{submission_date_str}_{tx_id_trunc}.csv", 'This is the content of index file.')
            zip_file.writestr(f"REC{submission_date_dm}_{tx_id_trunc}.DAT", 'This is the content of the receipt file.')
            zip_file.writestr(f"{survey_id}_{tx_id_trunc}.json", "This is the content of the json file.")

        # Get the bytes of the zip file
        zip_bytes = zip_buffer.getvalue()

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
                "period_id": "201605",
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
        
        files_dict = {
            SUBMISSION_FILE: FileHolder(json.dumps(submission_file).encode("utf-8")),
            TRANSFORMED_FILE: FileHolder(zip_bytes)
        }

        class MockRequest(Request):

            files = files_dict
            args = {
                FILE_NAME: tx_id,
                "tx_id": tx_id,
                VERSION: V2,
                MESSAGE_SCHEMA: V2
            }

        #response = deliver_legacy(MockRequest(data), tx_id)
