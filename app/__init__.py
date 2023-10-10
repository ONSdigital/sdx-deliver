import os

import gnupg
from sdx_gcp.app import get_logger, SdxApp

logger = get_logger()


ROOT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
project_id = os.getenv('PROJECT_ID', 'ons-sdx-sandbox')
data_sensitivity = os.getenv('DATA_SENSITIVITY', 'High')
data_recipient = os.getenv('DATA_RECIPIENT', 'dap@ons.gov.uk')


class Config:

    def __init__(self, proj_id) -> None:
        self.PROJECT_ID = proj_id
        self.BUCKET_NAME = f'{proj_id}-outputs'
        self.GPG = None
        self.DATA_SENSITIVITY = data_sensitivity
        self.RECIPIENTS = [data_recipient]


CONFIG = Config(project_id)

sdx_app = SdxApp("sdx-deliver", project_id)


def setup_keys():

    gpg = gnupg.GPG()
    with open(f'{ROOT_FOLDER}/sdx_public_gpg.asc') as f:
        key_data = f.read()
        f.close()
    gpg.import_keys(key_data)
    CONFIG.GPG = gpg
