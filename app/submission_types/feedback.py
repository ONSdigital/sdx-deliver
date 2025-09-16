from typing import Final

from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext
from app.definitions.location_name_repository import LookupKey
from app.definitions.submission_type import DECRYPT, UNZIP
from app.path_helper import get_ftp_path
from app.submission_types.bases.submission_type import SubmissionType

_JSON: Final[str] = "json"


class FeedbackSubmissionType(SubmissionType):

    def get_source_path(self) -> str:
        return "feedback"

    def get_actions(self) -> list[str]:
        return [DECRYPT, UNZIP]

    def get_file_config(self, context: BusinessSurveyContext) -> dict[str, list[File]]:
        return {
            _JSON: [{
                "location": LookupKey.FTP,
                "path": f"{get_ftp_path()}/EDC_QFeedback"
            }]
        }

    def get_mapping(self, filename: str) -> str:
        return _JSON
