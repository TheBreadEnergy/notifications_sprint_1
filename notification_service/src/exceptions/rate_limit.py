from http import HTTPStatus

from fastapi import HTTPException


class RateLimitException(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.TOO_MANY_REQUESTS)
