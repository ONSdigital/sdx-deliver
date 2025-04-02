from datetime import datetime

from sdx_gcp.app import get_logger

from app import CONFIG
from app.definitions import MessageSchema
from app.meta_wrapper import MetaWrapper
from app.output_type import OutputType

logger = get_logger()


def create_message(meta_data: MetaWrapper) -> MessageSchema:
    """
    Generates PubSub message using MetaWrapper
    """
    source_name = CONFIG.PROJECT_ID
    sensitivity = CONFIG.DATA_SENSITIVITY

    iteration2 = None

    if meta_data.output_type == OutputType.COMMENTS:
        dataset = "sdx_comments"
        iteration1 = None
    elif meta_data.output_type == OutputType.DAP and (meta_data.survey_id == "739" or meta_data.survey_id == "738" or meta_data.survey_id == "740"):
        dataset = "covid_resp_inf_surv_response"
        source_name = "ons"
        iteration1 = "prod" if CONFIG.PROJECT_ID == "ons-sdx-prod" else "test"
        if iteration1 != "prod":
            sensitivity = "Medium"
        if meta_data.survey_id == "740":
            iteration2 = "phm_740_health_insights_2024"
    else:
        dataset = meta_data.survey_id
        iteration1 = meta_data.period if meta_data.period else None

    message = {
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
        message['iterationL1'] = iteration1

    if iteration2 is not None:
        message['iterationL2'] = iteration2

    logger.info("Created pubsub message")
    return message


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
