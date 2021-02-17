import unittest
from unittest import mock

from app.publish import get_formatted_current_utc


class TestPublish(unittest.TestCase):

    # mocking utcnow() method
    def test_get_formatted_current_utc(self):
        # with freeze_time("2021-02-15"):
        #     assert datetime.datetime.now() != datetime.datetime(2021, 2, 15)
        with mock.patch('datetime.datetime') as date_mock:
            date_mock.utcnow.return_value = "2021-02-15T21:45:51.992Z"
            result = get_formatted_current_utc()