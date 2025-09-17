from typing import Final, Annotated

from fastapi import APIRouter, Form, UploadFile, File
from sdx_base.errors.errors import UnrecoverableError
from starlette.responses import JSONResponse

from app import get_logger
from app.definitions.context import AdhocSurveyContext, BusinessSurveyContext, CommentsFileContext

logger = get_logger()

FILE_NAME: Final[str] = "filename"
CONTEXT: Final[str] = 'context'
ZIP_FILE: Final[str] = 'zip_file'
SEFT_FILE: Final[str] = 'seft_file'

router = APIRouter()


@router.post("/deliver/v2/survey")
async def deliver_survey(filename: Annotated[str, Form()],
                         context: Annotated[BusinessSurveyContext | AdhocSurveyContext, Form()],
                         zip_file: UploadFile = File(...)):
    """
    Endpoint for business submissions that will use the version 2 schema for the nifi message.
    """
    logger.info('Processing business submission')
    if filename is None:
        logger.error("missing filename")

    if zip_file is None:
        logger.error("missing zip file")
        raise UnrecoverableError("Missing zip file")
    data_bytes = await zip_file.read()
    deliver_v2(filename, data_bytes, context)
    return JSONResponse(content={"success": True}, status_code=200)


async def deliver_comments_file(filename: Annotated[str, Form()],
                                context: Annotated[CommentsFileContext, Form()],
                                zip_file: UploadFile = File(...)):
    """
    Endpoint for the comments file using the version 2 schema for the nifi message.
    """
    logger.info('Processing comments')
    if zip_file is None:
        logger.error("missing zip file")
        raise UnrecoverableError("Missing zip file")
    data_bytes = await zip_file.read()
    deliver_v2(filename, data_bytes, context)
    return JSONResponse(content={"success": True}, status_code=200)


async def deliver_seft_submission(filename: Annotated[str, Form()],
                                  context: Annotated[BusinessSurveyContext, Form()],
                                  seft_file: UploadFile = File(...)):
    """
    Endpoint for seft submissions that will use the version 2 schema for the nifi message.
    """
    logger.info('Processing seft')

    if seft_file is None:
        logger.error("missing SEFT file")
        raise UnrecoverableError("Missing SEFT file")
    data_bytes = await seft_file.read()
    deliver_v2(filename, data_bytes, context)
    return JSONResponse(content={"success": True}, status_code=200)
