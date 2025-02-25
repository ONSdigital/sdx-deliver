from typing import Final, Optional

from app import CONFIG
from app.v2.definitions.config_schema import ConfigSchema
from app.v2.definitions.location_name_repository import LocationNameRepositoryBase

SDX_PROD: Final[str] = "sdx_prod"
SDX_PREPROD: Final[str] = "sdx_preprod"
SDX_PROD_ENV: Final[str] = "ons-sdx-prod"


FTP: Final[str] = "ftp"
SDX: Final[str] = "sdx"
SPP: Final[str] = "spp"
DAP: Final[str] = "dap"

PCK: Final[str] = "pck"
JPG: Final[str] = "jpg"
IMAGE: Final[str] = "image"
CSV: Final[str] = "csv"
INDEX: Final[str] = "index"
DAT: Final[str] = "dat"
RECEIPT: Final[str] = "receipt"
JSON: Final[str] = "json"
SEFT: Final[str] = "seft"

WINDOWS_SERVER: Final[str] = "windows_server"
GCS: Final[str] = "gcs"
S3: Final[str] = "s3"
CDP: Final[str] = "cdp"

SEFT_SURVEY: Final[str] = "seft_survey"
SPP_SURVEY: Final[str] = "spp_survey"
DAP_SURVEY: Final[str] = "dap_survey"
SPP_AND_DAP_SURVEY: Final[str] = "spp_and_dap_survey"
LEGACY_SURVEY: Final[str] = "legacy_survey"
COMMENTS: Final[str] = "comments"
FEEDBACK: Final[str] = "feedback"

UNZIP: Final[str] = "unzip"
DECRYPT: Final[str] = "decrypt"


class MessageConfig:
    def __init__(self, location_name_repo: LocationNameRepositoryBase):
        self._location_name_repo = location_name_repo

    def get_config(self, survey_id: Optional[str] = None) -> ConfigSchema:
        environment = SDX_PROD if CONFIG.PROJECT_ID == SDX_PROD_ENV else SDX_PREPROD
        environment_capitalised = environment.upper()
        return {
            "locations": {
                FTP: {
                    "location_type": WINDOWS_SERVER,
                    "location_name": self._location_name_repo.get_location_name(FTP)
                },
                SDX: {
                    "location_type": GCS,
                    "location_name": self._location_name_repo.get_location_name(SDX)
                },
                SPP: {
                    "location_type": S3,
                    "location_name": self._location_name_repo.get_location_name(SPP)
                },
                DAP: {
                    "location_type": CDP,
                    "location_name": self._location_name_repo.get_location_name(DAP)
                }
            },
            "submission_types": {
                SEFT_SURVEY: {
                    "actions": [DECRYPT],
                    "source": {
                        "location": SDX,
                        "path": "seft"
                    },
                    "outputs": {
                        SEFT: [{
                            "location": FTP,
                            "path": f"SDX_PREPROD/EDC_Submissions/{survey_id}"
                        }]
                    }
                },
                LEGACY_SURVEY: {
                    "actions": [DECRYPT, UNZIP],
                    "source": {
                        "location": SDX,
                        "path": "survey"
                    },
                    "outputs": {
                        PCK: [{
                            "location": FTP,
                            "path": f"{environment_capitalised}/EDC_QData"
                        }],
                        IMAGE: [{
                            "location": FTP,
                            "path": f"{environment_capitalised}/EDC_QImages/Images"
                        }],
                        INDEX: [{
                            "location": FTP,
                            "path": f"{environment_capitalised}/EDC_QImages/Index"
                        }],
                        RECEIPT: [{
                            "location": FTP,
                            "path": f"{environment_capitalised}/EDC_QReceipts"
                        }],
                        JSON: [{
                            "location": FTP,
                            "path": f"{environment_capitalised}/EDC_QJson"
                        }]
                    }
                },
                SPP_SURVEY: {
                    "actions": [DECRYPT, UNZIP],
                    "source": {
                        "location": SDX,
                        "path": "survey"
                    },
                    "outputs": {
                        IMAGE: [{
                            "location": FTP,
                            "path": "SDX_PREPROD/EDC_QImages/Images"
                        }],
                        INDEX: [{
                            "location": FTP,
                            "path": "SDX_PREPROD/EDC_QImages/Index"
                        }],
                        RECEIPT: [{
                            "location": FTP,
                            "path": "SDX_PREPROD/EDC_QReceipts"
                        }],
                        "spp_data": [
                            {
                                "location": SPP,
                                "path": f"sdc-response/{survey_id}/"
                            }
                        ]
                    }
                },
                DAP_SURVEY: {
                    "actions": [DECRYPT],
                    "source": {
                        "location": SDX,
                        "path": "dap"
                    },
                    "outputs": {
                        JSON: [{
                            "location": DAP,
                            "path": f"landing_zone/{environment}/{survey_id}"
                        }],
                    }
                },
                COMMENTS: {
                    "actions": [DECRYPT],
                    "source": {
                        "location": SDX,
                        "path": "comments"
                    },
                    "outputs": {
                        JSON: [{
                            "location": FTP,
                            "path": f"{environment_capitalised}/EDC_Submissions/Comments"
                        }],
                    }
                },
                FEEDBACK: {
                    "actions": [DECRYPT],
                    "source": {
                        "location": SDX,
                        "path": "feedback"
                    },
                    "outputs": {
                        JSON: [{
                            "location": FTP,
                            "path": f"{environment_capitalised}/EDC_QFeedback"
                        }],
                    }
                },
                SPP_AND_DAP_SURVEY: {
                    "actions": [DECRYPT, UNZIP],
                    "source": {
                        "location": SDX,
                        "path": "survey"
                    },
                    "outputs": {
                        IMAGE: [{
                            "location": FTP,
                            "path": f"{environment_capitalised}/EDC_QImages/Images"
                        }],
                        INDEX: [{
                            "location": FTP,
                            "path": f"{environment_capitalised}/EDC_QImages/Index"
                        }],
                        RECEIPT: [{
                            "location": FTP,
                            "path": f"{environment_capitalised}/EDC_QReceipts"
                        }],
                        "spp_data": [
                            {
                                "location": SPP,
                                "path": f"sdc-response/{survey_id}/"
                            },
                            {
                                "location": DAP,
                                "path": f"landing_zone/{environment}/{survey_id}"
                            }
                        ]
                    }
                }
            }
        }
