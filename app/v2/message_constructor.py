from app import CONFIG
from app.v2.config_lookup import ConfigLookup
from app.v2.definitions.filename_mapper import FileNameMapperBase
from app.v2.definitions.config_schema import ConfigSchema
from app.v2.definitions.message_schema import SchemaDataV2, Target, Location
from app.meta_wrapper import MetaWrapper, MetaWrapperAdhoc
from app.output_type import OutputType
from app.v2.definitions.submission_type_mapper import SubmissionTypeMapperBase


class MessageConstructor:

    def __init__(self, config_schema: ConfigSchema,
                 file_name_mapper: FileNameMapperBase,
                 submission_mapper: SubmissionTypeMapperBase):
        self.config_lookup = ConfigLookup(config_schema)
        self.file_name_mapper = file_name_mapper
        self.submission_mapper = submission_mapper

    def build_message(self, filenames: list[str], meta_data: MetaWrapper) -> SchemaDataV2:
        submission_type: str = self.submission_mapper.get_submission_type(meta_data.output_type)
        message: SchemaDataV2 = {
            "schema_version": "2",
            "sensitivity": CONFIG.DATA_SENSITIVITY,
            "sizeBytes": meta_data.sizeBytes,
            "md5sum": meta_data.md5sum,
            "context": self.get_context(meta_data),
            "source": self.get_source(meta_data.input_filename, submission_type),
            "actions": self.get_actions(submission_type),
            "targets": self.get_targets(filenames, submission_type)
        }
        return message

    def get_source(self, filename: str, submission_type: str) -> Location:
        location = self.config_lookup.get_source(submission_type, filename)
        return location

    def get_targets(self, filenames: list[str], submission_type: str) -> list[Target]:
        target_list: list[Target] = []
        for file in filenames:
            output_type = self.file_name_mapper.get_output_type(file)
            location_list = self.config_lookup.get_outputs(submission_type, output_type, file)
            outputs: list[Location] = []
            for location in location_list:
                outputs.append(location)

            target_list.append({"input": file, "outputs": outputs})

        return target_list

    def get_actions(self, submission_type: str) -> list[str]:
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
            "period_id": meta_data.period,
            "ru_ref": meta_data.ru_ref,
        }
