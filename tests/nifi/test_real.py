import hashlib
import io
import json
import unittest
import uuid
import zipfile

from sdx_gcp import Request

from app import setup_keys
from app.routes import FILE_NAME, VERSION, V2, MESSAGE_SCHEMA, SUBMISSION_FILE, deliver_feedback, ZIP_FILE, deliver_comments, METADATA_FILE, SEFT_FILE, \
    deliver_seft


class FileHolder:

    def __init__(self, file_bytes: bytes):
        self._file_bytes = file_bytes

    def read(self) -> bytes:
        return self._file_bytes


class TestRealV2(unittest.TestCase):

    def setUp(self):
        setup_keys()

    def test_feedback_survey(self):
        tx_id = str(uuid.uuid4())
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

    def test_comments(self):
        tx_id = str(uuid.uuid4())
        input_filename = "comments_test_3.zip"

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
        deliver_comments(MockRequest(data), tx_id)

    def test_seft(self):
        tx_id = str(uuid.uuid4())
        input_filename = "14112300153_202203_141_20220623072928.xlsx.gpg"

        file_contents = b"seft_file_contents"
        survey_id = "141"
        period_id = "202203"
        ruref = "14112300153"
        size_bytes = len(file_contents)
        md5sum = hashlib.md5(file_contents).hexdigest()

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
            SEFT_FILE: FileHolder(file_contents),
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
