import logging

from google.cloud import storage
from structlog import wrap_logger

from app import PROJECT_ID, BUCKET_NAME

logger = wrap_logger(logging.getLogger(__name__))


def write_to_bucket(data: str, filename: str, directory: str):
    """Uploads a string to the bucket."""
    path = f"{directory}/{filename}"
    storage_client = storage.Client(PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(path)
    blob.upload_from_string(data)
    logger.info(f"Successfully uploaded: {filename} to {directory}")
