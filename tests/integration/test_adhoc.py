import io
import json
import zipfile
from typing import Self

from app.definitions.context_type import ContextType
from app.definitions.message_schema import MessageSchemaV2
from app.definitions.survey_type import SurveyType
from tests.integration.test_base import TestBase


class TestAdhoc(TestBase):

    def test_adhoc(self: Self):
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

        response = self.client.post("/deliver/v2/adhoc",
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
                "location_name": "ons-sdx-sandbox-outputs",
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
                            "location_name": "nifi-location-cdp",
                            "path": "dapsen/landing_zone/ons/covid_resp_inf_surv_response/test/phm_740_health_insights_2024/v1/",
                            "filename": output_filename
                        }
                    ]
                }
            ]
        }

        self.assertEqual(expected_v2_message, self.mock_gcp.get_message())
