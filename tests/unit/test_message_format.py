import os
import unittest
import json

from jsonschema import validate
from jsonschema.exceptions import ValidationError


class TestMessageFormat(unittest.TestCase):
    def setUp(self):
        with open("message_format/schema.json", "r") as schema_file:
            schema = json.load(schema_file)
        self.schema = schema

    def validate_json(self, json_data):
        try:
            validate(instance=json_data, schema=self.schema)
        except ValidationError as err:
            self.fail(f"Validation error: {err.message}")

    def test_example(self):
        with open("message_format/example.json", "r") as json_file:
            json_data = json.load(json_file)
            self.validate_json(json_data)

    def test_new_examples(self):
        directory = "message_format/examples/v2"

        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                with open(f"{directory}/{filename}", "r") as json_file:
                    json_data = json.load(json_file)
                    self.validate_json(json_data)
