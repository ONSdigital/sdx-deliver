from typing import Final, override, cast

from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext, Context
from app.definitions.lookup_key import LookupKey
from app.definitions.submission_type import DECRYPT, UNZIP
from app.submission_types.bases.submission_type import SubmissionType

_JSON: Final[str] = "json"


class FeedbackSubmissionType(SubmissionType):
    @override
    def get_source_path(self) -> str:
        return "feedback"

    @override
    def get_actions(self) -> list[str]:
        return [DECRYPT, UNZIP]

    def create_file_config(self, context: Context) -> dict[str, list[File]]:
        business_context: BusinessSurveyContext = cast(BusinessSurveyContext, context)
        return self.get_file_config(business_context)

    def get_file_config(self, context: BusinessSurveyContext) -> dict[str, list[File]]:
        return {_JSON: [{"location": LookupKey.FTP, "path": f"{self._get_ftp_path()}/EDC_QFeedback"}]}

    @override
    def get_mapping(self, filename: str) -> str:
        return _JSON
