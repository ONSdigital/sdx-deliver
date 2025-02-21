import unittest

from app.v2.filename_mapper import FileExtensionMapper


class FileExtensionMapperTest(unittest.TestCase):
    def test_get_output_type_for_image(self):
        file_extension_mapper = FileExtensionMapper()
        filename = "file.jpg"
        expected = "image"

        actual = file_extension_mapper.get_output_type(filename)
        self.assertEqual(expected, actual)

    def test_get_output_type_for_index(self):
        file_extension_mapper = FileExtensionMapper()
        filename = "file.csv"
        expected = "index"

        actual = file_extension_mapper.get_output_type(filename)
        self.assertEqual(expected, actual)

    def test_get_output_type_for_pck(self):
        file_extension_mapper = FileExtensionMapper()
        filename = "file"
        expected = "pck"

        actual = file_extension_mapper.get_output_type(filename)
        self.assertEqual(expected, actual)
