from typing import Optional, Final

from app.v2.definitions.config_schema import File
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.submission_type import DECRYPT
from app.v2.submission_types.bases.submission_type import SubmissionType

_XLSX: Final[str] = "xlsx"


class SeftSubmissionType(SubmissionType):

    def get_source_path(self) -> str:
        return "seft"

    def get_actions(self) -> list[str]:
        return [DECRYPT]

    def get_file_config(self, survey_id: Optional[str] = None) -> dict[str, File]:
        return {
            _XLSX: {
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_Submissions/{survey_id}"
            }
        }

    def get_mapping(self, filename) -> str:
        return _XLSX
