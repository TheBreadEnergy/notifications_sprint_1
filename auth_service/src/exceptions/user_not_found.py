from http import HTTPStatus

from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    def __init__(self, message="User not found"):
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=message)
