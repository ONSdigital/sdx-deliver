import unittest
import pytest

from unittest import mock
from unittest.mock import patch, MagicMock
from flask import jsonify
from app import routes, app
from app.routes import SUBMISSION_FILE, TRANSFORMED_FILE, ZIP_FILE, SEFT_FILE, METADATA_FILE, process, server_error, \
    VERSION, V2, FILE_NAME, ADHOC


class FakeFileBytes:

    def __init__(self, submission: bytes) -> None:
        self.submission = submission

    def read(self) -> bytes:
        return self.submission


class TestRoutes(unittest.TestCase):

    @patch('app.routes.MetaWrapper')
    @patch('app.routes.deliver')
    @patch('app.routes.jsonify')
    def test_deliver_dap(self, mock_jsonify, mock_deliver, mock_meta_wrapper):
        filename = "test_filename"
        submission_bytes = b'{"survey_id":"283"}'

        mock_request = MagicMock()
        mock_request.args[FILE_NAME] = filename

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {SUBMISSION_FILE: mock_file_bytes}

        routes.request = mock_request
        routes.deliver_dap()

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapperV2')
    @patch('app.routes.deliver')
    @patch('app.routes.jsonify')
    def test_deliver_dap_v2(self, mock_jsonify, mock_deliver, mock_meta_wrapper):
        filename = "test_filename"
        submission_bytes = b'{"survey_id":"283"}'

        mock_request = MagicMock()
        args = {}
        args[FILE_NAME] = filename
        args[VERSION] = V2
        mock_request.args = args

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {SUBMISSION_FILE: mock_file_bytes}

        routes.request = mock_request
        routes.deliver_dap()

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapperAdhoc')
    @patch('app.routes.deliver')
    @patch('app.routes.jsonify')
    def test_deliver_dap_adhoc(self, mock_jsonify, mock_deliver, mock_meta_wrapper):
        filename = "test_filename"
        submission_bytes = b'{"survey_id":"283"}'

        mock_request = MagicMock()
        args = {}
        args[FILE_NAME] = filename
        args[VERSION] = ADHOC
        mock_request.args = args

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {SUBMISSION_FILE: mock_file_bytes}

        routes.request = mock_request
        routes.deliver_dap()

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapper')
    @patch('app.routes.deliver')
    @patch('app.routes.jsonify')
    def test_deliver_legacy(self, mock_jsonify, mock_deliver, mock_meta_wrapper):
        filename = "test_filename"
        submission_bytes = b'{"survey_id":"283"}'

        mock_request = MagicMock()
        mock_request.args[FILE_NAME] = filename

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {TRANSFORMED_FILE: mock_file_bytes, SUBMISSION_FILE: mock_file_bytes}

        routes.request = mock_request
        routes.deliver_legacy()

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapper')
    @patch('app.routes.deliver')
    @patch('app.routes.jsonify')
    def test_deliver_hybrid(self, mock_jsonify, mock_deliver, mock_meta_wrapper):
        filename = "test_filename"
        submission_bytes = b'{"survey_id":"147"}'

        mock_request = MagicMock()
        mock_request.args[FILE_NAME] = filename

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {TRANSFORMED_FILE: mock_file_bytes, SUBMISSION_FILE: mock_file_bytes}

        routes.request = mock_request
        routes.deliver_hybrid()

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapper')
    @patch('app.routes.deliver')
    @patch('app.routes.jsonify')
    def test_deliver_feedback(self, mock_jsonify, mock_deliver, mock_meta_wrapper):
        filename = "test_filename"
        submission_bytes = b'{"survey_id":"283"}'

        mock_request = MagicMock()
        mock_request.args[FILE_NAME] = filename

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {SUBMISSION_FILE: mock_file_bytes}

        routes.request = mock_request
        routes.deliver_feedback()

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapper')
    @patch('app.routes.deliver')
    @patch('app.routes.jsonify')
    def test_deliver_comments(self, mock_jsonify, mock_deliver, mock_meta_wrapper):
        filename = "test_filename"
        submission_bytes = b'{"survey_id":"283"}'

        mock_request = MagicMock()
        mock_request.args[FILE_NAME] = filename

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {ZIP_FILE: mock_file_bytes}

        routes.request = mock_request
        routes.deliver_comments()

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapper')
    @patch('app.routes.deliver')
    @patch('app.routes.jsonify')
    def test_deliver_seft(self, mock_jsonify, mock_deliver, mock_meta_wrapper):
        filename = "test_filename"
        submission_bytes = b'{"survey_id":"283"}'

        mock_request = MagicMock()
        mock_request.args[FILE_NAME] = filename

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {METADATA_FILE: mock_file_bytes, SEFT_FILE: mock_file_bytes}

        routes.request = mock_request
        routes.deliver_seft()

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapper')
    @mock.patch('app.routes.deliver', side_effect=Exception())
    def test_process_error(self, mock_deliver, mock_wrapper):
        with pytest.raises(Exception):
            submission_bytes = b'{"survey_id":"283"}'
            process(mock_wrapper, submission_bytes)

    def test_server_error(self):
        with app.app_context():
            error = Exception
            message = {
                'status': 500,
                'message': "Internal server error: " + repr(error),
            }
            resp = jsonify(message)
            resp.status_code = 500
            actual = server_error(error)
            assert actual.status_code == 500

    @patch('app.routes.jsonify')
    def test_healthcheck(self, mock_jsonify):
        routes.healthcheck()
        mock_jsonify.assert_called_with({'status': 'OK'})
