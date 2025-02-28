import unittest

from app.v2.config_lookup import ConfigLookup
from app.v2.definitions.config_schema import ConfigSchema
from app.v2.definitions.location_key_lookup import LocationKeyLookupBase, LocationKey
from app.v2.definitions.location_name_repository import LookupKey


class MockLocationKeyLookup(LocationKeyLookupBase):

    def get_location_key(self, lookup_key: LookupKey) -> LocationKey:
        if lookup_key == LookupKey.SDX:
            return {
                "location_type": "server1",
                "location_name": "server1_name"
            }
        if lookup_key == LookupKey.FTP:
            return {
                "location_type": "server2",
                "location_name": "server2_name"
            }
        if lookup_key == LookupKey.SPP:
            return {
                "location_type": "server3",
                "location_name": "server3_name"
            }
        if lookup_key == LookupKey.DAP:
            return {
                "location_type": "server4",
                "location_name": "server4_name"
            }


class TestConfigLookup(unittest.TestCase):

    def setUp(self):
        self._config_schema: ConfigSchema = {
            "submission_types": {
                "type1": {
                    "actions": ["decrypt"],
                    "source": {
                        "location": LookupKey.SDX,
                        "path": "test-path-1"
                    },
                    "outputs": {
                        "output1": [{
                            "location": LookupKey.SPP,
                            "path": "test-path-2"
                        }]
                    }
                },
                "type2": {
                    "actions": ["decrypt", "unzip"],
                    "source": {
                        "location": LookupKey.SDX,
                        "path": "test-path-3"
                    },
                    "outputs": {
                        "output1": [{
                            "location": LookupKey.FTP,
                            "path": "test-path-4"
                        }],
                        "output2": [
                            {
                                "location": LookupKey.DAP,
                                "path": "test-path-5"
                            },
                            {
                                "location": LookupKey.SPP,
                                "path": "test-path-6"
                            }
                        ]
                    }
                }
            }
        }
        self._config_lookup = ConfigLookup(self._config_schema, MockLocationKeyLookup())

    def test_get_source(self):
        submission_type = "type1"
        filename = "test-file-1"

        actual = self._config_lookup.get_source(submission_type=submission_type, filename=filename)
        expected = {
            "location_type": "server1",
            "location_name": "server1_name",
            "path": "test-path-1",
            "filename": "test-file-1"
        }
        self.assertEqual(expected, actual)

    def test_get_actions(self):
        submission_type = "type2"

        actual = self._config_lookup.get_actions(submission_type=submission_type)
        expected = ["decrypt", "unzip"]
        self.assertEqual(expected, actual)

    def test_get_single_output(self):
        submission_type = "type1"
        filename = "test-file-1"
        output_type = "output1"

        actual = self._config_lookup.get_outputs(submission_type=submission_type, output_type=output_type, filename=filename)
        expected = [{
            "location_type": "server3",
            "location_name": "server3_name",
            "path": "test-path-2",
            "filename": "test-file-1"
        }]
        self.assertEqual(expected, actual)

    def test_get_multiple_output(self):
        submission_type = "type2"
        filename = "test-file-1"
        output_type = "output2"

        actual = self._config_lookup.get_outputs(submission_type=submission_type, output_type=output_type, filename=filename)
        expected = [
            {
                "location_type": "server4",
                "location_name": "server4_name",
                "path": "test-path-5",
                "filename": "test-file-1"
            },
            {
                "location_type": "server3",
                "location_name": "server3_name",
                "path": "test-path-6",
                "filename": "test-file-1"
            }
        ]
        self.assertEqual(actual, expected)
