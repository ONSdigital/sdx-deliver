from abc import ABC, abstractmethod
from typing import Optional, Final

from app.v2.definitions.message_schema import Location

# Allowed Actions
UNZIP: Final[str] = "unzip"
DECRYPT: Final[str] = "decrypt"


class SubmissionTypeBase(ABC):

    @abstractmethod
    def get_source(self, filename: str) -> Location:
        """Return a Location that describes where Nifi should pick up this submission from"""
        pass

    @abstractmethod
    def get_actions(self) -> list[str]:
        """Return a list of actions for Nifi to perform when processing this submission"""
        pass

    @abstractmethod
    def get_outputs(self, filename: str, survey_id: Optional[str] = None) -> list[Location]:
        """Return a list of Locations that describe where Nifi should place
        the files generated from this submission"""
        pass
