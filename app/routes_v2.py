import json
from enum import StrEnum
from typing import Final, TypedDict

from sdx_gcp import Flask, Request, TX_ID
from sdx_gcp.app import get_logger

from app.deliver import deliver


logger = get_logger()

FILE_NAME: Final[str] = "filename"
CONTEXT: Final[str] = 'context'
ZIP_FILE: Final[str] = 'zip_file'


class SurveyType(StrEnum):
    DAP = "dap"
    LEGACY = "legacy"
    SPP = "spp"
    NS5 = "ns5"
    FEEDBACK = "feedback"


class BusinessSurveyContext(TypedDict):
    survey_type: SurveyType
    survey_id: str
    period_id: str
    ru_ref: str


def deliver_submission(req: Request, _tx_id: TX_ID):
    """
    Endpoint for submissions that will use the version 2 schema for the nifi message.
    """
    logger.info('Processing submission')
    filename: str = req.args.get(FILE_NAME)
    context: BusinessSurveyContext = json.loads(req.args.get(CONTEXT))
    files = req.files
    data_bytes = files[ZIP_FILE].read()
    deliver(meta, data_bytes, use_v2_message_schema(req.args))
    return Flask.jsonify(success=True)
