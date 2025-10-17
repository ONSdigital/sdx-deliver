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
from app.definitions.survey_type import SurveyType
from app.dependencies import get_settings, get_encryption_service, get_gcp_service
from app.routes import router
from tests.integration.mocks import MockSettings, get_mock_settings, get_mock_encryptor, get_mock_gcp


class TestMultiple(unittest.TestCase):

    def test_multiple(self: Self):
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

        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92c"
        context = {
            "survey_type": SurveyType.ADHOC,
            "context_type": ContextType.ADHOC_SURVEY,
            "tx_id": tx_id,
            "survey_id": survey_id,
            "title": title,
            "label": label,
        }

        response = client.post("/deliver/v2/adhoc",
                               params={
                                   "filename": input_filename,
                                   "context": json.dumps(context),
                                   "tx_id": tx_id
                               },
                               files={"zip_file": zip_bytes}
                               )

        self.assertTrue(response.is_success)
