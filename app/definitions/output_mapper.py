from abc import ABC, abstractmethod

from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext


class OutputMapperBase(ABC):
    @abstractmethod
    def lookup_output(self, key: str, is_prod_env: bool) -> File:
        pass

    @abstractmethod
    def map_output(self, context: BusinessSurveyContext, is_prod_env: bool) -> File:
        pass
