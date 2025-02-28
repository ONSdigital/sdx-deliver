from abc import ABC, abstractmethod
from typing import Optional, Final

from app.v2.definitions.message_schema import Location

UNZIP: Final[str] = "unzip"
DECRYPT: Final[str] = "decrypt"


class SubmissionTypeBase(ABC):

    @abstractmethod
    def get_source(self, filename: str) -> Location:
        pass

    @abstractmethod
    def get_actions(self) -> list[str]:
        pass

    @abstractmethod
    def get_outputs(self, filename: str, survey_id: Optional[str] = None) -> list[Location]:
        pass
