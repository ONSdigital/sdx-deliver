import hashlib
import io
import zipfile

from sdx_gcp.app import get_logger

from app import sdx_app, CONFIG
from app.meta_wrapper import MetaWrapper
from app.output_type import OutputType
from app.publish import get_message
from app.store import write_to_bucket

logger = get_logger()


def deliver(meta_data: MetaWrapper, data_bytes: bytes):
    """
    Encrypts any unencrypted data, writes to the appropriate location within the outputs GCP bucket and notifies DAP
    via PubSub
    """
    try:
        if meta_data.output_type != OutputType.SEFT:
            meta_data.md5sum = hashlib.md5(data_bytes).hexdigest()
            meta_data.sizeBytes = len(data_bytes)

        if meta_data.output_type == OutputType.LEGACY or meta_data.output_type == OutputType.HYBRID:
            zf = zipfile.ZipFile(io.BytesIO(data_bytes), "r")
            logger.info("Storing to bucket")
            path = ""
            for fileinfo in zf.infolist():
                try:
                    data: str = zf.read(fileinfo).decode()
                    path = write_to_bucket(data,
                                           filename=fileinfo.filename,
                                           output_type=meta_data.output_type,
                                           sub_dir=meta_data.filename)
                except Exception:
                    logger.info(f"Unable to decode: {fileinfo.filename}")

        else:
            path = write_to_bucket(data_bytes.decode(),
                                   filename=meta_data.filename,
                                   output_type=meta_data.output_type,
                                   sub_dir="")

        logger.info("Storing DAP notification")
        message: str = get_message(meta_data, path)
        sdx_app.gcs_write(message, f'{meta_data.filename}-message.txt', CONFIG.BUCKET_NAME, "messages")

        logger.info("Process completed successfully", survey_id=meta_data.survey_id)
    except Exception as e:
        logger.error(str(e))
