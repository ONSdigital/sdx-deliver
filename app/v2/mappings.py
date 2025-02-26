from app import sdx_app
from app import CONFIG
from app.output_type import OutputType
from app.v2.definitions.filename_mapper import FileNameMapperBase
from app.v2.definitions.location_name_repository import LocationNameRepositoryBase
from app.v2.definitions.submission_type_mapper import SubmissionTypeMapperBase
from app.v2.message_config import PCK, JPG, IMAGE, CSV, INDEX, DAT, RECEIPT, JSON, SEFT_SURVEY, SPP_SURVEY, \
    LEGACY_SURVEY, FTP, SDX, SPP, DAP, ZIP, SEFT, GPG, FEEDBACK

NIFI_LOCATION_FTP = "nifi-location-ftp"
NIFI_LOCATION_SPP = "nifi-location-spp"
NIFI_LOCATION_DAP = "nifi-location-dap"


class FileExtensionMapper(FileNameMapperBase):

    def get_output_type(self, filename: str, submission_type: str) -> str:
        if submission_type == FEEDBACK:
            return JSON

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
        if extension == ZIP:
            return ZIP
        if extension == GPG:
            return SEFT
        return JSON


class SubmissionTypeMapper(SubmissionTypeMapperBase):

    def get_submission_type(self, output_type: OutputType) -> str:
        if output_type == output_type.SEFT:
            return SEFT_SURVEY
        elif output_type == output_type.SPP:
            return SPP_SURVEY
        elif output_type == output_type.FEEDBACK:
            return FEEDBACK
        else:
            return LEGACY_SURVEY


class LocationNameMapper(LocationNameRepositoryBase):

    def __init__(self):
        self.locations_mapping = None

    def get_location_name(self, key: str) -> str:
        return self.locations_mapping[key]

    def load_location_values(self):
        if self.locations_mapping is None:
            self.locations_mapping = {
                FTP: sdx_app.secrets_get(NIFI_LOCATION_FTP)[0],
                SDX: CONFIG.BUCKET_NAME,
                SPP: sdx_app.secrets_get(NIFI_LOCATION_SPP)[0],
                DAP: sdx_app.secrets_get(NIFI_LOCATION_DAP)[0]
            }