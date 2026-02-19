import json
from typing import Self
from fastapi.testclient import TestClient

from app.definitions.context_type import ContextType
from app.definitions.message_schema import MessageSchemaV2
from app.definitions.survey_type import SurveyType
from tests.integration.test_base import TestBase


class TestSeft(TestBase):
    def set_context(self: Self, survey_id: str, period_id: str, ru_ref: str, tx_id: str) -> dict:
        return {
            "survey_type": SurveyType.SEFT,
            "context_type": ContextType.BUSINESS_SURVEY,
            "survey_id": survey_id,
            "period_id": period_id,
            "ru_ref": ru_ref,
            "tx_id": tx_id
        }

    def post_seft(self: Self, client: TestClient, input_filename: str, context: dict, tx_id: str):
        return client.post("/deliver/v2/seft",
                                    params={
                                        "filename": input_filename,
                                        "context": json.dumps(context),
                                        "tx_id": tx_id
                                    },
                                    files={"seft_file": b'file bytes'}
                                    )

    def test_057_itis(self: Self):
        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = "11110000005H_202206_057_20230518102856.xlsx.gpg"
        output_filename = "11110000005H_202206_057_20230518102856.xlsx"
        survey_id = "057"
        period_id = "202206"
        ru_ref = "11110000005"

        context = self.set_context(survey_id, period_id, ru_ref, tx_id)

        response = self.post_seft(self.client, input_filename, context, tx_id)

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
                            "location_name": "nifi-location-ns3",
                            "path": "OF1/ITIS/ITIS_SDB/Submissions_PreProd",
                            "filename": output_filename
                        }
                    ]
                }
            ]
        }

        self.assertEqual(expected_v2_message, self.mock_gcp.get_message())

    def test_062_fdi(self: Self):
        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = "60226421137T_202112_062_20220920110706.xlsx.gpg"
        output_filename = "60226421137T_202112_062_20220920110706.xlsx"
        survey_id = "062"
        period_id = "202112"
        ru_ref = "60226421137"

        context = self.set_context(survey_id, period_id, ru_ref, tx_id)

        response = self.post_seft(self.client, input_filename, context, tx_id)

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

    def test_063_fdi(self: Self):
        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = "60226421137T_202112_062_20220920110706.xlsx.gpg"
        output_filename = "60226421137T_202112_062_20220920110706.xlsx"
        survey_id = "063"
        period_id = "202112"
        ru_ref = "60226421137"

        context = self.set_context(survey_id, period_id, ru_ref, tx_id)

        response = self.post_seft(self.client, input_filename, context, tx_id)

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
                            "path": "SDX_PREPROD/EDC_Submissions/063",
                            "filename": output_filename
                        }
                    ]
                }
            ]
        }

        self.assertEqual(expected_v2_message, self.mock_gcp.get_message())

    def test_066_qsl(self: Self):
        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = "49910391699T_202306_066_20230605121256.xlsx.gpg"
        output_filename = "49910391699T_202306_066_20230605121256.xlsx"
        survey_id = "066"
        period_id = "202306"
        ru_ref = "49910391699"

        context = self.set_context(survey_id, period_id, ru_ref, tx_id)

        response = self.post_seft(self.client, input_filename, context, tx_id)

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
                            "path": "BDD_OGD/Submissions_PreProd",
                            "filename": output_filename
                        }
                    ]
                }
            ]
        }

        self.assertEqual(expected_v2_message, self.mock_gcp.get_message())

    def test_141_ashe(self: Self):
        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = "14112300153_202203_141_20220623072928.xlsx.gpg"
        output_filename = "14112300153_202203_141_20220623072928.xlsx"
        survey_id = "141"
        period_id = "202203"
        ru_ref = "14112300153"

        context = self.set_context(survey_id, period_id, ru_ref, tx_id)

        response = self.post_seft(self.client, input_filename, context, tx_id)

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