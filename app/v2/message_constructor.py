from app.v2.config_lookup import ConfigLookup
from app.v2.filename_mapper import FileNameMapperBase
from app.v2.models.config_schema import ConfigSchema
from app.v2.models.message_schema import SchemaDataV2, Target, Location


class MessageConstructor:

    def __init__(self, config_schema: ConfigSchema, file_name_mapper: FileNameMapperBase):
        self.config_lookup = ConfigLookup(config_schema)
        self.file_name_mapper = file_name_mapper

    def build_message(self, filenames: list[str], submission_type: str, context) -> SchemaDataV2:
        pass

    def get_source(self):
        pass

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
