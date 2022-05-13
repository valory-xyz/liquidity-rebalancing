# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tendermint.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database


# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x10tendermint.proto\x12\x1c\x61\x65\x61.valory.tendermint.v0_1_0"\x8a\x08\n\x11TendermintMessage\x12S\n\x05\x65rror\x18\x05 \x01(\x0b\x32\x42.aea.valory.tendermint.v0_1_0.TendermintMessage.Error_PerformativeH\x00\x12{\n\x19tendermint_config_request\x18\x06 \x01(\x0b\x32V.aea.valory.tendermint.v0_1_0.TendermintMessage.Tendermint_Config_Request_PerformativeH\x00\x12}\n\x1atendermint_config_response\x18\x07 \x01(\x0b\x32W.aea.valory.tendermint.v0_1_0.TendermintMessage.Tendermint_Config_Response_PerformativeH\x00\x1a\x8e\x01\n\tErrorCode\x12[\n\nerror_code\x18\x01 \x01(\x0e\x32G.aea.valory.tendermint.v0_1_0.TendermintMessage.ErrorCode.ErrorCodeEnum"$\n\rErrorCodeEnum\x12\x13\n\x0fINVALID_REQUEST\x10\x00\x1a\x37\n&Tendermint_Config_Request_Performative\x12\r\n\x05query\x18\x01 \x01(\t\x1a\xc7\x01\n\'Tendermint_Config_Response_Performative\x12o\n\x04info\x18\x01 \x03(\x0b\x32\x61.aea.valory.tendermint.v0_1_0.TendermintMessage.Tendermint_Config_Response_Performative.InfoEntry\x1a+\n\tInfoEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\xff\x01\n\x12\x45rror_Performative\x12M\n\nerror_code\x18\x01 \x01(\x0b\x32\x39.aea.valory.tendermint.v0_1_0.TendermintMessage.ErrorCode\x12\x11\n\terror_msg\x18\x02 \x01(\t\x12Z\n\x04info\x18\x03 \x03(\x0b\x32L.aea.valory.tendermint.v0_1_0.TendermintMessage.Error_Performative.InfoEntry\x1a+\n\tInfoEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x0e\n\x0cperformativeb\x06proto3'
)


