import io
import json
import zipfile
from typing import Self

from app.definitions.context_type import ContextType
from app.definitions.message_schema import MessageSchemaV2
from app.definitions.survey_type import SurveyType
from tests.integration.test_base import TestBase


class TestComments(TestBase):
    def test_comments(self: Self):
        tx_id = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        input_filename = "2025-01-01.zip"

        # Create the input zipfile
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("file1", "Some comments.")
            zip_file.writestr("file2", "Some more comments.")
            zip_file.writestr("file3", "Even more comments!")

        zip_bytes = zip_buffer.getvalue()

        context = {
            "survey_type": SurveyType.COMMENTS,
            "tx_id": tx_id,
            "title": "Comments.zip",
            "context_type": ContextType.COMMENTS_FILE,
        }

        response = self.client.post(
            "/deliver/v2/comments",
            params={"filename": input_filename, "context": json.dumps(context), "tx_id": tx_id},
            files={"zip_file": zip_bytes},
        )

        self.assertTrue(response.is_success)

        expected_v2_message: MessageSchemaV2 = {
            "schema_version": "2",
            "sensitivity": "Low",
            "sizeBytes": 10,
            "md5sum": "md5sum",
            "context": {
                "title": "Comments.zip",
                "context_type": ContextType.COMMENTS_FILE,
            },
            "source": {
                "location_type": "gcs",
                "location_name": "ons-sdx-sandbox-outputs",
                "path": "comments",
                "filename": input_filename,
            },
            "actions": ["decrypt"],
            "targets": [
                {
                    "input": input_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": "nifi-location-ftp",
                            "path": "SDX_PREPROD/EDC_Submissions/Comments",
                            "filename": input_filename,
                        }
                    ],
                }
            ],
        }

        self.assertEqual(expected_v2_message, self.mock_gcp.get_message())
