from app.v2.models.config_schema import ConfigSchema
from app.v2.models.message_schema import Location, Filetype

class ConfigLookup:
    def __init__(self, config_schema: ConfigSchema):
        self._config_schema = config_schema


    def get_source(self, submission_type: str, filename: str) -> Location:
        pass

    def get_actions(self, submission_type: str) -> list[str]:
        pass

    def get_outputs(self, submission_type: str, filename: str) -> list[Location]:
        pass
    