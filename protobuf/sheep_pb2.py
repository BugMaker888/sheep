# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sheep.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bsheep.proto\"\xb4\x03\n\x07GameMap\x12\x10\n\x08widthNum\x18\x01 \x01(\x05\x12\x11\n\theightNum\x18\x02 \x01(\x05\x12\x10\n\x08levelKey\x18\x03 \x01(\x05\x12\x32\n\rblockTypeData\x18\x04 \x03(\x0b\x32\x1b.GameMap.BlockTypeDataEntry\x12*\n\tlevelData\x18\x05 \x03(\x0b\x32\x17.GameMap.LevelDataEntry\x1a\x96\x01\n\x08NodeList\x12$\n\x04node\x18\x01 \x03(\x0b\x32\x16.GameMap.NodeList.Node\x1a\x64\n\x04Node\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\x05\x12\x0e\n\x06rolNum\x18\x03 \x01(\x05\x12\x0e\n\x06rowNum\x18\x04 \x01(\x05\x12\x10\n\x08layerNum\x18\x05 \x01(\x05\x12\x10\n\x08moldType\x18\x06 \x01(\x05\x1a\x34\n\x12\x42lockTypeDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x43\n\x0eLevelDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12 \n\x05value\x18\x02 \x01(\x0b\x32\x11.GameMap.NodeList:\x02\x38\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sheep_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GAMEMAP_BLOCKTYPEDATAENTRY._options = None
  _GAMEMAP_BLOCKTYPEDATAENTRY._serialized_options = b'8\001'
  _GAMEMAP_LEVELDATAENTRY._options = None
  _GAMEMAP_LEVELDATAENTRY._serialized_options = b'8\001'
  _GAMEMAP._serialized_start=16
  _GAMEMAP._serialized_end=452
  _GAMEMAP_NODELIST._serialized_start=179
  _GAMEMAP_NODELIST._serialized_end=329
  _GAMEMAP_NODELIST_NODE._serialized_start=229
  _GAMEMAP_NODELIST_NODE._serialized_end=329
  _GAMEMAP_BLOCKTYPEDATAENTRY._serialized_start=331
  _GAMEMAP_BLOCKTYPEDATAENTRY._serialized_end=383
  _GAMEMAP_LEVELDATAENTRY._serialized_start=385
  _GAMEMAP_LEVELDATAENTRY._serialized_end=452
# @@protoc_insertion_point(module_scope)