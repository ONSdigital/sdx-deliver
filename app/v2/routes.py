import json
from typing import Final

from sdx_gcp import Flask, Request, TX_ID
from sdx_gcp.app import get_logger

from app.v2.definitions.context import BusinessSurveyContext, AdhocSurveyContext, CommentsFileContext
from app.v2.deliver import deliver_v2

logger = get_logger()

FILE_NAME: Final[str] = "filename"
CONTEXT: Final[str] = 'context'
ZIP_FILE: Final[str] = 'zip_file'


def deliver_business_survey(req: Request, _tx_id: TX_ID):
    """
    Endpoint for submissions that will use the version 2 schema for the nifi message.
    """
    logger.info('Processing business submission')
    filename: str = req.args.get(FILE_NAME)
    if filename is None:
        logger.error("missing filename")
    context: BusinessSurveyContext = json.loads(req.args.get(CONTEXT))
    context["tx_id"] = _tx_id
    expected_keys = BusinessSurveyContext.__annotations__.keys()
    print(expected_keys)
    for key in expected_keys:
        if key not in context:
            logger.error(f"missing key: {key}")
    files = req.files
    zip_file = files[ZIP_FILE]
    if zip_file is None:
        logger.error("missing zip file")
    data_bytes = zip_file.read()
    deliver_v2(filename, data_bytes, context)
    return Flask.jsonify(success=True)


def deliver_adhoc_survey(req: Request, _tx_id: TX_ID):
    """
    Endpoint for submissions that will use the version 2 schema for the nifi message.
    """
    logger.info('Processing adhoc submission')
    filename: str = req.args.get(FILE_NAME)
    context: AdhocSurveyContext = json.loads(req.args.get(CONTEXT))
    context["tx_id"] = _tx_id
    files = req.files
    data_bytes = files[ZIP_FILE].read()
    deliver_v2(filename, data_bytes, context)
    return Flask.jsonify(success=True)


def deliver_comments(req: Request, _tx_id: TX_ID):
    """
    Endpoint for submissions that will use the version 2 schema for the nifi message.
    """
    logger.info('Processing comments')
    filename: str = req.args.get(FILE_NAME)
    context: CommentsFileContext = json.loads(req.args.get(CONTEXT))
    context["tx_id"] = _tx_id
    files = req.files
    data_bytes = files[ZIP_FILE].read()
    deliver_v2(filename, data_bytes, context)
    return Flask.jsonify(success=True)
