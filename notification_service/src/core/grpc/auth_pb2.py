# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auth.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from src.core.grpc.status_pb2 import *

from . import status_pb2 as status__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\nauth.proto\x1a\x0cstatus.proto"4\n!UserRegisteredNotificationRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t":\n\'UserActivatedAccountNotificationRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t"3\n UserLongNoSeeNotificationRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t2\xff\x01\n\x10UserNotification\x12M\n\x1cSendRegistrationNotification\x12".UserRegisteredNotificationRequest\x1a\x07.Status"\x00\x12Q\n\x1aSendActivationNotification\x12(.UserActivatedAccountNotificationRequest\x1a\x07.Status"\x00\x12I\n\x19SendLongNoSeeNotification\x12!.UserLongNoSeeNotificationRequest\x1a\x07.Status"\x00P\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "auth_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_USERREGISTEREDNOTIFICATIONREQUEST"]._serialized_start = 28
    _globals["_USERREGISTEREDNOTIFICATIONREQUEST"]._serialized_end = 80
    _globals["_USERACTIVATEDACCOUNTNOTIFICATIONREQUEST"]._serialized_start = 82
    _globals["_USERACTIVATEDACCOUNTNOTIFICATIONREQUEST"]._serialized_end = 140
    _globals["_USERLONGNOSEENOTIFICATIONREQUEST"]._serialized_start = 142
    _globals["_USERLONGNOSEENOTIFICATIONREQUEST"]._serialized_end = 193
    _globals["_USERNOTIFICATION"]._serialized_start = 196
    _globals["_USERNOTIFICATION"]._serialized_end = 451
# @@protoc_insertion_point(module_scope)
