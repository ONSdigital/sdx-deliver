import unittest
import json
import warnings

from jsonschema import validate
from jsonschema.exceptions import ValidationError


class TestMessageFormat(unittest.TestCase):

    def setUp(self):
        with open('message_format/schema.json', 'r') as schema_file:
            schema = json.load(schema_file)
        self.schema = schema

    def test_example(self):
        warnings.filterwarnings("ignore")
        with open('message_format/example.json', 'r') as json_file:
            json_data = json.load(json_file)

        try:
            validate(instance=json_data, schema=self.schema)
        except ValidationError as err:
            self.fail(f"Validation error: {err.message}")

