from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger

from common.schemas import ErrorResponse


def _dump_model(model):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning("HTTP error on {} {}: {}", request.method, request.url.path, exc.detail)
        response = ErrorResponse(status=exc.status_code, message=str(exc.detail))
        return JSONResponse(status_code=exc.status_code, content=_dump_model(response))

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning("Validation error on {} {}: {}", request.method, request.url.path, exc)
        response = ErrorResponse(status=422, message=str(exc))
        return JSONResponse(status_code=422, content=_dump_model(response))

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled error on {} {}: {}", request.method, request.url.path, exc)
        response = ErrorResponse(status=500, message="internal server error")
        return JSONResponse(status_code=500, content=_dump_model(response))
