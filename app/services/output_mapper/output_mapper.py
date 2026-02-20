from abc import abstractmethod

from sdx_base.errors.errors import UnrecoverableError

from app import get_logger
from app.definitions.config_schema import File
from app.definitions.context import Context
from app.definitions.output_mapper import OutputMapperBase
from app.services.output_mapper.output_mapper_configs import DEFAULT_KEY

logger = get_logger()


class OutputMapper[T: Context](OutputMapperBase[T]):
    def __init__(self, prod_config: dict[str, File], preprod_config: dict[str, File]) -> None:
        self.prod_config = prod_config
        self.preprod_config = preprod_config

    def lookup_output(self, key: str, is_prod_env: bool) -> File:
        """
        Looks up the output file configuration based on the provided key and environment,
        obtain the default configuration if the key is not found.
        """
        config = self.prod_config if is_prod_env else self.preprod_config
        file_output = config.get(key)
        # if the key is not found, return the default output
        if file_output is None:
            file_output = config.get(DEFAULT_KEY)

        if file_output is None:
            logger.error("No output file configuration is found and no default configuration is set!")
            logger.debug("Lookup key: %s, is_prod_env: %s", key, is_prod_env)
            raise UnrecoverableError("No output file configuration is found and no default configuration is set!")

        return file_output

    @abstractmethod
    def map_output(self, context: T, is_prod_env: bool) -> File:
        pass
