import json
import unittest
from app.routes_v2 import BusinessSurveyContext, SurveyType


class TestRoutesV2(unittest.TestCase):

    def test_context(self):
        context_json = '{"survey_type": "dap", "survey_id": "283", "period_id": "202503", "ru_ref": "123456789"}'
        context: BusinessSurveyContext = json.loads(context_json)
        if context["survey_type"] != SurveyType.DAP:
            self.fail()
