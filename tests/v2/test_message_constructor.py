import unittest

from app.v2.filename_mapper import FileNameMapperBase
from app.v2.message_constructor import MessageConstructor
from app.v2.models.config_schema import ConfigSchema


class TestFileMapper(FileNameMapperBase):

    def get_output_type(self, filename: str) -> str:
        if filename == "file1":
            return "output1"
        return "output2"


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
        self.message_constructor = MessageConstructor(config_schema=_config_schema, file_name_mapper=TestFileMapper())

    def test_build_message(self):
        pass

    def test_get_source(self):
        pass

    def test_get_target(self):
        filename_list = ["file1", "file2"]
        submission_type = "type2"
        target_list = self.message_constructor.get_target(filename_list, submission_type)

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
