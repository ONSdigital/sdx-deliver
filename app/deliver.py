import hashlib
import zipfile
from typing import io

from sdx_gcp.app import get_logger
from app.encrypt import encrypt_output
from app.meta_wrapper import MetaWrapper
from app.output_type import OutputType
from app.publish import send_message, publish_v2_schema
from app.store import write_to_bucket
from app.v2.definitions.config_schema import ConfigSchema
from app.v2.definitions.message_schema import SchemaDataV2
from app.v2.mappings import FileExtensionMapper, SubmissionTypeMapper
from app.v2.message_config import MessageConfig
from app.v2.message_constructor import MessageConstructor

logger = get_logger()


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
        message_config = MessageConfig(meta_data.survey_id).get_config()
        message_constructor = MessageConstructor(config_schema= message_config,
                                                 file_name_mapper=FileExtensionMapper(),
                                                 submission_mapper=SubmissionTypeMapper())

        # Create a BytesIO object from the bytes
        zip_file = io.BytesIO(data_bytes)

        # Open the zip file
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # List the filenames of the zip file
            filenames = zip_ref.namelist()

        v2_message: SchemaDataV2 = message_constructor.build_message(filenames, meta_data)
        publish_v2_schema(v2_message, meta_data.tx_id)

    else:
        send_message(meta_data, path)

    logger.info("Process completed successfully", survey_id=meta_data.survey_id)
