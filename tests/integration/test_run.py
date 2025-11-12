import io
import json
import zipfile
from typing import Self, Final

from app.definitions.context_type import ContextType
from app.definitions.survey_type import SurveyType
from tests.integration.test_base import TestBase


_tx_id: Final[str] = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
_input_filename: Final[str] = _tx_id


class TestRun(TestBase):
    def get_zip_and_context(self: Self) -> tuple[bytes, dict[str, str]]:
        survey_id = "009"
        period_id = "201605"
        ru_ref = "12346789012A"
        submission_date_str = "20210105"
        submission_date_dm = "0501"

        pck_filename: str = _tx_id
        tx_id_trunc = "c37a3efa-593c-4bab"
        image_filename = f"S{tx_id_trunc}_1.JPG"
        index_filename = f"EDC_{survey_id}_{submission_date_str}_{tx_id_trunc}.csv"
        receipt_filename = f"REC{submission_date_dm}_{tx_id_trunc}.DAT"

        # Create the input zipfile
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(pck_filename, "This is the content of the pck file.")
            zip_file.writestr(image_filename, "This is the content of image file.")
            zip_file.writestr(index_filename, "This is the content of index file.")
            zip_file.writestr(receipt_filename, "This is the content of the receipt file.")

        zip_bytes = zip_buffer.getvalue()

        context = {
            "survey_type": SurveyType.LEGACY,
            "context_type": ContextType.BUSINESS_SURVEY,
            "tx_id": _tx_id,
            "survey_id": survey_id,
            "period_id": period_id,
            "ru_ref": ru_ref,
        }

        return zip_bytes, context

    def test_run_success(self: Self):
        zip_bytes, context = self.get_zip_and_context()
        response = self.client.post(
            "/deliver/v2/survey",
            params={"filename": _input_filename, "context": json.dumps(context), "tx_id": _tx_id},
            files={"zip_file": zip_bytes},
        )

        self.assertTrue(response.is_success)

    def test_run_fail_on_bad_context(self: Self):
        zip_bytes, context = self.get_zip_and_context()
        del context["survey_id"]

        response = self.client.post(
            "/deliver/v2/survey",
            params={"filename": _input_filename, "context": json.dumps(context), "tx_id": _tx_id},
            files={"zip_file": zip_bytes},
        )

        self.assertFalse(response.is_success)
        self.assertEqual(400, response.status_code)

    def test_run_fail_on_bad_zip_file(self: Self):
        _, context = self.get_zip_and_context()
        response = self.client.post(
            "/deliver/v2/survey",
            params={"filename": _input_filename, "context": json.dumps(context), "tx_id": _tx_id},
            files={"zip_file": b"nothing to see here!"},
        )

        self.assertFalse(response.is_success)
        self.assertEqual(400, response.status_code)
