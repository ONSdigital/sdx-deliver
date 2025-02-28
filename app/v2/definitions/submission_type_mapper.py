from abc import ABC, abstractmethod

from app.output_type import OutputType
from app.v2.definitions.submission_type import SubmissionTypeBase


class SubmissionTypeMapperBase(ABC):

    @abstractmethod
    def get_submission_type(self, output_type: OutputType) -> SubmissionTypeBase:
        pass
