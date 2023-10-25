import unittest

from app.meta_wrapper import MetaWrapperAdhoc


class TestMetaWrapperAdhoc(unittest.TestCase):

    def setUp(self) -> None:
        self.test_adhoc = {
            "case_id": "36935987-f9c7-4671-b729-3d294227bf15",
            "tx_id": "12fa747d-0a6b-425c-8960-a34aa6bdafa3",
            "type": "uk.gov.ons.edc.eq:surveyresponse",
            "version": "v2",
            "data_version": "0.0.3",
            "origin": "uk.gov.ons.edc.eq",
            "collection_exercise_sid": "a1538005-a8c9-4352-9448-c8b1ca171684",
            "schema_name": "health_demo",
            "flushed": False,
            "submitted_at": "2023-01-12T16:07:01+00:00",
            "launch_language_code": "en",
            "survey_metadata": {
                "survey_id": "001",
                "qid": "6235410884491574",
                "form_type": "demo"
            },
            "data": {
                "answers": [{"answer_id": "answerfccc038a-059c-439e-8945-e2c919c914a3", "value": "Andy"},
                            {"answer_id": "answer921c327e-e210-4f54-88e8-f7b01f4dba2f", "value": "Bill"},
                            {"answer_id": "answer276704e9-6b84-47a6-9a1a-fb22fdefdf32", "value": "Clive"},
                            {"answer_id": "answerabf25311-c8d6-4cf7-b6cc-194ba81b67e8", "value": "Male"},
                            {"answer_id": "answer3e9d7c8a-4dda-4f4b-ba86-5989cb8c704a", "value": "Married"},
                            {"answer_id": "answer58c5ddd1-c972-4ae5-b2eb-c0f7bc6b6f64", "value": "1940-01-01"},
                            {"answer_id": "answer692de95a-42fa-47a1-88b2-1a1e3e78a098", "value": "No"}], "lists": []},
            "started_at": "2023-01-12T16:06:22.511125+00:00", "submission_language_code": "en"}

    def test_set_dap(self):
        filename = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        expected = "001 survey response for adhoc survey"
        meta_data = MetaWrapperAdhoc(filename)
        meta_data.set_dap(self.test_adhoc)
        actual = meta_data.get_description()
        self.assertEqual(expected, actual)
        self.assertEqual(f'{filename}.json:dap', meta_data.filename)

    def test_set_legacy(self):
        filename = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        expected = "001 survey response for adhoc survey"
        meta_data = MetaWrapperAdhoc(filename)
        meta_data.set_legacy(self.test_adhoc)
        actual = meta_data.get_description()
        self.assertEqual(expected, actual)
        self.assertEqual(f'{filename}:ftp', meta_data.filename)

    def test_set_hybrid(self):
        filename = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        expected = "001 survey response for adhoc survey"
        meta_data = MetaWrapperAdhoc(filename)
        meta_data.set_hybrid(self.test_adhoc)
        actual = meta_data.get_description()
        self.assertEqual(expected, actual)
        self.assertEqual(f'{filename}:hybrid', meta_data.filename)

    def test_wcis(self):
        filename = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        expected = "739 survey response for adhoc survey"
        meta_data = MetaWrapperAdhoc(filename)
        test_adhoc = self.test_adhoc
        test_adhoc["survey_metadata"]["survey_id"] = "739"
        meta_data.set_dap(test_adhoc)
        actual = meta_data.get_description()
        self.assertEqual(expected, actual)
        self.assertEqual(f'739-{filename}.json:dap', meta_data.filename)

    def test_fuis(self):
        filename = "c37a3efa-593c-4bab-b49c-bee0613c4fb2"
        expected = "738 survey response for adhoc survey"
        meta_data = MetaWrapperAdhoc(filename)
        test_adhoc = self.test_adhoc
        test_adhoc["survey_metadata"]["survey_id"] = "738"
        meta_data.set_dap(test_adhoc)
        actual = meta_data.get_description()
        self.assertEqual(expected, actual)
        self.assertEqual(f'738-{filename}.json:dap', meta_data.filename)
