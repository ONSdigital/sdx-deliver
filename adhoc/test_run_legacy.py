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


class TestRunLegacy(unittest.TestCase):

    def test_mbs(self: Self):
        os.environ["PROJECT_ID"] = "ons-sdx-nifi"
        os.environ["DATA_SENSITIVITY"] = "Low"
        os.environ["DATA_RECIPIENT"] = "ingest.service@ons.gov.uk"
        # os.environ["DATA_RECIPIENT"] = "dap@ons.gov.uk"
        proj_root = Path(__file__).parent.parent  # sdx-deliver dir

        app: FastAPI = run(Settings,
                           routers=[RouterConfig(router)],
                           proj_root=proj_root,
                           serve=lambda a, b: a
                           )

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
