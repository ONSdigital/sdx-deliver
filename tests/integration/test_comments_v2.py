import io
import json
import unittest
import zipfile
from typing import Self

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sdx_base.run import setup_loggers
from sdx_base.server.server import create_app

from app.definitions.context_type import ContextType
from app.definitions.message_schema import MessageSchemaV2
from app.definitions.survey_type import SurveyType
from app.dependencies import get_settings, get_encryption_service, get_gcp_service
from app.routes import router
from tests.integration.mocks import MockSettings, get_mock_settings, get_mock_encryptor, get_mock_gcp, MockGcp, \
    NIFI_LOCATION_FTP


class TestCommentsV2(unittest.TestCase):

    def test_comments(self: Self):
        settings = MockSettings()
        setup_loggers(settings.app_name, settings.app_version, settings.logging_level)
        app: FastAPI = create_app(app_name=settings.app_name,
                                  version=settings.app_version,
                                  routers=[router])

        app.dependency_overrides[get_settings] = get_mock_settings
        app.dependency_overrides[get_encryption_service] = get_mock_encryptor
        app.dependency_overrides[get_gcp_service] = get_mock_gcp

        tx_id = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        input_filename = "2025-01-01.zip"

        # Create the input zipfile
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("file1", 'Some comments.')
            zip_file.writestr("file2", 'Some more comments.')
            zip_file.writestr("file3", 'Even more comments!')

        zip_bytes = zip_buffer.getvalue()

        context = {
            "survey_type": SurveyType.COMMENTS,
            "tx_id": tx_id,
            "title": "Comments.zip",
            "context_type": ContextType.COMMENTS_FILE,
        }

        client = TestClient(app)
        response = client.post("/deliver/v2/comments",
                               params={
                                   "filename": input_filename,
                                   "context": json.dumps(context),
                                   "tx_id": tx_id
                               },
                               files={"zip_file": zip_bytes}
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
                "location_name": settings.get_bucket_name(),
                "path": "comments",
                "filename": input_filename
            },
            "actions": ["decrypt"],
            "targets": [
                {
                    "input": input_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": NIFI_LOCATION_FTP,
                            "path": "SDX_PREPROD/EDC_Submissions/Comments",
                            "filename": input_filename
                        }
                    ]
                }
            ]
        }

        self.assertEqual(expected_v2_message, MockGcp.get_message())
