from typing import Optional, Final

from app.v2.definitions.config_schema import LocationKey, File
from app.v2.definitions.location_key_lookup import LocationKeyLookupBase
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.message_schema import Location
from app.v2.message_config import DECRYPT
from app.v2.submission_types.submission_type import SubmissionType


_XLSX: Final[str] = "xlsx"


class SeftSubmissionType(SubmissionType):

    def get_file_config(self, survey_id: Optional[str] = None) -> dict[str, File]:
        return {
            _XLSX: {
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_Submissions/{survey_id}"
            }
        }

    def _get_mapping(self, filename) -> str:
        return _XLSX

    def get_source_path(self) -> str:
        return "seft"

    def get_actions(self) -> list[str]:
        return [DECRYPT]
