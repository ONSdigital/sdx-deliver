from app.output_type import OutputType
from app.v2.definitions.filename_mapper import FileNameMapperBase
from app.v2.definitions.submission_type_mapper import SubmissionTypeMapperBase
from app.v2.message_config import PCK, JPG, IMAGE, CSV, INDEX, DAT, RECEIPT, JSON, SEFT_SURVEY, SPP_SURVEY, \
    LEGACY_SURVEY


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
