from common.exception.http_error import HTTPError
from common.logger.handler import LoggerHandler
from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from typing import Union


async def exception_handler(request: Request, exception: HTTPError):
    """
    Middleware for exception messages.

    :param request: The client request.
    :param exception: The HTTP error.
    """
    response = {
        "error_code": exception.error_code,
        "message": exception.message,
        "detail": exception.detail,
        "target": "%(method)s|%(target)s"
        % {
            "method": request.method,
            "target": request.url._url,
        },
    }

    logger = LoggerHandler(request)
    logger.error(response)

    return JSONResponse(response, status_code=exception.http_status)


async def default_exception_handler(
    request: Request,
    exception: HTTPException,
):
    """
    Middleware for exception messages.

    :param request: The client request.
    :param exception: The request validation error.
    """
    response = {
        "error_code": "GenericExceptionRaised",
        "message": "Something went wrong inside a process.",
        "detail": exception.detail,
        "target": "%(method)s|%(target)s"
        % {
            "method": request.method,
            "target": request.url._url,
        },
    }

    logger = LoggerHandler(request)
    logger.error(response)

    return JSONResponse(response, status_code=exception.status_code)


async def python_exception_handler(
    request: Request,
    exception: Union[Exception, ValueError],
):
    """
    Middleware for exception messages.

    :param request: The client request.
    :param exception: The request validation error.
    """
    response = {
        "error_code": "InternalServerError",
        "message": "Something went wrong!",
        "detail": exception.__str__(),
        "target": "%(method)s|%(target)s"
        % {
            "method": request.method,
            "target": request.url._url,
        },
    }

    return JSONResponse(response, status_code=500)


async def request_validation_error_hanlder(
    request: Request,
    exception: RequestValidationError,
):
    """
    Middleware for RequestValidationError exception messages.

    :param request: The client request.
    :param exception: The request validation error.
    """
    response = {
        "error_code": "RequestValidationError",
        "message": "There are errors in the request.",
        "detail": exception.errors(),
        "target": "%(method)s|%(target)s"
        % {
            "method": request.method,
            "target": request.url._url,
        },
    }

    return JSONResponse(response, status_code=400)
