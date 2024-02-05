from fastapi import HTTPException


class RateLimitException(HTTPException):
    ...
