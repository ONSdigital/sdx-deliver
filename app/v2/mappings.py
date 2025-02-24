from typing import Final

from app.output_type import OutputType
from app.v2.definitions.filename_mapper import FileNameMapperBase
from app.v2.definitions.submission_type_mapper import SubmissionTypeMapperBase

PCK: Final[str] = "pck"
JPG: Final[str] = "jpg"
IMAGE: Final[str] = "image"
CSV: Final[str] = "csv"
INDEX: Final[str] = "index"
DAT: Final[str] = "dat"
RECEIPT: Final[str] = "receipt"
JSON: Final[str] = "json"

SEFT_SURVEY: Final[str] = "seft_survey"
SPP_SURVEY: Final[str] = "spp_survey"
LEGACY_SURVEY: Final[str] = "legacy_survey"


class FileExtensionMapper(FileNameMapperBase):

    def get_output_type(self, filename: str) -> str:
        split_string = filename.split(".")
        if len(split_string) == 1:
            return PCK
        extension = split_string[1].lower()
        if extension == JPG:
            return IMAGE
        if extension == CSV:
            return INDEX
        if extension == DAT:
            return RECEIPT
        return JSON


class SubmissionTypeMapper(SubmissionTypeMapperBase):

    def get_submission_type(self, output_type: OutputType) -> str:
        if output_type == output_type.SEFT:
            return SEFT_SURVEY
        elif output_type == output_type.SPP:
            return SPP_SURVEY
        else:
            return LEGACY_SURVEY
