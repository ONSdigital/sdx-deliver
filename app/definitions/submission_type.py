from abc import ABC, abstractmethod
from typing import Final

from app.definitions.message_schema import Location
from app.definitions.context import Context

UNZIP: Final[str] = "unzip"
DECRYPT: Final[str] = "decrypt"
BATCH: Final[str] = "batch"


class SubmissionTypeBase(ABC):
    @abstractmethod
    def get_source(self, filename: str) -> Location:
        pass

    @abstractmethod
    def get_actions(self) -> list[str]:
        pass

    @abstractmethod
    def get_outputs(self, filename: str, context: Context) -> list[Location]:
        pass
