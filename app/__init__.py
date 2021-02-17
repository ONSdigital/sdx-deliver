import logging
import os
import gnupg

from google.cloud import pubsub_v1
from flask import Flask
from app.logger import logging_config
from app.secret_manager import get_secret

logging_config()

PROJECT_ID = os.getenv('PROJECT_ID', 'ons-sdx-chaitali')
BUCKET_NAME = f'{PROJECT_ID}-outputs'
dap_topic_id = "dap-topic"
dap_publisher = pubsub_v1.PublisherClient()
dap_topic_path = dap_publisher.topic_path(PROJECT_ID, dap_topic_id)

gpg = gnupg.GPG()

ENCRYPTION_KEY = get_secret(PROJECT_ID, 'sdx-deliver-encryption')
import_result = gpg.import_keys(ENCRYPTION_KEY)


app = Flask(__name__)
from app import routes
