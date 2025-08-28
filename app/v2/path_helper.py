from typing import Final

from app import CONFIG


PROD_PROJECT: Final[str] = "ons-sdx-prod"


def get_ftp_path() -> str:
    return "SDX_Prod" if CONFIG.PROJECT_ID == PROD_PROJECT else "SDX_PREPROD"


def get_dap_path() -> str:
    prod_path = "Covid_Survey/prod"
    preprod_path = "Covid_Survey/pre-prod"
    return prod_path if CONFIG.PROJECT_ID == PROD_PROJECT else preprod_path


def get_ns5_path() -> str:
    return "prod" if CONFIG.PROJECT_ID == PROD_PROJECT else "preprod"
