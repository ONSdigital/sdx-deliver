import hashlib
import json

from sdx_gcp.app import get_logger
from app.encrypt import encrypt_output
from app.meta_wrapper import MetaWrapper
from app.output_type import OutputType
from app.publish import send_message, publish_v2_schema
from app.store import write_to_bucket
from app.v2.definitions.location_key_lookup import LocationKeyLookupBase
from app.v2.definitions.message_schema import SchemaDataV2
from app.v2.location_key_lookup import LocationKeyLookup
from app.v2.submission_type_mapper import SubmissionTypeMapper
from app.v2.location_name_repo import LocationNameRepo
from app.v2.message_builder import MessageBuilder
from app.v2.definitions.location_name_repository import LocationNameRepositoryBase
from app.v2.zip import unzip

logger = get_logger()
location_name_repo: LocationNameRepositoryBase = LocationNameRepo()


def deliver(meta_data: MetaWrapper, data_bytes: bytes, v2_message_schema: bool = False):
    """
    Encrypts any unencrypted data, writes to the appropriate location within the outputs GCP bucket and notifies DAP
    via PubSub
    """
    if meta_data.output_type == OutputType.SEFT:
        encrypted_output = data_bytes
    else:
        logger.info("Encrypting output")
        encrypted_output = encrypt_output(data_bytes)
        encrypted_bytes = encrypted_output.encode()
        meta_data.md5sum = hashlib.md5(encrypted_bytes).hexdigest()
        meta_data.sizeBytes = len(encrypted_bytes)

    logger.info("Storing to bucket")
    path = write_to_bucket(encrypted_output, filename=meta_data.filename, output_type=meta_data.output_type)

    logger.info("Sending DAP notification")
    if v2_message_schema:
        location_name_repo.load_location_values()
        location_key_lookup: LocationKeyLookupBase = LocationKeyLookup(location_name_repo)
        message_constructor = MessageBuilder(submission_mapper=SubmissionTypeMapper(location_key_lookup))

        if meta_data.output_type == OutputType.LEGACY or meta_data.output_type == OutputType.SPP or meta_data.output_type == OutputType.DYNAMIC:
            filenames = unzip(data_bytes)
        else:
            filenames = [meta_data.output_filename]

        v2_message: SchemaDataV2 = message_constructor.build_message(filenames, meta_data)
        print(json.dumps(v2_message))
        publish_v2_schema(v2_message, meta_data.tx_id)

    else:
        send_message(meta_data, path)

    logger.info("Process completed successfully", survey_id=meta_data.survey_id)
