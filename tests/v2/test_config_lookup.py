import unittest

from app.v2.config_lookup import ConfigLookup
from app.v2.models.config_schema import ConfigSchema


class TestConfigLookup(unittest.TestCase):

    def setUp(self):
        self._config_schema: ConfigSchema = {
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
        self._config_lookup = ConfigLookup(self._config_schema)

    def test_get_source(self):
        submission_type = "type1"
        filename = "test-file-1"

        actual = self._config_lookup.get_source(submission_type=submission_type, filename=filename)
        expected = {
            "location_type": "server2",
            "location_name": "server2-name",
            "path": "test-path-1",
            "filename": "test-file-1"
        }
        self.assertEqual(actual, expected)

    def test_get_actions(self):
        submission_type = "type2"

        actual = self._config_lookup.get_actions(submission_type=submission_type)
        expected = ["decrypt", "unzip"]
        self.assertEqual(actual, expected)

    def test_get_single_output(self):
        submission_type = "type1"
        filename = "test-file-1"
        output_type = "output1"

        actual = self._config_lookup.get_outputs(submission_type=submission_type, output_type=output_type, filename=filename)
        expected = [{
            "location_type": "server1",
            "location_name": "server1-name",
            "path": "test-path-2",
            "filename": "test-file-1"
        }]
        self.assertEqual(actual, expected)

    def test_get_multiple_output(self):
        submission_type = "type2"
        filename = "test-file-1"
        output_type = "output2"

        actual = self._config_lookup.get_outputs(submission_type=submission_type, output_type=output_type, filename=filename)
        expected = [{
                "location_type": "server1",
                "location_name": "server1-name",
                "path": "test-path-5",
                "filename": "test-file-1"
            },
            {
                "location_type": "server2",
                "location_name": "server2-name",
                "path": "test-path-6",
                "filename": "test-file-1"
            }
        ]
        self.assertEqual(actual, expected)
