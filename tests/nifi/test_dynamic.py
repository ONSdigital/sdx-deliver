import unittest
from io import BytesIO
from unittest.mock import patch, Mock
from zipfile import ZipFile, ZIP_DEFLATED

from app import setup_keys
from app.deliver import deliver
from app.meta_wrapper import MetaWrapperV2


def create_zip(files: dict[str, bytes]) -> bytes:
    """
    Takes a dictionary that maps the name of the file, to its contents
    and converts it to a zip file in memory.
    """
    archive = BytesIO()

    with ZipFile(archive, "w", ZIP_DEFLATED, False) as zip_archive:
        for filename, file_contents in files.items():
            zip_archive.writestr(filename, file_contents)

    archive.seek(0)

    return archive.read()


def deliver_dynamic(zip_name: str, files: dict[str, bytes]):
    meta = MetaWrapperV2(zip_name)
    meta.set_dynamic()
    data_bytes = create_zip(files)
    deliver(meta, data_bytes, True)


class TestDynamicLogic(unittest.TestCase):

    def setUp(self):
        setup_keys()

    @patch('app.deliver.write_to_bucket')
    @patch('app.deliver.publish_v2_schema')
    def test_dynamic_simple(self,
                            mock_publish_v2_schema: Mock,
                            mock_write_to_bucket: Mock):
        mock_write_to_bucket.return_value = "My fake bucket path"

        files: dict[str, bytes] = {
            "spp_file.json": b"spp_file",
            "data_file": b"data_file",
            "index_file.csv": b"index_file"
        }

        deliver_dynamic("test_1.zip", files)

    @patch('app.deliver.write_to_bucket')
    @patch('app.deliver.publish_v2_schema')
    def test_dynamic_complex(self,
                             mock_publish_v2_schema: Mock,
                             mock_write_to_bucket: Mock):
        mock_write_to_bucket.return_value = "My fake bucket path"

        files: dict[str, bytes] = {
            "spp_json_file.json": b"spp_json_file",
            "data_image_index": b"data_image_index",
            "receipt.dat": b"receipt",
            "json_file": b"json",
        }

        deliver_dynamic("test_2.zip", files)


# This is an integration test. It will data to Nifi!!!
class TestDynamicNifi(unittest.TestCase):

    def setUp(self):
        setup_keys()

    def test_1(self):
        files: dict[str, bytes] = {
            "spp_file.json": b"spp_file",
            "data_file": b"data_file",
            "index_file.csv": b"index_file"
        }

        deliver_dynamic("test_1.zip", files)

    def test_2(self):
        files: dict[str, bytes] = {
            "spp_json_file.json": b"spp_json_file",
            "data_image_index": b"data_image_index",
            "receipt.dat": b"receipt",
            "json_file": b"json",
        }

        deliver_dynamic("test_2.zip", files)
