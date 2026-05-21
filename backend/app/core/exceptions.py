"""
app/core/exceptions.py
Global HTTP exception handlers for consistent error responses
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def not_found_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=404,
        content={"error": "not_found", "message": str(exc.detail), "path": str(request.url.path)},
    )


def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"field": ".".join(str(l) for l in e["loc"]), "message": e["msg"]}
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"error": "validation_error", "details": errors},
    )


def server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "message": "An unexpected error occurred"},
    )
