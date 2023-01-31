import json
import threading
from typing import Dict

import structlog

from flask import request, jsonify, Response
from structlog.contextvars import bind_contextvars, unbind_contextvars

from app import app
from app.deliver import deliver
from app.meta_wrapper import MetaWrapper, MetaWrapperV2, MetaWrapperAdhoc

logger = structlog.get_logger()

ZIP_FILE = 'zip'
SUBMISSION_FILE = 'submission'
TRANSFORMED_FILE = 'transformed'
METADATA_FILE = 'metadata'
SEFT_FILE = 'seft'
FILE_NAME = "filename"
VERSION = "version"
V1 = "v1"
V2 = "v2"
ADHOC = "adhoc"


def get_wrapper(req_args: Dict[str, str]) -> MetaWrapper:
    filename = req_args.get(FILE_NAME)
    version = req_args.get(VERSION, V1)

    if version == V2:
        return MetaWrapperV2(filename)
    elif version == ADHOC:
        return MetaWrapperAdhoc(filename)
    else:
        return MetaWrapper(filename)


@app.post('/deliver/dap')
def deliver_dap():
    """
    Endpoint for submissions only intended for DAP. POST request requires the submission JSON to be uploaded
    as "submission" and the filename passed in the query parameters.
    """
    logger.info('Processing DAP submission')
    meta = get_wrapper(request.args)
    files = request.files
    submission_bytes = files[SUBMISSION_FILE].read()
    survey_dict = json.loads(submission_bytes.decode())
    data_bytes = submission_bytes
    meta.set_dap(survey_dict)
    return process(meta, data_bytes)


@app.post('/deliver/legacy')
def deliver_legacy():
    """
    Endpoint for submissions intended for legacy systems. POST request requires the submission JSON to be uploaded as
    "submission", the zipped transformed artifact as "transformed", and the filename passed in the query
    parameters.
    """
    logger.info('Processing Legacy submission')
    meta = get_wrapper(request.args)
    files = request.files
    submission_bytes = files[SUBMISSION_FILE].read()
    survey_dict = json.loads(submission_bytes.decode())
    data_bytes = files[TRANSFORMED_FILE].read()
    meta.set_legacy(survey_dict)
    return process(meta, data_bytes)


@app.post('/deliver/hybrid')
def deliver_hybrid():
    """
    Endpoint for submissions intended for dap and legacy systems. POST request requires the submission JSON to be
    uploaded as "submission", the zipped transformed artifact as "transformed", and the filename passed in the
    query parameters.
    """
    logger.info('Processing Hybrid submission')
    meta = get_wrapper(request.args)
    files = request.files
    submission_bytes = files[SUBMISSION_FILE].read()
    survey_dict = json.loads(submission_bytes.decode())
    data_bytes = files[TRANSFORMED_FILE].read()
    meta.set_hybrid(survey_dict)
    return process(meta, data_bytes)


@app.post('/deliver/feedback')
def deliver_feedback():
    """
    Endpoint for feedback submissions only. POST request requires the feedback JSON to be uploaded as
    "submission", and the filename passed in the query parameters.
    """
    logger.info('Processing Feedback submission')
    meta = get_wrapper(request.args)
    files = request.files
    submission_bytes = files[SUBMISSION_FILE].read()
    survey_dict = json.loads(submission_bytes.decode())
    data_bytes = submission_bytes
    meta.set_feedback(survey_dict)
    return process(meta, data_bytes)


@app.post('/deliver/comments')
def deliver_comments():
    """
    Endpoint for delivering daily comment report. POST request requires the zipped up comments to be uploaded as
    "zip", and the filename passed in the query parameters.
    """
    logger.info('Processing Comments submission')
    meta = get_wrapper(request.args)
    files = request.files
    data_bytes = files[ZIP_FILE].read()
    meta.set_comments()
    return process(meta, data_bytes)


@app.post('/deliver/seft')
def deliver_seft():
    """
    Endpoint for delivering SEFT submissions. POST request requires the encrypted SEFT to be uploaded as
    "seft", metadata JSON as "metadata", and the filename passed in the query parameters.
    Metadata file is required to provide information about the submissions to construct the PubSub message.
    """
    logger.info('Processing SEFT submission')
    meta = get_wrapper(request.args)
    files = request.files
    meta_bytes = files[METADATA_FILE].read()
    meta_dict = json.loads(meta_bytes.decode())
    data_bytes = files[SEFT_FILE].read()
    meta.set_seft(meta_dict)
    return process(meta, data_bytes)


@app.get('/healthcheck')
def healthcheck():
    return jsonify({'status': 'OK'})


@app.errorhandler(500)
def server_error(error=None):
    logger.error("Server error", error=repr(error))
    message = {
        'status': 500,
        'message': "Internal server error: " + repr(error),
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp


def process(meta_data: MetaWrapper, data_bytes: bytes) -> Response:
    """
    Binds submission data to logger and begins deliver process
    """
    try:
        bind_contextvars(
            tx_id=meta_data.tx_id,
            survey_id=meta_data.survey_id,
            output_type=meta_data.output_type,
            thread=threading.currentThread().getName()
        )
        logger.info("Processing request")
        deliver(meta_data, data_bytes)
        """
        WE USE THE BELOW LOG MESSAGE "logger.info("Process completed successfully")" 
        TO CREATE "LOG-BASED" CUSTOM METRICS.
        DO NOT CHANGE THIS STATEMENT.
        """
        logger.info("Process completed successfully")
        return jsonify(success=True)

    except Exception as e:
        return server_error(e)

    finally:
        unbind_contextvars(
            'tx_id',
            'survey_id',
            'output_type',
            'thread'
        )
