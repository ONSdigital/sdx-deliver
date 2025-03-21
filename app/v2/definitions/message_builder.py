from abc import ABC, abstractmethod

from app.v2.definitions.message_schema import MessageSchemaV2, Location, Target
from app.v2.definitions.submission_type import SubmissionTypeBase
from app.v2.definitions.context import Context
from app.v2.definitions.zip_details import ZipDetails


class MessageBuilderBase(ABC):

    @abstractmethod
    def build_message(self, zip_details: ZipDetails, context: Context) -> MessageSchemaV2:
        pass

    @abstractmethod
    def get_source(self, filename: str, submission_type: SubmissionTypeBase) -> Location:
        pass

    @abstractmethod
    def get_targets(self, filenames: list[str], submission_type: SubmissionTypeBase, context: Context) -> list[Target]:
        pass

    @abstractmethod
    def get_actions(self, submission_type: SubmissionTypeBase) -> list[str]:
        pass

    @abstractmethod
    def get_context(self, context: Context) -> dict[str, str]:
        pass
