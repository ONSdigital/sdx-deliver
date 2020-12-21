import logging

from structlog import wrap_logger

from app.encrypt import encrypt_data
from app.publish import notify_dap
from app.store import write_to_bucket


logger = wrap_logger(logging.getLogger(__name__))


def deliver(file_bytes: bytes,
            filename: str,
            dataset: str,
            description: str,
            iteration: str,
            directory: str):

    logger.info("encrypting")
    encrypted_payload = encrypt_data(file_bytes)

    logger.info("storing")
    write_to_bucket(encrypted_payload, filename=filename, directory=directory)

    logger.info("sending dap notification")
    notify_dap(data=encrypted_payload,
               filename=filename,
               dataset=dataset,
               description=description,
               iteration=iteration)
