from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from src.grpc.models import status_pb2 as _status_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class FilmUploadedNotificationRequest(_message.Message):
    __slots__ = ("film_id",)
    FILM_ID_FIELD_NUMBER: _ClassVar[int]
    film_id: str
    def __init__(self, film_id: _Optional[str] = ...) -> None: ...
