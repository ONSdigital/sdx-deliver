from typing import Final, override

from sdx_base.errors.errors import DataError

from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext
from app.definitions.lookup_key import LookupKey

from app.submission_types.bases.survey_submission import SurveySubmission

# file types
_IMAGE: Final[str] = "image"
_INDEX: Final[str] = "index"
_RECEIPT: Final[str] = "receipt"
_SPP: Final[str] = "spp"

# file extensions
_JPG: Final[str] = "jpg"
_CSV: Final[str] = "csv"
_DAT: Final[str] = "dat"


class SppSubmissionType(SurveySubmission):

    @override
    def get_file_config(self, context: BusinessSurveyContext) -> dict[str, list[File]]:
        return {
            _IMAGE: [self.get_ftp_image()],
            _INDEX: [self.get_ftp_index()],
            _RECEIPT: [self.get_ftp_receipt()],
            _SPP: [{
                "location": LookupKey.SPP,
                "path": f"sdc-response/{context.survey_id}/"
            }]
        }

    @override
    def get_mapping(self, filename: str) -> str:
        split_string = filename.split(".")
        if len(split_string) < 2:
            raise DataError("All filenames to SPP should have a file extension!")
        extension = split_string[1].lower()
        if extension == _JPG:
            return _IMAGE
        if extension == _CSV:
            return _INDEX
        if extension == _DAT:
            return _RECEIPT
        return _SPP
