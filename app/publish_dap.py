from app import dap_publisher, dap_topic_path
import hashlib
import json
from datetime import datetime


def notify_dap(data: bytes, filename: str, dataset: str, description: str, iteration: str):
    message_str = create_dap_message(data,
                                     filename=filename,
                                     dataset=dataset,
                                     description=description,
                                     iteration=iteration)
    publish_data(message_str, filename)


def publish_data(message_str: str, filename: str):
    # Data must be a byte-string
    message = message_str.encode("utf-8")
    # When you publish a message, the client returns a future.
    future = dap_publisher.publish(dap_topic_path, message, filename=filename)
    return future.result()


def get_description(survey_dict: dict) -> str:
    return "{} survey response for period {} sample unit {}".format(
        survey_dict['survey_id'],
        survey_dict['collection']['period'],
        survey_dict['metadata']['ru_ref']
    )


def get_iteration(survey_dict: dict) -> str:
    return survey_dict['collection']['period']


def create_dap_message(survey_bytes: bytes,
                       filename: str,
                       dataset: str,
                       description: str,
                       iteration: str) -> str:

    md5_hash = hashlib.md5(survey_bytes).hexdigest()

    dap_message = {
        'version': '1',
        'files': [{
            'name': filename,
            'URL': f"http://sdx-store:5000/responses/{filename}",
            'sizeBytes': len(survey_bytes),
            'md5sum': md5_hash
        }],
        'sensitivity': 'High',
        'sourceName': 'sdx-development',
        'manifestCreated': get_formatted_current_utc(),
        'description': description,
        'iterationL1': iteration,
        'dataset': dataset,
        'schemaversion': '1'
    }

    print("Created dap data")
    str_dap_message = json.dumps(dap_message)
    return str_dap_message


def get_formatted_current_utc():
    """
    Returns a formatted utc date with only 3 milliseconds as opposed to the ususal 6 that python provides.
    Additionally, we provide the Zulu time indicator (Z) at the end to indicate it being UTC time. This is
    done for consistency with timestamps provided in other languages.
    The format the time is returned is YYYY-mm-ddTHH:MM:SS.fffZ (e.g., 2018-10-10T08:42:24.737Z)
    """
    date_time = datetime.utcnow()
    milliseconds = date_time.strftime("%f")[:3]
    return f"{date_time.strftime('%Y-%m-%dT%H:%M:%S')}.{milliseconds}Z"
