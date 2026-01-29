from typing import Final, override

from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext
from app.submission_types.bases.survey_submission import SurveySubmission

# file types
_RECEIPT: Final[str] = "receipt"

# file extensions
_DAT: Final[str] = "dat"


class SEFTReceiptSubmissionType(SurveySubmission):

    @override
    def get_file_config(self, context: BusinessSurveyContext) -> dict[str, list[File]]:
        return {
            _RECEIPT: [self.get_ftp_receipt()],
        }

    @override
    def get_mapping(self, filename: str) -> str:
        return _RECEIPT
