import unittest

from unittest.mock import patch
from app import routes
from app.routes import SUBMISSION_FILE


class FakeRequest:

    def __init__(self) -> None:
        self.args = {}


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

        mock_request = FakeRequest()
        mock_request.args['filename'] = filename

        mock_file_bytes = FakeFileBytes(submission_bytes)
        mock_request.files = {SUBMISSION_FILE: mock_file_bytes}

        routes.request = mock_request
        routes.deliver_dap()

        mock_deliver.assert_called()
        mock_jsonify.assert_called_with(success=True)
