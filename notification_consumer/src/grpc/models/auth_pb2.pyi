from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from src.grpc.models import status_pb2 as _status_pb2
from status_pb2 import Status as Status

DESCRIPTOR: _descriptor.FileDescriptor

class UserRegisteredNotificationRequest(_message.Message):
    __slots__ = ("user_id", "short_url")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SHORT_URL_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    short_url: str
    def __init__(
        self, user_id: _Optional[str] = ..., short_url: _Optional[str] = ...
    ) -> None: ...

class UserActivatedAccountNotificationRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class UserLongNoSeeNotificationRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...
