from typing import Optional, Final

from app.v2.definitions.config_schema import File
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.submission_type import DECRYPT
from app.v2.submission_types.submission_type import SubmissionType

_ZIP: Final[str] = "zip"


class CommentsSubmissionType(SubmissionType):

    def get_source_path(self) -> str:
        return "comments"

    def get_actions(self) -> list[str]:
        return [DECRYPT]

    def get_file_config(self, survey_id: Optional[str] = None) -> dict[str, File]:
        return {
            _ZIP: {
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_Submissions/Comments"
            }
        }

    def get_mapping(self, filename) -> str:
        return _ZIP
