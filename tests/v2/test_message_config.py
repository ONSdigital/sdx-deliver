import unittest

from app.v2.definitions.location_name_repository import LocationNameRepositoryBase
from app.v2.message_config import MessageConfig, FTP, WINDOWS_SERVER, SDX, SPP, DAP, SEFT_SURVEY, DECRYPT, SEFT, \
    LEGACY_SURVEY, UNZIP, PCK, IMAGE, INDEX, RECEIPT, JSON, SPP_SURVEY, DAP_SURVEY, COMMENTS, FEEDBACK, \
    SPP_AND_DAP_SURVEY, GCS, S3, CDP


class MockLocationNameRepository(LocationNameRepositoryBase):

    def get_location_name(self, key: str) -> str:
        if key == FTP:
            return "ftp"
        if key == SDX:
            return "sdx"
        if key == SPP:
            return "spp"
        if key == DAP:
            return "dap"


class TestMessageConfig(unittest.TestCase):
    def setUp(self) -> None:
        self._mocked_location_name_repository = MockLocationNameRepository()

    def test_get_config_with_survey_id(self):
        survey_id = "001"
        environment = "sdx_preprod"
        environment_capitalised = environment.upper()
        message_config = MessageConfig(self._mocked_location_name_repository)

        actual = message_config.get_config(survey_id)

        expected = {
            "locations": {
                FTP: {
                    "location_type": WINDOWS_SERVER,
                    "location_name": self._mocked_location_name_repository.get_location_name(FTP)
                },
                SDX: {
                    "location_type": GCS,
                    "location_name": self._mocked_location_name_repository.get_location_name(SDX)
                },
                SPP: {
                    "location_type": S3,
                    "location_name": self._mocked_location_name_repository.get_location_name(SPP)
                },
                DAP: {
                    "location_type": CDP,
                    "location_name": self._mocked_location_name_repository.get_location_name(DAP)
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

        self.assertEqual(expected, actual)

    def test_get_config_without_survey_id(self):
        environment = "sdx_preprod"
        environment_capitalised = environment.upper()
        survey_id = None
        message_config = MessageConfig(self._mocked_location_name_repository)

        actual = message_config.get_config()

        expected = {
            "locations": {
                FTP: {
                    "location_type": WINDOWS_SERVER,
                    "location_name": self._mocked_location_name_repository.get_location_name(FTP)
                },
                SDX: {
                    "location_type": GCS,
                    "location_name": self._mocked_location_name_repository.get_location_name(SDX)
                },
                SPP: {
                    "location_type": S3,
                    "location_name": self._mocked_location_name_repository.get_location_name(SPP)
                },
                DAP: {
                    "location_type": CDP,
                    "location_name": self._mocked_location_name_repository.get_location_name(DAP)
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

        self.assertEqual(expected, actual)
