from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class Status(_message.Message):
    __slots__ = ("status", "message", "description")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    status: str
    message: str
    description: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        status: _Optional[str] = ...,
        message: _Optional[str] = ...,
        description: _Optional[_Iterable[str]] = ...,
    ) -> None: ...
