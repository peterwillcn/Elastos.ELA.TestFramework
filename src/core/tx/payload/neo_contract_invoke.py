#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/7/1 11:21 AM
# author: liteng

import struct
from src.tools import serialize
from src.core.tx.payload.function_code import FunctionCode
from src.core.tx.payload.payload import Payload


class NeoInvokeContract(Payload):

    CMD_PACK = 0xc1

    def __init__(self, params: dict, program_hash=None, gas=0):
        Payload.__init__(self, Payload.DEFAULT_VERSION)
        self.code_hash = "1c7779c302193ebc1523a7fe627497a31808fede95"
        self.code = None
        self.params = params
        self.program_hash = program_hash
        self.gas = gas
        self.gen_code()

    def to_code(self, params: dict):
        length = len(params)
        i = length - 1

        keys = params.keys()
        values = params.values()
        r = b""

        while i >= 0:
            key = list(keys)[i]
            value = list(values)[i]
            if key == FunctionCode.TYPE_BOOLEAN:
                r += serialize.write_neo_bool(value)
            elif key == FunctionCode.TYPE_INTEGER:
                v = float(value)
                r += serialize.write_neo_integer(int(v))
            elif key == FunctionCode.TYPE_STRING:
                r += serialize.write_neo_bytes(bytes(value.encode()))
            elif key == FunctionCode.TYPE_PUBLIC_KEY:
                r += serialize.write_neo_bytes(bytes.fromhex(value))
            elif key == FunctionCode.TYPE_BYTE_ARRAY or key == FunctionCode.TYPE_HASH256 or \
                key == FunctionCode.TYPE_HASH168 or key == FunctionCode.TYPE_SIGNATURE:
                r += serialize.write_neo_bytes(bytes.fromhex(value))
            elif key == FunctionCode.TYPE_HASH160 or key == FunctionCode.TYPE_HASH160_2:
                value_bytes = bytes.fromhex(value)
                if len(value_bytes) == 21:
                    r += serialize.write_neo_bytes(value_bytes[1:])
                else:
                    r += serialize.write_neo_bytes(value_bytes)
            elif key == FunctionCode.TYPE_ARRAY:
                count = len(value[0])
                r = self.to_code(value[0])
                r += serialize.write_neo_integer(count)
                r += struct.pack("<B", self.CMD_PACK)

            i -= 1

        return r

    @staticmethod
    def append_code_hash():
        r = b""
        r += struct.pack("<B", 0x69)
        code_hash = "1c7779c302193ebc1523a7fe627497a31808fede95"
        code_hash_bytes = bytes.fromhex(code_hash)[1:]
        r += code_hash_bytes[::-1]

        return r

    def gen_code(self):
        code = self.to_code(self.params)
        code += self.append_code_hash()
        self.code = code

    def data(self, version: int):
        r = b""
        r = self.serialize(r, version)

        return r

    def serialize(self, r: bytes, version: int):
        r += bytes.fromhex(self.code_hash)
        r = serialize.write_var_bytes(r, self.code)
        r += self.program_hash
        r += struct.pack("<q", self.gas)

        return r

    def deserialize(self, r: bytes, version: int):
        pass


if __name__ == '__main__':
    contract_params2 = {FunctionCode.TYPE_STRING: "transfer", FunctionCode.TYPE_ARRAY: [{
        FunctionCode.TYPE_HASH160: "ab555802d53185891cc51bdac7bcc8e78c3053d7",
        FunctionCode.TYPE_HASH160_2: "21329e67ca972c63c256c671da5d4e35eb244062c1",
        FunctionCode.TYPE_INTEGER: 1000000,
    }]}
    invoke_payload2 = NeoInvokeContract(
        params=contract_params2,
        program_hash=bytes.fromhex("21329e67ca972c63c256c671da5d4e35eb244062c1"),
        gas=0,
    )

