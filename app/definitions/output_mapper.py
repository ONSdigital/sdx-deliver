from abc import ABC, abstractmethod
from app.definitions.config_schema import File
from app.definitions.context import Context

class OutputMapperBase[T: Context](ABC):
    @abstractmethod
    def lookup_output(self, key: str) -> File:
        pass

    @abstractmethod
    def map_output(self, context: T) -> File:
        pass
