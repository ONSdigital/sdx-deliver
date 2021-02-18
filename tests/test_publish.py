import json
import unittest
from unittest import mock
from unittest.mock import patch

from google.cloud import pubsub_v1

from app import app
from app.meta_wrapper import MetaWrapper
from app.publish import get_formatted_current_utc, send_message, create_message_data, publish_data


class TestPublish(unittest.TestCase):

    # mocking utcnow() method
    def test_get_formatted_current_utc(self):
        # with freeze_time("2021-02-15"):
        #     assert datetime.datetime.now() != datetime.datetime(2021, 2, 15)
        with mock.patch('datetime.datetime') as date_mock:
            date_mock.utcnow.return_value = "2021-02-15T21:45:51.992Z"
            result = get_formatted_current_utc()

    def test_create_message_data(self):
        filename = "9010576d-f3df-4011-aa41-adecd9bee011"
        meta_data = MetaWrapper(filename)
        actual = create_message_data(meta_data)
        expected = {
            'version': '1',
            'files': [{
                'name': "9010576d-f3df-4011-aa41-adecd9bee011",
                'sizeBytes': 5,
                'md5sum': "4b3a6218bb3e3a7303e8a171a60fcf92"
            }],
            'sensitivity': 'High',
            'sourceName': "ons-sdx-sandbox",
            'manifestCreated': self.test_get_formatted_current_utc(),
            'description': "message",
            'iterationL1': None,
            'dataset': "dataset",
            'schemaversion': '1'
        }
        self.assertEqual(actual, json.dumps(expected))

    # @patch('app.publish.publish_data')
    def test_publish_data(self):
        dap_publisher = pubsub_v1.PublisherClient()
        dap_topic_path = dap_publisher.topic_path('ons-sdx-sandbox', "dap-topic")
        attributes = {
            'gcs.bucket': "ons-sdx-sandbox-outputs",
            'gcs.key': "/dap",
            'tx_id': "8010576d-f3df-4011-aa41-adecd9bee011"
        }
        message_str = "The message to be published"
        message = message_str.encode("utf-8")
        actual = publish_data(message_str, "8010576d-f3df-4011-aa41-adecd9bee011", "/dap")
        # mock_publish_data.assert_called_with(dap_topic_path, message, **attributes)

    @patch('app.publish.create_message_data')
    @patch('app.publish.publish_data')
    def test_send_message(self, mock_publish_data, mock_create_message_data):
        message_data = {
            'version': '1',
            'files': [{
                'name': "9010576d-f3df-4011-aa41-adecd9bee011",
                'sizeBytes': 0,
                'md5sum': 0
            }],
            'sensitivity': 'High',
            'sourceName': 'ons-sdx-sandbox',
            'manifestCreated': self.test_get_formatted_current_utc(),
            'description': "Description",
            'dataset': "Dataset",
            'schemaversion': '1'
        }
        str_dap_message = json.dumps(message_data)
        filename = "9010576d-f3df-4011-aa41-adecd9bee011"
        tx_id = "9010576d-f3df-4011-aa41-adecd9bee011"
        meta_data = MetaWrapper(filename)
        path = "dap/"
        mock_create_message_data.return_value = str_dap_message
        send_message(meta_data, path)
        mock_publish_data.assert_called_with(str_dap_message, filename, path)