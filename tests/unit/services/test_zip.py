import unittest
import zipfile
import io

from app.services.zip import ZipService


class TestUnzip(unittest.TestCase):

    def test_unzip(self):
        service = ZipService()
        zip_buffer = io.BytesIO()

        # Create a new zip file in the BytesIO object
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add files to the zip file
            zip_file.writestr('file1.txt', 'This is the content of file1.')
            zip_file.writestr('file2.txt', 'This is the content of file2.')

        # Get the bytes of the zip file
        zip_bytes = zip_buffer.getvalue()

        actual = service.unzip(zip_bytes)
        expected = ['file1.txt', 'file2.txt']
        self.assertEqual(expected, actual)
