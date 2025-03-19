from typing import Optional, Final

from app.v2.definitions.config_schema import File
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.submission_type import UNZIP, DECRYPT
from app.v2.submission_types.submission_type import SubmissionType

# file types
_SPP: Final[str] = "spp"
_SPP_JSON: Final[str] = "spp_json"
_DATA: Final[str] = "data"
_IMAGE: Final[str] = "image"
_INDEX: Final[str] = "index"
_RECEIPT: Final[str] = "receipt"
_JSON: Final[str] = "json"
_DATA_IMAGE_INDEX: Final[str] = "data_image_index"


class DynamicSubmissionType(SubmissionType):

    def get_source_path(self) -> str:
        return "dynamic"

    def get_actions(self) -> list[str]:
        return [DECRYPT, UNZIP]

    def get_file_config(self, survey_id: Optional[str] = None) -> dict[str, list[File]]:
        return {
            "test": [{
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_Test"
            }],
            _SPP: [{
                "location": LookupKey.SPP,
                "path": f"sdc-response/{survey_id}/"
            }],
            _SPP_JSON: [
                {
                    "location": LookupKey.SPP,
                    "path": f"sdc-response/{survey_id}/"
                },
                {
                    "location": LookupKey.FTP,
                    "path": f"{self.get_env_prefix()}/EDC_QJson"
                }
            ],
            _DATA: [{
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_QData"
            }],
            _IMAGE: [{
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_QImages/Images"
            }],
            _INDEX: [{
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_QImages/Index"
            }],
            _RECEIPT: [{
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_QReceipts"
            }],
            _JSON: [{
                "location": LookupKey.FTP,
                "path": f"{self.get_env_prefix()}/EDC_QJson"
            }],
            _DATA_IMAGE_INDEX: [
                {
                    "location": LookupKey.FTP,
                    "path": f"{self.get_env_prefix()}/EDC_QData"
                },
                {
                    "location": LookupKey.FTP,
                    "path": f"{self.get_env_prefix()}/EDC_QImages/Images"
                },
                {
                    "location": LookupKey.FTP,
                    "path": f"{self.get_env_prefix()}/EDC_QImages/Index"
                },
            ]
        }

    def get_mapping(self, filename: str) -> str:
        """
        For Legacy submissions the Files can be
        determined by the file extension alone.
        """
        for f in [_DATA_IMAGE_INDEX, _SPP_JSON, _SPP, _DATA, _IMAGE, _INDEX, _RECEIPT, _JSON]:
            if f in filename:
                return f

        return _JSON
