from typing import Final, override, cast

from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext, Context
from app.definitions.lookup_key import LookupKey
from app.definitions.submission_type import DECRYPT
from app.submission_types.bases.submission_type import SubmissionType

_XLSX: Final[str] = "xlsx"


class SeftSubmissionType(SubmissionType):
    @override
    def get_source_path(self) -> str:
        return "seft"

    @override
    def get_actions(self) -> list[str]:
        return [DECRYPT]

    @override
    def create_file_config(self, context: Context) -> dict[str, list[File]]:
        business_context: BusinessSurveyContext = cast(BusinessSurveyContext, context)
        return self.get_file_config(business_context)

    def get_file_config(self, context: BusinessSurveyContext) -> dict[str, list[File]]:
        if context.survey_id == "141":
            ashe_dir: str = "ASHE_Python_Submissions" if self._is_prod_env() else "ASHE_Python_Submissions_TEST"
            return {_XLSX: [{"location": LookupKey.NS2, "path": f"s&e/ASHE/{ashe_dir}"}]}
        else:
            return {
                _XLSX: [
                    {"location": LookupKey.FTP, "path": f"{self._get_ftp_path()}/EDC_Submissions/{context.survey_id}"}
                ]
            }

    @override
    def get_mapping(self, filename: str) -> str:
        return _XLSX

    @override
    def get_output_filename(self, filename: str, _context: Context) -> str:
        # remove the .gpg extension
        return filename[:-4]
