from app.output_type import OutputType
from app.v2.definitions.location_key_lookup import LocationKeyLookupBase
from app.v2.definitions.submission_type import SubmissionTypeBase
from app.v2.definitions.submission_type_mapper import SubmissionTypeMapperBase
from app.v2.submission_types.comments import CommentsSubmissionType
from app.v2.submission_types.dap_survey import DapSubmissionType
from app.v2.submission_types.feedback import FeedbackSubmissionType
from app.v2.submission_types.legacy_survey import LegacySubmissionType
from app.v2.submission_types.seft_survey import SeftSubmissionType
from app.v2.submission_types.spp_survey import SppSubmissionType


class SubmissionTypeMapper(SubmissionTypeMapperBase):

    def __init__(self, location_key_lookup: LocationKeyLookupBase):
        self._location_key_lookup = location_key_lookup

    def get_submission_type(self, output_type: OutputType) -> SubmissionTypeBase:
        if output_type == output_type.SEFT:
            return SeftSubmissionType(self._location_key_lookup)
        elif output_type == output_type.SPP:
            return SppSubmissionType(self._location_key_lookup)
        elif output_type == output_type.FEEDBACK:
            return FeedbackSubmissionType(self._location_key_lookup)
        elif output_type == output_type.COMMENTS:
            return CommentsSubmissionType(self._location_key_lookup)
        elif output_type == output_type.DAP:
            return DapSubmissionType(self._location_key_lookup)
        else:
            return LegacySubmissionType(self._location_key_lookup)
