import io
import unittest
import zipfile
from unittest.mock import patch, Mock

from sdx_gcp import Request

from app.definitions import MessageSchema
from app.routes import FILE_NAME, VERSION, V2, MESSAGE_SCHEMA, V1, ZIP_FILE, deliver_comments
from tests.integration.v1 import FileHolder


class CommentsTest(unittest.TestCase):

    @patch('app.deliver.write_to_bucket')
    @patch('app.deliver.publish_message')
    @patch('app.deliver.encrypt_output')
    @patch('app.message.get_formatted_current_utc')
    @patch('app.message.CONFIG')
    @patch('app.routes.Flask.jsonify')
    def test_comments(self,
                      mock_jsonify: Mock,
                      mock_config: Mock,
                      mock_time: Mock,
                      mock_encrypt: Mock,
                      mock_publish_message: Mock,
                      mock_write_to_bucket: Mock):
        fake_path = "My fake bucket path"
        fake_time = "2021-10-10T08:42:24.737Z"
        fake_project = "ons-sdx-fake"

        mock_time.return_value = fake_time
        mock_config.PROJECT_ID = fake_project
        mock_config.DATA_SENSITIVITY = "High"
        mock_encrypt.return_value = "My encrypted output"
        mock_write_to_bucket.return_value = fake_path
        mock_jsonify.return_value = {"success": True}

        tx_id = "2025-01-01.zip:ftp"  # why?
        input_filename = "2025-01-01.zip"
        output_filename = f"{input_filename}:ftp"

        # Create the input zipfile
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("file1", 'Some comments.')
            zip_file.writestr("file2", 'Some more comments.')
            zip_file.writestr("file3", 'Even more comments!')

        zip_bytes = zip_buffer.getvalue()

        # Create the fake Request object

        files_dict = {
            ZIP_FILE: FileHolder(zip_bytes)
        }

        data = {
            FILE_NAME: input_filename,
            VERSION: V2,
            "tx_id": tx_id,
            MESSAGE_SCHEMA: V1
        }

        class MockRequest(Request):
            files = files_dict
            args = data

        # Call the endpoint
        response = deliver_comments(MockRequest(data), tx_id)
        self.assertTrue(response["success"])

        expected_message: MessageSchema = {
            'version': '1',
            'files': [{
                'name': output_filename,
                'sizeBytes': 19,
                'md5sum': '3190f8a68aad6a9e33a624c318516ebb',
            }],
            'sensitivity': 'High',
            'sourceName': fake_project,
            'manifestCreated': "2021-10-10T08:42:24.737Z",
            'description': 'Comments.zip',
            'dataset': 'sdx_comments',
            'schemaversion': '1',
        }

        mock_publish_message.assert_called_with(expected_message, tx_id, fake_path)
