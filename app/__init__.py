import logging
import os

from google.cloud import pubsub_v1
from flask import Flask

LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'INFO'))
LOGGING_FORMAT = "%(asctime)s.%(msecs)06dZ|%(levelname)s: sdx-deliver: %(message)s"

logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=LOGGING_LEVEL,
)

project_id = "ons-sdx-sandbox"
dap_topic_id = "dap-topic"
dap_publisher = pubsub_v1.PublisherClient()
dap_topic_path = dap_publisher.topic_path(project_id, dap_topic_id)

app = Flask(__name__)
from app import routes
