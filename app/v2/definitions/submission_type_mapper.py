from abc import ABC, abstractmethod

from app.output_type import OutputType


class SubmissionTypeMapperBase(ABC):

    @abstractmethod
    def get_submission_type(self, output_type: OutputType) -> str:
        pass


