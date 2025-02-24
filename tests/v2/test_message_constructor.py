import unittest

from app.v2.definitions.filename_mapper import FileNameMapperBase
from app.v2.message_constructor import MessageConstructor
from app.v2.definitions.config_schema import ConfigSchema
from app.meta_wrapper import MetaWrapperV2, MetaWrapperAdhoc
from app.output_type import OutputType
from app.v2.definitions.submission_type_mapper import SubmissionTypeMapperBase


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


class MockFileMapper(FileNameMapperBase):

    def get_output_type(self, filename: str) -> str:
        if filename == "file1":
            return "output1"
        return "output2"


class MockSubmissionTypeMapper(SubmissionTypeMapperBase):

    def get_submission_type(self, output_type: OutputType) -> str:
        if output_type == OutputType.SPP:
            return "type2"
        return "type1"


class TestMessageConstructor(unittest.TestCase):

    def setUp(self):
        _config_schema: ConfigSchema = {
            "locations": {
                "loc1": {
                    "location_type": "server1",
                    "location_name": "server1-name"
                },
                "loc2": {
                    "location_type": "server2",
                    "location_name": "server2-name"
                }
            },
            "submission_types": {
                "type1": {
                    "actions": ["decrypt"],
                    "source": {
                        "location": "loc2",
                        "path": "test-path-1"
                    },
                    "outputs": {
                        "output1": [{
                            "location": "loc1",
                            "path": "test-path-2"
                        }]
                    }
                },
                "type2": {
                    "actions": ["decrypt", "unzip"],
                    "source": {
                        "location": "loc2",
                        "path": "test-path-3"
                    },
                    "outputs": {
                        "output1": [{
                            "location": "loc1",
                            "path": "test-path-4"
                        }],
                        "output2": [
                            {
                                "location": "loc1",
                                "path": "test-path-5"
                            },
                            {
                                "location": "loc2",
                                "path": "test-path-6"
                            }
                        ]
                    }
                }
            }
        }
        self.message_constructor = MessageConstructor(
            config_schema=_config_schema,
            file_name_mapper=MockFileMapper(),
            submission_mapper=MockSubmissionTypeMapper()
        )

    def test_get_source(self):
        filename = "file1"
        submission_type = "type2"
        source = self.message_constructor.get_source(filename, submission_type)

        expected = {
            "location_type": "server2",
            "location_name": "server2-name",
            "path": "test-path-3",
            "filename": "file1"
        }

        self.assertEqual(expected, source)

    def test_get_target(self):
        filename_list = ["file1", "file2"]
        submission_type = "type2"
        target_list = self.message_constructor.get_targets(filename_list, submission_type)

        expected = [
            {
                "input": "file1",
                "outputs": [
                    {
                        "location_type": "server1",
                        "location_name": "server1-name",
                        "path": "test-path-4",
                        "filename": "file1"
                    }
                ]
            },
            {
                "input": "file2",
                "outputs": [
                    {
                        "location_type": "server1",
                        "location_name": "server1-name",
                        "path": "test-path-5",
                        "filename": "file2"
                    },
                    {
                        "location_type": "server2",
                        "location_name": "server2-name",
                        "path": "test-path-6",
                        "filename": "file2"
                    }
                ]
            }
        ]

        self.assertEqual(expected, target_list)

    def test_get_action(self):
        submission_type = "type2"
        actions = self.message_constructor.get_actions(submission_type)

        expected = ["decrypt", "unzip"]
        self.assertEqual(expected, actions)

    def test_get_business_survey_context(self):
        meta_data = MockMetaWrapper(filename="file1", output_type=OutputType.SPP)
        context = self.message_constructor.get_context(meta_data)

        expected = {
            "survey_id": "101",
            "period_id": "202101",
            "ru_ref": "10550"
        }

        self.assertEqual(expected, context)

    def test_get_comments_context(self):
        meta_data = MockMetaWrapper(filename="file1", output_type=OutputType.COMMENTS)
        context = self.message_constructor.get_context(meta_data)

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
        context = self.message_constructor.get_context(meta_data)

        expected = {
            "survey_id": "101",
            "title": "101 survey response for adhoc survey"
        }

        self.assertEqual(expected, context)

    def test_build_message(self):
        input_filename = "input_file"
        filenames = ["file1", "file2"]

        meta_data = MockMetaWrapper(filename=input_filename, output_type=OutputType.SPP)
        actual = self.message_constructor.build_message(filenames, meta_data)

        expected = {
            "schema_version": "2",
            "sensitivity": "High",
            "sizeBytes": 100,
            "md5sum": "51252",
            "context": {
                "survey_id": "101",
                "period_id": "202101",
                "ru_ref": "10550"
            },
            "source": {
                "location_type": "server2",
                "location_name": "server2-name",
                "path": "test-path-3",
                "filename": input_filename
            },
            "actions": ["decrypt", "unzip"],
            "targets": [
                {
                    "input": "file1",
                    "outputs": [
                        {
                            "location_type": "server1",
                            "location_name": "server1-name",
                            "path": "test-path-4",
                            "filename": "file1"
                        }
                    ]
                },
                {
                    "input": "file2",
                    "outputs": [
                        {
                            "location_type": "server1",
                            "location_name": "server1-name",
                            "path": "test-path-5",
                            "filename": "file2"
                        },
                        {
                            "location_type": "server2",
                            "location_name": "server2-name",
                            "path": "test-path-6",
                            "filename": "file2"
                        }
                    ]
                }
            ]
        }

        self.assertEqual(expected, actual)
