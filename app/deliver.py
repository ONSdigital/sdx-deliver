import hashlib
from typing import cast

from app import sdx_app, CONFIG
from app.encrypt import encrypt_output
from app.publish import publish_v2_message
from app.definitions import Context, AdhocSurveyContext, BusinessSurveyContext
from app.definitions import LocationKeyLookupBase
from app.definitions import MessageSchemaV2
from app.definitions import SurveyType
from app.definitions import ZipDetails
from app.location_key_lookup import LocationKeyLookup
from app.submission_type_mapper import SubmissionTypeMapper
from app.location_name_repo import LocationNameRepo
from app.message_builder import MessageBuilder
from app.definitions import LocationNameRepositoryBase
from app.zip import unzip

logger = get_logger()
location_name_repo: LocationNameRepositoryBase = LocationNameRepo()


def deliver_v2(filename: str, data_bytes: bytes, context: Context):
    """
    Encrypts any unencrypted data, writes to the appropriate location within the outputs GCP bucket and notifies DAP
    via PubSub
    """
    encrypted_bytes: bytes
    if context["survey_type"] == SurveyType.SEFT:
        encrypted_bytes = data_bytes
    else:
        logger.info("Encrypting output")
        encrypted_output: str = encrypt_output(data_bytes)
        encrypted_bytes = encrypted_output.encode()

    md5sum: str = hashlib.md5(encrypted_bytes).hexdigest()
    size_bytes: int = len(encrypted_bytes)

    location_name_repo.load_location_values()
    location_key_lookup: LocationKeyLookupBase = LocationKeyLookup(location_name_repo)
    message_constructor = MessageBuilder(submission_mapper=SubmissionTypeMapper(location_key_lookup))

    filenames: list[str]
    if context["survey_type"] == SurveyType.COMMENTS or context["survey_type"] == SurveyType.SEFT:
        filenames = [filename]
    else:
        filenames = unzip(data_bytes)

    zip_details: ZipDetails = {
        "filename": filename,
        "size_bytes": size_bytes,
        "md5sum": md5sum,
        "filenames": filenames,
    }
    v2_message: MessageSchemaV2 = message_constructor.build_message(zip_details, context)

    logger.info("Storing to bucket")
    sdx_app.gcs_write(encrypted_bytes, filename, CONFIG.BUCKET_NAME, get_output_path(v2_message))

    logger.info("Sending Nifi message")
    publish_v2_message(v2_message, context["tx_id"])

    logger.info("Process completed successfully", survey_id=get_survey_id(context))


def get_survey_id(context: Context) -> str:
    if context["survey_type"] == SurveyType.COMMENTS:
        return "Comments"
    elif context["survey_type"] == SurveyType.ADHOC:
        adhoc_context: AdhocSurveyContext = cast(AdhocSurveyContext, context)
        return adhoc_context["survey_id"]
    else:
        business_context: BusinessSurveyContext = cast(BusinessSurveyContext, context)
        return business_context["survey_id"]


def get_output_path(v2_message: MessageSchemaV2) -> str:
    return v2_message["source"]["path"]
