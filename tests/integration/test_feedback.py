import io
import json
import zipfile
from typing import Self

from app.definitions.context_type import ContextType
from app.definitions.message_schema import MessageSchemaV2
from app.definitions.survey_type import SurveyType
from tests.integration.test_base import TestBase


class TestFeedback(TestBase):
    def test_feedback_survey(self: Self):
        tx_id = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        input_filename = tx_id
        output_filename = f"{tx_id}-fb-16-25-27_26-02-2025"
        survey_id = "009"
        period_id = "202505"
        ru_ref = "49900000001A"

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(output_filename, "This is the content of the feedback file.")

        zip_bytes = zip_buffer.getvalue()

        context = {
            "survey_type": SurveyType.FEEDBACK,
            "context_type": ContextType.BUSINESS_SURVEY,
            "tx_id": tx_id,
            "survey_id": survey_id,
            "period_id": period_id,
            "ru_ref": ru_ref,
        }

        response = self.client.post(
            "/deliver/v2/survey",
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
                "survey_id": survey_id,
                "period_id": period_id,
                "ru_ref": ru_ref,
                "context_type": ContextType.BUSINESS_SURVEY,
            },
            "source": {
                "location_type": "gcs",
                "location_name": "ons-sdx-sandbox-outputs",
                "path": "feedback",
                "filename": input_filename,
            },
            "actions": ["decrypt", "unzip"],
            "targets": [
                {
                    "input": output_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": "nifi-location-ftp",
                            "path": "SDX_PREPROD/EDC_QFeedback",
                            "filename": output_filename,
                        }
                    ],
                }
            ],
        }

        self.assertEqual(expected_v2_message, self.mock_gcp.get_message())

    def test_feedback_adhoc(self: Self):
        tx_id = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        input_filename = tx_id
        output_filename = f"{tx_id}-fb-16-25-27_26-02-2025"
        survey_id = "740"
        title = "covid_resp_inf_surv_response"
        label = "phm_740_health_insights_2024"

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(output_filename, "This is the content of the feedback file.")

        zip_bytes = zip_buffer.getvalue()

        context = {
            "survey_type": SurveyType.FEEDBACK,
            "context_type": ContextType.ADHOC_SURVEY,
            "tx_id": tx_id,
            "survey_id": survey_id,
            "title": title,
            "label": label,
        }

        response = self.client.post(
            "/deliver/v2/adhoc",
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
                "survey_id": survey_id,
                "title": title,
                "label": label,
                "context_type": ContextType.ADHOC_SURVEY,
            },
            "source": {
                "location_type": "gcs",
                "location_name": "ons-sdx-sandbox-outputs",
                "path": "feedback",
                "filename": input_filename,
            },
            "actions": ["decrypt", "unzip"],
            "targets": [
                {
                    "input": output_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": "nifi-location-ftp",
                            "path": "SDX_PREPROD/EDC_QFeedback",
                            "filename": output_filename,
                        }
                    ],
                }
            ],
        }

        self.assertEqual(expected_v2_message, self.mock_gcp.get_message())
