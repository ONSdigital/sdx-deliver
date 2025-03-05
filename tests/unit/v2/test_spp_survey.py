import unittest

from app.v2.submission_types.spp_survey import is_spp_json_filename


class TestSppSubmissionType(unittest.TestCase):
    def test_is_spp_json_filename(self):
        spp_filename = "123_SDC_2021-01-01T01-01-01_c37a3efa-593c-4bab-b49c-bee0613c4fb2.json"

        self.assertTrue(is_spp_json_filename(spp_filename))

    def test_is_not_spp_json_filename(self):
        spp_filename = "c37a3efa-593c-4bab-b49c-bee0613c4fb2.json"

        self.assertFalse(is_spp_json_filename(spp_filename))

    def test_is_not_json_filename(self):
        spp_filename = "123_SDC_2021-01-01T01-01-01_c37a3efa-593c-4bab-b49c-bee0613c4fb2.jpg"

        self.assertFalse(is_spp_json_filename(spp_filename))
