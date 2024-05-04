from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class NotificationTypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    email: _ClassVar[NotificationTypeEnum]
    sms: _ClassVar[NotificationTypeEnum]
    push: _ClassVar[NotificationTypeEnum]

email: NotificationTypeEnum
sms: NotificationTypeEnum
push: NotificationTypeEnum

class SendBatchNotificationRequest(_message.Message):
    __slots__ = ("user_ids", "template_id", "subject", "text", "type")
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    template_id: str
    subject: str
    text: str
    type: NotificationTypeEnum
    def __init__(
        self,
        user_ids: _Optional[_Iterable[str]] = ...,
        template_id: _Optional[str] = ...,
        subject: _Optional[str] = ...,
        text: _Optional[str] = ...,
        type: _Optional[_Union[NotificationTypeEnum, str]] = ...,
    ) -> None: ...

class CreateDelayedNotificationRequest(_message.Message):
    __slots__ = (
        "user_ids",
        "template_id",
        "subject",
        "text",
        "type",
        "created",
        "delta",
    )
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    DELTA_FIELD_NUMBER: _ClassVar[int]
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    template_id: str
    subject: str
    text: str
    type: _containers.RepeatedScalarFieldContainer[NotificationTypeEnum]
    created: _timestamp_pb2.Timestamp
    delta: int
    def __init__(
        self,
        user_ids: _Optional[_Iterable[str]] = ...,
        template_id: _Optional[str] = ...,
        subject: _Optional[str] = ...,
        text: _Optional[str] = ...,
        type: _Optional[_Iterable[_Union[NotificationTypeEnum, str]]] = ...,
        created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        delta: _Optional[int] = ...,
    ) -> None: ...

class CreateReccurentNotificationRequest(_message.Message):
    __slots__ = ("user_ids", "template_id", "subject", "text", "type", "cron_string")
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CRON_STRING_FIELD_NUMBER: _ClassVar[int]
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    template_id: str
    subject: str
    text: str
    type: _containers.RepeatedScalarFieldContainer[NotificationTypeEnum]
    cron_string: str
    def __init__(
        self,
        user_ids: _Optional[_Iterable[str]] = ...,
        template_id: _Optional[str] = ...,
        subject: _Optional[str] = ...,
        text: _Optional[str] = ...,
        type: _Optional[_Iterable[_Union[NotificationTypeEnum, str]]] = ...,
        cron_string: _Optional[str] = ...,
    ) -> None: ...

class NotificationResponse(_message.Message):
    __slots__ = ("notification_id",)
    NOTIFICATION_ID_FIELD_NUMBER: _ClassVar[int]
    notification_id: str
    def __init__(self, notification_id: _Optional[str] = ...) -> None: ...
