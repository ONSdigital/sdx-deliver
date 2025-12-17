from typing import cast

from app import get_logger
from app.definitions.context import Context, AdhocSurveyContext, BusinessSurveyContext
from app.definitions.encryption import EncryptionBase
from app.definitions.gcp import GcpBase
from app.definitions.message_builder import MessageBuilderBase
from app.definitions.message_schema import MessageSchemaV2
from app.definitions.survey_type import SurveyType
from app.definitions.zip import ZipBase
from app.definitions.zip_details import ZipDetails

logger = get_logger()


class Deliver:

    def __init__(self,
                 message_builder: MessageBuilderBase,
                 encrypter: EncryptionBase,
                 gcp: GcpBase,
                 zipper: ZipBase):
        self._message_builder = message_builder
        self._encrypter = encrypter
        self._gcp = gcp
        self._zipper = zipper

    def deliver_v2(self, filename: str, data_bytes: bytes, context: Context):
        """
        Encrypts any unencrypted data, writes to the appropriate location within the outputs GCP bucket and notifies DAP
        via PubSub
        """
        encrypted_bytes: bytes
        if context.survey_type == SurveyType.SEFT:
            encrypted_bytes = data_bytes
        else:
            logger.info("Encrypting output")
            encrypted_output: str = self._encrypter.encrypt(data_bytes)
            encrypted_bytes = encrypted_output.encode()

        md5sum: str
        size_bytes: int
        md5sum, size_bytes = self._encrypter.get_md5_and_size(encrypted_bytes)

        filenames: list[str]
        if context.survey_type == SurveyType.COMMENTS or context.survey_type == SurveyType.SEFT:
            filenames = [filename]
        else:
            filenames = self._zipper.unzip(data_bytes)

        zip_details: ZipDetails = {
            "filename": filename,
            "size_bytes": size_bytes,
            "md5sum": md5sum,
            "filenames": filenames,
        }
        v2_message: MessageSchemaV2 = self._message_builder.build_message(zip_details, context)

        logger.info("Storing to bucket")
        self._gcp.store(encrypted_bytes, filename, _get_output_path(v2_message))

        logger.info("Sending Nifi message")
        self._gcp.publish_v2_message(v2_message, context.tx_id)

        logger.info("Process completed successfully", {"survey_id": _get_survey_id(context)})


def _get_survey_id(context: Context) -> str:
    if context.survey_type == SurveyType.COMMENTS:
        return "Comments"
    elif context.survey_type == SurveyType.ADHOC:
        adhoc_context: AdhocSurveyContext = cast(AdhocSurveyContext, context)
        return adhoc_context.survey_id
    else:
        business_context: BusinessSurveyContext = cast(BusinessSurveyContext, context)
        return business_context.survey_id


def _get_output_path(v2_message: MessageSchemaV2) -> str:
    return v2_message["source"]["path"]
