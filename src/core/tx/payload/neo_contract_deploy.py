#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/6/28 11:02 AM
# author: liteng


import struct

from src.tools import serialize
from src.core.tx.payload.payload import Payload
from src.core.tx.payload.function_code import FunctionCode


class NeoDeployContract(Payload):

    def __init__(self, function_code: FunctionCode, name="", code_version="", author="", email="", description="",
                 program_hash=None, gas=0):
        Payload.__init__(self, Payload.DEFAULT_VERSION)
        self.function_code = function_code
        self.name = name
        self.code_version = code_version
        self.author = author
        self.email = email
        self.description = description
        self.program_hash = program_hash
        self.gas = gas

    def data(self, version: int):
        r = b""
        r = self.serialize(r, self.version)

        return r

    def serialize(self, r: bytes, version: int):
        r = self.function_code.serialize(r)
        r = serialize.write_var_bytes(r, bytes(self.name.encode()))
        r = serialize.write_var_bytes(r, bytes(self.code_version.encode()))
        r = serialize.write_var_bytes(r, bytes(self.author.encode()))
        r = serialize.write_var_bytes(r, bytes(self.email.encode()))
        r = serialize.write_var_bytes(r, bytes(self.description.encode()))
        r += self.program_hash
        r += struct.pack("<q", self.gas)

        return r

    def deserialize(self, r: bytes, version: int):
        pass

    def __repr__(self):
        return "NeoDeployContract{}"

# if __name__ == '__main__':
#
#     program_hash = bytes.fromhex("21e372cd15f4cfd3b0ae4e4624a94b492ead356afb")
#     code = "5bc56b6c766b00527ac46c766b51527ac4616168164e656f2e52756e74696d652e47"
#     function_code = FunctionCode(code, [FunctionCode.TYPE_STRING, FunctionCode.TYPE_ARRAY], FunctionCode.TYPE_OBJECT)
#
#     con = NeoDeployContract(
#         function_code=function_code,
#         name="aaa",
#         code_version="v0.1",
#         author="abc",
#         email="abc@163.com",
#         description="simple neo contract",
#         program_hash=program_hash,
#         gas=10,
#     )
#
#     r = con.serialize()
#     print("serialize: {}".format(r.hex()))



