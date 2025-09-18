from app.definitions.submission_type import SubmissionTypeBase
from app.definitions.submission_type_mapper import SubmissionTypeMapperBase
from app.definitions.survey_type import SurveyType
from app.submission_types.bases.submission_type import LocationKeyLookuper
from app.submission_types.comments import CommentsSubmissionType
from app.submission_types.dap_survey import DapSubmissionType
from app.submission_types.environmental_survey import EnvironmentalSubmissionType
from app.submission_types.feedback import FeedbackSubmissionType
from app.submission_types.legacy_survey import LegacySubmissionType
from app.submission_types.materials_survey import MaterialsSubmissionType
from app.submission_types.seft_survey import SeftSubmissionType
from app.submission_types.spp_survey import SppSubmissionType


class SubmissionTypeMapper(SubmissionTypeMapperBase):

    def __init__(self, key_lookup: LocationKeyLookuper):
        self._key_lookup = key_lookup

    def get_submission_type(self, survey_type: SurveyType) -> SubmissionTypeBase:
        if survey_type == SurveyType.SEFT:
            return SeftSubmissionType(self._key_lookup)
        elif survey_type == SurveyType.SPP:
            return SppSubmissionType(self._key_lookup)
        elif survey_type == SurveyType.FEEDBACK:
            return FeedbackSubmissionType(self._key_lookup)
        elif survey_type == SurveyType.COMMENTS:
            return CommentsSubmissionType(self._key_lookup)
        elif survey_type == SurveyType.DAP:
            return DapSubmissionType(self._key_lookup)
        elif survey_type == SurveyType.ENVIRONMENTAL:
            return EnvironmentalSubmissionType(self._key_lookup)
        elif survey_type == SurveyType.MATERIALS:
            return MaterialsSubmissionType(self._key_lookup)
        else:
            return LegacySubmissionType(self._key_lookup)
