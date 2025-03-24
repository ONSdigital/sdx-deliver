import hashlib
import unittest

from unittest.mock import patch, Mock

from app.message import create_message
from app.meta_wrapper import MetaWrapper, MetaWrapperAdhoc
from app.output_type import OutputType
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

    @patch('app.message.get_formatted_current_utc')
    def test_create_message_data_dap(self, mock_time: Mock):
        mock_time.return_value = "2021-10-10T08:42:24.737Z"
        self.meta_data.output_type = OutputType.DAP
        self.expected['manifestCreated'] = mock_time.return_value
        self.expected['description'] = "023 survey response for period 0216 sample unit 12345"

        actual = create_message(self.meta_data)
        self.assertEqual(self.expected, actual)

    @patch('app.message.get_formatted_current_utc')
    def test_create_message_data_feedback(self, mock_time: Mock):
        mock_time.return_value = "2021-10-10T08:42:24.737Z"
        self.meta_data.output_type = OutputType.FEEDBACK
        self.expected['manifestCreated'] = mock_time.return_value
        self.expected['description'] = '023 feedback response for period 0216 sample unit 12345'

        actual = create_message(self.meta_data)
        self.assertEqual(self.expected, actual)

    @patch('app.message.get_formatted_current_utc')
    def test_create_message_data_comment(self, mock_time: Mock):
        mock_time.return_value = "2021-10-10T08:42:24.737Z"
        self.meta_data.output_type = OutputType.COMMENTS
        self.expected['manifestCreated'] = mock_time.return_value
        self.expected['description'] = "Comments.zip"
        self.expected['dataset'] = "sdx_comments"
        self.expected.pop('iterationL1')

        actual = create_message(self.meta_data)
        self.assertEqual(self.expected, actual)

    @patch('app.message.get_formatted_current_utc')
    @patch('app.message.CONFIG')
    def test_create_message_for_adhoc_prod(self, mock_config: Mock, mock_time: Mock):
        mock_time.return_value = "2021-10-10T08:42:24.737Z"
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

        actual = create_message(self.meta_data)
        self.assertEqual(self.expected, actual)

    @patch('app.message.get_formatted_current_utc')
    @patch('app.message.CONFIG')
    def test_create_message_for_adhoc_preprod(self, mock_config: Mock, mock_time: Mock):
        mock_time.return_value = "2021-10-10T08:42:24.737Z"
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

        actual = create_message(self.meta_data)
        self.assertEqual(self.expected, actual)

    @patch('app.message.get_formatted_current_utc')
    @patch('app.message.CONFIG')
    def test_create_message_for_wcis(self, mock_config: Mock, mock_time: Mock):
        mock_time.return_value = "2021-10-10T08:42:24.737Z"
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

        actual = create_message(self.meta_data)
        self.assertEqual(self.expected, actual)

    @patch('app.message.get_formatted_current_utc')
    @patch('app.message.CONFIG')
    def test_create_message_for_fuis(self, mock_config: Mock, mock_time: Mock):
        mock_time.return_value = "2021-10-10T08:42:24.737Z"
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

        actual = create_message(self.meta_data)
        self.assertEqual(self.expected, actual)

    @patch('app.message.get_formatted_current_utc')
    @patch('app.message.CONFIG')
    def test_create_message_for_wcis_feedback(self, mock_config: Mock, mock_time: Mock):
        mock_time.return_value = "2021-10-10T08:42:24.737Z"
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

        actual = create_message(self.meta_data)
        self.assertEqual(self.expected, actual)

    @patch('app.message.get_formatted_current_utc')
    @patch('app.message.CONFIG')
    def test_create_message_for_phm(self, mock_config: Mock, mock_time: Mock):
        mock_time.return_value = "2021-10-10T08:42:24.737Z"
        mock_config.PROJECT_ID = "ons-sdx-prod"
        mock_config.DATA_SENSITIVITY = "High"
        self.meta_data = MetaWrapperAdhoc('test_file_name')
        self.meta_data.output_type = OutputType.DAP
        self.meta_data.survey_id = "740"
        self.meta_data.period = None
        self.meta_data.ru_ref = None
        self.meta_data.sizeBytes = len(b"bytes")
        self.meta_data.md5sum = hashlib.md5(b"bytes").hexdigest()

        self.expected['manifestCreated'] = mock_time.return_value
        self.expected['sourceName'] = "ons"
        self.expected['dataset'] = "covid_resp_inf_surv_response"
        self.expected['description'] = "740 survey response for adhoc survey"
        self.expected['iterationL1'] = "prod"
        self.expected['iterationL2'] = "phm_740_health_insights_2024"

        actual = create_message(self.meta_data)
        self.assertEqual(self.expected, actual)
