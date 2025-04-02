import json
import unittest
from app.v2.definitions.context import BusinessSurveyContext
from app.v2.definitions.survey_type import SurveyType


class TestRoutesV2(unittest.TestCase):

    def test_context(self):
        context_json = '{"survey_type": "dap", "survey_id": "283", "period_id": "202503", "ru_ref": "123456789"}'
        context: BusinessSurveyContext = json.loads(context_json)
        if context["survey_type"] != SurveyType.DAP:
            self.fail()

    def test_business_context(self):
        context_json = '{"survey_type": "dap", "period_id": "202503", "ru_ref": "123456789"}'
        context: BusinessSurveyContext = json.loads(context_json)
        expected_keys = BusinessSurveyContext.__annotations__.keys()
        print(expected_keys)
        for key in expected_keys:
            if key not in context:
                print(f"missing key: {key}")
