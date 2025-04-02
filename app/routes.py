import json

from sdx_gcp import Flask, Request, TX_ID
from sdx_gcp.app import get_logger

from app.deliver import deliver
from app.meta_wrapper import MetaWrapper, MetaWrapperV2, MetaWrapperAdhoc

logger = get_logger()

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


def get_wrapper(req_args: dict[str, str]) -> MetaWrapper:
    filename = req_args.get(FILE_NAME)
    version = req_args.get(VERSION, V1)

    if version == V2:
        return MetaWrapperV2(filename)
    elif version == ADHOC:
        return MetaWrapperAdhoc(filename)
    else:
        return MetaWrapper(filename)


def deliver_dap(req: Request, _tx_id: TX_ID):
    """
    Endpoint for submissions only intended for DAP. POST request requires the submission JSON to be uploaded
    as "submission" and the filename passed in the query parameters.
    """
    logger.info('Processing DAP submission')
    meta = get_wrapper(req.args)
    files = req.files
    submission_bytes = files[SUBMISSION_FILE].read()
    survey_dict = json.loads(submission_bytes.decode())
    data_bytes = submission_bytes
    meta.set_dap(survey_dict)
    deliver(meta, data_bytes)
    return Flask.jsonify(success=True)


def deliver_legacy(req: Request, _tx_id: TX_ID):
    """
    Endpoint for submissions intended for legacy systems. POST request requires the submission JSON to be uploaded as
    "submission", the zipped transformed artifact as "transformed", and the filename passed in the query
    parameters.
    """
    logger.info('Processing Legacy submission')
    meta = get_wrapper(req.args)
    files = req.files
    submission_bytes = files[SUBMISSION_FILE].read()
    survey_dict = json.loads(submission_bytes.decode())
    data_bytes = files[TRANSFORMED_FILE].read()
    meta.set_legacy(survey_dict)
    deliver(meta, data_bytes)
    return Flask.jsonify(success=True)


def deliver_hybrid(req: Request, _tx_id: TX_ID):
    """
    Endpoint for submissions intended for dap and legacy systems. POST request requires the submission JSON to be
    uploaded as "submission", the zipped transformed artifact as "transformed", and the filename passed in the
    query parameters.
    """
    logger.info('Processing Hybrid submission')
    meta = get_wrapper(req.args)
    files = req.files
    submission_bytes = files[SUBMISSION_FILE].read()
    survey_dict = json.loads(submission_bytes.decode())
    data_bytes = files[TRANSFORMED_FILE].read()
    meta.set_hybrid(survey_dict)
    deliver(meta, data_bytes)
    return Flask.jsonify(success=True)


def deliver_feedback(req: Request, _tx_id: TX_ID):
    """
    Endpoint for feedback submissions only. POST request requires the feedback JSON to be uploaded as
    "submission", and the filename passed in the query parameters.
    """
    logger.info('Processing Feedback submission')
    meta = get_wrapper(req.args)
    files = req.files
    submission_bytes = files[SUBMISSION_FILE].read()
    survey_dict = json.loads(submission_bytes.decode())
    data_bytes = submission_bytes
    meta.set_feedback(survey_dict)
    deliver(meta, data_bytes)
    return Flask.jsonify(success=True)


def deliver_comments(req: Request, _tx_id: TX_ID):
    """
    Endpoint for delivering daily comment report. POST request requires the zipped up comments to be uploaded as
    "zip", and the filename passed in the query parameters.
    """
    logger.info('Processing Comments submission')
    meta = get_wrapper(req.args)
    files = req.files
    data_bytes = files[ZIP_FILE].read()
    meta.set_comments()
    deliver(meta, data_bytes)
    return Flask.jsonify(success=True)


def deliver_seft(req: Request, _tx_id: TX_ID):
    """
    Endpoint for delivering SEFT submissions. POST request requires the encrypted SEFT to be uploaded as
    "seft", metadata JSON as "metadata", and the filename passed in the query parameters.
    Metadata file is required to provide information about the submissions to construct the PubSub message.
    """
    logger.info('Processing SEFT submission')
    meta = get_wrapper(req.args)
    files = req.files
    meta_bytes = files[METADATA_FILE].read()
    meta_dict = json.loads(meta_bytes.decode())
    data_bytes = files[SEFT_FILE].read()
    meta.set_seft(meta_dict)
    deliver(meta, data_bytes)
    return Flask.jsonify(success=True)
