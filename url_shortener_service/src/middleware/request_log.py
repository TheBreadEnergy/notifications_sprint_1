import uuid

from fastapi import Request, Response
from loguru import logger
from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware


def write_log_data(request: Request, response: Response):
    request_id = request.headers.get("X-Request-Id", uuid.uuid4())
    extra = {
        "request_id": request_id,
        "host": request.headers.get("host"),
        "user-agent": request.headers.get("user-agent"),
        "method": request.method,
        "path": request.url.path,
        "query_params": str(request.query_params),
        "status_code": response.status_code,
    }

    logger.bind(**extra).info(f"{request.method} {request.url.path}")


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.background = BackgroundTask(write_log_data, request, response)
        return response
