from sdx_gcp.app import get_logger

from app import CONFIG
import json
from datetime import datetime
from app.meta_wrapper import MetaWrapper
from app.output_type import OutputType

logger = get_logger()


def get_message(meta_data: MetaWrapper, path: str) -> str:
    """
    Get the Pubsub message, based on the Metawrapper data
    """
    message_str = create_message_data(meta_data)
    return publish_data(message_str, meta_data.tx_id, path)


def create_message_data(meta_data: MetaWrapper) -> str:
    """
    Generates PubSub message using MetaWrapper
    """
    source_name = CONFIG.PROJECT_ID
    sensitivity = CONFIG.DATA_SENSITIVITY

    if meta_data.output_type == OutputType.COMMENTS:
        dataset = "sdx_comments"
        iteration1 = None
    elif meta_data.survey_id == "739":
        dataset = "covid_resp_inf_surv_response"
        source_name = "ons"
        iteration1 = "prod" if CONFIG.PROJECT_ID == "ons-sdx-prod" else "test"
        if iteration1 != "prod":
            sensitivity = "Medium"
    else:
        dataset = meta_data.survey_id
        iteration1 = meta_data.period if meta_data.period else None

    message_data = {
        'version': '1',
        'files': [{
            'name': meta_data.filename,
            'sizeBytes': meta_data.sizeBytes,
            'md5sum': meta_data.md5sum
        }],
        'sensitivity': sensitivity,
        'sourceName': source_name,
        'manifestCreated': get_formatted_current_utc(),
        'description': meta_data.get_description(),
        'dataset': dataset,
        'schemaversion': '1'
    }

    if iteration1 is not None:
        message_data['iterationL1'] = iteration1

    logger.info("Created pubsub message")
    str_dap_message = json.dumps(message_data)
    return str_dap_message


def get_formatted_current_utc():
    """
    Returns a formatted utc date with only 3 milliseconds as opposed to the usual 6 that python provides.
    Additionally, we provide the Zulu time indicator (Z) at the end to indicate it being UTC time. This is
    done for consistency with timestamps provided in other languages.
    The format the time is returned is YYYY-mm-ddTHH:MM:SS.fffZ (e.g., 2018-10-10T08:42:24.737Z)
    """
    date_time = datetime.utcnow()
    milliseconds = date_time.strftime("%f")[:3]
    return f"{date_time.strftime('%Y-%m-%dT%H:%M:%S')}.{milliseconds}Z"


def publish_data(message_str: str, tx_id: str, path: str) -> str:
    """
    Publishes message to DAP
    """
    # NIFI can't handle forward slash
    key = path.replace("/", "|")
    attributes = {
        'gcs.bucket': CONFIG.BUCKET_NAME,
        'gcs.key': key,
        'tx_id': tx_id
    }

    return json.dumps({"data": message_str, "attributes": attributes})
