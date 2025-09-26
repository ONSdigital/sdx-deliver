from typing import Final

from fastapi import APIRouter, UploadFile, Depends
from sdx_base.errors.errors import UnrecoverableError
from starlette.responses import JSONResponse

from app import get_logger
from app.definitions.context import BusinessSurveyContext, CommentsFileContext
from app.deliver import Deliver
from app.dependencies import get_deliver_service

logger = get_logger()

FILE_NAME: Final[str] = "filename"
CONTEXT: Final[str] = 'context'
ZIP_FILE: Final[str] = 'zip_file'
SEFT_FILE: Final[str] = 'seft_file'

router = APIRouter()


@router.post("/deliver/v2/survey")
async def deliver_survey(filename: str,
                         context: str,
                         zip_file: UploadFile,
                         deliver: Deliver = Depends(get_deliver_service)):
    """
    Endpoint for business submissions that will use the version 2 schema for the nifi message.
    """
    logger.info('Processing business submission')
    if filename is None:
        logger.error("missing filename")
        raise UnrecoverableError("Missing filename")

    if zip_file is None:
        logger.error("missing zip file")
        raise UnrecoverableError("Missing zip file")
    data_bytes = await zip_file.read()
    context_obj = BusinessSurveyContext.model_validate_json(context)
    deliver.deliver_v2(filename, data_bytes, context_obj)
    return JSONResponse(content={"success": True}, status_code=200)


@router.post("/deliver/v2/comments")
async def deliver_comments_file(filename: str,
                                context: str,
                                zip_file: UploadFile,
                                deliver: Deliver = Depends(get_deliver_service)):
    """
    Endpoint for the comments file using the version 2 schema for the nifi message.
    """
    logger.info('Processing comments')
    if zip_file is None:
        logger.error("missing zip file")
        raise UnrecoverableError("Missing zip file")
    data_bytes = await zip_file.read()
    context_obj = CommentsFileContext.model_validate_json(context)
    deliver.deliver_v2(filename, data_bytes, context_obj)
    return JSONResponse(content={"success": True}, status_code=200)


@router.post("/deliver/v2/seft")
async def deliver_seft_submission(filename: str,
                                  context: str,
                                  seft_file: UploadFile,
                                  deliver: Deliver = Depends(get_deliver_service)):
    """
    Endpoint for seft submissions that will use the version 2 schema for the nifi message.
    """
    logger.info('Processing seft')
    context_obj = BusinessSurveyContext.model_validate_json(context)

    if seft_file is None:
        logger.error("missing SEFT file")
        raise UnrecoverableError("Missing SEFT file")
    data_bytes = await seft_file.read()
    deliver.deliver_v2(filename, data_bytes, context_obj)
    return JSONResponse(content={"success": True}, status_code=200)
