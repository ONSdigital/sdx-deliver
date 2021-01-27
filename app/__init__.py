import logging
import os
import gnupg
from google.cloud import pubsub_v1
from flask import Flask

LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'DEBUG'))
LOGGING_FORMAT = "%(asctime)s.%(msecs)06dZ|%(levelname)s: sdx-deliver: %(message)s"

logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=LOGGING_LEVEL,
)

PROJECT_ID = os.getenv('PROJECT_ID', 'ons-sdx-sandbox')
BUCKET_NAME = f'{PROJECT_ID}-outputs'
dap_topic_id = "dap-topic"
dap_publisher = pubsub_v1.PublisherClient()
dap_topic_path = dap_publisher.topic_path(PROJECT_ID, dap_topic_id)

gpg = gnupg.GPG()

with open('dap_public_key.asc') as f:
    key_data = f.read()
import_result = gpg.import_keys(key_data)


app = Flask(__name__)
from app import routes
