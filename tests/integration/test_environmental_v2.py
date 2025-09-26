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
    NIFI_LOCATION_FTP, NIFI_LOCATION_NS5


class TestEnvironmentalV2(unittest.TestCase):

    def test_environmental_survey(self: Self):
        settings = MockSettings()
        setup_loggers(settings.app_name, settings.app_version, settings.logging_level)
        app: FastAPI = create_app(app_name=settings.app_name,
                                  version=settings.app_version,
                                  routers=[router])

        app.dependency_overrides[get_settings] = get_mock_settings
        app.dependency_overrides[get_encryption_service] = get_mock_encryptor
        app.dependency_overrides[get_gcp_service] = get_mock_gcp

        tx_id = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        input_filename = tx_id
        tx_id_trunc = "c37a3efa-593c-4bab"
        survey_id = "007"
        period_id = "201605"
        ru_ref = "12346789012A"
        submission_date_str = "20210105"
        submission_date_dm = "0501"

        json_filename = f"{survey_id}_{tx_id_trunc}.json"
        image_filename = f"S{tx_id_trunc}_1.JPG"
        index_filename = f"EDC_{survey_id}_{submission_date_str}_{tx_id_trunc}.csv"
        receipt_filename = f"REC{submission_date_dm}_{tx_id_trunc}.DAT"

        # Create the input zipfile
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(json_filename, 'This is the content of the json file.')
            zip_file.writestr(image_filename, 'This is the content of image file.')
            zip_file.writestr(index_filename, 'This is the content of index file.')
            zip_file.writestr(receipt_filename, 'This is the content of the receipt file.')

        zip_bytes = zip_buffer.getvalue()

        context = {
            "survey_type": SurveyType.ENVIRONMENTAL,
            "context_type": ContextType.BUSINESS_SURVEY,
            "tx_id": tx_id,
            "survey_id": survey_id,
            "period_id": period_id,
            "ru_ref": ru_ref,
        }

        client = TestClient(app)
        response = client.post("/deliver/v2/survey",
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
                "survey_id": survey_id,
                "period_id": period_id,
                "ru_ref": ru_ref,
                "context_type": ContextType.BUSINESS_SURVEY,
            },
            "source": {
                "location_type": "gcs",
                "location_name": settings.get_bucket_name(),
                "path": "survey",
                "filename": input_filename
            },
            "actions": ["decrypt", "unzip"],
            "targets": [
                {
                    "input": json_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": NIFI_LOCATION_NS5,
                            "path": f"lcres/LCRES_EQ_data/preprod/{period_id}/v1",
                            "filename": json_filename
                        }
                    ]
                },
                {
                    "input": image_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": NIFI_LOCATION_FTP,
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
                            "location_name": NIFI_LOCATION_FTP,
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
                            "location_name": NIFI_LOCATION_FTP,
                            "path": "SDX_PREPROD/EDC_QReceipts",
                            "filename": receipt_filename
                        }
                    ]
                }
            ]
        }

        self.assertEqual(expected_v2_message, MockGcp.get_message())
