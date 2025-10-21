import io
import json
import os
import unittest
import zipfile
from pathlib import Path
from typing import Self

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sdx_base.run import run
from sdx_base.server.server import RouterConfig

from app.definitions.context_type import ContextType
from app.definitions.survey_type import SurveyType
from app.routes import router
from app.settings import Settings


class TestRun(unittest.TestCase):

    def test_run(self: Self):
        os.environ["PROJECT_ID"] = "ons-sdx-nifi"
        os.environ["DATA_SENSITIVITY"] = "Low"
        # os.environ["DATA_RECIPIENT"] = "ingest.service@ons.gov.uk"
        os.environ["DATA_RECIPIENT"] = "dap@ons.gov.uk"
        proj_root = Path(__file__).parent.parent  # sdx-deliver dir

        app: FastAPI = run(Settings,
                           routers=[RouterConfig(router)],
                           proj_root=proj_root,
                           serve=lambda a, b: a
                           )

        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92c"
        input_filename = tx_id
        output_filename = f'{tx_id}.json'
        survey_id = "740"
        title = "covid_resp_inf_surv_response"
        label = "phm_740_health_insights_2024"

        submission = {
            "case_id": "6b7fe1d3-b8a9-406e-a521-5a8dd2f86b28",
            "tx_id": tx_id,
            "type": "uk.gov.ons.edc.eq:surveyresponse",
            "version": "v2",
            "data_version": "0.0.3",
            "origin": "uk.gov.ons.edc.eq",
            "collection_exercise_sid": "97f4b3e2-5b5f-4bc2-a361-b4b1183afe81",
            "schema_name": "wcis_0001",
            "flushed": False,
            "submitted_at": "2023-03-21T10:08:37+00:00",
            "launch_language_code": "en",
            "survey_metadata": {
                "survey_id": "740",
                "BLOOD_TEST_BARCODE": "",
                "SWAB_TEST_BARCODE": "SWT33333333",
                "FIRST_NAME": "Bradley",
                "qid": "0130000001408548",
                "PARTICIPANT_ID": "DHR-11111111111",
                "PORTAL_ID": "1111111",
                "PARTICIPANT_WINDOW_ID": "DHR-11111111111-000",
                "TEST_QUESTIONS": "T",
                "WINDOW_CLOSE_DATE": "2023-02-03",
                "WINDOW_START_DATE": "2023-01-20"
            },
            "data": {
                "answers": [
                    {
                        "answer_id": "answerbbdb0b77-e4d2-4a94-bb52-c7b6e91ab850",
                        "value": "No"
                    },
                    {
                        "answer_id": "answer3cbbbc81-3d85-4eca-b230-9a24e7203f38",
                        "value": "No"
                    },
                    {
                        "answer_id": "answer3d3e4020-8795-444f-98e4-057ec571ec07",
                        "value": ["Continue"]
                    }
                ],
                "lists": [],
                "answer_codes": [
                    {
                        "answer_id": "answerbbdb0b77-e4d2-4a94-bb52-c7b6e91ab850",
                        "code": "PHM-FUP-INT-003"
                    },
                    {
                        "answer_id": "answer3cbbbc81-3d85-4eca-b230-9a24e7203f38",
                        "code": "PHM-FUP-INT-004"
                    },
                    {
                        "answer_id": "answer3d3e4020-8795-444f-98e4-057ec571ec07",
                        "code": "PHM-FUP-INT-005"
                    }
                ]
            },
            "channel": "RH",
            "started_at": "2023-03-21T10:08:32.556293+00:00",
            "submission_language_code": "en"
        }

        # Create the input zipfile
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(output_filename, json.dumps(submission))

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
