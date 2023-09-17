from http.client import responses
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from loguru import logger
from src.schemas.exception_schema import ErrorResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_type = "ValidationError"
    error_schema = ErrorResponse(error_type=error_type, error_message=repr(exc))

    logger.error(
        f"Method: {request.method} | URL: {request.url} Details: {exc.errors()}"
    )
    logger.exception(exc)
    return JSONResponse(
        error_schema.model_dump_json(), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"Method: {request.method} | URL: {request.url} Details: {exc.detail}")
    logger.exception(exc)
    logger.debug(exc.detail)
    error_schema = ErrorResponse(
        error_type=responses[exc.status_code], error_message=repr(exc.detail)
    )
    return JSONResponse(
        status_code=exc.status_code, content=error_schema.model_dump_json()
    )
