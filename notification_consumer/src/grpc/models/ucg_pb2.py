# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ucg.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from src.grpc.models import status_pb2 as status__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\tucg.proto\x1a\x0cstatus.proto"3\n OldBookmarkedNotificationRequest\x12\x0f\n\x07user_id\x18\x02 \x01(\t2`\n\x0fUcgNotification\x12M\n\x1dSendOldBookmarkedNotification\x12!.OldBookmarkedNotificationRequest\x1a\x07.Status"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "ucg_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_OLDBOOKMARKEDNOTIFICATIONREQUEST"]._serialized_start = 27
    _globals["_OLDBOOKMARKEDNOTIFICATIONREQUEST"]._serialized_end = 78
    _globals["_UCGNOTIFICATION"]._serialized_start = 80
    _globals["_UCGNOTIFICATION"]._serialized_end = 176
# @@protoc_insertion_point(module_scope)
