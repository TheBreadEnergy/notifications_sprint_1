import dataclasses
from typing import Self

from pydantic import BaseModel


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
        return Result(is_success=True)