_TENDERMINTMESSAGE = DESCRIPTOR.message_types_by_name["TendermintMessage"]
_TENDERMINTMESSAGE_ERRORCODE = _TENDERMINTMESSAGE.nested_types_by_name["ErrorCode"]
_TENDERMINTMESSAGE_TENDERMINT_CONFIG_REQUEST_PERFORMATIVE = (
    _TENDERMINTMESSAGE.nested_types_by_name["Tendermint_Config_Request_Performative"]
)
_TENDERMINTMESSAGE_TENDERMINT_CONFIG_RESPONSE_PERFORMATIVE = (
    _TENDERMINTMESSAGE.nested_types_by_name["Tendermint_Config_Response_Performative"]
)
_TENDERMINTMESSAGE_TENDERMINT_CONFIG_RESPONSE_PERFORMATIVE_INFOENTRY = (
    _TENDERMINTMESSAGE_TENDERMINT_CONFIG_RESPONSE_PERFORMATIVE.nested_types_by_name[
        "InfoEntry"
    ]
)
_TENDERMINTMESSAGE_ERROR_PERFORMATIVE = _TENDERMINTMESSAGE.nested_types_by_name[
    "Error_Performative"
]
_TENDERMINTMESSAGE_ERROR_PERFORMATIVE_INFOENTRY = (
    _TENDERMINTMESSAGE_ERROR_PERFORMATIVE.nested_types_by_name["InfoEntry"]
)
_TENDERMINTMESSAGE_ERRORCODE_ERRORCODEENUM = (
    _TENDERMINTMESSAGE_ERRORCODE.enum_types_by_name["ErrorCodeEnum"]
)
TendermintMessage = _reflection.GeneratedProtocolMessageType(
    "TendermintMessage",
    (_message.Message,),
    {
        "ErrorCode": _reflection.GeneratedProtocolMessageType(
            "ErrorCode",
            (_message.Message,),
            {
                "DESCRIPTOR": _TENDERMINTMESSAGE_ERRORCODE,
                "__module__": "tendermint_pb2"
                # @@protoc_insertion_point(class_scope:aea.valory.tendermint.v0_1_0.TendermintMessage.ErrorCode)
            },
        ),
        "Tendermint_Config_Request_Performative": _reflection.GeneratedProtocolMessageType(
            "Tendermint_Config_Request_Performative",
            (_message.Message,),
            {
                "DESCRIPTOR": _TENDERMINTMESSAGE_TENDERMINT_CONFIG_REQUEST_PERFORMATIVE,
                "__module__": "tendermint_pb2"
                # @@protoc_insertion_point(class_scope:aea.valory.tendermint.v0_1_0.TendermintMessage.Tendermint_Config_Request_Performative)
            },
        ),
        "Tendermint_Config_Response_Performative": _reflection.GeneratedProtocolMessageType(
            "Tendermint_Config_Response_Performative",
            (_message.Message,),
            {
                "InfoEntry": _reflection.GeneratedProtocolMessageType(
                    "InfoEntry",
                    (_message.Message,),
                    {
                        "DESCRIPTOR": _TENDERMINTMESSAGE_TENDERMINT_CONFIG_RESPONSE_PERFORMATIVE_INFOENTRY,
                        "__module__": "tendermint_pb2"
                        # @@protoc_insertion_point(class_scope:aea.valory.tendermint.v0_1_0.TendermintMessage.Tendermint_Config_Response_Performative.InfoEntry)
                    },
                ),
                "DESCRIPTOR": _TENDERMINTMESSAGE_TENDERMINT_CONFIG_RESPONSE_PERFORMATIVE,
                "__module__": "tendermint_pb2"
                # @@protoc_insertion_point(class_scope:aea.valory.tendermint.v0_1_0.TendermintMessage.Tendermint_Config_Response_Performative)
            },
        ),
        "Error_Performative": _reflection.GeneratedProtocolMessageType(
            "Error_Performative",
            (_message.Message,),
            {
                "InfoEntry": _reflection.GeneratedProtocolMessageType(
                    "InfoEntry",
                    (_message.Message,),
                    {
                        "DESCRIPTOR": _TENDERMINTMESSAGE_ERROR_PERFORMATIVE_INFOENTRY,
                        "__module__": "tendermint_pb2"
                        # @@protoc_insertion_point(class_scope:aea.valory.tendermint.v0_1_0.TendermintMessage.Error_Performative.InfoEntry)
                    },
                ),
                "DESCRIPTOR": _TENDERMINTMESSAGE_ERROR_PERFORMATIVE,
                "__module__": "tendermint_pb2"
                # @@protoc_insertion_point(class_scope:aea.valory.tendermint.v0_1_0.TendermintMessage.Error_Performative)
            },
        ),
        "DESCRIPTOR": _TENDERMINTMESSAGE,
        "__module__": "tendermint_pb2"
        # @@protoc_insertion_point(class_scope:aea.valory.tendermint.v0_1_0.TendermintMessage)
    },
)
_sym_db.RegisterMessage(TendermintMessage)
_sym_db.RegisterMessage(TendermintMessage.ErrorCode)
_sym_db.RegisterMessage(TendermintMessage.Tendermint_Config_Request_Performative)
_sym_db.RegisterMessage(TendermintMessage.Tendermint_Config_Response_Performative)
_sym_db.RegisterMessage(
    TendermintMessage.Tendermint_Config_Response_Performative.InfoEntry
)
_sym_db.RegisterMessage(TendermintMessage.Error_Performative)
_sym_db.RegisterMessage(TendermintMessage.Error_Performative.InfoEntry)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _TENDERMINTMESSAGE_TENDERMINT_CONFIG_RESPONSE_PERFORMATIVE_INFOENTRY._options = None
    _TENDERMINTMESSAGE_TENDERMINT_CONFIG_RESPONSE_PERFORMATIVE_INFOENTRY._serialized_options = (
        b"8\001"
    )
    _TENDERMINTMESSAGE_ERROR_PERFORMATIVE_INFOENTRY._options = None
    _TENDERMINTMESSAGE_ERROR_PERFORMATIVE_INFOENTRY._serialized_options = b"8\001"
    _TENDERMINTMESSAGE._serialized_start = 51
    _TENDERMINTMESSAGE._serialized_end = 1085
    _TENDERMINTMESSAGE_ERRORCODE._serialized_start = 410
    _TENDERMINTMESSAGE_ERRORCODE._serialized_end = 552
    _TENDERMINTMESSAGE_ERRORCODE_ERRORCODEENUM._serialized_start = 516
    _TENDERMINTMESSAGE_ERRORCODE_ERRORCODEENUM._serialized_end = 552
    _TENDERMINTMESSAGE_TENDERMINT_CONFIG_REQUEST_PERFORMATIVE._serialized_start = 554
    _TENDERMINTMESSAGE_TENDERMINT_CONFIG_REQUEST_PERFORMATIVE._serialized_end = 609
    _TENDERMINTMESSAGE_TENDERMINT_CONFIG_RESPONSE_PERFORMATIVE._serialized_start = 612
    _TENDERMINTMESSAGE_TENDERMINT_CONFIG_RESPONSE_PERFORMATIVE._serialized_end = 811
    _TENDERMINTMESSAGE_TENDERMINT_CONFIG_RESPONSE_PERFORMATIVE_INFOENTRY._serialized_start = (
        768
    )
    _TENDERMINTMESSAGE_TENDERMINT_CONFIG_RESPONSE_PERFORMATIVE_INFOENTRY._serialized_end = (
        811
    )
    _TENDERMINTMESSAGE_ERROR_PERFORMATIVE._serialized_start = 814
    _TENDERMINTMESSAGE_ERROR_PERFORMATIVE._serialized_end = 1069
    _TENDERMINTMESSAGE_ERROR_PERFORMATIVE_INFOENTRY._serialized_start = 768
    _TENDERMINTMESSAGE_ERROR_PERFORMATIVE_INFOENTRY._serialized_end = 811
# @@protoc_insertion_point(module_scope)
