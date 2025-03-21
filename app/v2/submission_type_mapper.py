from app.v2.definitions.location_key_lookup import LocationKeyLookupBase
from app.v2.definitions.submission_type import SubmissionTypeBase
from app.v2.definitions.submission_type_mapper import SubmissionTypeMapperBase
from app.v2.definitions.survey_type import SurveyType
from app.v2.submission_types.comments import CommentsSubmissionType
from app.v2.submission_types.dap_survey import DapSubmissionType
from app.v2.submission_types.feedback import FeedbackSubmissionType
from app.v2.submission_types.legacy_survey import LegacySubmissionType
from app.v2.submission_types.ns5_survey import Ns5SubmissionType
from app.v2.submission_types.seft_survey import SeftSubmissionType
from app.v2.submission_types.spp_survey import SppSubmissionType


class SubmissionTypeMapper(SubmissionTypeMapperBase):

    def __init__(self, location_key_lookup: LocationKeyLookupBase):
        self._location_key_lookup = location_key_lookup

    def get_submission_type(self, survey_type: SurveyType) -> SubmissionTypeBase:
        if survey_type == SurveyType.SEFT:
            return SeftSubmissionType(self._location_key_lookup)
        elif survey_type == SurveyType.SPP:
            return SppSubmissionType(self._location_key_lookup)
        elif survey_type == SurveyType.FEEDBACK:
            return FeedbackSubmissionType(self._location_key_lookup)
        elif survey_type == SurveyType.COMMENTS:
            return CommentsSubmissionType(self._location_key_lookup)
        elif survey_type == SurveyType.DAP:
            return DapSubmissionType(self._location_key_lookup)
        elif survey_type == SurveyType.NS5:
            return Ns5SubmissionType(self._location_key_lookup)
        else:
            return LegacySubmissionType(self._location_key_lookup)
