from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class UserRegisteredNotificationRequest(_message.Message):
    __slots__ = ("user_id", "registered_at")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_AT_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    registered_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        user_id: _Optional[str] = ...,
        registered_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class BatchUserRegisteredNotificationRequest(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[
        BatchUserRegisteredNotificationRequest
    ]
    def __init__(
        self,
        events: _Optional[
            _Iterable[_Union[BatchUserRegisteredNotificationRequest, _Mapping]]
        ] = ...,
    ) -> None: ...

class UserActivatedAccountNotificationRequest(_message.Message):
    __slots__ = ("user_id", "activated_at")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVATED_AT_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    activated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        user_id: _Optional[str] = ...,
        activated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class BatchUserActivatedAccountNotificationRequest(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[
        BatchUserActivatedAccountNotificationRequest
    ]
    def __init__(
        self,
        events: _Optional[
            _Iterable[_Union[BatchUserActivatedAccountNotificationRequest, _Mapping]]
        ] = ...,
    ) -> None: ...

class UserLongNoSeeNotificationRequest(_message.Message):
    __slots__ = ("user_id", "duration")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    duration: _duration_pb2.Duration
    def __init__(
        self,
        user_id: _Optional[str] = ...,
        duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...

class BatchLongNoSeeNotificationRequest(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[
        UserLongNoSeeNotificationRequest
    ]
    def __init__(
        self,
        events: _Optional[
            _Iterable[_Union[UserLongNoSeeNotificationRequest, _Mapping]]
        ] = ...,
    ) -> None: ...

class UserNotificationResponse(_message.Message):
    __slots__ = ("notification_id",)
    NOTIFICATION_ID_FIELD_NUMBER: _ClassVar[int]
    notification_id: str
    def __init__(self, notification_id: _Optional[str] = ...) -> None: ...
