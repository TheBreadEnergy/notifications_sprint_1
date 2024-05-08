from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import message as _message
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

class SendNotificationRequest(_message.Message):
    __slots__ = (
        "manager_id",
        "user_ids",
        "notification_id",
        "template_id",
        "subject",
        "text",
        "type",
    )
    MANAGER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    manager_id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    notification_id: str
    template_id: str
    subject: str
    text: str
    type: NotificationTypeEnum
    def __init__(
        self,
        manager_id: _Optional[str] = ...,
        user_ids: _Optional[_Iterable[str]] = ...,
        notification_id: _Optional[str] = ...,
        template_id: _Optional[str] = ...,
        subject: _Optional[str] = ...,
        text: _Optional[str] = ...,
        type: _Optional[_Union[NotificationTypeEnum, str]] = ...,
    ) -> None: ...

class CreateDelayedNotificationRequest(_message.Message):
    __slots__ = (
        "manager_id",
        "user_ids",
        "notification_id",
        "template_id",
        "subject",
        "text",
        "type",
        "delay",
    )
    MANAGER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    manager_id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    notification_id: str
    template_id: str
    subject: str
    text: str
    type: _containers.RepeatedScalarFieldContainer[NotificationTypeEnum]
    delay: int
    def __init__(
        self,
        manager_id: _Optional[str] = ...,
        user_ids: _Optional[_Iterable[str]] = ...,
        notification_id: _Optional[str] = ...,
        template_id: _Optional[str] = ...,
        subject: _Optional[str] = ...,
        text: _Optional[str] = ...,
        type: _Optional[_Iterable[_Union[NotificationTypeEnum, str]]] = ...,
        delay: _Optional[int] = ...,
    ) -> None: ...

class NotificationResponse(_message.Message):
    __slots__ = ("task_id",)
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    def __init__(self, task_id: _Optional[str] = ...) -> None: ...
