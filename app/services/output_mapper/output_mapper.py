from abc import abstractmethod

from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext
from app.definitions.output_mapper import OutputMapperBase
from app.services.output_mapper.output_mapper_configs import DEFAULT_KEY


class OutputMapper(OutputMapperBase):
    def __init__(self, prod_config: dict[str, File], preprod_config: dict[str, File]) -> None:
        self.prod_config = prod_config
        self.preprod_config = preprod_config

    def lookup_output(self, key: str, is_prod_env: bool) -> File:
        """
        Looks up the output file configuration based on the provided key and environment,
        obtain the default configuration if the key is not found,
        and returns a copy of the file configuration to prevent unintended mutations.
        """
        config = self.prod_config if is_prod_env else self.preprod_config
        file_output = config.get(key)
        # if the key is not found, return the default output
        if file_output is None:
            file_output = config.get(DEFAULT_KEY)

        return file_output.copy()

    @abstractmethod
    def map_output(self, context: BusinessSurveyContext, is_prod_env: bool) -> File:
        pass
