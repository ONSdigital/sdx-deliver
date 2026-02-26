from abc import abstractmethod

from sdx_base.errors.errors import UnrecoverableError

from app import get_logger
from app.definitions.config_schema import File
from app.definitions.context import Context
from app.definitions.output_mapper import OutputMapperBase
from app.services.output_mapper.output_mapper_configs import DEFAULT_KEY

logger = get_logger()


class OutputMapper[T: Context](OutputMapperBase[T]):
    def __init__(self, output_config: dict[str, File]) -> None:
        self._output_config = output_config

    def lookup_output(self, key: str) -> File:
        """
        Looks up the output file configuration based on the provided key and environment,
        obtain the default configuration if the key is not found.
        """
        file_output = self._output_config.get(key)
        # if the key is not found, return the default output
        if file_output is None:
            file_output = self._output_config.get(DEFAULT_KEY)

        if file_output is None:
            logger.error("No output file configuration is found and no default configuration is set!")
            logger.debug("Lookup key: %s", key)
            raise UnrecoverableError("No output file configuration is found and no default configuration is set!")

        return file_output

    @abstractmethod
    def map_output(self, context: T) -> File:
        pass
