from typing import Final, Self, cast, override

from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext, Context
from app.definitions.lookup_key import LookupKey
from app.definitions.submission_type import DECRYPT, UNZIP
from app.submission_types.bases.submission_type import SubmissionType

_JSON: Final[str] = "json"


class DapSubmissionType(SubmissionType):
    @override
    def create_file_config(self, context: Context) -> dict[str, list[File]]:
        business_context: BusinessSurveyContext = cast(BusinessSurveyContext, context)
        return self.get_file_config(business_context)

    @override
    def get_source_path(self: Self) -> str:
        return "survey"

    @override
    def get_actions(self: Self) -> list[str]:
        return [DECRYPT, UNZIP]

    def _get_dap_path(self: Self) -> str:
        prod_path = "Covid_Survey/prod"
        preprod_path = "Covid_Survey/pre-prod"
        return prod_path if self._is_prod_env() else preprod_path

    def get_file_config(self, context: BusinessSurveyContext) -> dict[str, list[File]]:
        return {
            _JSON: [
                {"location": LookupKey.DAP, "path": f"{self._get_dap_path()}/{context.survey_id}/{context.period_id}/v1"}
            ]
        }

    def get_mapping(self, filename: str) -> str:
        return _JSON
