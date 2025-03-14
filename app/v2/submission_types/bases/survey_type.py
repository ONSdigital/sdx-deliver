from abc import ABC

from app.v2.definitions.config_schema import File
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.submission_types.bases.submission_type import SubmissionType


class SurveyType(SubmissionType, ABC):

    def get_ftp_image(self) -> File:
        return {
            "location": LookupKey.FTP,
            "path": f"{self.get_env_prefix()}/EDC_QImages/Images"
        }

    def get_ftp_index(self) -> File:
        return {
            "location": LookupKey.FTP,
            "path": f"{self.get_env_prefix()}/EDC_QImages/Index"
        }

    def get_ftp_receipt(self) -> File:
        return {
            "location": LookupKey.FTP,
            "path": f"{self.get_env_prefix()}/EDC_QReceipts"
        }

    def get_ftp_eq_json(self) -> File:
        return {
            "location": LookupKey.FTP,
            "path": f"{self.get_env_prefix()}/EDC_QJson"
        }
