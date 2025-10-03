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
    NIFI_LOCATION_CDP


class TestAdhocV2(unittest.TestCase):

    def test_adhoc(self: Self):
        settings = MockSettings()
        setup_loggers(settings.app_name, settings.app_version, settings.logging_level)
        app: FastAPI = create_app(app_name=settings.app_name,
                                  version=settings.app_version,
                                  routers=[router])

        app.dependency_overrides[get_settings] = get_mock_settings
        app.dependency_overrides[get_encryption_service] = get_mock_encryptor
        app.dependency_overrides[get_gcp_service] = get_mock_gcp

        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = tx_id
        output_filename = f'{tx_id}.json'
        survey_id = "740"
        title = "covid_resp_inf_surv_response"
        label = "phm_740_health_insights_2024"

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(output_filename, "This is the content of the json file.")

        zip_bytes = zip_buffer.getvalue()

        context = {
            "survey_type": SurveyType.ADHOC,
            "context_type": ContextType.ADHOC_SURVEY,
            "tx_id": tx_id,
            "survey_id": survey_id,
            "title": title,
            "label": label,
        }

        client = TestClient(app)
        response = client.post("/deliver/v2/adhoc",
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
                "title": title,
                "label": label,
                "context_type": ContextType.ADHOC_SURVEY,
            },
            "source": {
                "location_type": "gcs",
                "location_name": settings.get_bucket_name(),
                "path": "survey",
                "filename": input_filename
            },
            "actions": ["decrypt", "unzip", "batch"],
            "targets": [
                {
                    "input": output_filename,
                    "outputs": [
                        {
                            "location_type": "cdp",
                            "location_name": NIFI_LOCATION_CDP,
                            "path": "dapsen/landing_zone/ons/covid_resp_inf_surv_response/prod/phm_740_health_insights_2024/v1/",
                            "filename": output_filename
                        }
                    ]
                }
            ]
        }

        self.assertEqual(expected_v2_message, MockGcp.get_message())
