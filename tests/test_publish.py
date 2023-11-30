import hashlib
import json
import unittest

from unittest import mock
from unittest.mock import patch
from app.meta_wrapper import MetaWrapper, MetaWrapperAdhoc
from app.output_type import OutputType
from app.publish import get_formatted_current_utc, send_message, create_message_data
from app import CONFIG


class TestPublish(unittest.TestCase):

    def setUp(self):
        self.meta_data = MetaWrapper('test_file_name')
        self.meta_data.output_type = None
        self.meta_data.survey_id = "023"
        self.meta_data.period = "0216"
        self.meta_data.ru_ref = "12345"
        self.meta_data.sizeBytes = len(b"bytes")
        self.meta_data.md5sum = hashlib.md5(b"bytes").hexdigest()

        self.expected = {
            'version': '1',
            'files': [{
                'name': self.meta_data.filename,
                'sizeBytes': self.meta_data.sizeBytes,
                'md5sum': self.meta_data.md5sum
            }],
            'sensitivity': 'High',
            'sourceName': CONFIG.PROJECT_ID,
            'manifestCreated': '',
            'description': '',
            'dataset': self.meta_data.survey_id,
            'schemaversion': '1',
            'iterationL1': self.meta_data.period
        }

    def test_get_formatted_current_utc(self):
        with mock.patch('datetime.datetime') as date_mock:
            date_mock.utcnow.return_value = "2021-02-15T21:45:51.991Z"
            result = get_formatted_current_utc()
            return result

    @patch('app.publish.get_formatted_current_utc', return_value="2021-10-10T08:42:24.737Z")
    def test_create_message_data_dap(self, mock_time):
        self.meta_data.output_type = OutputType.DAP
        self.expected['manifestCreated'] = mock_time.return_value
        self.expected['description'] = "023 survey response for period 0216 sample unit 12345"

        actual = create_message_data(self.meta_data)
        self.assertEqual(json.dumps(self.expected), actual)

    @patch('app.publish.get_formatted_current_utc', return_value="2021-10-10T08:42:24.737Z")
    def test_create_message_data_feedback(self, mock_time):
        self.meta_data.output_type = OutputType.FEEDBACK
        self.expected['manifestCreated'] = mock_time.return_value
        self.expected['description'] = '023 feedback response for period 0216 sample unit 12345'

        actual = create_message_data(self.meta_data)
        self.assertEqual(json.dumps(self.expected), actual)

    @patch('app.publish.get_formatted_current_utc', return_value="2021-10-10T08:42:24.737Z")
    def test_create_message_data_comment(self, mock_time):
        self.meta_data.output_type = OutputType.COMMENTS
        self.expected['manifestCreated'] = mock_time.return_value
        self.expected['description'] = "Comments.zip"
        self.expected['dataset'] = "sdx_comments"
        self.expected.pop('iterationL1')

        actual = create_message_data(self.meta_data)
        self.assertEqual(json.dumps(self.expected), actual)

    @patch('app.publish.create_message_data')
    @patch('app.publish.publish_data')
    def test_send_message_dap(self, mock_publish_data, mock_create_message_data):
        self.meta_data.output_type = OutputType.DAP
        self.meta_data.tx_id = "9010576d-f3df-4011-aa41-adecd9bee011"

        str_dap_message = json.dumps(self.expected)
        path = "dap/"
        mock_create_message_data.return_value = str_dap_message
        send_message(self.meta_data, path)
        mock_publish_data.assert_called_with(str_dap_message, self.meta_data.tx_id, path)

    @patch('app.publish.create_message_data')
    @patch('app.publish.publish_data')
    def test_send_message_feedback(self, mock_publish_data, mock_create_message_data):
        self.meta_data.output_type = OutputType.FEEDBACK
        self.meta_data.tx_id = "9010576d-f3df-4011-aa41-adecd9bee011"

        str_dap_message = json.dumps(self.expected)
        path = "feedback/"
        mock_create_message_data.return_value = str_dap_message
        send_message(self.meta_data, path)
        mock_publish_data.assert_called_with(str_dap_message, self.meta_data.tx_id, path)

    @patch('app.publish.create_message_data')
    @patch('app.publish.publish_data')
    def test_send_message_comment(self, mock_publish_data, mock_create_message_data):
        self.meta_data.output_type = OutputType.COMMENTS
        self.meta_data.tx_id = "9010576d-f3df-4011-aa41-adecd9bee011"

        str_dap_message = json.dumps(self.expected)
        path = "comments/"
        mock_create_message_data.return_value = str_dap_message
        send_message(self.meta_data, path)
        mock_publish_data.assert_called_with(str_dap_message, self.meta_data.tx_id, path)

    @patch('app.publish.create_message_data')
    @patch('app.publish.publish_data')
    def test_send_message_legacy(self, mock_publish_data, mock_create_message_data):
        self.meta_data.output_type = OutputType.LEGACY
        self.meta_data.tx_id = "9010576d-f3df-4011-aa41-adecd9bee011"

        str_dap_message = json.dumps(self.expected)
        path = "legacy/"
        mock_create_message_data.return_value = str_dap_message
        send_message(self.meta_data, path)
        mock_publish_data.assert_called_with(str_dap_message, self.meta_data.tx_id, path)

    @patch('app.publish.create_message_data')
    @patch('app.publish.publish_data')
    def test_send_message_seft(self, mock_publish_data, mock_create_message_data):
        self.meta_data.output_type = OutputType.SEFT
        self.meta_data.tx_id = "9010576d-f3df-4011-aa41-adecd9bee011"

        str_dap_message = json.dumps(self.expected)
        path = "seft/"
        mock_create_message_data.return_value = str_dap_message
        send_message(self.meta_data, path)
        mock_publish_data.assert_called_with(str_dap_message, self.meta_data.tx_id, path)

    @patch('app.publish.get_formatted_current_utc', return_value="2021-10-10T08:42:24.737Z")
    @patch('app.publish.CONFIG')
    def test_create_message_for_adhoc_prod(self, mock_config, mock_time):
        mock_config.PROJECT_ID = "ons-sdx-prod"
        mock_config.DATA_SENSITIVITY = "High"
        self.meta_data = MetaWrapperAdhoc('test_file_name')
        self.meta_data.output_type = OutputType.DAP
        self.meta_data.survey_id = "739"
        self.meta_data.period = None
        self.meta_data.ru_ref = None
        self.meta_data.sizeBytes = len(b"bytes")
        self.meta_data.md5sum = hashlib.md5(b"bytes").hexdigest()

        self.expected['manifestCreated'] = mock_time.return_value
        self.expected['sourceName'] = "ons"
        self.expected['dataset'] = "covid_resp_inf_surv_response"
        self.expected['description'] = "739 survey response for adhoc survey"
        self.expected['iterationL1'] = "prod"

        actual = create_message_data(self.meta_data)
        self.assertEqual(json.dumps(self.expected), actual)

    @patch('app.publish.get_formatted_current_utc', return_value="2021-10-10T08:42:24.737Z")
    @patch('app.publish.CONFIG')
    def test_create_message_for_adhoc_preprod(self, mock_config, mock_time):
        mock_config.PROJECT_ID = "ons-sdx-preprod"
        mock_config.DATA_SENSITIVITY = "Medium"
        self.meta_data = MetaWrapperAdhoc('test_file_name')
        self.meta_data.output_type = OutputType.DAP
        self.meta_data.survey_id = "739"
        self.meta_data.period = None
        self.meta_data.ru_ref = None
        self.meta_data.sizeBytes = len(b"bytes")
        self.meta_data.md5sum = hashlib.md5(b"bytes").hexdigest()

        self.expected['manifestCreated'] = mock_time.return_value
        self.expected['sourceName'] = "ons"
        self.expected['dataset'] = "covid_resp_inf_surv_response"
        self.expected['description'] = "739 survey response for adhoc survey"
        self.expected['sensitivity'] = "Medium"
        self.expected['iterationL1'] = "test"

        actual = create_message_data(self.meta_data)
        self.assertEqual(json.dumps(self.expected), actual)

    @patch('app.publish.get_formatted_current_utc', return_value="2021-10-10T08:42:24.737Z")
    @patch('app.publish.CONFIG')
    def test_create_message_for_wcis(self, mock_config, mock_time):
        mock_config.PROJECT_ID = "ons-sdx-prod"
        mock_config.DATA_SENSITIVITY = "High"
        self.meta_data = MetaWrapperAdhoc('test_file_name')
        self.meta_data.output_type = OutputType.DAP
        self.meta_data.survey_id = "739"
        self.meta_data.period = None
        self.meta_data.ru_ref = None
        self.meta_data.sizeBytes = len(b"bytes")
        self.meta_data.md5sum = hashlib.md5(b"bytes").hexdigest()

        self.expected['manifestCreated'] = mock_time.return_value
        self.expected['sourceName'] = "ons"
        self.expected['dataset'] = "covid_resp_inf_surv_response"
        self.expected['description'] = "739 survey response for adhoc survey"
        self.expected['iterationL1'] = "prod"

        actual = create_message_data(self.meta_data)
        self.assertEqual(json.dumps(self.expected), actual)

    @patch('app.publish.get_formatted_current_utc', return_value="2021-10-10T08:42:24.737Z")
    @patch('app.publish.CONFIG')
    def test_create_message_for_fuis(self, mock_config, mock_time):
        mock_config.PROJECT_ID = "ons-sdx-prod"
        mock_config.DATA_SENSITIVITY = "High"
        self.meta_data = MetaWrapperAdhoc('test_file_name')
        self.meta_data.output_type = OutputType.DAP
        self.meta_data.survey_id = "738"
        self.meta_data.period = None
        self.meta_data.ru_ref = None
        self.meta_data.sizeBytes = len(b"bytes")
        self.meta_data.md5sum = hashlib.md5(b"bytes").hexdigest()

        self.expected['manifestCreated'] = mock_time.return_value
        self.expected['sourceName'] = "ons"
        self.expected['dataset'] = "covid_resp_inf_surv_response"
        self.expected['description'] = "738 survey response for adhoc survey"
        self.expected['iterationL1'] = "prod"

        actual = create_message_data(self.meta_data)
        self.assertEqual(json.dumps(self.expected), actual)

    @patch('app.publish.get_formatted_current_utc', return_value="2021-10-10T08:42:24.737Z")
    @patch('app.publish.CONFIG')
    def test_create_message_for_wcis_feedback(self, mock_config, mock_time):
        mock_config.PROJECT_ID = "ons-sdx-prod"
        mock_config.DATA_SENSITIVITY = "High"
        self.meta_data = MetaWrapperAdhoc('test_file_name')
        self.meta_data.output_type = OutputType.FEEDBACK
        self.meta_data.survey_id = "739"
        self.meta_data.period = "2305"
        self.meta_data.ru_ref = None
        self.meta_data.sizeBytes = len(b"bytes")
        self.meta_data.md5sum = hashlib.md5(b"bytes").hexdigest()

        self.expected['manifestCreated'] = mock_time.return_value
        self.expected['sourceName'] = "ons-sdx-prod"
        self.expected['dataset'] = "739"
        self.expected["iterationL1"] = "2305"
        self.expected['description'] = "739 feedback response for adhoc survey"

        actual = create_message_data(self.meta_data)
        self.assertEqual(json.dumps(self.expected), actual)
