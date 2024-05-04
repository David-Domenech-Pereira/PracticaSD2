# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: store.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bstore.proto\x12\x10\x64istributedstore\" \n\x11\x61skVoteGetRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"F\n\x11\x61skVoteGetRespone\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\r\n\x05value\x18\x02 \x01(\t\x12\x11\n\tvote_size\x18\x03 \x01(\x05\"7\n\x11\x61skVotePutRespone\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x11\n\tvote_size\x18\x02 \x01(\x05\"/\n\x11\x61skVotePutRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"$\n\x08\x64Message\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"\x19\n\tdResponse\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\"\n\x0f\x64oCommitRespone\x12\x0f\n\x07success\x18\x01 \x01(\x08\"-\n\x0f\x64oCommitRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"+\n\rCommitRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\" \n\rCommitRespone\x12\x0f\n\x07success\x18\x01 \x01(\x08\"(\n\nPutRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\x1e\n\x0bPutResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x19\n\nGetRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"+\n\x0bGetResponse\x12\r\n\x05value\x18\x01 \x01(\t\x12\r\n\x05\x66ound\x18\x02 \x01(\x08\" \n\x0fSlowdownRequest\x12\r\n\x05\x64\x65lay\x18\x01 \x01(\x05\"#\n\x10SlowDownResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x10\n\x0eRestoreRequest\"\"\n\x0fRestoreResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x07\n\x05\x45mpty2\xd7\x05\n\rKeyValueStore\x12\x42\n\x03put\x12\x1c.distributedstore.PutRequest\x1a\x1d.distributedstore.PutResponse\x12\x42\n\x03get\x12\x1c.distributedstore.GetRequest\x1a\x1d.distributedstore.GetResponse\x12Q\n\x08slowDown\x12!.distributedstore.SlowdownRequest\x1a\".distributedstore.SlowDownResponse\x12N\n\x07restore\x12 .distributedstore.RestoreRequest\x1a!.distributedstore.RestoreResponse\x12M\n\tcanCommit\x12\x1f.distributedstore.CommitRequest\x1a\x1f.distributedstore.CommitRespone\x12P\n\x08\x64oCommit\x12!.distributedstore.doCommitRequest\x1a!.distributedstore.doCommitRespone\x12J\n\x0f\x64iscoverMessage\x12\x1a.distributedstore.dMessage\x1a\x1b.distributedstore.dResponse\x12V\n\naskVotePut\x12#.distributedstore.askVotePutRequest\x1a#.distributedstore.askVotePutRespone\x12V\n\naskVoteGet\x12#.distributedstore.askVoteGetRequest\x1a#.distributedstore.askVoteGetResponeb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'store_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ASKVOTEGETREQUEST']._serialized_start=33
  _globals['_ASKVOTEGETREQUEST']._serialized_end=65
  _globals['_ASKVOTEGETRESPONE']._serialized_start=67
  _globals['_ASKVOTEGETRESPONE']._serialized_end=137
  _globals['_ASKVOTEPUTRESPONE']._serialized_start=139
  _globals['_ASKVOTEPUTRESPONE']._serialized_end=194
  _globals['_ASKVOTEPUTREQUEST']._serialized_start=196
  _globals['_ASKVOTEPUTREQUEST']._serialized_end=243
  _globals['_DMESSAGE']._serialized_start=245
  _globals['_DMESSAGE']._serialized_end=281
  _globals['_DRESPONSE']._serialized_start=283
  _globals['_DRESPONSE']._serialized_end=308
  _globals['_DOCOMMITRESPONE']._serialized_start=310
  _globals['_DOCOMMITRESPONE']._serialized_end=344
  _globals['_DOCOMMITREQUEST']._serialized_start=346
  _globals['_DOCOMMITREQUEST']._serialized_end=391
  _globals['_COMMITREQUEST']._serialized_start=393
  _globals['_COMMITREQUEST']._serialized_end=436
  _globals['_COMMITRESPONE']._serialized_start=438
  _globals['_COMMITRESPONE']._serialized_end=470
  _globals['_PUTREQUEST']._serialized_start=472
  _globals['_PUTREQUEST']._serialized_end=512
  _globals['_PUTRESPONSE']._serialized_start=514
  _globals['_PUTRESPONSE']._serialized_end=544
  _globals['_GETREQUEST']._serialized_start=546
  _globals['_GETREQUEST']._serialized_end=571
  _globals['_GETRESPONSE']._serialized_start=573
  _globals['_GETRESPONSE']._serialized_end=616
  _globals['_SLOWDOWNREQUEST']._serialized_start=618
  _globals['_SLOWDOWNREQUEST']._serialized_end=650
  _globals['_SLOWDOWNRESPONSE']._serialized_start=652
  _globals['_SLOWDOWNRESPONSE']._serialized_end=687
  _globals['_RESTOREREQUEST']._serialized_start=689
  _globals['_RESTOREREQUEST']._serialized_end=705
  _globals['_RESTORERESPONSE']._serialized_start=707
  _globals['_RESTORERESPONSE']._serialized_end=741
  _globals['_EMPTY']._serialized_start=743
  _globals['_EMPTY']._serialized_end=750
  _globals['_KEYVALUESTORE']._serialized_start=753
  _globals['_KEYVALUESTORE']._serialized_end=1480
# @@protoc_insertion_point(module_scope)
