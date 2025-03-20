import hashlib

from sdx_gcp.app import get_logger

from app import sdx_app, CONFIG
from app.definitions import MessageSchema
from app.encrypt import encrypt_output
from app.message import create_message
from app.meta_wrapper import MetaWrapper
from app.output_type import OutputType
from app.publish import publish_v2_message, publish_message
from app.routes_v2 import BusinessSurveyContext
from app.store import write_to_bucket
from app.v2.definitions.location_key_lookup import LocationKeyLookupBase
from app.v2.definitions.message_schema import MessageSchemaV2
from app.v2.location_key_lookup import LocationKeyLookup
from app.v2.submission_type_mapper import SubmissionTypeMapper
from app.v2.location_name_repo import LocationNameRepo
from app.v2.message_builder import MessageBuilder
from app.v2.definitions.location_name_repository import LocationNameRepositoryBase
from app.v2.zip import unzip

logger = get_logger()
location_name_repo: LocationNameRepositoryBase = LocationNameRepo()


def deliver_survey(filename: str, context: BusinessSurveyContext, data_bytes: bytes):
    """
    Encrypts any unencrypted data, writes to the appropriate location within the outputs GCP bucket and notifies DAP
    via PubSub
    """
    logger.info("Encrypting output")
    encrypted_output = encrypt_output(data_bytes)
    encrypted_bytes = encrypted_output.encode()
    md5sum = hashlib.md5(encrypted_bytes).hexdigest()
    size_bytes = len(encrypted_bytes)

    logger.info("Storing to bucket")
    sdx_app.gcs_write(encrypted_output, filename, CONFIG.BUCKET_NAME, "survey")

    logger.info("Sending Nifi message")

    location_name_repo.load_location_values()
    location_key_lookup: LocationKeyLookupBase = LocationKeyLookup(location_name_repo)
    message_constructor = MessageBuilder(submission_mapper=SubmissionTypeMapper(location_key_lookup))

    filenames = unzip(data_bytes)
    v2_message: MessageSchemaV2 = message_constructor.build_message(filenames, meta_data)
    publish_v2_message(v2_message, meta_data.tx_id)

    logger.info("Process completed successfully", survey_id=meta_data.survey_id)
