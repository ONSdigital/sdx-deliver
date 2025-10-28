from typing import Final, Self, cast, override

from app.definitions.config_schema import File
from app.definitions.context import Context, AdhocSurveyContext
from app.definitions.lookup_key import LookupKey
from app.definitions.submission_type import DECRYPT, UNZIP, BATCH
from app.submission_types.bases.submission_type import SubmissionType

_JSON: Final[str] = "json"


class AdhocSubmissionType(SubmissionType):

    @override
    def create_file_config(self, context: Context) -> dict[str, list[File]]:
        business_context: AdhocSurveyContext = cast(AdhocSurveyContext, context)
        return self.get_file_config(business_context)

    @override
    def get_source_path(self: Self) -> str:
        return "survey"

    @override
    def get_actions(self: Self) -> list[str]:
        return [DECRYPT, UNZIP, BATCH]

    def _get_dap_path(self: Self) -> str:
        if self._is_prod_env():
            return "dapsen/landing_zone/ons/covid_resp_inf_surv_response/prod/phm_740_health_insights_2024/v1/"
        else:
            return "dapsen/landing_zone/ons/covid_resp_inf_surv_response/preprod/phm_740_health_insights_2024/v1/"

    def get_file_config(self, _context: AdhocSurveyContext) -> dict[str, list[File]]:
        return {
            _JSON: [{
                "location": LookupKey.CDP,
                "path": self._get_dap_path()
            }]
        }

    def get_mapping(self, filename: str) -> str:
        return _JSON
