from typing import Optional

from app.definitions.location import LocationBase
from app.definitions.output_mapper import OutputMapperBase
from app.definitions.submission_type import SubmissionTypeBase
from app.definitions.submission_type_mapper import SubmissionTypeMapperBase
from app.definitions.survey_type import SurveyType
from app.services.output_mapper.output_mapper_configs import SEFTOutputConfigProd, SEFTOutputConfigPreProd
from app.services.output_mapper.seft_output_mapper import SEFTOutputMapper
from app.submission_types.adhoc_survey import AdhocSubmissionType
from app.submission_types.comments import CommentsSubmissionType
from app.submission_types.dap_survey import DapSubmissionType
from app.submission_types.dexta_survey import DextaSubmissionType
from app.submission_types.environmental_survey import EnvironmentalSubmissionType
from app.submission_types.feedback import FeedbackSubmissionType
from app.submission_types.legacy_survey import LegacySubmissionType
from app.submission_types.materials_survey import MaterialsSubmissionType
from app.submission_types.seft_receipt import SEFTReceiptSubmissionType
from app.submission_types.seft_survey import SeftSubmissionType
from app.submission_types.spp_survey import SppSubmissionType


class SubmissionTypeMapper(SubmissionTypeMapperBase):

    def __init__(self, location_service: LocationBase) -> None:
        self._location_service = location_service

    def get_submission_type(self,
                            survey_type: SurveyType) -> SubmissionTypeBase:
        if survey_type == SurveyType.ADHOC:
            return AdhocSubmissionType(self._location_service)
        elif survey_type == SurveyType.SEFT:
            seft_output_mapper = self.get_seft_output_mapper()
            return SeftSubmissionType(self._location_service, seft_output_mapper)
        elif survey_type == SurveyType.SEFT_RECEIPT:
            return SEFTReceiptSubmissionType(self._location_service)
        elif survey_type == SurveyType.SPP:
            return SppSubmissionType(self._location_service)
        elif survey_type == SurveyType.FEEDBACK:
            return FeedbackSubmissionType(self._location_service)
        elif survey_type == SurveyType.COMMENTS:
            return CommentsSubmissionType(self._location_service)
        elif survey_type == SurveyType.DAP:
            return DapSubmissionType(self._location_service)
        elif survey_type == SurveyType.ENVIRONMENTAL:
            return EnvironmentalSubmissionType(self._location_service)
        elif survey_type == SurveyType.MATERIALS:
            return MaterialsSubmissionType(self._location_service)
        elif survey_type == SurveyType.DEXTA:
            return DextaSubmissionType(self._location_service)
        else:
            return LegacySubmissionType(self._location_service)

    def get_seft_output_mapper(self) -> SEFTOutputMapper:
        output_config = SEFTOutputConfigProd if self._location_service.is_prod_env() else SEFTOutputConfigPreProd
        return SEFTOutputMapper(output_config=output_config)


