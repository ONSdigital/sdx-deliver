import unittest
from unittest.mock import patch, Mock

from app.meta_wrapper import MetaWrapperV2


class TestMetaWrapperV2(unittest.TestCase):

    business_v2 = {
        "case_id": "a9bf1f7c-3f86-407b-9a0f-86cc1c18e8b1",
        "tx_id": "04743704-e33d-4aef-9006-445d9dd31907",
        "type": "uk.gov.ons.edc.eq:surveyresponse",
        "version": "v2",
        "data_version": "0.0.1",
        "origin": "uk.gov.ons.edc.eq",
        "collection_exercise_sid": "8ad61a89-015f-4512-bf28-8381ff90bcae",
        "schema_name": "mbs_0106",
        "flushed": False,
        "submitted_at": "2023-01-12T14:53:00+00:00",
        "launch_language_code": "en",
        "survey_metadata": {
            "survey_id": "009",
            "trad_as": "ESSENTIAL ENTERPRISE LTD.",
            "ref_p_end_date": "2016-05-31",
            "ref_p_start_date": "2016-05-01",
            "ru_name": "ESSENTIAL ENTERPRISE LTD.",
            "user_id": "UNKNOWN",
            "ru_ref": "12346789012A",
            "period_id": "201605",
            "form_type": "0106"
        },
        "data": {"9999": "Yes, I can report for this period", "40": "28000", "146": "Very good survey!"},
        "started_at": "2023-01-12T14:52:30.136084+00:00",
        "submission_language_code": "en"
    }

    feedback_v2 = {
        "tx_id": "ea82c224-0f80-41cc-b877-8a7804b56c26",
        "type": "uk.gov.ons.edc.eq:surveyresponse",
        "version": "v2",
        "data_version": "0.0.1",
        "origin": "uk.gov.ons.edc.eq",
        "flushed": False,
        "submitted_at": "2016-05-21T16:37:56.551086",
        "launch_language_code": "en",
        "submission_language_code": "en",
        "collection_exercise_sid": "9ced8dc9-f2f3-49f3-95af-2f3ca0b74ee3",
        "schema_name": "mbs_0001",
        "started_at": "2016-05-21T16:33:30.665144",
        "case_id": "a386b2de-a615-42c8-a0f4-e274f9eb28ee",
        "region_code": "GB-ENG",
        "channel": "RAS",
        "survey_metadata": {
            "survey_id": "009",
            "case_ref": "1000000000000001",
            "case_type": "B",
            "display_address": "ONS, Government Buildings, Cardiff Rd",
            "employment_date": "2021-03-01",
            "form_type": "0253",
            "period_id": "202101",
            "period_str": "January 2021",
            "ref_p_end_date": "2021-06-01",
            "ref_p_start_date": "2021-01-01",
            "ru_name": "ACME T&T Limited",
            "ru_ref": "49900000001A",
            "trad_as": "ACME LTD.",
            "user_id": "64389274239"
        },
        "data": {
            "feedback_text": "Page design feedback",
            "feedback_type": "Page design and structure",
            "feedback_count": "7"
        }
    }

    def test_set_dap(self):
        filename = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        expected = "009 survey response for period 201605 sample unit 12346789012A"
        meta_data = MetaWrapperV2(filename)
        meta_data.set_dap(self.business_v2)
        actual = meta_data.get_description()
        self.assertEqual(expected, actual)
        self.assertEqual(f'{filename}.json:dap', meta_data.filename)

    def test_set_legacy(self):
        filename = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        expected = "009 survey response for period 201605 sample unit 12346789012A"
        meta_data = MetaWrapperV2(filename)
        meta_data.set_legacy(self.business_v2)
        actual = meta_data.get_description()
        self.assertEqual(expected, actual)
        self.assertEqual(f'{filename}:ftp', meta_data.filename)

    def test_set_hybrid(self):
        filename = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        expected = "009 survey response for period 201605 sample unit 12346789012A"
        meta_data = MetaWrapperV2(filename)
        meta_data.set_hybrid(self.business_v2)
        actual = meta_data.get_description()
        self.assertEqual(expected, actual)
        self.assertEqual(f'{filename}:hybrid', meta_data.filename)

    @patch('app.meta_wrapper.datetime')
    def test_set_feedback(self, mock_datetime):
        mock_today = Mock()
        mock_today.strftime.return_value = '15-47-27_05-09-2022'
        mock_datetime.today.return_value = mock_today
        filename = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        expected = "009 feedback response for period 202101 sample unit 49900000001A"
        meta_data = MetaWrapperV2(filename)
        meta_data.set_feedback(self.feedback_v2)
        actual = meta_data.get_description()
        self.assertEqual(expected, actual)
        self.assertEqual(f'{filename}-fb-15-47-27_05-09-2022:ftp', meta_data.filename)
