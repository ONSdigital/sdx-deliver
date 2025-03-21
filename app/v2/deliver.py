import hashlib
from typing import cast

from sdx_gcp.app import get_logger

from app import sdx_app, CONFIG
from app.encrypt import encrypt_output
from app.publish import publish_v2_message
from app.v2.definitions.context import Context, AdhocSurveyContext, BusinessSurveyContext
from app.v2.definitions.location_key_lookup import LocationKeyLookupBase
from app.v2.definitions.message_schema import MessageSchemaV2
from app.v2.definitions.survey_type import SurveyType
from app.v2.definitions.zip_details import ZipDetails
from app.v2.location_key_lookup import LocationKeyLookup
from app.v2.submission_type_mapper import SubmissionTypeMapper
from app.v2.location_name_repo import LocationNameRepo
from app.v2.message_builder import MessageBuilder
from app.v2.definitions.location_name_repository import LocationNameRepositoryBase
from app.v2.zip import unzip

logger = get_logger()
location_name_repo: LocationNameRepositoryBase = LocationNameRepo()


def deliver_v2(filename: str, data_bytes: bytes, context: Context):
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
    sdx_app.gcs_write(encrypted_output, filename, CONFIG.BUCKET_NAME, get_output_path(context))

    logger.info("Sending Nifi message")
    location_name_repo.load_location_values()
    location_key_lookup: LocationKeyLookupBase = LocationKeyLookup(location_name_repo)
    message_constructor = MessageBuilder(submission_mapper=SubmissionTypeMapper(location_key_lookup))

    filenames: list[str]
    if context["survey_type"] == SurveyType.COMMENTS:
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


def get_output_path(context: Context) -> str:
    if context["survey_type"] == SurveyType.COMMENTS:
        return "comments"
    elif context["survey_type"] == SurveyType.SEFT:
        return "seft"
    else:
        return "survey"
