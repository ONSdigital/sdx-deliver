import json
from typing import Final

from sdx_gcp import Flask, Request, TX_ID
from sdx_gcp.app import get_logger
from sdx_gcp.errors import UnrecoverableError

from app.v2.definitions.context import BusinessSurveyContext, AdhocSurveyContext, CommentsFileContext, Context
from app.v2.definitions.survey_type import SurveyType
from app.v2.deliver import deliver_v2

logger = get_logger()

FILE_NAME: Final[str] = "filename"
CONTEXT: Final[str] = 'context'
ZIP_FILE: Final[str] = 'zip_file'
SEFT_FILE: Final[str] = 'seft_file'


def _check_context_args(context: Context, context_type: Context.__class__):
    expected_keys = context_type.__annotations__.keys()
    for key in expected_keys:
        if key not in context:
            logger.error(f"missing key: {key}")


def deliver_survey(req: Request, _tx_id: TX_ID):
    """
    Endpoint for business submissions that will use the version 2 schema for the nifi message.
    """
    logger.info('Processing business submission')
    filename: str = req.args.get(FILE_NAME)
    if filename is None:
        logger.error("missing filename")

    context: Context = json.loads(req.args.get(CONTEXT))
    if context["survey_type"] == SurveyType.ADHOC:
        context: AdhocSurveyContext = json.loads(req.args.get(CONTEXT))
        _check_context_args(context, AdhocSurveyContext)
    else:
        context: BusinessSurveyContext = json.loads(req.args.get(CONTEXT))
        _check_context_args(context, BusinessSurveyContext)

    files = req.files
    zip_file = files.get(ZIP_FILE)
    if zip_file is None:
        logger.error("missing zip file")
        raise UnrecoverableError("Missing zip file")
    data_bytes = zip_file.read()
    deliver_v2(filename, data_bytes, context)
    return Flask.jsonify(success=True)


def deliver_comments_file(req: Request, _tx_id: TX_ID):
    """
    Endpoint for the comments file using the version 2 schema for the nifi message.
    """
    logger.info('Processing comments')
    filename: str = req.args.get(FILE_NAME)
    context: CommentsFileContext = json.loads(req.args.get(CONTEXT))
    _check_context_args(context, CommentsFileContext)
    files = req.files
    zip_file = files.get(ZIP_FILE)
    if zip_file is None:
        logger.error("missing zip file")
        raise UnrecoverableError("Missing zip file")
    data_bytes = zip_file.read()
    deliver_v2(filename, data_bytes, context)
    return Flask.jsonify(success=True)


def deliver_seft_submission(req: Request, _tx_id: TX_ID):
    """
    Endpoint for seft submissions that will use the version 2 schema for the nifi message.
    """
    logger.info('Processing seft')
    filename: str = req.args.get(FILE_NAME)
    context: BusinessSurveyContext = json.loads(req.args.get(CONTEXT))
    _check_context_args(context, BusinessSurveyContext)
    files = req.files
    seft_file = files.get(SEFT_FILE)
    if seft_file is None:
        logger.error("missing SEFT file")
        raise UnrecoverableError("Missing SEFT file")
    data_bytes = seft_file.read()
    deliver_v2(filename, data_bytes, context)
    return Flask.jsonify(success=True)
