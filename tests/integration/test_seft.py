import json
from typing import Self

from app.definitions.context_type import ContextType
from app.definitions.message_schema import MessageSchemaV2
from app.definitions.survey_type import SurveyType
from tests.integration.test_base import TestBase


class TestSeft(TestBase):

    def test_fdi(self: Self):
        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = "60226421137T_202112_062_20220920110706.xlsx.gpg"
        output_filename = "60226421137T_202112_062_20220920110706.xlsx"
        survey_id = "062"
        period_id = "202112"
        ru_ref = "60226421137"

        context = {
            "survey_type": SurveyType.SEFT,
            "context_type": ContextType.BUSINESS_SURVEY,
            "survey_id": survey_id,
            "period_id": period_id,
            "ru_ref": ru_ref,
            "tx_id": tx_id
        }

        response = self.client.post("/deliver/v2/seft",
                    params={
                        "filename": input_filename,
                        "context": json.dumps(context),
                        "tx_id": tx_id
                    },
                    files={"seft_file": b'file bytes'}
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
                "path": "seft",
                "filename": input_filename
            },
            "actions": ["decrypt"],
            "targets": [
                {
                    "input": input_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": "nifi-location-ftp",
                            "path": "SDX_PREPROD/EDC_Submissions/062",
                            "filename": output_filename
                        }
                    ]
                }
            ]
        }

        self.assertEqual(expected_v2_message, self.mock_gcp.get_message())

    def test_ashe(self: Self):
        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = "14112300153_202203_141_20220623072928.xlsx.gpg"
        output_filename = "14112300153_202203_141_20220623072928.xlsx"
        survey_id = "141"
        period_id = "202203"
        ru_ref = "14112300153"

        context = {
            "survey_type": SurveyType.SEFT,
            "context_type": ContextType.BUSINESS_SURVEY,
            "survey_id": survey_id,
            "period_id": period_id,
            "ru_ref": ru_ref,
            "tx_id": tx_id
        }

        response = self.client.post("/deliver/v2/seft",
                    params={
                        "filename": input_filename,
                        "context": json.dumps(context),
                        "tx_id": tx_id
                    },
                    files={"seft_file": b'file bytes'}
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
                "path": "seft",
                "filename": input_filename
            },
            "actions": ["decrypt"],
            "targets": [
                {
                    "input": input_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": "nifi-location-ns2",
                            "path": "s&e/ASHE/ASHE_Python_Submissions_TEST",
                            "filename": output_filename
                        }
                    ]
                }
            ]
        }

        self.assertEqual(expected_v2_message, self.mock_gcp.get_message())
