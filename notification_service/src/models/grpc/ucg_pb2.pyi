from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class CommentNotificationRequest(_message.Message):
    __slots__ = ("film_id", "user_id")
    FILM_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    film_id: str
    user_id: str
    def __init__(
        self, film_id: _Optional[str] = ..., user_id: _Optional[str] = ...
    ) -> None: ...

class OldBookmarkedNotificationRequest(_message.Message):
    __slots__ = ("bookmark_id", "user_id")
    BOOKMARK_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    bookmark_id: str
    user_id: str
    def __init__(
        self, bookmark_id: _Optional[str] = ..., user_id: _Optional[str] = ...
    ) -> None: ...
