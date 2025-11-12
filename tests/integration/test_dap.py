import io
import json
import zipfile
from typing import Self

from app.definitions.context_type import ContextType
from app.definitions.message_schema import MessageSchemaV2
from app.definitions.survey_type import SurveyType
from tests.integration.test_base import TestBase


class TestDap(TestBase):
    def test_dap(self: Self):
        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = tx_id
        output_filename = f"{tx_id}.json"
        survey_id = "283"
        period_id = "202505"
        ru_ref = "49900000001A"

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(output_filename, "This is the content of the json file.")

        zip_bytes = zip_buffer.getvalue()

        context = {
            "survey_type": SurveyType.DAP,
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
                "path": "survey",
                "filename": input_filename,
            },
            "actions": ["decrypt", "unzip"],
            "targets": [
                {
                    "input": output_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": "nifi-location-dap",
                            "path": f"Covid_Survey/pre-prod/{survey_id}/{period_id}/v1",
                            "filename": output_filename,
                        }
                    ],
                }
            ],
        }

        self.assertEqual(expected_v2_message, self.mock_gcp.get_message())
