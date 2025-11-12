import io
import json
import zipfile
from typing import Self

from app.definitions.context_type import ContextType
from app.definitions.message_schema import MessageSchemaV2
from app.definitions.survey_type import SurveyType
from tests.integration.test_base import TestBase


class TestEnvironmental(TestBase):
    def test_environmental_survey(self: Self):
        tx_id = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        input_filename = tx_id
        tx_id_trunc = "c37a3efa-593c-4bab"
        survey_id = "007"
        period_id = "201605"
        ru_ref = "12346789012A"
        submission_date_str = "20210105"
        submission_date_dm = "0501"

        json_filename = f"{survey_id}_{tx_id_trunc}.json"
        image_filename = f"S{tx_id_trunc}_1.JPG"
        index_filename = f"EDC_{survey_id}_{submission_date_str}_{tx_id_trunc}.csv"
        receipt_filename = f"REC{submission_date_dm}_{tx_id_trunc}.DAT"

        # Create the input zipfile
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(json_filename, "This is the content of the json file.")
            zip_file.writestr(image_filename, "This is the content of image file.")
            zip_file.writestr(index_filename, "This is the content of index file.")
            zip_file.writestr(receipt_filename, "This is the content of the receipt file.")

        zip_bytes = zip_buffer.getvalue()

        context = {
            "survey_type": SurveyType.ENVIRONMENTAL,
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
                    "input": json_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": "nifi-location-ns5",
                            "path": f"lcres/LCRES_EQ_data/preprod/{period_id}/v1",
                            "filename": json_filename,
                        }
                    ],
                },
                {
                    "input": image_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": "nifi-location-ftp",
                            "path": "SDX_PREPROD/EDC_QImages/Images",
                            "filename": image_filename,
                        }
                    ],
                },
                {
                    "input": index_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": "nifi-location-ftp",
                            "path": "SDX_PREPROD/EDC_QImages/Index",
                            "filename": index_filename,
                        }
                    ],
                },
                {
                    "input": receipt_filename,
                    "outputs": [
                        {
                            "location_type": "windows_server",
                            "location_name": "nifi-location-ftp",
                            "path": "SDX_PREPROD/EDC_QReceipts",
                            "filename": receipt_filename,
                        }
                    ],
                },
            ],
        }

        self.assertEqual(expected_v2_message, self.mock_gcp.get_message())
