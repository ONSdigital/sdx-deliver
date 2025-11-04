from abc import ABC, abstractmethod
from typing import cast, override

from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext, Context
from app.definitions.lookup_key import LookupKey
from app.definitions.submission_type import UNZIP, DECRYPT
from app.submission_types.bases.submission_type import SubmissionType


class SurveySubmission(SubmissionType, ABC):

    @abstractmethod
    def get_file_config(self, context: BusinessSurveyContext) -> dict[str, list[File]]:
        pass

    @override
    def create_file_config(self, context: Context) -> dict[str, list[File]]:
        business_context: BusinessSurveyContext = cast(BusinessSurveyContext, context)
        return self.get_file_config(business_context)

    @override
    def get_source_path(self) -> str:
        return "survey"

    @override
    def get_actions(self) -> list[str]:
        return [DECRYPT, UNZIP]

    def get_ftp_image(self) -> File:
        return {
            "location": LookupKey.FTP,
            "path": f"{self._get_ftp_path()}/EDC_QImages/Images"
        }

    def get_ftp_index(self) -> File:
        return {
            "location": LookupKey.FTP,
            "path": f"{self._get_ftp_path()}/EDC_QImages/Index"
        }

    def get_ftp_receipt(self) -> File:
        return {
            "location": LookupKey.FTP,
            "path": f"{self._get_ftp_path()}/EDC_QReceipts"
        }

    def get_ftp_eq_json(self) -> File:
        return {
            "location": LookupKey.FTP,
            "path": f"{self._get_ftp_path()}/EDC_QJson"
        }
