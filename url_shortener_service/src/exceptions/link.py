from http import HTTPStatus

from fastapi import HTTPException


class LinkExpiredException(HTTPException):
    def __init__(self, message="Link expired"):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=message)


class LinkNotFound(HTTPException):
    def __init__(self, message="Link not found"):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=message)
