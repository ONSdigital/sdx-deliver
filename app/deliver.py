import logging

from structlog import wrap_logger

from app.encrypt import encrypt_output
from app.output_type import OutputType
from app.publish import notify_dap
from app.store import write_to_bucket


logger = wrap_logger(logging.getLogger(__name__))


def deliver(filename: str, data_bytes: bytes, survey_dict: dict, output_type: OutputType):

    logger.info("encrypting")
    encrypted_output = encrypt_output(data_bytes, output_type)

    logger.info("storing")
    path = write_to_bucket(data_bytes, filename=filename, output_type=output_type)

    logger.info("sending dap notification")
    notify_dap(data=encrypted_payload,
               filename=filename,
               tx_id=tx_id,
               dataset=dataset,
               description=description,
               iteration=iteration)
