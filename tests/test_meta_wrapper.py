import unittest

from app.meta_wrapper import MetaWrapper
from app.output_type import OutputType


class TestMetaWrapper(unittest.TestCase):

    test_data = {
            "collection": {
                "exercise_sid": "XxsteeWv",
                "instrument_id": "0167",
                "period": "2019"
            },
            "data": {
                "46": "123",
                "47": "456",
                "50": "789",
                "51": "111",
                "52": "222",
                "53": "333",
                "54": "444",
                "146": "different comment.",
                "d12": "Yes",
                "d40": "Yes"
            },
            "flushed": False,
            "metadata": {
                "ref_period_end_date": "2016-05-31",
                "ref_period_start_date": "2016-05-01",
                "ru_ref": "49900108249D",
                "user_id": "UNKNOWN"
            },
            "origin": "uk.gov.ons.edc.eq",
            "started_at": "2017-07-05T10:54:11.548611+00:00",
            "submitted_at": "2017-07-05T14:49:33.448608+00:00",
            "type": "uk.gov.ons.edc.eq:surveyresponse",
            "version": "0.0.1",
            "survey_id": "009",
            "tx_id": "c37a3efa-593c-4bab-b49c-bee0613c4fb2",
            "case_id": "4c0bc9ec-06d4-4f66-88b6-2e42b79f17b3"
        }

    def test_dap_description(self):
        filename = "9010576d-f3df-4011-aa41-adecd9bee011"
        expected = "023 survey response for period 0216 sample unit 12345"
        meta_data = MetaWrapper(filename)
        meta_data.output_type = OutputType.DAP
        meta_data.survey_id = "023"
        meta_data.period = "0216"
        meta_data.ru_ref = "12345"
        actual = meta_data.get_description()
        self.assertEqual(expected, actual)