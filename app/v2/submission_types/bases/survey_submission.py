from abc import ABC, abstractmethod

from app.v2.definitions.config_schema import File
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.submission_type import DECRYPT, UNZIP
from app.v2.path_helper import get_ftp_path
from app.v2.definitions.context import BusinessSurveyContext
from app.v2.submission_types.bases.submission_type import SubmissionType


class SurveySubmission(SubmissionType, ABC):

    @abstractmethod
    def get_file_config(self, context: BusinessSurveyContext) -> dict[str, [File]]:
        pass

    def get_source_path(self) -> str:
        return "survey"

    def get_actions(self) -> list[str]:
        return [DECRYPT, UNZIP]

    def get_ftp_image(self) -> File:
        return {
            "location": LookupKey.FTP,
            "path": f"{get_ftp_path()}/EDC_QImages/Images"
        }

    def get_ftp_index(self) -> File:
        return {
            "location": LookupKey.FTP,
            "path": f"{get_ftp_path()}/EDC_QImages/Index"
        }

    def get_ftp_receipt(self) -> File:
        return {
            "location": LookupKey.FTP,
            "path": f"{get_ftp_path()}/EDC_QReceipts"
        }

    def get_ftp_eq_json(self) -> File:
        return {
            "location": LookupKey.FTP,
            "path": f"{get_ftp_path()}/EDC_QJson"
        }
