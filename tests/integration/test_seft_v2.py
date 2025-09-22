import json
import unittest

from typing import Self

from fastapi import FastAPI
from fastapi.testclient import TestClient

from sdx_base.server.server import create_app

from app.definitions.survey_type import SurveyType

from app.definitions.context_type import ContextType
from app.dependencies import get_settings, get_encryption_service, get_gcp_service
from app.routes import router
from tests.integration.mocks import MockSettings, MockEncryptor, MockGcp


class TestSeftV2(unittest.TestCase):

    def test_seft(self: Self):

        settings = MockSettings()
        app: FastAPI = create_app(app_name=settings.app_name,
                                  version=settings.app_version,
                                  routers=[router])

        app.dependency_overrides[get_settings] = MockSettings
        app.dependency_overrides[get_encryption_service] = MockEncryptor
        app.dependency_overrides[get_gcp_service] = MockGcp

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

        client = TestClient(app)
        response = client.post("/deliver/v2/seft",
                    params={
                        "filename": input_filename,
                        "context": json.dumps(context),
                        "tx_id": tx_id
                    },
                    files={"seft_file": b'file bytes'}
                    )


        print(response)

        # expected_v2_message: MessageSchemaV2 = {
        #     "schema_version": "2",
        #     "sensitivity": "High",
        #     "sizeBytes": size_bytes,
        #     "md5sum": md5sum,
        #     "context": {
        #         "survey_id": survey_id,
        #         "period_id": period_id,
        #         "ru_ref": ru_ref,
        #         "context_type": ContextType.BUSINESS_SURVEY,
        #     },
        #     "source": {
        #         "location_type": "gcs",
        #         "location_name": SDX_LOCATION_NAME,
        #         "path": "seft",
        #         "filename": input_filename
        #     },
        #     "actions": ["decrypt"],
        #     "targets": [
        #         {
        #             "input": input_filename,
        #             "outputs": [
        #                 {
        #                     "location_type": "windows_server",
        #                     "location_name": FTP_LOCATION_NAME,
        #                     "path": "SDX_PREPROD/EDC_Submissions/141",
        #                     "filename": output_filename
        #                 }
        #             ]
        #         }
        #     ]
        # }
        #
        # mock_publish_v2_schema.assert_called_with(expected_v2_message, tx_id)
