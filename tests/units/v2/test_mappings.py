import unittest

from app.output_type import OutputType
from app.v2.mappings import (FileExtensionMapper, SubmissionTypeMapper, LocationNameMapper,
                             IMAGE, INDEX, PCK, SEFT_SURVEY, SPP_SURVEY, LEGACY_SURVEY, FTP)
from unittest.mock import patch


class FileExtensionMapperTest(unittest.TestCase):

    def test_get_output_type_for_image(self):
        file_extension_mapper = FileExtensionMapper()
        filename = "file.jpg"
        expected = IMAGE

        actual = file_extension_mapper.get_output_type(filename, LEGACY_SURVEY)
        self.assertEqual(expected, actual)

    def test_get_output_type_for_image_capitals(self):
        file_extension_mapper = FileExtensionMapper()
        filename = "file.JPG"
        expected = IMAGE

        actual = file_extension_mapper.get_output_type(filename, LEGACY_SURVEY)
        self.assertEqual(expected, actual)

    def test_get_output_type_for_index(self):
        file_extension_mapper = FileExtensionMapper()
        filename = "file.csv"
        expected = INDEX

        actual = file_extension_mapper.get_output_type(filename, LEGACY_SURVEY)
        self.assertEqual(expected, actual)

    def test_get_output_type_for_pck(self):
        file_extension_mapper = FileExtensionMapper()
        filename = "file"
        expected = PCK

        actual = file_extension_mapper.get_output_type(filename, LEGACY_SURVEY)
        self.assertEqual(expected, actual)


class SubmissionTypeMapperTest(unittest.TestCase):
    def test_get_submission_type_for_seft(self):
        submission_type_mapper = SubmissionTypeMapper()
        output_type = OutputType.SEFT
        expected = SEFT_SURVEY

        actual = submission_type_mapper.get_submission_type(output_type)
        self.assertEqual(expected, actual)

    def test_get_submission_type_for_spp(self):
        submission_type_mapper = SubmissionTypeMapper()
        output_type = OutputType.SPP
        expected = SPP_SURVEY

        actual = submission_type_mapper.get_submission_type(output_type)
        self.assertEqual(expected, actual)

    def test_get_submission_type_for_legacy(self):
        submission_type_mapper = SubmissionTypeMapper()
        output_type = OutputType.LEGACY
        expected = LEGACY_SURVEY

        actual = submission_type_mapper.get_submission_type(output_type)
        self.assertEqual(expected, actual)


class LocationNameMapperTest(unittest.TestCase):

    @patch('app.v2.mappings.sdx_app.secrets_get', return_value=["ftp"])
    def test_get_location_name_for_ftp(self, mock_secrets_get):
        location_name_mapper = LocationNameMapper()

        expected = "ftp"
        location_name_mapper.load_location_values()
        actual = location_name_mapper.get_location_name(FTP)
        self.assertEqual(expected, actual)
