from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext
from app.services.output_mapper.output_mapper import OutputMapper
from app.services.output_mapper.output_mapper_configs import SURVEY_TAG


class SEFTOutputMapper(OutputMapper):
    def map_output(self, context: BusinessSurveyContext, is_prod_env: bool) -> File:
        file_output = self.lookup_output(context.survey_id, is_prod_env)

        return self.format_output(file_output, context)

    def format_output(self, file_output: File, context: BusinessSurveyContext) -> File:
        """
        Copy the output file configuration and formats it by replacing any placeholders in the path
        with actual values from the context for dynamic path
        """
        return_file_output: File = file_output.copy()
        if SURVEY_TAG in return_file_output["path"]:
            return_file_output["path"] = return_file_output["path"].format(survey_id=context.survey_id)

        return return_file_output
