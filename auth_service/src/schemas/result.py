import dataclasses
from typing import Generic, TypeVar

from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


@dataclasses.dataclass
class Error:
    reason: str
    error_code: str


@dataclasses.dataclass
class Result:
    is_success: bool
    error: Error | None

    @staticmethod
    def failure(error: Error):
        return Result(is_success=False, error=error)

    @staticmethod
    def success():
        return Result(is_success=True, error=None)


@dataclasses.dataclass
class GenericResult(Result, Generic[ModelType]):
    response: ModelType | None
    is_success: bool
    error: Error | None

    @staticmethod
    def failure(error: Error):
        return GenericResult(is_success=False, error=error, response=None)

    @staticmethod
    def success(value: ModelType):
        return GenericResult(is_success=True, error=None, response=value)
