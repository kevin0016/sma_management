# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import rpc.services.funds_pb2 as funds__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='server.proto',
  package='rpc',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0cserver.proto\x12\x03rpc\x1a\x0b\x66unds.proto2\xe5\x01\n\nRpcService\x12J\n\x13\x46undCategoryHandler\x12\x18.rpc.FundCategoryRequest\x1a\x19.rpc.FundCategoryResponse\x12M\n\x14\x46undBasicInfoHandler\x12\x19.rpc.FundBasicInfoRequest\x1a\x1a.rpc.FundBasicInfoResponse\x12<\n\x14PortfolioCoreHandler\x12\x10.rpc.NullRequest\x1a\x12.rpc.FundsResponseb\x06proto3'
  ,
  dependencies=[funds__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_RPCSERVICE = _descriptor.ServiceDescriptor(
  name='RpcService',
  full_name='rpc.RpcService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=35,
  serialized_end=264,
  methods=[
  _descriptor.MethodDescriptor(
    name='FundCategoryHandler',
    full_name='rpc.RpcService.FundCategoryHandler',
    index=0,
    containing_service=None,
    input_type=funds__pb2._FUNDCATEGORYREQUEST,
    output_type=funds__pb2._FUNDCATEGORYRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='FundBasicInfoHandler',
    full_name='rpc.RpcService.FundBasicInfoHandler',
    index=1,
    containing_service=None,
    input_type=funds__pb2._FUNDBASICINFOREQUEST,
    output_type=funds__pb2._FUNDBASICINFORESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='PortfolioCoreHandler',
    full_name='rpc.RpcService.PortfolioCoreHandler',
    index=2,
    containing_service=None,
    input_type=funds__pb2._NULLREQUEST,
    output_type=funds__pb2._FUNDSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_RPCSERVICE)

DESCRIPTOR.services_by_name['RpcService'] = _RPCSERVICE

# @@protoc_insertion_point(module_scope)
