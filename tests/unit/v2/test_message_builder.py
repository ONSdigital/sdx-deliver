import unittest

from app.meta_wrapper import MetaWrapperV2, MetaWrapperAdhoc, MetaWrapper
from app.output_type import OutputType
from app.v2.definitions.location_key_lookup import LocationKeyLookupBase, LocationKey
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.message_schema import Location
from app.v2.definitions.submission_type import DECRYPT, SubmissionTypeBase
from app.v2.definitions.submission_type_mapper import SubmissionTypeMapperBase
from app.v2.message_builder import MessageBuilder
from app.v2.definitions.survey_type import SurveyType


class MockMetaWrapper(MetaWrapperV2):

    def __init__(self, filename: str, output_type: OutputType):
        super().__init__(filename=filename)
        self.filename = filename
        self.tx_id = "123"
        self.survey_id = "101"
        self.period = "202101"
        self.ru_ref = "10550"
        self.md5sum = "51252"
        self.sizeBytes = 100
        self.output_type = output_type


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

    def get_outputs(self, filename: str, metadata: MetaWrapper) -> list[Location]:
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
        target_list = self.message_builder.get_targets(filename_list,
                                                       MockSubmissionType(),
                                                       MockMetaWrapper("filename", output_type=OutputType.HYBRID))

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
        meta_data = MockMetaWrapper(filename="file1", output_type=OutputType.SPP)
        context = self.message_builder.get_context(meta_data)

        expected = {
            "survey_id": "101",
            "period_id": "202101",
            "ru_ref": "10550"
        }

        self.assertEqual(expected, context)

    def test_get_comments_context(self):
        meta_data = MockMetaWrapper(filename="file1", output_type=OutputType.COMMENTS)
        context = self.message_builder.get_context(meta_data)

        expected = {
            "title": "Comments.zip"
        }

        self.assertEqual(expected, context)

    def test_get_adhoc_context(self):
        class TestMetaWrapperAdhoc(MetaWrapperAdhoc):
            def __init__(self, filename: str, output_type: OutputType):
                super().__init__(filename=filename)
                self.filename = filename
                self.tx_id = "123"
                self.survey_id = "101"
                self.period = "202101"
                self.ru_ref = "10550"
                self.md5sum = "51252"
                self.sizeBytes = 100
                self.output_type = output_type

        meta_data = TestMetaWrapperAdhoc(filename="file1", output_type=OutputType.SPP)
        context = self.message_builder.get_context(meta_data)

        expected = {
            "survey_id": "101",
            "title": "101 survey response for adhoc survey"
        }

        self.assertEqual(expected, context)

    def test_build_message(self):
        input_filename = "input_file"
        filenames = ["file1", "file2"]

        meta_data = MockMetaWrapper(filename=input_filename, output_type=OutputType.SPP)
        actual = self.message_builder.build_message(filenames, meta_data)

        expected = {'actions': ['decrypt'],
                    'context': {'period_id': '202101', 'ru_ref': '10550', 'survey_id': '101'},
                    'md5sum': '51252',
                    'schema_version': '2',
                    'sensitivity': 'High',
                    'sizeBytes': 100,
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
