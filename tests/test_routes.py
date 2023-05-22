import unittest
from unittest.mock import patch, MagicMock
from app import routes
from app.routes import SUBMISSION_FILE, TRANSFORMED_FILE, ZIP_FILE, SEFT_FILE, METADATA_FILE, VERSION, V2, FILE_NAME, ADHOC


class FakeFileBytes:

    def __init__(self, submission: bytes) -> None:
        self.submission = submission

    def read(self) -> bytes:
        return self.submission


class TestRoutes(unittest.TestCase):

    @patch('app.routes.MetaWrapper')
    @patch('app.routes.deliver')
    @patch('app.routes.Flask.jsonify')
    def test_deliver_dap(self, mock_jsonify, mock_deliver, mock_meta_wrapper):
        filename = "test_filename"
        submission_bytes = b'{"survey_id":"283"}'

        mock_request = MagicMock()
        mock_request.args[FILE_NAME] = filename

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {SUBMISSION_FILE: mock_file_bytes}

        routes.deliver_dap(mock_request)

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapperV2')
    @patch('app.routes.deliver')
    @patch('app.routes.Flask.jsonify')
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

        routes.deliver_dap(mock_request)

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapperAdhoc')
    @patch('app.routes.deliver')
    @patch('app.routes.Flask.jsonify')
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

        routes.deliver_dap(mock_request)

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapper')
    @patch('app.routes.deliver')
    @patch('app.routes.Flask.jsonify')
    def test_deliver_legacy(self, mock_jsonify, mock_deliver, mock_meta_wrapper):
        filename = "test_filename"
        submission_bytes = b'{"survey_id":"283"}'

        mock_request = MagicMock()
        mock_request.args[FILE_NAME] = filename

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {TRANSFORMED_FILE: mock_file_bytes, SUBMISSION_FILE: mock_file_bytes}

        routes.deliver_legacy(mock_request)

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapper')
    @patch('app.routes.deliver')
    @patch('app.routes.Flask.jsonify')
    def test_deliver_hybrid(self, mock_jsonify, mock_deliver, mock_meta_wrapper):
        filename = "test_filename"
        submission_bytes = b'{"survey_id":"147"}'

        mock_request = MagicMock()
        mock_request.args[FILE_NAME] = filename

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {TRANSFORMED_FILE: mock_file_bytes, SUBMISSION_FILE: mock_file_bytes}

        routes.deliver_hybrid(mock_request)

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapper')
    @patch('app.routes.deliver')
    @patch('app.routes.Flask.jsonify')
    def test_deliver_feedback(self, mock_jsonify, mock_deliver, mock_meta_wrapper):
        filename = "test_filename"
        submission_bytes = b'{"survey_id":"283"}'

        mock_request = MagicMock()
        mock_request.args[FILE_NAME] = filename

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {SUBMISSION_FILE: mock_file_bytes}

        routes.deliver_feedback(mock_request)

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapper')
    @patch('app.routes.deliver')
    @patch('app.routes.Flask.jsonify')
    def test_deliver_comments(self, mock_jsonify, mock_deliver, mock_meta_wrapper):
        filename = "test_filename"
        submission_bytes = b'{"survey_id":"283"}'

        mock_request = MagicMock()
        mock_request.args[FILE_NAME] = filename

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {ZIP_FILE: mock_file_bytes}

        routes.deliver_comments(mock_request)

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()

    @patch('app.routes.MetaWrapper')
    @patch('app.routes.deliver')
    @patch('app.routes.Flask.jsonify')
    def test_deliver_seft(self, mock_jsonify, mock_deliver, mock_meta_wrapper):
        filename = "test_filename"
        submission_bytes = b'{"survey_id":"283"}'

        mock_request = MagicMock()
        mock_request.args[FILE_NAME] = filename

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {METADATA_FILE: mock_file_bytes, SEFT_FILE: mock_file_bytes}

        routes.deliver_seft(mock_request)

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
        mock_meta_wrapper.assert_called()
