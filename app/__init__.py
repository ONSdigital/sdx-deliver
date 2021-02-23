import os
import gnupg

from google.cloud import pubsub_v1, storage
from flask import Flask
from app.logger import logging_config
from app.secret_manager import get_secret

logging_config()

PROJECT_ID = os.getenv('PROJECT_ID', 'ons-sdx-sandbox')

BUCKET_NAME = f'{PROJECT_ID}-outputs'
storage_client = storage.Client(PROJECT_ID)
BUCKET = storage_client.bucket(BUCKET_NAME)
dap_topic_id = "dap-topic"
dap_publisher = None
dap_topic_path = None

# key
ENCRYPTION_KEY = None
gpg = gnupg.GPG()


def load_config():
    global dap_publisher
    dap_publisher = pubsub_v1.PublisherClient()
    global dap_topic_path
    dap_topic_path = dap_publisher.topic_path(PROJECT_ID, dap_topic_id)

    global ENCRYPTION_KEY
    ENCRYPTION_KEY = get_secret(PROJECT_ID, 'sdx-deliver-encryption')
    gpg.import_keys(ENCRYPTION_KEY)


app = Flask(__name__)
from app import routes
