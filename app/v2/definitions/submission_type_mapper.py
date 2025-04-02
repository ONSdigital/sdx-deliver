from abc import ABC, abstractmethod

from app.v2.definitions.submission_type import SubmissionTypeBase
from app.v2.definitions.survey_type import SurveyType


class SubmissionTypeMapperBase(ABC):

    @abstractmethod
    def get_submission_type(self, survey_type: SurveyType) -> SubmissionTypeBase:
        pass
