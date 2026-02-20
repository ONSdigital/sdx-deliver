import unittest

from sdx_base.errors.errors import UnrecoverableError

from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext
from app.definitions.context_type import ContextType
from app.definitions.lookup_key import LookupKey
from app.definitions.survey_type import SurveyType
from app.services.output_mapper.output_mapper_configs import DEFAULT_KEY, SURVEY_TAG
from app.services.output_mapper.seft_output_mapper import SEFTOutputMapper


TestConfigProd: dict[str, File] = {
    "survey1":{
        "location": LookupKey.FTP,
        "path": "prod/path1"
    },
    "survey2":{
        "location": LookupKey.NS2,
        "path": f"prod/{SURVEY_TAG}/path2"
    },
    DEFAULT_KEY: {
        "location": LookupKey.NS5,
        "path": f"default_path/prod/{SURVEY_TAG}"
    }
}

TestConfigPreProd: dict[str, File] = {
    "survey1":{
        "location": LookupKey.FTP,
        "path": "preprod/path1"
    },
    "survey2":{
        "location": LookupKey.SDX,
        "path": f"preprod/{SURVEY_TAG}/path2"
    },
    DEFAULT_KEY: {
        "location": LookupKey.NS5,
        "path": f"default_path/preprod/{SURVEY_TAG}"
    }
}

TestConfigWithoutDefault: dict[str, File] = {
    "survey1":{
        "location": LookupKey.FTP,
        "path": "prod/path1"
    },
    "survey2":{
        "location": LookupKey.NS2,
        "path": f"prod/{SURVEY_TAG}/path2"
    }
}

def create_test_context(survey_id: str) -> BusinessSurveyContext:
    return BusinessSurveyContext(
        survey_type=SurveyType.SEFT,
        context_type=ContextType.BUSINESS_SURVEY,
        survey_id=survey_id,
        period_id="2024",
        ru_ref="60226421137",
        tx_id="016931f2-6230-4ca3-b84e-136e02e3f92b"
    )

class TestSeftOutputMapper(unittest.TestCase):

    def setUp(self):
        self.output_mapper_prod = SEFTOutputMapper(
            output_config=TestConfigProd
        )
        self.output_mapper_preprod = SEFTOutputMapper(
            output_config=TestConfigPreProd
        )
        self.output_mapper_without_default = SEFTOutputMapper(
            output_config=TestConfigWithoutDefault
        )

    def test_map_output_prod(self):
        survey_id = "survey1"
        context = create_test_context(survey_id=survey_id)

        output = self.output_mapper_prod.map_output(context)
        expected_output: File = {
            "location": LookupKey.FTP,
            "path": "prod/path1"
        }
        self.assertEqual(output, expected_output)

    def test_map_output_preprod(self):
        survey_id = "survey1"
        context = create_test_context(survey_id=survey_id)

        output = self.output_mapper_preprod.map_output(context)
        expected_output: File = {
            "location": LookupKey.FTP,
            "path": "preprod/path1"
        }
        self.assertEqual(output, expected_output)

    def test_map_output_prod_with_placeholder(self):
        survey_id = "survey2"
        context = create_test_context(survey_id=survey_id)

        output = self.output_mapper_prod.map_output(context)
        expected_output: File = {
            "location": LookupKey.NS2,
            "path": "prod/survey2/path2"
        }
        self.assertEqual(output, expected_output)

    def test_map_output_preprod_with_placeholder(self):
        survey_id = "survey2"
        context = create_test_context(survey_id=survey_id)

        output = self.output_mapper_preprod.map_output(context)
        expected_output: File = {
            "location": LookupKey.SDX,
            "path": "preprod/survey2/path2"
        }
        self.assertEqual(output, expected_output)

    def test_map_output_prod_with_default(self):
        survey_id = "non_existent_survey"
        context = create_test_context(survey_id=survey_id)

        output = self.output_mapper_prod.map_output(context)
        expected_output: File = {
                "location": LookupKey.NS5,
                "path": f"default_path/prod/non_existent_survey"
        }

        self.assertEqual(output, expected_output)

    def test_map_output_prod_with_default_2(self):
        """
        This test is intended to be a copy of the previous test to ensure that the
        default output is returned consistently for different non-existent survey ids in the prod environment.
        """
        survey_id = "non_existent_survey_2"
        context = create_test_context(survey_id=survey_id)

        output = self.output_mapper_prod.map_output(context)
        expected_output: File = {
                "location": LookupKey.NS5,
                "path": f"default_path/prod/non_existent_survey_2"
        }

        self.assertEqual(output, expected_output)

    def test_map_output_preprod_with_default(self):
        survey_id = "non_existent_survey"
        context = create_test_context(survey_id=survey_id)

        output = self.output_mapper_preprod.map_output(context)
        expected_output: File = {
                "location": LookupKey.NS5,
                "path": f"default_path/preprod/non_existent_survey"
        }

        self.assertEqual(output, expected_output)

    def test_error_when_no_config_and_no_default_prod(self):
        survey_id = "non_existent_survey"
        context = create_test_context(survey_id=survey_id)

        with self.assertRaises(UnrecoverableError) as error:
            self.output_mapper_without_default.map_output(context)

        self.assertIn("No output file configuration is found and no default configuration is set",
                      str(error.exception))
