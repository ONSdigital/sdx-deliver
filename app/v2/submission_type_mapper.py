from abc import ABC, abstractmethod

from app.output_type import OutputType


class SubmissionTypeMapperBase(ABC):

    @abstractmethod
    def get_submission_type(self, output_type: OutputType) -> str:
        pass


class SubmissionTypeMapper(SubmissionTypeMapperBase):

    def get_submission_type(self, output_type: OutputType) -> str:
        if output_type.SEFT:
            return "seft_survey"
