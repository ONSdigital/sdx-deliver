from typing import override

from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext
from app.services.output_mapper.output_mapper import OutputMapper
from app.services.output_mapper.output_mapper_configs import SURVEY_TAG


class SEFTOutputMapper(OutputMapper):
    @override
    def map_output(self, context: BusinessSurveyContext, is_prod_env: bool) -> File:
        file_output = self.lookup_output(context.survey_id, is_prod_env)

        return self.format_output(file_output, context)

    def format_output(self, file_output: File, context: BusinessSurveyContext) -> File:
        """
        Formats the output file configuration by replacing any placeholders in the path
        with actual values from the context for dynamic path
        """
        if SURVEY_TAG in file_output["path"]:
            file_output["path"] = file_output["path"].format(survey_id=context.survey_id)

        return file_output
