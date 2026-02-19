from abc import ABC, abstractmethod

from app.definitions.config_schema import File
from app.definitions.context import Context


class OutputMapperBase(ABC):
    @abstractmethod
    def lookup_output(self, key: str, is_prod_env: bool) -> File:
        pass

    @abstractmethod
    def map_output(self, context: Context, is_prod_env: bool) -> File:
        pass
