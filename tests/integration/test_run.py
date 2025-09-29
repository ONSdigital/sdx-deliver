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

from app.definitions.context_type import ContextType
from app.definitions.survey_type import SurveyType
from app.dependencies import get_encryption_service, get_gcp_service
from app.routes import router
from app.settings import Settings
from tests.integration.mocks import get_mock_encryptor, get_mock_gcp, NIFI_LOCATION_FTP


class MockSecretReader:

    def get_secret(self, _project_id: str, secret_id: str) -> str:
        if secret_id == "dap-public-gpg":
            return "mock key"
        elif secret_id == "nifi-location-ftp":
            return NIFI_LOCATION_FTP
        else:
            return ""


class TestRun(unittest.TestCase):

    def test_run(self: Self):
        os.environ["PROJECT_ID"] = "my-project"
        os.environ["DATA_SENSITIVITY"] = "Low"
        os.environ["DATA_RECIPIENT"] = "mock-recipient"
        proj_root = Path(__file__).parent.parent.parent  # sdx-deliver dir

        app: FastAPI = run(Settings,
                           routers=[router],
                           proj_root=proj_root,
                           secret_reader=MockSecretReader(),
                           serve=lambda a, b: a
                           )

        app.dependency_overrides[get_encryption_service] = get_mock_encryptor
        app.dependency_overrides[get_gcp_service] = get_mock_gcp

        tx_id = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        input_filename = tx_id
        tx_id_trunc = "c37a3efa-593c-4bab"
        survey_id = "009"
        period_id = "201605"
        ru_ref = "12346789012A"
        submission_date_str = "20210105"
        submission_date_dm = "0501"

        pck_filename = tx_id
        image_filename = f"S{tx_id_trunc}_1.JPG"
        index_filename = f"EDC_{survey_id}_{submission_date_str}_{tx_id_trunc}.csv"
        receipt_filename = f"REC{submission_date_dm}_{tx_id_trunc}.DAT"

        # Create the input zipfile
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(pck_filename, 'This is the content of the pck file.')
            zip_file.writestr(image_filename, 'This is the content of image file.')
            zip_file.writestr(index_filename, 'This is the content of index file.')
            zip_file.writestr(receipt_filename, 'This is the content of the receipt file.')

        zip_bytes = zip_buffer.getvalue()

        context = {
            "survey_type": SurveyType.LEGACY,
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