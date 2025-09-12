import logging
import os
from logging import Logger

import gnupg


def get_logger() -> Logger:
    return logging.getLogger("sdx-deliver")


logger = get_logger()


project_id = os.getenv('PROJECT_ID', 'ons-sdx-sandbox')
data_sensitivity = os.getenv('DATA_SENSITIVITY', 'High')
data_recipient = os.getenv('DATA_RECIPIENT', 'dap@ons.gov.uk')


class Config:

    def __init__(self, proj_id) -> None:
        self.PROJECT_ID = proj_id
        self.BUCKET_NAME = f'{proj_id}-outputs'
        self.DAP_TOPIC_ID = "dap-topic"
        self.ENCRYPTION_KEY = None
        self.GPG = None
        self.DATA_SENSITIVITY = data_sensitivity
        self.RECIPIENTS = [data_recipient]


CONFIG = Config(project_id)

sdx_app = SdxApp("sdx-deliver", project_id)


def setup_keys():

    gpg = gnupg.GPG()
    encryption_key = sdx_app.secrets_get('dap-public-gpg')[0]

    gpg.import_keys(encryption_key)
    CONFIG.ENCRYPTION_KEY = encryption_key
    CONFIG.GPG = gpg
