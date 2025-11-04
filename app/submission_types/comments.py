from typing import Final, override, cast

from app.definitions.config_schema import File
from app.definitions.context import CommentsFileContext, Context
from app.definitions.lookup_key import LookupKey
from app.definitions.submission_type import DECRYPT
from app.submission_types.bases.submission_type import SubmissionType

_ZIP: Final[str] = "zip"


class CommentsSubmissionType(SubmissionType):

    @override
    def get_source_path(self) -> str:
        return "comments"

    @override
    def get_actions(self) -> list[str]:
        return [DECRYPT]

    @override
    def create_file_config(self, context: Context) -> dict[str, list[File]]:
        comments_context: CommentsFileContext = cast(CommentsFileContext, context)
        return self.get_file_config(comments_context)

    def get_file_config(self, _context: CommentsFileContext) -> dict[str, list[File]]:
        return {
            _ZIP: [{
                "location": LookupKey.FTP,
                "path": f"{self._get_ftp_path()}/EDC_Submissions/Comments"
            }]
        }

    @override
    def get_mapping(self, filename: str) -> str:
        return _ZIP
