from app.v2.config_lookup import ConfigLookup
from app.v2.filename_mapper import FileNameMapperBase
from app.v2.models.config_schema import ConfigSchema
from app.v2.models.message_schema import SchemaDataV2, Target, Location
from app.meta_wrapper import MetaWrapper, MetaWrapperAdhoc
from app.output_type import OutputType


class MessageConstructor:

    def __init__(self, config_schema: ConfigSchema, file_name_mapper: FileNameMapperBase):
        self.config_lookup = ConfigLookup(config_schema)
        self.file_name_mapper = file_name_mapper

    def build_message(self, filenames: list[str], meta_data: MetaWrapper) -> SchemaDataV2:
        pass

    def get_source(self, filename: str, submission_type: str) -> Location:
        location = self.config_lookup.get_source(submission_type, filename)
        return location

    def get_target(self, filenames: list[str], submission_type: str) -> list[Target]:
        target_list: list[Target] = []
        for file in filenames:
            output_type = self.file_name_mapper.get_output_type(file)
            location_list = self.config_lookup.get_outputs(submission_type, output_type, file)
            outputs: list[Location] = []
            for location in location_list:
                outputs.append(location)

            target_list.append({"input": file, "outputs": outputs})

        return target_list

    def get_action(self, submission_type: str) -> list[str]:
        return self.config_lookup.get_actions(submission_type)
    
    def get_context(self, meta_data: MetaWrapper) -> dict[str, str]:
        if meta_data.output_type == OutputType.COMMENTS:
            return {
                "title": "Comments.zip"
            }
        
        if isinstance(meta_data, MetaWrapperAdhoc):
            return {
                "survey_id": meta_data.survey_id,
                "title": meta_data.get_description()
            }

        return {
            "survey_id": meta_data.survey_id,
            "period": meta_data.period,
            "ru_ref": meta_data.ru_ref,
        }