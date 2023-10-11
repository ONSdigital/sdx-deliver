import os

import gnupg
from sdx_gcp.app import get_logger, SdxApp

logger = get_logger()


project_id = os.getenv('PROJECT_ID', 'ons-sdx-sandbox')
data_sensitivity = os.getenv('DATA_SENSITIVITY', 'High')
data_recipient = os.getenv('DATA_RECIPIENT', 'dap@ons.gov.uk')
prepop_recipient = "sdx_dev@ons.gov.uk"
nifi_bucket = f'{project_id}-nifi'


class Config:

    def __init__(self, proj_id) -> None:
        self.PROJECT_ID = proj_id
        self.BUCKET_NAME = f'{proj_id}-outputs'
        self.GPG = None
        self.DATA_SENSITIVITY = data_sensitivity
        self.RECIPIENTS = [data_recipient]
        self.PREPOP_RECIPIENTS = [prepop_recipient]
        self.NIFI_BUCKET_NAME = nifi_bucket
        self.SDS_INPUT_BUCKET_NAME: str = f"{proj_id}-prepop-data"


CONFIG = Config(project_id)

sdx_app = SdxApp("sdx-deliver", project_id)


def setup_keys():

    gpg = gnupg.GPG()
    with open('sdx_public_gpg.asc') as f:
        key_data = f.read()
        f.close()
    gpg.import_keys(key_data)
    CONFIG.GPG = gpg
