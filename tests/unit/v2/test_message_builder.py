import unittest

from app.v2.definitions.context import BusinessSurveyContext, Context, CommentsFileContext, AdhocSurveyContext
from app.v2.definitions.location_key_lookup import LocationKeyLookupBase, LocationKey
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.message_schema import Location
from app.v2.definitions.submission_type import DECRYPT, SubmissionTypeBase
from app.v2.definitions.submission_type_mapper import SubmissionTypeMapperBase
from app.v2.definitions.zip_details import ZipDetails
from app.v2.message_builder import MessageBuilder
from app.v2.definitions.survey_type import SurveyType


class MockLocationKeyLookup(LocationKeyLookupBase):

    def __init__(self):
        ftp_key = LookupKey.FTP.value
        sdx_key = LookupKey.SDX.value
        spp_key = LookupKey.SPP.value
        dap_key = LookupKey.DAP.value
        self._location_keys = {
            ftp_key: {
                "location_type": "server1",
                "location_name": "server1_name"
            },
            sdx_key: {
                "location_type": "server2",
                "location_name": "server2_name"
            },
            spp_key: {
                "location_type": "server3",
                "location_name": "server3_name"
            },
            dap_key: {
                "location_type": "server4",
                "location_name": "server4_name"
            }
        }

    def get_location_key(self, lookup_key: LookupKey) -> LocationKey:
        return self._location_keys[lookup_key.value]


class MockSubmissionType(SubmissionTypeBase):

    def get_source(self, filename: str) -> Location:
        return {
            "location_type": "server1",
            "location_name": "server1-name",
            "path": "test-path-1",
            "filename": filename
        }

    def get_actions(self) -> list[str]:
        return [DECRYPT]

    def get_outputs(self, filename: str, context: Context) -> list[Location]:
        return [{
            "location_type": "server2",
            "location_name": "server2-name",
            "path": "test-path-2",
            "filename": filename
        }]


class MockSubmissionTypeMapper(SubmissionTypeMapperBase):

    def get_submission_type(self, survey_type: SurveyType) -> SubmissionTypeBase:
        return MockSubmissionType()


class TestMessageConstructor(unittest.TestCase):

    def setUp(self):
        self.message_builder = MessageBuilder(
            submission_mapper=MockSubmissionTypeMapper()
        )

    def test_get_source(self):
        filename = "file1"
        source = self.message_builder.get_source(filename, MockSubmissionType())

        expected = {
            "location_type": "server1",
            "location_name": "server1-name",
            "path": "test-path-1",
            "filename": "file1"
        }

        self.assertEqual(expected, source)

    def test_get_target(self):
        filename_list = ["file1", "file2"]
        context: Context = {
            "tx_id": "123",
            "survey_type": SurveyType.SPP
        }
        target_list = self.message_builder.get_targets(filename_list,
                                                       MockSubmissionType(),
                                                       context)

        expected = [
            {
                "input": "file1",
                "outputs": [
                    {
                        "location_type": "server2",
                        "location_name": "server2-name",
                        "path": "test-path-2",
                        "filename": "file1"
                    }
                ]
            },
            {
                "input": "file2",
                "outputs": [
                    {
                        "location_type": "server2",
                        "location_name": "server2-name",
                        "path": "test-path-2",
                        "filename": "file2"
                    },
                ]
            }
        ]

        self.assertEqual(expected, target_list)

    def test_get_action(self):
        actions = self.message_builder.get_actions(MockSubmissionType())

        expected = ["decrypt"]
        self.assertEqual(expected, actions)

    def test_get_business_survey_context(self):
        context: BusinessSurveyContext = {
            "tx_id": "123",
            "survey_type": SurveyType.LEGACY,
            "survey_id": "666",
            "period_id": "202101",
            "ru_ref": "10550"
        }

        actual = self.message_builder.get_context(context)

        expected = {
            "survey_id": "666",
            "period_id": "202101",
            "ru_ref": "10550"
        }

        self.assertEqual(expected, actual)

    def test_get_comments_context(self):
        context: CommentsFileContext = {
            "tx_id": "123",
            "survey_type": SurveyType.COMMENTS,
            "title": "Comments.zip"
        }

        actual = self.message_builder.get_context(context)

        expected = {
            "title": "Comments.zip"
        }

        self.assertEqual(expected, actual)

    def test_get_adhoc_context(self):
        context: AdhocSurveyContext = {
            "tx_id": "123",
            "survey_type": SurveyType.ADHOC,
            "survey_id": "101",
            "title": "101 survey response for adhoc survey",
            "label": "adhoc label"
        }

        actual = self.message_builder.get_context(context)

        expected = {
            "survey_id": "101",
            "title": "101 survey response for adhoc survey",
            "label": "adhoc label"
        }

        self.assertEqual(expected, actual)

    def test_build_message(self):
        input_filename = "input_file"
        filenames = ["file1", "file2"]
        size_bytes = 100
        md5sum = '51252'
        survey_id = "666"
        period_id = "202101"
        ru_ref = "10550"

        context: BusinessSurveyContext = {
            "tx_id": "123",
            "survey_type": SurveyType.LEGACY,
            "survey_id": survey_id,
            "period_id": period_id,
            "ru_ref": ru_ref
        }

        zip_details: ZipDetails = {
            "filename": input_filename,
            "size_bytes": size_bytes,
            "md5sum": md5sum,
            "filenames": filenames
        }

        actual = self.message_builder.build_message(zip_details, context)

        expected = {'actions': ['decrypt'],
                    'context': {'period_id': period_id, 'ru_ref': ru_ref, 'survey_id': survey_id},
                    'md5sum': md5sum,
                    'schema_version': '2',
                    'sensitivity': 'High',
                    'sizeBytes': size_bytes,
                    'source': {'filename': 'input_file',
                               'location_name': 'server1-name',
                               'location_type': 'server1',
                               'path': 'test-path-1'},
                    'targets': [{'input': 'file1',
                                 'outputs': [{'filename': 'file1',
                                              'location_name': 'server2-name',
                                              'location_type': 'server2',
                                              'path': 'test-path-2'}]},
                                {'input': 'file2',
                                 'outputs': [{'filename': 'file2',
                                              'location_name': 'server2-name',
                                              'location_type': 'server2',
                                              'path': 'test-path-2'}]}]}

        self.assertEqual(expected, actual)
