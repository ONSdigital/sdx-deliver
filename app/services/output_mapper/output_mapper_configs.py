from typing import Final

from app.definitions.config_schema import File
from app.definitions.lookup_key import LookupKey

SURVEY_TAG: Final[str] = "{survey_id}"
DEFAULT_KEY: Final[str] = "default"

SEFTOutputConfigProd: dict[str, File] = {
    "057": {
        "location": LookupKey.NS3,
        "path": "OF1/ITIS/ITIS_SDB/Submissions"
    },
    "058": {
        "location": LookupKey.NS3,
        "path": "OF1/ITIS/ITIS_SDB/Submissions"
    },
    "062": {
        "location": LookupKey.FTP,
        "path": "SDX_Prod/EDC_Submissions/062"
    },
    "063": {
        "location": LookupKey.FTP,
        "path": "SDX_Prod/EDC_Submissions/063"
    },
    "064": {
        "location": LookupKey.FTP,
        "path": "SDX_Prod/EDC_Submissions/064"
    },
    "065": {
        "location": LookupKey.FTP,
        "path": "SDX_Prod/EDC_Submissions/065"
    },
    "066": {
        "location": LookupKey.FTP,
        "path": "BDD_OGD/Submissions"
    },
    "073": {
        "location": LookupKey.FTP,
        "path": "BDD_OGD/Submissions"
    },
    "074": {
        "location": LookupKey.FTP,
        "path": "BDD_OGD/Submissions"
    },
    "093": {
        "location": LookupKey.LD7,
        "path": "FiTP Pensions/Downstream_System_V3.0/production/inputs/upload_folder"
    },
    "137": {
        "location": LookupKey.FTP,
        "path": "NA_GPC/Submissions"
    },
    "141": {
        "location": LookupKey.NS2,
        "path": "s&e/ASHE/ASHE_Python_Submissions"
    },
    "200": {
        "location": LookupKey.FTP,
        "path": "OGD_GOVERD/Submissions"
    },
    "221": {
        "location": LookupKey.FTP,
        "path": "BDD_BRES/Submissions"
    },
    DEFAULT_KEY: {
        "location": LookupKey.FTP,
        "path": f"SDX_Prod/EDC_Submissions/{SURVEY_TAG}"
    }
}

SEFTOutputConfigPreProd: dict[str, File] = {
    "057": {
        "location": LookupKey.NS3,
        "path": "OF1/UAT Submissions"
    },
    "058": {
        "location": LookupKey.NS3,
        "path": "OF1/UAT Submissions"
    },
    "062": {
        "location": LookupKey.FTP,
        "path": "SDX_PREPROD/EDC_Submissions/062"
    },
    "063": {
        "location": LookupKey.FTP,
        "path": "SDX_PREPROD/EDC_Submissions/063"
    },
    "064": {
        "location": LookupKey.FTP,
        "path": "SDX_PREPROD/EDC_Submissions/064"
    },
    "065": {
        "location": LookupKey.FTP,
        "path": "SDX_PREPROD/EDC_Submissions/065"
    },
    "066": {
        "location": LookupKey.FTP,
        "path": "BDD_OGD/Submissions_PreProd"
    },
    "073": {
        "location": LookupKey.FTP,
        "path": "BDD_OGD/Submissions_PreProd"
    },
    "074": {
        "location": LookupKey.FTP,
        "path": "BDD_OGD/Submissions_PreProd"
    },
    "093": {
        "location": LookupKey.LD7,
        "path": "FiTP Pensions/Downstream_System_V3.0/Pensions_Data/Upload folder Preprod"
    },
    "137": {
        "location": LookupKey.FTP,
        "path": "NA_GPC/Submissions_PreProd"
    },
    "141": {
        "location": LookupKey.NS2,
        "path": "s&e/ASHE/ASHE_Python_Submissions_TEST"
    },
    "200": {
        "location": LookupKey.FTP,
        "path": "OGD_GOVERD/Submissions_PreProd"
    },
    "221": {
        "location": LookupKey.FTP,
        "path": "BDD_BRES/Submissions_PreProd"
    },
    DEFAULT_KEY: {
        "location": LookupKey.FTP,
        "path": f"SDX_PREPROD/EDC_Submissions/{SURVEY_TAG}"
    }
}