import unittest

from app.meta_wrapper import MetaWrapperV2


class TestMetaWrapperV2(unittest.TestCase):

    test_business_v2 = {
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

    def test_set_dap(self):
        filename = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        expected = "009 survey response for period 201605 sample unit 12346789012A"
        meta_data = MetaWrapperV2(filename)
        meta_data.set_dap(self.test_business_v2)
        actual = meta_data.get_description()
        self.assertEqual(expected, actual)
        self.assertEqual(f'{filename}.json:dap', meta_data.filename)

    def test_set_legacy(self):
        filename = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        expected = "009 survey response for period 201605 sample unit 12346789012A"
        meta_data = MetaWrapperV2(filename)
        meta_data.set_legacy(self.test_business_v2)
        actual = meta_data.get_description()
        self.assertEqual(expected, actual)
        self.assertEqual(f'{filename}:ftp', meta_data.filename)

    def test_set_hybrid(self):
        filename = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        expected = "009 survey response for period 201605 sample unit 12346789012A"
        meta_data = MetaWrapperV2(filename)
        meta_data.set_hybrid(self.test_business_v2)
        actual = meta_data.get_description()
        self.assertEqual(expected, actual)
        self.assertEqual(f'{filename}:hybrid', meta_data.filename)
